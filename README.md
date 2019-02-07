# Just learning some Ansible.

### Based on a [course](https://training.talkpython.fm/courses/explore_ansible/introduction-to-ansible-with-python) by Matt Makai from [TalkPython](https://training.talkpython.fm/).


### Spinning off into two main areas:
- local setup of workstations 
- remote configuration for a MongoDB server


#### Workstation setup:
- Mainly tested/used on Ubuntu 18.04 and some 16.04.
- Programs:
    - python 3.7.2
    - vim 8.1
    - tmux 2.8
    - Docker CE 18.09
    - ROS Kinetic
    - gazebo 7

To run, fill out your username and your password in the `host_vars/local.yml` like so:
```
ansible_connection: local
user: your_username
ansible_sudo_pass: your_password
```
Then run the following:
`ansible-playbook -i ./hosts programs_local.yml`

#### MongoDB setup:
This installs MongoDB 4.0 on a Ubuntu VM and sets up automatic backups which get stored in s3.

More to come...

host_vars/db-1.yml
```
ansible_ssh_host: ip_address
mongo_admin_user: db_user
mongo_admin_password: db_password
db_name: test_db

aws_region: us-west-2
aws_access_key: key
aws_secret_key: secret_key
bucket_name: bucket
```