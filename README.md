# Python monitoring agent 

Python monitoring agent export CPU, Memory, Storage partitions metrics and service logs to InfluxDB which is an open-source time series database.

### Requirements for this solution to run:
  - Python ver. 3.5 or greater
  - Influxdb for storage
  - Grafana for visualization

### Installation of agent on ubuntu 18.04:
```
$ python3 –V
Python 3.6.9
```
>if python3 is not installed
```sh
$ sudo apt update
$ sudo apt install -y python3 python3-pip
```

#### Creating virtual environment:
```sh
$ sudo pip3 install virtualenv
$ mkdir ~/code && cd code
$ virtualenv -p /usr/bin/python3.6 venv
$ source venv/bin/activate
```
#### Clone the agent code
```sh
$ git clone https://github.com/ullahsalik/grafana-influxdb-python.git
$ cd grafana-influxdb-python
$ pip install -r requirements.txt
$ vim secret.config 
```

> copy the below content in the secret.config file
```
[db_credentials]
db_host = <db-host-name>
db_port = <port-number>
db_user = <user-name>
db_passwd = <password>

[db_config]
db_name = server_metric
log_db_name = server_log
log_file_path = /var/log/syslog
```

#### Run the agent:
```sh
$ python main.py
```

### Visualization:
Log on to 
