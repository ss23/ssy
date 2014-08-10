import boto.dynamodb2, time
from boto.dynamodb2.table import Table

HOST_UP = 1
HOST_DOWN = 0

connection = boto.dynamodb2.connect_to_region('ap-southeast-2')

scans = Table('host_up', connection=connection)

scan1 = {
    'ip': '127.0.0.1',
    'datetime': int(time.time()),
    'status': HOST_UP
}

scans.put_item(data=scan1)
print(scan1)
