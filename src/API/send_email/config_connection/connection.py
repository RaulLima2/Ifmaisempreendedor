import os
import dataclasses
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request


class Connection(object):
        def __init__(self, file_token=str, api_name=str, api_version=str, scope=list):
            self.creds = None
            self.scope = None
            self.file_token = None
            self.api_name = None
            self.api_version = None
            self.service = None

            self.api_name = api_name
            self.api_version = api_version
            self.scope = scope
            self.file_token = file_token

        def get_connection(self):

            pickle_file = f'token_{self.api_name}_{self.api_version}.pickle'

            if os.path.exists(pickle_file):
                with open(pickle_file, 'rb') as token:
                    self.creds = pickle.load(token)
            
            if not self.creds or not self.creds.valid:
                if self.creds and self.creds.expired and self.creds.refresh_token:
                    self.creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(self.file_token, self.scope)
                    self.creds = flow.run_local_server()

                with open(pickle_file, 'wb') as token:
                    pickle.dump(self.creds, token)

            try:
                service =  build(self.api_name, self.api_version, credentials=self.creds)
                print(self.api_name, 'serviço criado com sucesso\n')
                return service
            except Exception as e:
                print("Erro de conexão\n")
                print(e)
                return None