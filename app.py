#!/bin/env python3
"""
Line Notify Gateway Application
License: MIT
"""

import logging, sys
import requests
from datetime import datetime
from flask import Flask, render_template, request, jsonify

import manage_logs

#LOG_PATH = 'logs/line-notify-gateway.log'
LINE_NOTIFY_URL = 'https://notify-api.line.me/api/notify'
app = Flask(__name__)


def reformat_datetime(datetime):
    """
    Reformat of datetime to humand readable.
    """
    datetime = datetime.split('T')
    date = datetime[0]
    time = datetime[1].split('.')[0]
    return date + " " + time


def firing_alert(request):
    """
    Firing alert to line notification with message payload.
    """
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    if request.json['status'] == 'firing':
        icon = "⛔⛔⛔ 😡 ⛔⛔⛔"
        status = "Firing"
        time = reformat_datetime(request.json['alerts'][0]['startsAt'])
    else:
        icon = "🔷🔷🔷 😎 🔷🔷🔷"
        status = "Resolved"
        time = str(datetime.now().date()) + ' ' + str(datetime.now().time().strftime('%H:%M:%S'))
    header = {'Authorization':request.headers['AUTHORIZATION']}
    for alert in request.json['alerts']:
        msg = "Alertmanger: " + icon + "\nStatus: " + status + "\nSeverity: " + alert['labels']['severity'] + "\nTime: " + time + "\nSummary: " + alert['annotations']['summary'] + "\nDescription: " + alert['annotations']['description']
        msg = {'message': msg}
        logging.debug(str(msg))
        logging.debug(str(header))
        response = requests.post(LINE_NOTIFY_URL, headers=header, data=msg)

@app.route('/')
def index():
    """
    Show summary information on web browser.
    """
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    return render_template('index.html', name='index')


@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    """
    Firing message to Line notify API when it's triggered.
    """
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    logging.debug(str(request))
    if request.method == 'GET':
        return jsonify({'status':'success'}), 200
    if request.method == 'POST':
        try:
            firing_alert(request)
            return jsonify({'status':'success'}), 200
        except:
            return jsonify({'status':'bad request'}), 400

@app.route('/metrics')
def metrics():
    """
    Expose metrics for monitoring tools.
    """

if __name__ == "__main__":
    app.run(host='0.0.0.0')
