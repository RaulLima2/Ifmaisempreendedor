import numpy as np
import pandas as pd
import dataclasses

class MatrixInterna():
    def __init__(self):
        self.bancodepontuacoesforte = pd.DataFrame({
            "Combinações Forte": [["Forte", "Totalmente importante"], ["Forte", "Muito importante"], ["Forte","Importante"], ["Forte", "Pouca importância"], ["Forte", "Totalmente sem importância"]],
            "Pontuação Forte": np.arange(10, 0, -2)
        })
        
        self.bancodepontuacoesfraco = pd.DataFrame({
            "Combinações Fraca": [["Fraco","Totalmente importante"], ["Fraco", "Muito importante"], ["Fraco","Importante"], ["Fraco", "Pouca importância"], ["Fraco", "Totalmente sem importância"]],
            "Pontuação Fraca": np.arange(10, 0, -2)
        })

    def organizar_dadosinternos(self, dicionario_derepostas=dict):
        nomes_dascolunas = list(dicionario_derepostas.keys())
        valores_dascolunas = list(dicionario_derepostas.values())
        nome_dodado = valores_dascolunas[0]

        dados_organizadosinternos = pd.DataFrame({
                                                "Pergunta": nomes_dascolunas[1],
                                                "Classificação": valores_dascolunas[1][0],
                                                "Grau de Importancia":valores_dascolunas[1][1],
                                                "Pontuação": valores_dascolunas[1]
                                            })
        
        for i in range(2, len(nomes_dascolunas) - 1):
            dados_organizadosinternos.append(
                {
                    "Pergunta": nomes_dascolunas[i],
                    "Classificação": valores_dascolunas[i][0],
                    "Grau de Importancia":valores_dascolunas[i][1],
                    "Pontuação": valores_dascolunas[i]
                }
            , ignore_index=True) 


        return dados_organizadosinternos, nome_dodado

    def analisar_respostasinterna(self, dicionario_derepostas=dict):

        respostas_analisada = self.analisar_resposta(dicionario_derepostas)

        return respostas_analisada
    
    def analisar_resposta(self, dicionario_derepostas=dict):
        lista_derespostas = list(dicionario_derepostas.values())
        
        vetor_depontuacao = np.zeros(len(lista_derespostas) + 1)

        combinacao_fraca = self.bancodepontuacoesfraco["Combinações Fraca"]
        pontuacao_fraca = self.bancodepontuacoesfraco["Pontuação Fraca"]
        combinacao_forte = self.bancodepontuacoesforte["Combinações Forte"]
        pontuacao_forte = self.bancodepontuacoesforte["Pontuação Forte"]

        for umarespostas in lista_derespostas:    
            for umacombinacao_fraca, umapontuacao_fraca, umacombinacao_forte, umapontuacao_forte in zip(combinacao_fraca, pontuacao_fraca, combinacao_forte, pontuacao_forte):                
                if np.array_equal(umacombinacao_fraca, umarespostas) == True:
                    vetor_depontuacao = np.append(vetor_depontuacao, umapontuacao_fraca)
                elif np.array_equal(umacombinacao_forte, umarespostas) == True:
                    vetor_depontuacao = np.append(vetor_depontuacao, umapontuacao_forte)
                
        
        return vetor_depontuacao