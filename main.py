import argparse, time
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
DBNAME = parser.get('db_config', 'db_name')
LOG_DBNAME = parser.get('db_config', 'log_db_name')
LOG_PATH = parser.get('db_config', 'log_file_path')


def main(host=db_host, port=db_port):

    client_1 = InfluxDBClient(host, port, USER, PASSWORD, DBNAME)
    client_2 = InfluxDBClient(host, port, USER, PASSWORD, LOG_DBNAME)
    print("Check for database: " + DBNAME + ", " + LOG_DBNAME)
    try:
        client_1.create_database(DBNAME)
        client_2.create_database(LOG_DBNAME)
    except InfluxDBClientError as e:
        print(e)

    try:
        print("Checking for the log file: " + LOG_PATH)
        f = open(LOG_PATH, 'r')
        log_file_name = LOG_PATH.split('/')[-1]
    except Exception as e:
        print(e)

    metric = socket.gethostname()
    while True:
        line = ''
        while len(line) == 0 or line[-1] != '\n':
            tail = f.readline()
            if tail == '':
                time.sleep(0.1)          # avoid busy waiting
                # f.seek(0, io.SEEK_CUR) # appears to be unneccessary
                continue
            line += tail

        point_log_value = [{
            "measurement": "{}-{}".format(metric, log_file_name),
            "fields": {
                "log": line,
            },
            "tags": {
                "hostName": socket.gethostname(),
            },
        }]
        client_2.write_points(point_log_value)

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
        client_1.write_points(pointValues)


def parse_args():
    """Parse the args."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, required=False, default=db_host, help='hostname influxdb http API')
    parser.add_argument('--port', type=int, required=False, default=db_port, help='port influxdb http API')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    main(host=args.host, port=args.port)
