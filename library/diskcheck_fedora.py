#!/usr/bin/python
# Copyright: (c) 2018, canit00 <[email protected]>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
module: diskcheck_fedora

short_description: Gathers disk utilization percentage.

description:
    - Gathers volumes and validates to be present. Then gathers volume utilization percentage. If it exceeds 85% use it alarms.

version_added: "2.7"

author: "Your AWESOME name (@awesome-github-id)"

options:
    option_name:
        description:
            - Description of the options goes here.
            - Must be written in sentences.
        required: true || false
        default: a string or the word null
        choices:
          - enable
          - disable
        aliases:
          - repo_name
        version_added: "1.X"

notes:
    - Other things consumers of your module should know.

requirements:
    - null >= 1.0
'''

EXAMPLES = '''
- name: Print disk utilization %
  diskcheck_fedora:
  register: disk
  when: ansible_distribution == "Fedora"
'''

RETURN = '''
msg:
    description: Returns volume disk utilization %
    returned: always
    type: dict
    sample: {"/var/lib/openshift": [0.3], "/var/lib/docker": [0.3], "changed": false, "/var/lib/containers": [0.2]}
'''

from ansible.module_utils.basic import AnsibleModule
import psutil,json

volumes = dict()

def run_module():

    threshold_exceeded = False

    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        volumes=dict(type='str', required=True),
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # change is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(changed=False)

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    vol = module.params['volumes']

    disk_usage = psutil.disk_usage(vol)
    if disk_usage.percent < 85.0:
        result.setdefault(vol, []).append(disk_usage.percent)
    elif disk_usage.percent >= 85.0:
        result.setdefault(vol, []).append(disk_usage.percent)
        threshold_exceeded = True

    # use whatever logic you need to determine whether or not this module
    # made any modifications to your target
    if threshold_exceeded and "threshold" not in result:
        result.setdefault("threshold", []).append("exceeded")

    # during the execution of the module, if there is an exception or a
    # conditional state that effectively causes a failure, run
    # AnsibleModule.fail_json() to pass in the message and the result
    #if module.params['volumes'] == 'fail me':
    #    module.fail_json(msg='You requested this to fail', **result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
