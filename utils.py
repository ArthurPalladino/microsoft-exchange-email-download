from datetime import datetime
from configparser import ConfigParser
import json

def load_config():
    config = ConfigParser()
    config.read('config.cfg')
    user_id=config.get("auth","user_id")
    client_id=config.get("auth","client_id")
    client_secret=config.get("auth","client_secret")
    tenant_id=config.get("auth","tenant_id")
    graph_api_url=config.get("graph_api","graph_api_url")
    scopes=config.get("graph_api","scopes")
    login_url=config.get("graph_api","login_url")
    return  user_id,client_id,client_secret,tenant_id,graph_api_url,scopes,login_url


def append_dict(filename, d):
    with open(filename, 'w', encoding='utf-8') as fp:
        fp.write(json.dumps(d))
        fp.write("\n")

def read_json_file(path):
    dict=""
    with open(path,encoding='utf-8') as f:
        dict = json.load(f)
    return dict

def load_already_read_json():
    try:
        return read_json_file('jsons/already_read.json')
    except:
        return []

def check_if_already_read(mail_id,already_read_json,received_date):
    now=datetime.now()
    if received_date.day==now.day:
        for js in already_read_json:
            if js["id"]==mail_id:
                return True
        return False
    return True

def write_to_log(message):
    now=datetime.now()
    with open(f"logs/{now.date()}.txt", "a") as f:
        f.write(f"\n{now.hour}:{now.minute} : {message}")
    