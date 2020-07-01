import argparse
import psutil, socket
from influxdb import InfluxDBClient
from influxdb.client import InfluxDBClientError
from configparser import ConfigParser


parser = ConfigParser()
parser.read('secret.config')
db_host = parser.get('db_credentials', 'db_host')
db_port = parser.get('db_credentials', 'db_port')
USER = parser.get('db_credentials', 'db_user')
PASSWORD = parser.get('db_credentials', 'db_passwd')
DBNAME = parser.get('db_credentials', 'db_name')


def main(host=db_host, port=db_port):
    client = InfluxDBClient(host, port, USER, PASSWORD, DBNAME)
    print("Create database: " + DBNAME)
    try:
        client.create_database(DBNAME)
    except InfluxDBClientError as e:
        print(e)

    metric = socket.gethostname()
    while True:
        pointValues = [{
            "measurement": metric,
            "fields": {
                "cpu_usage": psutil.cpu_percent(interval=1),
                "cpu_count": psutil.cpu_count(logical=True),
                "memory_total": float('%.2f' % (psutil.virtual_memory().total / (1024.0 ** 3))),
                "memory_usage": psutil.virtual_memory().percent,
                "disk_usage of /": psutil.disk_usage('/').percent,
                "disk_usage of /home": psutil.disk_usage('/home').percent,
            },
            "tags": {
                "hostName": socket.gethostname(),
            },
        }]
        client.write_points(pointValues)

def parse_args():
    """Parse the args."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, required=False, default=db_host, help='hostname influxdb http API')
    parser.add_argument('--port', type=int, required=False, default=db_port, help='port influxdb http API')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    main(host=args.host, port=args.port)
