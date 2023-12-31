"""CiscoConfParse examples.

- Get config from the Fortigate by SSH
- Create CiscoConfParse object
- Filter all JunosCfgLine objects of wan interfaces
- Print some data in CiscoConfParse objects
- Filter all wan interfaces blocks

for more details see https://github.com/mpenning/ciscoconfparse
"""
import logging
from pprint import pprint

from fortigate_api import FortigateAPI
from fortigate_api import ccp

logging.getLogger().setLevel(logging.DEBUG)

HOST = "host"
USERNAME = "username"
PASSWORD = "password"

fgt = FortigateAPI(host=HOST, username=USERNAME, password=PASSWORD)
fgt.login()

# get config from the Fortigate by SSH
config = fgt.ssh.send_command("show system interface")
print(config)
# config system interface
#     edit "wan1"
#         set vdom "root"
#         set mode dhcp
#         set status down
#         set type physical
#         set role wan
#         set snmp-index 3
#     next
#     edit "wan2"
#         set vdom "root"
#         set mode dhcp
#         set status down
#         set type physical
#         set role wan
#         set snmp-index 4
#     next
# end

# create CiscoConfParse object
# filter all JunosCfgLine objects of wan interfaces
parser = ccp.FgtConfParse(config=config)
interfaces = ccp.find_by_re_keys(ccp=parser, keys=["config system interface", r"edit .wan\d"])
pprint(interfaces)
# [<JunosCfgLine # 23 '    edit "wan1"' (parent is # 0)>,
#  <JunosCfgLine # 32 '    edit "wan2"' (parent is # 0)>]

# print some data in CiscoConfParse objects
for interface in interfaces:
    print(interface.text)
    print([o.text for o in interface.all_children if o.text.find("snmp-index")][0])
#     edit "wan1"
#         set vdom "root"
#     edit "wan2"
#         set vdom "root"

# filter all wan interfaces blocks
blocks = ccp.find_re_blocks(ccp=parser, regex=r"edit .wan\d")
pprint(blocks)
# ['    edit "wan1"\n'
#  '        set vdom "root"\n'
#  '        set mode dhcp\n'
#  '        set status down\n'
#  '        set type physical\n'
#  '        set role wan\n'
#  '        set snmp-index 3',
#  '    edit "wan2"\n'
#  '        set vdom "root"\n'
#  '        set mode dhcp\n'
#  '        set status down\n'
#  '        set type physical\n'
#  '        set role wan\n'
#  '        set snmp-index 4']
