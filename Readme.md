Thu Aug 25 11:17:46 EDT 2022

Ansible Information:

OpenBSD implementation:

Current:
ansible [core 2.15.4]
  config file = /etc/ansible/ansible.cfg
  configured module search path = ['/home/ansible/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/local/lib/python3.10/site-packages/ansible
  ansible collection location = /home/ansible/.ansible/collections:/usr/share/ansible/collections
  executable location = /usr/local/bin/ansible
  python version = 3.10.13 (main, Oct  5 2023, 16:21:31) [Clang 13.0.0 ] (/usr/local/bin/python3.10)
  jinja version = 3.1.2
  libyaml = True

Formerly:
ansible [core 2.13.4]
  config file = /etc/ansible/ansible.cfg
  configured module search path = ['/home/ansible/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/local/lib/python3.9/site-packages/ansible
  ansible collection location = /home/ansible/.ansible/collections:/usr/share/ansible/collections
  executable location = /usr/local/bin/ansible
  python version = 3.9.15 (main, Oct 21 2022, 14:01:40) [Clang 13.0.0 ]
  jinja version = 3.1.2
  libyaml = True

Some Ansible defintions:

Control node:
   Where one runs the ansible and ansible-playbook commands.
   In our case it is doghaus, under the ansible user
   This machine has to have a current version of python installed

Managed nodes:
	The network devices (and/or servers) you manage with Ansible.
  Managed nodes are also sometimes called hosts.
	Ansible is not installed on managed nodes.

Inventory:
	A list of managed nodes. An inventory file is also sometimes called
	a hostfile. Your inventory can specify information like IP
	address for each managed node. An inventory can also organize managed
	nodes, creating and nesting groups for easier scaling.
	This is in YAML format

Collections:
	Collections are a distribution format for Ansible content that can
	include playbooks, roles, modules, and plugins. You can install and
	use collections through Ansible Galaxy. To learn more about
	collections, see Using collections. These are like standard libraries
	and are installed using the  ansible-galaxy command

Modules:
	The units of code Ansible executes. Each module has a particular
	or use, from administering users on a specific type of database to
	managing VLAN interfaces on a specific type of network device. You
	can invoke a single module with a task, or invoke several different
	modules in a playbook. Starting in Ansible 2.10, modules are grouped
	in collections. For an idea of how many collections Ansible includes,
	take a look at the Collection Index.
  Modules operate on the nodes, the remote hosts

Plugins:
  Plugins operate on the control node, rather than on the managed nodes.
  E.g. lookup()

Tasks:
	The units of action in Ansible. You can execute a single task once with an ad hoc command.

Playbooks:
	Ordered lists of tasks, saved so you can run those tasks in that
	order repeatedly. Playbooks can include variables as well as tasks.
	Playbooks are written in YAML and are easy to read, write, share
	and understand. To learn more about playbooks, see Intro to playbooks.

Fri May  5 15:09:40 EDT 2023

ansible [core 2.14.3]
  config file = /etc/ansible/ansible.cfg
  configured module search path = ['/home/ansible/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/local/lib/python3.10/site-packages/ansible
  ansible collection location = /home/ansible/.ansible/collections:/usr/share/ansible/collections
  executable location = /usr/local/bin/ansible
  python version = 3.10.11 (main, Apr 13 2023, 01:52:20) [Clang 13.0.0 ] (/usr/local/bin/python3.10)
  jinja version = 3.1.2
  libyaml = True

Wed Jan 24 13:50:45 EST 2024
OpenBSD doghaus.eis.utoronto.ca 7.4 GENERIC.MP#2 amd64
ansible [core 2.15.4]
  config file = /etc/ansible/ansible.cfg
  configured module search path = ['/home/ansible/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/local/lib/python3.10/site-packages/ansible
  ansible collection location = /home/ansible/.ansible/collections:/usr/share/ansible/collections
  executable location = /usr/local/bin/ansible
  python version = 3.10.13 (main, Oct  5 2023, 16:21:31) [Clang 13.0.0 ] (/usr/local/bin/python3.10)
  jinja version = 3.1.2
  libyaml = True

Fri Jan 26 09:48:32 EST 2024

Some Ansible Commands:

$ ansible-inventory --version
ansible-inventory [core 2.15.4]
  config file = /etc/ansible/ansible.cfg
  configured module search path = ['/home/ansible/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/local/lib/python3.10/site-packages/ansible
  ansible collection location = /home/ansible/.ansible/collections:/usr/share/ansible/collections
  executable location = /usr/local/bin/ansible-inventory
  python version = 3.10.13 (main, Oct  5 2023, 16:21:31) [Clang 13.0.0 ] (/usr/local/bin/python3.10)
  jinja version = 3.1.2
  libyaml = True
