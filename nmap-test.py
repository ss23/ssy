from libnmap.process import NmapProcess
from libnmap.parser import NmapParser, NmapParserException

nm = NmapProcess('192.168.0.*', options='-v -sn')

rc = nm.run()

try:
    parsed = NmapParser.parse(nm.stdout)
except NmapParserException as e:
    print("Exception raised while parsing scan: %s" % (e.msg))

for host in parsed.hosts:
    print("Host {0} is {1}".format(host.address, host.status))


