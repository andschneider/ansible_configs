# Just learning some Ansible.

### Based on a [course](https://training.talkpython.fm/courses/explore_ansible/introduction-to-ansible-with-python) by Matt Makai from [TalkPython](https://training.talkpython.fm/).


### Spinning off into two main areas:
- local setup of workstations 
- remote configuration for a MongoDB server


#### Configuration files:
host_vars/local.yml:
```
ansible_connection: local
user: username
ansible_sudo_pass: password
```

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