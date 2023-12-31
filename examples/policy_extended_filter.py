"""Policy Extended Filter examples.

- Get the rules where source prefix is equals 127.0.1.0/30
- Get the rules where source prefix is not equals 127.0.1.0/30
- Get the rules where source addresses are in subnets of 127.0.1.0/24
- Get the rules where source prefixes are supernets of address 127.0.1.1/32
- Get the rules where source prefix are equals 127.0.1.0/30 and destination prefix are equals 127.0.2.0/30
- Delete policy, address-group, addresses from the Fortigate (order is important)
"""

import logging

from fortigate_api import FortigateAPI

logging.getLogger().setLevel(logging.DEBUG)

HOST = "host"
USERNAME = "username"
PASSWORD = "password"

fgt = FortigateAPI(host=HOST, username=USERNAME, password=PASSWORD)
fgt.login()

print("\nCreates address and address_group in the Fortigate")
data = {"name": "ADDRESS1",
        "obj-type": "ip",
        "subnet": "127.0.1.0 255.255.255.252",
        "type": "ipmask"}
response = fgt.address.create(data=data)
print("address.create", response)  # post <Response [200]>
data = {"name": "ADDRESS2",
        "obj-type": "ip",
        "subnet": "127.0.2.0 255.255.255.252",
        "type": "ipmask"}
response = fgt.address.create(data=data)
print("address.create", response)  # post <Response [200]>
data = {"name": "ADDR_GROUP", "member": [{"name": "ADDRESS2"}]}
response = fgt.address_group.create(data=data)
print("address_group.create", response)  # post <Response [200]>

print("\nCreates policy in the Fortigate")
data = dict(
    name="POLICY",
    status="enable",
    action="accept",
    srcintf=[{"name": "any"}],
    dstintf=[{"name": "any"}],
    srcaddr=[{"name": "ADDRESS1"}],
    dstaddr=[{"name": "ADDR_GROUP"}],
    service=[{"name": "ALL"}],
    schedule="always",
)
response = fgt.policy.create(data=data)
print("policy.create", response)  # post <Response [200]>

print("\nGets the rules where source prefix is equals 127.0.1.0/30")
efilter = "srcaddr==127.0.1.0/30"
policies = fgt.policy.get(efilter=efilter)
print(f"{efilter=}", len(policies))  # efilter='srcaddr==127.0.1.0/30' 1

print("\nGets the rules where source prefix is not equals 127.0.1.0/30")
efilter = "srcaddr!=127.0.1.0/30"
policies = fgt.policy.get(efilter=efilter)
print(f"{efilter=}", len(policies))  # efilter='srcaddr!=127.0.1.0/30' 35

print("\nGets the rules where source addresses are in subnets of 127.0.1.0/24")
efilter = "srcaddr<=127.0.1.0/24"
policies = fgt.policy.get(efilter=efilter)
print(f"{efilter=}", len(policies))  # efilter='srcaddr<=127.0.1.0/24' 1

print("\nGets the rules where source prefixes are supernets of address 127.0.1.1/32")
efilter = "srcaddr>=127.0.1.1/32"
policies = fgt.policy.get(efilter=efilter)
print(f"{efilter=}", len(policies))  # efilter='srcaddr>=127.0.1.1/32' 7

print("\nGets the rules where source prefix are equals 127.0.1.0/30 and")
print("\ndestination prefix are equals 127.0.2.0/30")
efilters = ["srcaddr==127.0.1.0/30", "dstaddr==127.0.2.0/30"]
policies = fgt.policy.get(efilter=efilters)
print(f"{efilters=}", len(policies))
print("\nefilters=['srcaddr==127.0.1.0/30', 'dstaddr==127.0.2.0/30'] 1")

print("\nDelete policy, address-group, addresses from the Fortigate (order is important)")
response = fgt.address.delete(uid="ADDRESS1")
print("address.delete", response.ok)  # address.delete <Response [200]>
response = fgt.policy.delete(filter="name==POLICY")
print("policy.delete", response.ok)  # policy.delete <Response [200]>
response = fgt.address_group.delete(uid="ADDR_GROUP")
print("address_group.delete", response.ok)  # address_group.delete <Response [200]>
response = fgt.address.delete(uid="ADDRESS1")
print("address.delete", response.ok)  # address.delete <Response [200]>
response = fgt.address.delete(uid="ADDRESS2")
print("address.delete", response.ok)  # address.delete <Response [200]>

fgt.logout()
