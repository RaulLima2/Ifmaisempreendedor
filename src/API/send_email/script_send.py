import os
import base64
import mimetypes
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from .config_connection import Connection

class Gmail(object):
    def __init__(self):
        self.gmails = list
        self.assunto = str
        self.conecao = Connection

    def pegar_gmail(self, gmails=list):
        self.gmails=gmails
    
    def pegar_assunto(self, assunto=str):
        self.assunto = assunto

    def conectar_gmail(self, connection=Connection()):
        try:
            self.conecao = connection
            return 200, "OK"
        except Exception:
            print(Exception)
            return 401, "Error"

    def enviar_gmail(self):
        try:
            arquivos_anexados = [r'.\Anexar\*.csv']
            mensagem_gmail = "Segue em anexo os dados das matrix swot e a analise"
            mimemessage = MIMEMultipart()

            mimemessage['to'] = self.gmails
            mimemessage['subject'] = self.assunto

            mimemessage.attach(mensagem_gmail,'plain')

            for arquivo in arquivos_anexados:
                tipo_conteudo, encode = mimetypes.guess_type(arquivo)
                tipo_main, tipo_sub = tipo_conteudo.split('/', 1)

                nome_arquivo = os.path.basename(arquivo)

                abri_arquivo = open(arquivo, "rb")

                meuarquivo = MIMEBase(tipo_main, tipo_sub)
                meuarquivo.set_payload(abri_arquivo.read())
                meuarquivo.add_header('Content-Disposition', 'attachment', filename=nome_arquivo)
                encoders.encode_base64(meuarquivo)

                abri_arquivo.close()

                mimemessage.attach(meuarquivo)

            linha_string = base64.urlsafe_b64encode(mimemessage.as_bytes()).decode()

            self.conecao.users().messages().send(
                userId='me',
                body={
                    'raw': linha_string
                }
            ).execute()


            return 200, "OK"
        except Exception:
            print(Exception)
            return 401, "Error"
        