import boto.sqs, time, struct, socket
from boto.sqs.message import Message

def ip2int(addr):                                                               
    return struct.unpack("!I", socket.inet_aton(addr))[0]                       

def int2ip(addr):                                                               
    return socket.inet_ntoa(struct.pack("!I", addr)) 

conn = boto.sqs.connect_to_region('ap-southeast-2')

q = conn.create_queue('scan-queue')

# 130.123.0.0,130.123.255.255
start = ip2int('130.123.0.0');
end = ip2int('130.123.255.255');

# This has some overrun but it's okay for testing
for ips in range(start, end, 10):
    messages = []
    for ip in range(ips, ips + 10):
        messages.append((ip, 'scan ' + int2ip(ip), 0))
    q.write_batch(messages)

#m = Message()
#m.set_body('scan 127.0.0.1')
#q.write(m)


