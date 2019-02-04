Role Name
=========

Ansible role written using a [custom-module](https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_documenting.html#developing-modules-documenting) verifies if volume mounts are present and returns a warning if utilization >= 85%

Requirements
------------


Role Variables
--------------


Dependencies
------------

Example Playbook
----------------

    ---
    - hosts: 127.0.0.1
      connection: local
      gather_facts: no
      roles:
      - { role: role_ansible_custom_module }

License
-------

BSD

Author Information
------------------

An optional section for the role authors to include contact information, or a website (HTML is not allowed).
