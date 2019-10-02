# Cisco DCNM Ansible Module

## Pre-requisite

Ansible must be installed. 

Clone the repository from Chris Gascoigne:
```
git clone https://github.com/cgascoig/dcnm-ansible
```
I leverage Chris's dcnm-ansible module to complete the work

## Usage
Create the dcnm ip and login variable in overlay_network_operations/vars/main.yml:

---
# vars file for dcnm
baseurl: https://<dcnm-ip>/rest
username: admin
password: "cisco"



Create a playbook, like this example:

```yaml

---
- name: test dcnm module
  hosts: localhost
  connection: local
  gather_facts: no
  vars:
    fabric_name: "Demo1"
    network_name: "MyNetwork_30003"
    vrf_name: "MyVRF_50000"
    network_id: "32003"
    gateway_ip: "192.168.40.254/24"
    vlan_id: "2303"
    switch_ports: "Ethernet1/6"
    state: "absent"

  roles:
    - overlay_network_operations


The Ansible modules closely mirror the DCNM REST API for top-down network provisioning so look at the API documentation for more details on the parameters: https://<DCNM_IP>/api-docs/

Execute playbook:

```
ansible-playbook test-playbook.yml
```
