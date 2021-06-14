# ERPNext x Reinforcement Learning

This repository shows an implementation of a reinforcement learning algorithm in the ERP Software ERPNext.

Setup process: 

1. Install ERPNext + Dependencies
2. Configure ERPNext and Import Data
3. Setup a Virtual Environment and the OpenAI Gym Environment
4. Edit Token
5. Start Training an Agent
--------
6. Using the Trained Model


# Setup

Tested on a virtual machine with the following specifications:

- Ubuntu 20.04.2.0 LTS (Server Version)
- Python 3.7
- 4 vCPUs
- 8GB RAM
- 40GB storage volume
    


## 1. Install ERPNext + Dependencies

#### Intsall Dependencies    
    
    apt update
    apt -y upgrade
    apt install software-properties-common
    add-apt-repository ppa:deadsnakes/ppa
    apt install python3.7 python3.7-dev python3.7-doc python3-pip
    pip3 install ansible
    apt-key adv --recv-keys --keyserver hkp://keyserver.ubuntu.com:80 0xF1656F24C74CD1D8
    add-apt-repository 'deb [arch=amd64,i386,ppc64el] http://mirror.nodesdirect.com/mariadb/repo/10.3/ubuntu bionic main'


#### Install and Configure MariaDB

    sudo apt update 
    sudo apt -y install mariadb-server libmysqlclient-dev
    sudo apt install curl nano git pv
    sudo nano /etc/mysql/my.cnf

Add the following snippet below [mysqld]

    innodb-file-format=barracuda
    innodb-file-per-table=1
    innodb-large-prefix=1
    character-set-client-handshake = FALSE
    character-set-server = utf8mb4
    collation-server = utf8mb4_unicode_ci

Add the following snippet below [mysql]

    default-character-set = utf8mb4

Change innodb_buffer_pool_size to 2GB

    innodb_buffer_pool_size = 2000M

Finnish MariaDB Installation

    sudo systemctl restart mariadb
    sudo systemctl enable mariadb
    sudo service mysql restart
    sudo mysql_secure_installation


#### Install Node and yarn

    sudo curl --silent --location https://deb.nodesource.com/setup_12.x | sudo bash -

    curl -sL https://dl.yarnpkg.com/debian/pubkey.gpg | gpg --dearmor | sudo tee /usr/share/keyrings/yarnkey.gpg >/dev/null

    echo "deb [signed-by=/usr/share/keyrings/yarnkey.gpg] https://dl.yarnpkg.com/debian stable main" | sudo tee /etc/apt/sources.list.d/yarn.list

    sudo apt-get update && sudo apt-get install yarn


#### Install nginx, nodejs, redis, supervisor

    sudo apt -y install nginx nodejs redis-server supervisor

    sudo systemctl start nginx
    sudo systemctl enable nginx

    sudo systemctl start redis-server
    sudo systemctl enable redis-server

#### Install wkhtmltopdf

    sudo apt -y install libxrender1 libxext6 xfonts-75dpi xfonts-base

    wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.focal_amd64.deb

    sudo dpkg -i wkhtmltox_0.12.6-1.focal_amd64.deb

    sudo apt -f install

    sudo dpkg -i wkhtmltox_0.12.6-1.focal_amd64.deb


#### Install Bench

    sudo adduser frappe
    sudo usermod -a -G sudo frappe
    sudo su - frappe
    sudo pip3 install frappe-bench
    bench init --frappe-branch=version-13 frappe-bench --python=python3.7


#### Add ERPNext to Bench

    cd frappe-bench
    bench new-site site1.local
    bench get-app --branch version-13 erpnext
    bench new-site site1.local
    bench --site site1.local install-app erpnext
    bench start

Eneable developer mode
    bench set-config developer_mode 1
Eneable custom scripting
    bench --site site1.local set-config server_script_enabled true

#### Implement a Command for Stopping the Bench

Not necessary but very useful: https://github.com/proenterprise/bench-stop

Command for stopping the bench

    python3 stop.py


## 2. Configure ERPNext and Import Data

Either Setup ERPNext by your own or use the following restore command to restore [my version](https://github.com/HauptschuIe/erpnext_x_rl/tree/main/ERP-System/Backup)

        bench --site site1.local --force restore \
        --mariadb-root-username root \
        --mariadb-root-password admin \
        --with-public-files ./sites/site1.local/private/backups/*files.tar \
        --with-private-files ./sites/site1.local/private/backups/*private-files.tar \
        ./sites/site1.local/private/backups/*database.sql.gz


## 3. Setup a Virtual Environment and the OpenAI Gym Environment

Setup a virtual environment following this tutorial: https://janakiev.com/blog/jupyter-virtual-envs/

Clone the Custom-Environment directory from this repository

Enter the virtual envionment

    virtualenv <env_name>
    
    source <env_name>/bin/activate

Install dependencies from the [requirements text file](https://github.com/HauptschuIe/erpnext_x_rl/blob/main/virtualenv/requirements.txt)

    pip install -r path/to/requirements.txt

Install the custom environment and its dependencies

    pip install -e .


## 4. Edit Token

Enter the ERPNext Token and the IP-Adress in the [token file](https://github.com/HauptschuIe/erpnext_x_rl/blob/main/Custom-Environment/gym-stock/gym_stock/envs/token.py)

## 5. Training an Agent

Start training an agent by running the [PPO.py file](https://github.com/HauptschuIe/erpnext_x_rl/tree/main/Rl-Algorithms)
    
    python PPO.py



## 6. Using the Trained Model

![architecture](https://github.com/HauptschuIe/erpnext_x_rl/blob/main/docs/training.png?raw=true "Architecture")

1. Insert the path to the model in the continual [training file](https://github.com/HauptschuIe/erpnext_x_rl/blob/main/Rl-Algorithms/continualtraining.py)
2. Continue to train the model by running the [training file](https://github.com/HauptschuIe/erpnext_x_rl/blob/main/Rl-Algorithms/continualtraining.py)
3. The  Environment receives the current state of the ERP system, i.e. the current stock levels taking into account goods receipts and goods issues. For example [93, 120, 17]
4. The modell decides which product should be purchased and emits an action. For example, [12, 0, 20]
5. As a result of the action, a Material Request is created via the API in the ERP system.
6. The user can now view this Material Request and make changes, for example to the order quantities. The user then confirms the Material Request and a Purchase Order is created from the Material Request in the ERP system. 5.
7. The Gym Environment recognizes this and calculates the difference between the proposed order quantity and the order quantity executed by the user. The difference results in the feedback to the agent. If there is no difference between the quantity suggested by the agent and the quantity in the Purchase Order, the reward is r=1. If the quantity is different, a negative reward is calculated from the difference. Note that this reward is in the same order of magnitude as the rewards from the environment for training.


## Sources and Useful Links

Backup and Restore: https://wiki.erpnext.org/pages/viewpage.action?pageId=40337533

Guide for installing ERPNext on Ubuntu: https://www.vultr.com/docs/how-to-install-erpnext-open-source-erp-on-ubuntu-17-04-22771

Guide for Installing Specific Python Versions: https://docs.python-guide.org/starting/install3/linux/

Stable Baselines3 Documentation: https://stable-baselines3.readthedocs.io/en/master/

OpenAI Gym: https://gym.openai.com/

Soccer Custom Environment: https://github.com/openai/gym-soccer
