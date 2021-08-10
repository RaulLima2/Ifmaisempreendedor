import dataclasses
import pandas as pd
from textblob import TextBlob
from src.scripts.analise.analise import Analise
from textblob.sentiments import NaiveBayesAnalyzer

@dataclasses.dataclass
class AnaliseQualitativa(Analise):
    def __init__(cls):
        cls.nomemetodo = "Analise Qualitativa"
    
    def analisaramostras(self, dataframepandas=pd.DataFrame):
        dataframe = {}

        chaves = ["amostras", "classificação","pontos positivos","pontos negativos"]
        dataframe = dataframe.fromkeys(chaves)
        df = pd.DataFrame([dataframe])
        amostras = self.geraramostras(dataframepandas)

        for item in amostras:
            self.analisetextblob(df, chaves, item)
        
        classification_sentiments = df
        return classification_sentiments

    def analisetextblob(self, dataframe, chaves, item):
        try:
            itemtranduzido = str(TextBlob(item).translate(to='en'))
            blob = TextBlob(itemtranduzido, analyzer=NaiveBayesAnalyzer())
            dataframe.append({
                chaves[0]: item,
                chaves[1]: blob.sentiment.classification,
                chaves[2]: blob.sentiment.p_pos,
                chaves[3]: blob.sentiment.p_neg       
            }, ignore_index=True)
        except Exception as e:
            print(e)

    def geraramostras(self, dataframepandas=pd.DataFrame):
        try:
            amostras = []
            grau, classificacao, pergunta, pontospositivos, pontosnegativos = self.separardados(dataframepandas)
            for i in range(len(grau)):
                amostras.append("É " + grau[i] + " pois " + pergunta[i] +", logo é uma " + classificacao[i])
            
            pontospositivos.to_csv('Anexar/pontospositivos.csv')
            pontosnegativos.to_csv('Anexar/pontosnegativos.csv')

            del pontosnegativos
            del pontospositivos

            return amostras
        except Exception as e:
            print(e)
            return None

    def separardados(self, dataframepandas=pd.DataFrame):
        chaves = dataframepandas.keys()
        grau = dataframepandas[chaves[2]]
        classificacao = dataframepandas[chaves[1]]
        pergunta = dataframepandas[chaves[0]]
        pontospositivos = dataframepandas[dataframepandas[chaves[3]] > 0]
        pontosnegativos = dataframepandas[dataframepandas[chaves[3]] < 0]

        return grau, classificacao, pergunta, pontospositivos, pontosnegativos