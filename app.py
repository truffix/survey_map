from flask import Flask, render_template, render_template_string, request
from datetime import datetime
from bitrix_to_db import fetch_selected_tasks, update_db, get_last_tasks, make_backup_db
from webhook import webhook_out, webhook_in
from get_data import render_map, get_data_from_table
import schedule
import time
import threading


db_path, table_name = 'db/survey_db.db', 'survey'
backup_db = 'buckup_db/backup.db'

def any_saver(data):
    with open('log_out_webhook.txt', 'a') as f:
        f.write(f"{datetime.now()} {str(data)}\r")

def scheduled_backup(db_path, backup_db):
    schedule.every().day.at("00:00").do(make_backup_db, db_path, backup_db)

def scheduled_get_last_tasks(db_path, table_name, webhook_out):
    schedule.every().hour.do(get_last_tasks, db_path, table_name, webhook_out)

def run_scheduled_jobs():
    while True:
        schedule.run_pending()
        time.sleep(1)

app = Flask(__name__, template_folder='templates')


@app.route("/", methods=["GET"])
def map():
    return render_template("map.html")


@app.route("/btirix/", methods=['POST'])
def outwebhook():
    any_saver(request.headers.get('Content-Type'))
    request_data = request.form
    any_saver(request_data)
    request_data = request_data.to_dict()
    any_saver(request_data)

    if request_data['auth[application_token]'] == webhook_in:
        update_db(db_path, table_name, fetch_selected_tasks(webhook_out))
        render_map(get_data_from_table(db_path, table_name))
    else:
        print ('ssss')
    return "WORK"


if __name__ == "__main__":
    threading.Thread(target=run_scheduled_jobs).start()

    scheduled_backup(db_path, backup_db)
    scheduled_get_last_tasks(db_path, table_name, webhook_out)

    app.run(debug=True)

