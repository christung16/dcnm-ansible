#!/usr/bin/python

# Copyright: (c) 2018, Chris Gascoigne <cgascoig@cisco.com>

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: my_sample_module

short_description: This is my sample module

version_added: "2.4"

description:
    - "This is my longer description explaining my sample module"

options:
    name:
        description:
            - This is the message to send to the sample module
        required: true
    new:
        description:
            - Control to demo if the result of this module is changed or not
        required: false

extends_documentation_fragment:
    - azure

author:
    - Your Name (@yourhandle)
'''

EXAMPLES = '''
# Pass in a message
- name: Test with a message
  my_new_test_module:
    name: hello world

# pass in a message and have changed true
- name: Test with a message and changed output
  my_new_test_module:
    name: hello world
    new: true

# fail the module
- name: Test failure of the module
  my_new_test_module:
    name: fail me
'''

RETURN = '''
original_message:
    description: The original name param that was passed in
    type: str
message:
    description: The output message that the sample module generates
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.dcnm import DCNM, dcnm_argument_spec


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dcnm_argument_spec
    module_args.update(
        fabric_name=dict(type='str', required=True),
        vrf_name=dict(type='str', required=True),
        vrf_template=dict(type='str', required=False, default="Default_VRF_Universal"),
        vrf_extension_template=dict(type='str', required=False, default="Default_VRF_Extension_Universal"),
        vrf_template_config=dict(type='dict', required=True),
        vrf_id=dict(type='int', required=True),
        state=dict(type='str', choices=['present', 'absent'], default='present'),

    )

    # seed the result dict
    result = dict(
        changed=False,
        ansible_facts=dict()
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    try:
        dcnm = DCNM(module.params['baseurl'], module.params['username'], module.params['password'], verify=module.params['verify'])

        dcnm.login()

        vrf = dcnm.get_vrf(module.params['fabric_name'], module.params['vrf_name'])

        # Handle state==absent cases
        if module.params['state'] == 'absent':
            if vrf is not None:
                # VRF exists but shouldn't ... delete it
                if not module.check_mode:
                    dcnm.delete_vrf(module.params['fabric_name'], module.params['vrf_name'])
                result['changed'] = True
                module.exit_json(**result)
            else:
                module.exit_json(**result)

        # Handle state==present cases
        if vrf is not None:
            # VRF already exists
            need_update = dcnm.compare_vrf_attrs(vrf, module.params)

            if need_update==False:
                module.exit_json(**result)

            # Update VRF
            if not module.check_mode:
                vrf = dcnm.update_vrf(module.params)
            
            result['changed'] = True
            module.exit_json(**result)
            

        # Create VRF        
        if not module.check_mode:
                vrf = dcnm.create_vrf(module.params)

        result['changed'] = True
        module.exit_json(**result)

    except Exception as e:
        module.fail_json(msg=str(e), result=result)

def main():
    run_module()

if __name__ == '__main__':
    main()