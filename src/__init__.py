from .API import Gmail
from .API.send_email.config_connection import Connection
from .scripts.matrix_swot import MatrixSwot

gmail = Gmail()
gmail.conectar_gmail(connection=Connection(file_token="src/API/send_email/config_connection/client_secret.json", api_name="gmail", api_version="v1", scope=['https://mail.google.com/']).get_connection())