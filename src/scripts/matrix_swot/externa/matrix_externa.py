import numpy as np
import pandas as pd
import dataclasses

class MatrixExterna():
    def __init__(self):
        constante_ameaca = "Ameaça"
        const_oportunidade = "Oportunidade"
        self.bancodepontuacoesoportunidade = pd.DataFrame({
            "Combinações Oportunidade": [[const_oportunidade, "Totalmente importante"], [const_oportunidade, "Muito importante"], [const_oportunidade,"Importante"], [const_oportunidade, "Pouca importância"], [const_oportunidade, "Totalmente sem importância"]],
            "Pontuação Oportunidade": np.arange(10, 0, -2)
        })
        
        self.bancodepontuacoesameaca = pd.DataFrame({
            "Combinações Ameaçada": [[constante_ameaca,"Totalmente importante"], [constante_ameaca, "Muito importante"], [constante_ameaca,"Importante"], [constante_ameaca, "Pouca importância"], [constante_ameaca, "Totalmente sem importância"]],
            "Pontuação Ameaçada": np.arange(10, 0, -2)
        })

    def organizar_dadosexterno(self, dicionario_derepostas=dict):
        nomes_dascolunas = list(dicionario_derepostas.keys())
        valores_dascolunas = list(dicionario_derepostas.values())
        nome_dodado = valores_dascolunas[0][0]
        vetor_depontuacao = np.array(valores_dascolunas[17])

        dados_organizadosexterno = pd.DataFrame({
                                                "Pergunta": nomes_dascolunas[1],
                                                "Classificação": valores_dascolunas[1][0],
                                                "Grau de Importancia":valores_dascolunas[1][1],
                                                "Pontuação": [vetor_depontuacao[0]]
                                            })
            
        for i in range(2, len(nomes_dascolunas) - 2):
            j = 1
            dados_organizadosexterno = dados_organizadosexterno.append(
                {
                    "Pergunta": nomes_dascolunas[i],
                    "Classificação": valores_dascolunas[i][0],
                    "Grau de Importancia":valores_dascolunas[i][1],
                    "Pontuação": [vetor_depontuacao[j]]
                }
            , ignore_index=True)

            j += 1

        del i
        del j
        del nomes_dascolunas
        del valores_dascolunas

        return dados_organizadosexterno, nome_dodado

    def analisar_respostasexterna(self, dicionario_derepostas=dict):

        respostas_analisada = self.analisar_respostas(dicionario_derepostas)

        return respostas_analisada
    
    # Função que analisar as respostas que teve como escolha o parametro fraco
    # Que consiste em pontuar as combinações com a parametro fraco

    def analisar_respostas(self, dicionario_derepostas=dict):
        lista_derespostas = list(dicionario_derepostas.values())
        
        vetor_depontuacao = []

        combinacao_oportunidade = self.bancodepontuacoesoportunidade["Combinações Oportunidade"]
        pontuacao_oportunidade = self.bancodepontuacoesoportunidade["Pontuação Oportunidade"]
        combinacao_ameaca = self.bancodepontuacoesameaca["Combinações Ameaçada"]
        pontuacao_ameaca = self.bancodepontuacoesameaca["Pontuação Ameaçada"]

        for umarespostas in lista_derespostas:    
            for umacombinacao_oportunidade, umapontuacao_oportunidade, umacombinacao_ameaca, umapontuacao_ameaca in zip(combinacao_oportunidade, pontuacao_oportunidade, combinacao_ameaca, pontuacao_ameaca):                
                if np.array_equal(umacombinacao_oportunidade, umarespostas) == True:
                    vetor_depontuacao.append(umapontuacao_oportunidade)
                elif np.array_equal(umacombinacao_ameaca, umarespostas) == True:
                    vetor_depontuacao.append(umapontuacao_ameaca)
                
        
        return np.array(vetor_depontuacao)