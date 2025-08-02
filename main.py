
import msal
import requests
import base64
from time import sleep
from datetime import datetime

from utils import append_dict, check_if_already_read, load_already_read_json, load_config, write_to_log
    
def load_all_emails(url,headers):
    values_to_return=[]
    while True:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            emails = response.json()
            values_to_return.extend(emails['value'])
            url=emails.get("@odata.nextLink",0)
            if url==0:
                break
        else:
            write_to_log(f"Erro ao obter e-mails \nSTATUS: {response.status_code}")
            write_to_log(f"RESPONSE:{response.json()}")
            break
    return values_to_return

def download_attachment(attachments,mail_id,received_date,already_read):
    for attachment in attachments['value']:
        if 'contentBytes' in attachment:
            content_data = attachment['contentBytes']
            file_name = attachment['name']
            file_extension = file_name.split('.')[-1].lower()
            try:
                if file_extension == 'xlsx':
                    with open("attachments/"+file_name, 'wb') as f:
                        f.write(base64.b64decode(content_data))  
                    write_to_log(f"{file_name} salvo com sucesso.")
                    already_read.append({"id":mail_id,"receivedDate":f"{received_date}"})
                    append_dict('jsons/already_read.json',already_read)
            except Exception as e:
                write_to_log(f"Erro ao baixar anexo \n{e}")

def main():
    user_id,client_id,client_secret,tenant_id,graph_api_url,scopes,login_url=load_config()
    already_read=load_already_read_json()

    app = msal.ConfidentialClientApplication(client_id, authority=login_url+tenant_id, client_credential=client_secret)
    token_response = app.acquire_token_for_client(scopes=eval(scopes))
    access_token = token_response['access_token']
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    values=load_all_emails(graph_api_url+user_id+'/messages',headers)

    for email in values:
        received_date=datetime.strptime(email["receivedDateTime"].replace("T"," ").replace("Z",""),"%Y-%m-%d %H:%M:%S")
        mail_id=email['id']
        if email["hasAttachments"] and not check_if_already_read(mail_id,already_read,received_date):
            attachments_response = requests.get(f'{graph_api_url}{user_id}/messages/{mail_id}/attachments', headers=headers)
            if attachments_response.status_code == 200:
                download_attachment(attachments_response.json(),mail_id,received_date,already_read)
            else:
                write_to_log(f"Erro ao obter anexos \nSTATUS: {attachments_response.status_code}")
                write_to_log(f"RESPONSE:{attachments_response.json()}")
            sleep(1)    

if __name__ == "__main__":
    main()