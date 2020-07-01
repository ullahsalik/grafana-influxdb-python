# -*- coding: utf-8 -*-
"""Tutorial on using the server functions."""

from __future__ import print_function
import argparse

import datetime
import random
import time, psutil

from influxdb import InfluxDBClient
from influxdb.client import InfluxDBClientError

USER = 'admin'
PASSWORD = 'Password1'
DBNAME = 'cpu_usage'


def main(host='3.7.64.142', port=8086):
    client = InfluxDBClient(host, port, USER, PASSWORD, DBNAME)
    print("Create database: " + DBNAME)
    try:
        client.create_database(DBNAME)
    except InfluxDBClientError as e:
        print(e)

    metric = "server1"
    series = []
    while True:
        pointValues = [{
            "measurement": metric,
            "fields": {
                "value": psutil.cpu_percent(interval=1),
            },
            "tags": {
                "hostName": "106.215.151.188",
            },
        }]
        client.write_points(pointValues)

def parse_args():
    """Parse the args."""
    parser = argparse.ArgumentParser(
        description='example code to play with InfluxDB')
    parser.add_argument('--host', type=str, required=False,
                        default='3.7.64.142',
                        help='hostname influxdb http API')
    parser.add_argument('--port', type=int, required=False, default=8086,
                        help='port influxdb http API')
    parser.add_argument('--nb_day', type=int, required=False, default=15,
                        help='number of days to generate time series data')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    main(host=args.host, port=args.port)
