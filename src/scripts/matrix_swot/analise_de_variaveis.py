import csv
from numpy.lib.function_base import select
import pandas as pd
from .interna import MatrixInterna
from .externa import MatrixExterna


class MatrixSwot(object):
    nomearquivo: str

    def pegarnomedoarquivo(self, nome):
        self.nomearquivo = nome
    
    def retornarnomedoarquivo(self):
        return self.nomearquivo
    
    def pegar_pontosfortesefracosda_interna(self, interna=MatrixInterna(), dicionario_derepostas=dict):
        self.pegarnomedoarquivo(dicionario_derepostas["Nomeempreendedora"][0])
        dicionario_derepostas.pop('submit')
        dicionario_derepostas.update({"Pontuação": interna.analisar_respostasinterna(dicionario_derepostas)})
        return interna.organizar_dadosinternos(dicionario_derepostas)
        
    def pegar_pontosamecaeoportunidadesda_externa(self, externa=MatrixExterna(), dicionario_derepostas=dict):
        dicionario_derepostas.pop('submit')
        dicionario_derepostas.update({"Pontuação": externa.analisar_respostasexterna(dicionario_derepostas)})
        return externa.organizar_dadosexterno(dicionario_derepostas)

    def prepar_arquivo(self, nomedoarquivo=str, dicionario=pd.DataFrame):
        try:
            if dicionario.empty != True:
                dicionario.to_csv("Anexar/{nome}.csv".format(nome=nomedoarquivo), index=False)
        except Exception:
            print(Exception)

    @staticmethod
    def listadearquivos(nomedoarquivo):
        listadearqu = []
        for item in nomedoarquivo:
            listadearqu.append("Anexar/{nome}.csv".format(nome=item))
        
        return listadearqu

    def enviar_matrixswot(self, gmail, nomedoarquivo:list, enderecoeletronico=str, assuntodoenvio=str):
        try:
            print(2)
            gmail.pegar_conecao()

            gmail.pegar_arquivos(self.listadearquivos(nomedoarquivo))
            gmail.pegar_gmail(enderecoeletronico)
            gmail.pegar_assunto(assuntodoenvio)
            gmail.enviar_gmail()
            return True
        except Exception:
            print(Exception)
            return False