import csv
import numpy as np
import pandas as pd
from .interna import MatrixInterna
from .externa import MatrixExterna

class MatrixSwot(object):
    def __init__(self):
        self.nome_doarquivo = str
    
    def pegar_pontosfortesefracosda_interna(self, interna=MatrixInterna(), dicionario_derepostas=dict):
        dicionario_derepostas = dicionario_derepostas.pop('submit')
        dicionario_derepostas.update({"Pontuação":interna.analisar_resposta(dicionario_derepostas)})
        return interna.organizar_dadosinternos(dicionario_derepostas)
        
    def pegar_pontosamecaeoportunidadesda_externa(self, externa=MatrixExterna(), dicionario_derepostas=dict):
        dicionario_derepostas = dicionario_derepostas.pop('submit')
        dicionario_derepostas.update({"Pontuação":externa.analisar_respostasexterna(dicionario_derepostas)})
        return externa.organizar_dadosexterno(dicionario_derepostas)
    

    def prepar_arquivo(self, dicionario=pd.DataFrame):
        if dicionario.empty != True:
            dicionario.to_csv(r".\Anexar\{nome}.csv".format(nome=self.nome_doarquivo), index=False)

    def enviar_matrixswot(self, gmail, endereco_eletronico=str, assunto_doenvio=str):
        try:
            gmail.conectar_gmail()
            gmail.pegar_gmail(endereco_eletronico)
            gmail.pegar_assunto(assunto_doenvio)
      
            gmail.enviar_gmail()
        except Exception:
            print(Exception)
        