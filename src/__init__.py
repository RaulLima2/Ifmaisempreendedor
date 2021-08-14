from .API import Gmail
from .API.send_email.config_connection import Connection
from .scripts.matrix_swot import MatrixSwot
from .scripts.empreendedor import Empreendedor

gmail = Gmail()

swot = MatrixSwot()

empreendedor = Empreendedor()