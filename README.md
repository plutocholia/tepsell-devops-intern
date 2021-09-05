# Tapsell-DevOps-Intern


## Automation Part

There are several ansible playbooks available in ansible directory. 

pre requirements for running ansibel playbooks:

    1. pip install -r requirements.txt
    2. run "ansible-galaxy collection install" for each of collections in ansible-collection-list.txt


Note: there are several variables defined in ansible/vars directory for each of those automation and configuration files. Make sure to check those files and change them to your own needs.

### Database Servers

    1. run "ansible-playbook -i inventory mysql_init.yml"
    2. run "ansible-playbook -i inventory mysql_data.yml"
    3. run "ansible-playbook -i inventory redis_init.yml"

Note: doing firewall stuff is not automated due to security and lack of risk-acceptance. :)

To add a new host to the given mysql database:

    1. add the ip address to the mysql_remote_host list in ansible/vars/mysql_defaults.yml
    2. run "ansible-playbook -i inventory mysql_data.yml --tags=new-user"
    3. don't forget to allow port 3306 (mysql port) to that ip :)

### Web Servers

    1. run "ansible-playbook -i inventory docker-init.yml"
    2. run "ansible-playbook -i inventory k8s_init.yml"

Note: after installation of docker and kubernetes, you have to make systemd as the cgroup of the containerd and kubernetes. (the ansible file does not support this part due to **Ajib Gharib** k8s doc instructions)

Note: There is no automation for k8s cluster, deployments and services creation.

## Post Automation

make sure to login to your docker account 
    
    run "docker login" 

create a pull secret key

    run "kubectl create secret generic regcred --from-file=.dockerconfigjson=/root/.docker/config.json --type=kubernetes.io/dockerconfigjson"

create k8s cluster.

create services and deployments based on deployments directory files.
