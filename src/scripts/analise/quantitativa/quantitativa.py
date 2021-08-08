import dataclasses
import numpy as np
from os import name
import pandas as pd
import matplotlib.pyplot as plt
from numpy.lib.function_base import median
from src.scripts.analise.analise import Analise

@dataclasses.dataclass
class AnaliseQuantitativa(Analise):
    def __init__(cls):
        cls.nomedometodo = "Analise Quantitativa"
    
    def analisaramostras(self, amostras=np.array):
        try:
            if  amostras.size != 0:
                soma = sum(amostras)
                maximu = max(amostras)
                minimu = min(amostras)
                variance_tax = np.median(amostras)
                return "A o maxímo da pontuação da sua empressa é {max} e o minimo da pontuação da empresa é {min}, sendo a taxa média igual a {media} e a soma é {soma}".format(max=maximu, min=minimu, media=variance_tax, soma=soma)
        except Exception as e:
            print("Erro: {e}".format(e=e))
            return "Amostra vazia"
    
    def geraramostras(self, dataframes=pd.DataFrame):
        try:
            amostrastotal, amostrapositiva, amostranegativa = self.separardados(dataframe=dataframes)
            return amostrastotal, amostrapositiva, amostranegativa
        except Exception as e:
            print(e)
            return None

    def separardados(self, dataframe=pd.DataFrame):
        chaves = dataframe.keys()
        return dataframe[chaves[3]], dataframe[dataframe[chaves[3]] > 0],  dataframe[dataframe[chaves[3]] < 0]
    
