import os
import base64
import mimetypes
import traceback
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from .config_connection import Connection

class Gmail(object):
    arquivos: list
    gmails: list
    assunto: str
    conecao: Connection

    def __init__(self):
        self.arquivos = None
        self.gmails = None
        self.assunto = None
        self.conecao = Connection(file_token="src/API/send_email/config_connection/client_secret.json", api_name="gmail", api_version="v1", scope=['https://mail.google.com/'])

    def pegar_arquivos(self, arquivos=list):
        self.arquivos = arquivos

    def pegar_gmail(self, gmails=list):
        self.gmails=gmails
    
    def pegar_assunto(self, assunto=str):
        self.assunto = assunto

    def pegar_conecao(self, connection=Connection()):
        try:
            self.conecao = self.conecao.get_connection()
            return 200, "OK"
        except AssertionError:
            print(AssertionError)
            return 401, "Erro"

    def crear_menssagem(self, conteudo=str):
        menssagem = MIMEMultipart()
        menssagem['to'] = self.gmails
        menssagem['subject'] = self.assunto

        msg = MIMEText(conteudo)
        menssagem.attach(msg)

        return self.anexar_arquivo(msg, menssagem)

    def anexar_arquivo(self, msg, menssagem):
        arquivos_anexados = '{local}'.format(local=self.arquivos)
        tipo_conteudo, encoding = mimetypes.guess_type(arquivos_anexados)
        tipo_main, tipo_sub = tipo_conteudo.split('/', 1)

        if tipo_main == 'text':
            nomede_arquivo = os.path.basename(arquivos_anexados)
            arquivo_aberto = open(arquivos_anexados, 'rb')
            arquivo = MIMEBase(tipo_main, tipo_sub)
            arquivo.set_payload(arquivo_aberto.read())
            arquivo.add_header('Content-Disposition', 'attachment', filename=nomede_arquivo)
            encoders.encode_base64(arquivo)
            arquivo_aberto.close()

        menssagem.attach(arquivo)

        return {'raw': base64.urlsafe_b64encode(menssagem.as_bytes()).decode()}

    def enviar_gmail(self):
        try:
            mensagem_gmail = "Segue em anexo os dados das matrix swot e a analise"
            
            print('1')
            mensagem = self.conecao.users().messages().send(
                                                                userId='me',
                                                                body=self.crear_menssagem(mensagem_gmail)
                                                            ).execute()
            print(mensagem['id'])

            return mensagem
        except Exception as error:
            traceback.print_exc()
        