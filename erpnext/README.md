# Installation

### Dependencies    
    
    apt update
    apt -y upgrade
    apt install software-properties-common
    add-apt-repository ppa:deadsnakes/ppa
    apt install python3.7 python3.7-dev python3.7-doc python3-pip
    pip3 install ansible
    apt-key adv --recv-keys --keyserver hkp://keyserver.ubuntu.com:80 0xF1656F24C74CD1D8
    add-apt-repository 'deb [arch=amd64,i386,ppc64el] http://mirror.nodesdirect.com/mariadb/repo/10.3/ubuntu bionic main'


### Install and configure MariaDB

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

Finnish installation

    sudo systemctl restart mariadb
    sudo systemctl enable mariadb
    sudo service mysql restart
    sudo mysql_secure_installation


### Install Node and yarn

    sudo curl --silent --location https://deb.nodesource.com/setup_12.x | sudo bash -

    curl -sL https://dl.yarnpkg.com/debian/pubkey.gpg | gpg --dearmor | sudo tee /usr/share/keyrings/yarnkey.gpg >/dev/null

    echo "deb [signed-by=/usr/share/keyrings/yarnkey.gpg] https://dl.yarnpkg.com/debian stable main" | sudo tee /etc/apt/sources.list.d/yarn.list

    sudo apt-get update && sudo apt-get install yarn


### Install nginx, nodejs, redis, supervisor

    sudo apt -y install nginx nodejs redis-server supervisor

    sudo systemctl start nginx
    sudo systemctl enable nginx

    sudo systemctl start redis-server
    sudo systemctl enable redis-server

### Install wkhtmltopdf

    sudo apt -y install libxrender1 libxext6 xfonts-75dpi xfonts-base

    wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.focal_amd64.deb

    sudo dpkg -i wkhtmltox_0.12.6-1.focal_amd64.deb

    sudo apt -f install

    sudo dpkg -i wkhtmltox_0.12.6-1.focal_amd64.deb


## Install Bench

    sudo adduser frappe
    sudo usermod -a -G sudo frappe
    sudo su - frappe
    sudo pip3 install frappe-bench
    bench init --frappe-branch=version-13 frappe-bench --python=python3.7


## Add ERPNext to Bench

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

### Implement command for stopping the bench


https://github.com/proenterprise/bench-stop

Command for stopping the bench
    python3 stop.py



###

## Source

https://www.vultr.com/docs/how-to-install-erpnext-open-source-erp-on-ubuntu-17-04-22771

https://docs.python-guide.org/starting/install3/linux/

https://youtu.be/Pw78nj58Hy4

