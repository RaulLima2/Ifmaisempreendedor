import csv
import numpy as np
import pandas as pd
from API import Gmail
from .interna import MatrixInterna
from .externa import MatrixExterna

class MatrixSwot(object):
    def __init__(self):
        self.dicionario_interno = pd
        self.dicionario_externo = pd
        self.nome_doarquivo = str
    
    def pegar_pontosfortesefracosda_interna(self, interna=MatrixInterna(), dicionario_derepostas=dict):
        dicionario_derepostas.update({"Pontuação":interna.analisar_resposta(dicionario_derepostas)})
        self.dicionario_interno, self.nome_doarquivo = interna.organizar_dadosinternos(dicionario_derepostas)
        
    def pegar_pontosamecaeoportunidadesda_externa(self, externa=MatrixExterna(), dicionario_derepostas=dict):
        dicionario_derepostas.update({"Pontuação":externa.analisar_respostasexterna(dicionario_derepostas)})
        self.dicionario_externo, self.nome_doarquivo = externa.organizar_dadosexterno(dicionario_derepostas)
    

    def prepar_arquivo(self):
        if self.dicionario_interno != None:
            self.nome_doarquivo = "{}_interno.csv".format(self.nome_doarquivo)
            self.dicionario_interno.to_csv(self.nome_doarquivo, delimiter=",")
        elif self.dicionario_externo != None:
            self.nome_doarquivo = "{}_externo.csv".format(self.nome_doarquivo)
            self.dicionario_interno.to_csv(self.nome_doarquivo, delimiter=",")

    def enviar_matrixswot(self, gmail=Gmail(), endereco_eletronico=str, assunto_doenvio=str):
        try:
            gmail.conectar_gmail()
            gmail.pegar_gmail(endereco_eletronico)
            gmail.pegar_assunto(assunto_doenvio)
            gmail.enviar_gmail()
        except Exception:
            print(Exception)
        