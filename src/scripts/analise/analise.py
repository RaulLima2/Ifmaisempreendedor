import abc
import dataclasses
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

@dataclasses.dataclass
class Analise(abc.ABC):
    nomedometodo: str

    def __init__(self, nomedometodo:str):
        self.nomedometodo = nomedometodo

    @abc.abstractclassmethod
    def analisaramostras(self):
        pass
    
    @abc.abstractclassmethod
    def geraramostras(self):
        pass
    
    @abc.abstractclassmethod
    def separardados(self):
        pass
   
    def imprimirosgraficos(self, x, y, legenda, nomegrafico):
        plt.plot(x, y, 'r--')
        plt.title(nomegrafico)
        plt.xlabel(legenda[0])
        plt.ylabel(legenda[1])
        plt.savefig('Anexar/{nomegrafico}.png'.format(nomegrafico=nomegrafico))