from fast_bitrix24 import Bitrix
from datetime import datetime, timedelta
import sqlite3
from webhook import webhook_out, webhook_in


webhook = webhook_out


def fetch_selected_tasks(webhook, tasks_ids):
    webhook = webhook
    b = Bitrix(webhook)
    tasks_ids = tasks_ids

    tasks_info = b.get_by_ID(
        'tasks.task.get',
        ID_list=tasks_ids,
        ID_field_name='taskId')

    new_values = []
    for task in tasks_ids:
        ids = tasks_info[task]['task']['id']
        title = tasks_info[task]['task']['title']
        resp = tasks_info[task]['task']['responsible']['name']
        discrp = tasks_info[task]['task']['description'].split('    ')
        type_order = discrp[0].split(': ')[1]
        try:
            FIO = discrp[1].split(': ')[1]
        except:
            FIO = ''
        adress = discrp[2].split(': ')[1]

        try:
            cad_num = discrp[3].split(': ')[1]
        except:
            cad_num = ''

        coord_x = discrp[4].split(': ')[1].split(', ')[0]
        coord_y = discrp[4].split(': ')[1].split(', ')[1]
        date_create = datetime.fromisoformat(tasks_info[task]['task']['createdDate']).strftime("%d.%m.%Y")
        date_accepted = discrp[5].split(': ')[1]

        try:
            date_call = discrp[6].split(': ')[1]
        except:
            date_call = ''

        date_work = discrp[7].split(': ')[1]
        time_work = discrp[8].split(': ')[1]
        status = discrp[9].split(': ')[1]

        try:
            dots = discrp[10].split(': ')[1]
        except:
            dots = ''

        try:
            m_sqr = discrp[11].split(': ')[1]
        except:
            m_sqr = ''

        try:
            time_consumed = discrp[12].split(': ')[1]
        except:
            time_consumed = ''

        try:
            date_complete = discrp[13].split(': ')[1]
        except:
            date_complete = ''

        list_task = (ids,
                     title,
                     resp,
                     type_order,
                     FIO,
                     adress,
                     cad_num,
                     coord_x,
                     coord_y,
                     date_create,
                     date_accepted,
                     date_call,
                     date_work,
                     time_work,
                     status,
                     dots,
                     m_sqr,
                     time_consumed,
                     date_complete)

        new_values.append(list_task)

    return new_values

def fetch_all_tasks(webhook=webhook_out):
    webhook = webhook
    b = Bitrix(webhook)

    tasks = b.get_all('tasks.task.list')
    tasks_ids = [d['id'] for d in tasks]

    tasks_info = b.get_by_ID(
        'tasks.task.get',
        ID_list=tasks_ids,
        ID_field_name='taskId')

    new_values = []
    for task in tasks_ids:
        ids = tasks_info[task]['task']['id']
        title = tasks_info[task]['task']['title']
        resp = tasks_info[task]['task']['responsible']['name']
        discrp = tasks_info[task]['task']['description'].split('    ')
        type_order = discrp[0].split(': ')[1]
        try:
            FIO = discrp[1].split(': ')[1]
        except:
            FIO = ''
        adress = discrp[2].split(': ')[1]

        try:
            cad_num = discrp[3].split(': ')[1]
        except:
            cad_num = ''

        coord_x = discrp[4].split(': ')[1].split(', ')[0]
        coord_y = discrp[4].split(': ')[1].split(', ')[1]
        date_create = datetime.fromisoformat(tasks_info[task]['task']['createdDate']).strftime("%d.%m.%Y")
        date_accepted = discrp[5].split(': ')[1]

        try:
            date_call = discrp[6].split(': ')[1]
        except:
            date_call = ''

        date_work = discrp[7].split(': ')[1]
        time_work = discrp[8].split(': ')[1]
        status = discrp[9].split(': ')[1]

        try:
            dots = discrp[10].split(': ')[1]
        except:
            dots = ''

        try:
            m_sqr = discrp[11].split(': ')[1]
        except:
            m_sqr = ''

        try:
            time_consumed = discrp[12].split(': ')[1]
        except:
            time_consumed = ''

        try:
            date_complete = discrp[13].split(': ')[1]
        except:
            date_complete = ''

        list_task = (ids,
                     title,
                     resp,
                     type_order,
                     FIO,
                     adress,
                     cad_num,
                     coord_x,
                     coord_y,
                     date_create,
                     date_accepted,
                     date_call,
                     date_work,
                     time_work,
                     status,
                     dots,
                     m_sqr,
                     time_consumed,
                     date_complete)

        new_values.append(list_task)

    return new_values

# print(fetch_all_tasks(webhook))

def create_table(name_dir,table_name):
    conn = sqlite3.connect(name_dir)
    cursor = conn.cursor()
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            Номер_задачи INTEGER PRIMARY KEY,
            номер_заявки_договора TEXT,
            ответственный TEXT,
            вид_работ TEXT,
            фио_заказчика TEXT,
            адрес TEXT,
            кадастровый_номер TEXT,
            координаты_участка_x REAL,
            координаты_участка_y REAL,
            дата_постановки_задачи TEXT,
            дата_принятия_в_работу TEXT,
            дата_звонка_заказчику_и_назначения_выезда TEXT,
            дата_выезда TEXT,
            время_выезда TEXT,
            статус TEXT,
            точек_вынесено INTEGER,
            м2_снято REAL,
            времени_затрачено_с_дорогой_час REAL,
            дата_выдачи_съемки TEXT
        )
    ''')

    conn.commit()
    conn.close()

# create_table('db/survey_db.db','survey')


def update_db(name_dir, table_name, values):
    conn = sqlite3.connect(name_dir)
    cursor = conn.cursor()

    cursor.executemany(f'''
        INSERT OR IGNORE INTO {table_name} (
            Номер_задачи, номер_заявки_договора, ответственный, вид_работ, фио_заказчика, адрес, кадастровый_номер,
            координаты_участка_x, координаты_участка_y, дата_постановки_задачи, дата_принятия_в_работу,
            дата_звонка_заказчику_и_назначения_выезда, дата_выезда, время_выезда, статус,
            точек_вынесено, м2_снято, времени_затрачено_с_дорогой_час, дата_выдачи_съемки
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', values)

    conn.commit()
    conn.close()

# update_db('db/survey_db.db','survey', fetch_all_tasks(webhook))

def make_backup_db(exist_db,backup_path):
    def progress(status, remaining, total):
        print(f'Copied {total-remaining} of {total} pages...')

    con = sqlite3.connect(exist_db)
    bck = sqlite3.connect(backup_path)
    with bck:
        con.backup(bck, pages=1, progress=progress)
    bck.close()
    con.close()

# backup_db('db/survey_db.db','buckup_db/backup.db')


def get_last_tasks(name_dir, table_name, webhook):
    conn = sqlite3.connect(name_dir)
    cursor = conn.cursor()
    max_id = cursor.execute(f'''
           SELECT MAX(Номер_задачи)  FROM {table_name} 
        ''').fetchone()[0]
    print(max_id)
    webhook = webhook
    b = Bitrix(webhook)

    tasks = b.get_all('tasks.task.list', params={'filter': { ">ID": max_id }})
    tasks_ids = [d['id'] for d in tasks]

    tasks_info = b.get_by_ID(
        'tasks.task.get',
        ID_list=tasks_ids,
        ID_field_name='taskId')

    new_values = []
    for task in tasks_ids:
        ids = tasks_info[task]['task']['id']
        title = tasks_info[task]['task']['title']
        resp = tasks_info[task]['task']['responsible']['name']
        discrp = tasks_info[task]['task']['description'].split('    ')
        type_order = discrp[0].split(': ')[1]
        try:
            FIO = discrp[1].split(': ')[1]
        except:
            FIO = ''
        adress = discrp[2].split(': ')[1]

        try:
            cad_num = discrp[3].split(': ')[1]
        except:
            cad_num = ''

        coord_x = discrp[4].split(': ')[1].split(', ')[0]
        coord_y = discrp[4].split(': ')[1].split(', ')[1]
        date_create = datetime.fromisoformat(tasks_info[task]['task']['createdDate']).strftime("%d.%m.%Y")
        date_accepted = discrp[5].split(': ')[1]

        try:
            date_call = discrp[6].split(': ')[1]
        except:
            date_call = ''

        date_work = discrp[7].split(': ')[1]
        time_work = discrp[8].split(': ')[1]
        status = discrp[9].split(': ')[1]

        try:
            dots = discrp[10].split(': ')[1]
        except:
            dots = ''

        try:
            m_sqr = discrp[11].split(': ')[1]
        except:
            m_sqr = ''

        try:
            time_consumed = discrp[12].split(': ')[1]
        except:
            time_consumed = ''

        try:
            date_complete = discrp[13].split(': ')[1]
        except:
            date_complete = ''

        list_task = (ids,
                     title,
                     resp,
                     type_order,
                     FIO,
                     adress,
                     cad_num,
                     coord_x,
                     coord_y,
                     date_create,
                     date_accepted,
                     date_call,
                     date_work,
                     time_work,
                     status,
                     dots,
                     m_sqr,
                     time_consumed,
                     date_complete)

        new_values.append(list_task)

    return new_values

# print(get_last_tasks('db/survey_db.db','survey', webhook))