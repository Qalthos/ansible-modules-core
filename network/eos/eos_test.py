#!/usr/bin/python
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#
DOCUMENTATION = """
---
module: eos_test
version_added: "2.2"
author: "Nathaniel Case (@Qalthos)"
short_description: Unit tests on Arista EOS module
description:
  - Arista EOS configurations use a simple block indent file sytanx
extends_documentation_fragment: eos
options:
  test:
    description:
      - The name of the test to run.
    required: true
"""

EXAMPLES = """
- eos_test:
    test: "get_config"
"""


def get_config(module):
    config = module.params['config'] or dict()
    if not config and not module.params['force']:
        config = module.config
    return config

def main():
    """ main entry point for module execution
    """
    argument_spec = dict(
        test=dict(required=True, type='str'),
    )
    module = get_module(argument_spec=argument_spec)

    test = module.params['test']

    result = {}
    if test == 'get_config':
        result['output'] = module.config.get_config()
    elif test == 'load_config':
        commands = ['ip access-list test', '10 permit ip any any log', 'exit']
        result['output'] = module.config.load_config(commands, commit=True)
        if result['output']:
            result['changed'] = True

    module.exit_json(**result)

from ansible.module_utils.eos import *
if __name__ == '__main__':
    main()

