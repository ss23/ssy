import boto.sqs, time
from boto.sqs.message import Message

from libnmap.process import NmapProcess
from libnmap.parser import NmapParser, NmapParserException

conn = boto.sqs.connect_to_region('ap-southeast-2')

q = conn.create_queue('scan-queue')

rs = q.get_messages(10)

targets = []
for message in rs:
    targets.append(message.get_body().split(' ')[1])

nm = NmapProcess(targets, options='-v -sn')
rc = nm.run()

try:
    parsed = NmapParser.parse(nm.stdout)
except NmapParserException as e:
    print("Exception raised while parsing scan: %s" % (e.msg))

import boto.dynamodb2, time
from boto.dynamodb2.table import Table

HOST_UP = 1
HOST_DOWN = 0

ddbcon = boto.dynamodb2.connect_to_region('ap-southeast-2')

scans = Table('host_up', connection=ddbcon)

with scans.batch_write() as batch:
    for host in parsed.hosts:
        # Insert into database and delete from queue
        if (host.status == 'down'):
            status = 0
        elif (host.status == 'up'):
            status = 1
        else:
            status = -1

        batch.put_item(data={
            'ip': host.address,
            'status': status,
            'datetime': int(time.time())
        })

# If we get here, assume we're done
for message in rs:
    q.delete_message(message)

