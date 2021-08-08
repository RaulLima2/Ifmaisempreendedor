import numpy as np
import pandas as pd
import dataclasses

@dataclasses.dataclass
class MatrixExterna():
    def __init__(self):
        constante_ameaca = "Ameaça"
        constante_oportunidade = "Oportunidade"
        self.bancodepontuacoesoportunidade = pd.DataFrame({
            "Combinações Oportunidade": [[constante_oportunidade, "Totalmente importante"], [constante_oportunidade, "Muito importante"], [constante_oportunidade,"Importante"], [constante_oportunidade, "Pouca importância"], [constante_oportunidade, "Totalmente sem importância"]],
            "Pontuação Oportunidade": np.arange(10, -2.5, -2.5)
        })
        
        self.bancodepontuacoesameaca = pd.DataFrame({
            "Combinações Ameaçada": [[constante_ameaca,"Totalmente importante"], [constante_ameaca, "Muito importante"], [constante_ameaca,"Importante"], [constante_ameaca, "Pouca importância"], [constante_ameaca, "Totalmente sem importância"]],
            "Pontuação Ameaçada": np.arange(-10, 2.5, 2.5)
        })

    def organizar_dadosexterno(self, dicionario_derepostas=dict):
        nomes_dascolunas = list(dicionario_derepostas.keys())
        valores_dascolunas = list(dicionario_derepostas.values())
        vetor_depontuacao = np.array(valores_dascolunas[16])

        dados_organizadosexterno = pd.DataFrame({
                                                "Pergunta": nomes_dascolunas[0],
                                                "Classificação": valores_dascolunas[0][0],
                                                "Grau de Importancia":valores_dascolunas[0][1],
                                                "Pontuação": [vetor_depontuacao[0]]
                                            })
            
        j = 1
        for i in range(1, len(nomes_dascolunas) - 1):
            dados_organizadosexterno = dados_organizadosexterno.append(
                {
                    "Pergunta": nomes_dascolunas[i],
                    "Classificação": valores_dascolunas[i][0],
                    "Grau de Importancia":valores_dascolunas[i][1],
                    "Pontuação": vetor_depontuacao[j]
                }
            , ignore_index=True)

            j += 1

        del i
        del j
        del nomes_dascolunas
        del valores_dascolunas

        dados_organizadosexterno["Pontuação"] = dados_organizadosexterno["Pontuação"].astype(str).astype(float)

        return dados_organizadosexterno

    def analisar_respostasexterna(self, dicionario_derepostas=dict):

        respostas_analisada = self.analisar_respostase(dicionario_derepostas)

        return respostas_analisada
    
    # Função que analisar as respostas que teve como escolha o parametro fraco
    # Que consiste em pontuar as combinações com a parametro fraco

    def analisar_respostase(self, dicionario_derepostas=dict):
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