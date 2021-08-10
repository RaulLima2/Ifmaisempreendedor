import os
import numpy as np
import pandas as pd
from .quantitativa import AnaliseQuantitativa
from .qualitativa import AnaliseQualitativa
from pylatex import Document, Section, Subsection, Command, Itemize, Figure, Table, Tabular
from pylatex.utils import  NoEscape

def criar_extrutura(doc):
    doc.preamble.append(Command('title', 'Relatorio da Analise Swot'))
    doc.preamble.append(Command('author', 'Raul Bruno Santos Lima'))
    doc.preamble.append(Command('date', NoEscape(r'\today')))
    doc.create(Figure(position='htp!').add_image("static/logo_ifmais_empreendedor.png", width='89px'))
    doc.append(NoEscape(r'\maketitle'))

def criarsection(doc, namesection=str, text=list):
     with doc.create(Section(namesection)):
         for item in text:
             doc.append(item)

def criarsubsection(doc, namesubsection=str, text=list):
     with doc.create(Subsection(namesubsection)):
         for item in text:
             doc.append(item)

def criaritem(doc, text=list):
    with doc.create(Itemize()) as i:
        for item in text:
            i.add_item(item)

def criartabela(doc, text=dict):
    chaves = text.keys()
    with doc.create(Table(position='htp!')):
        with doc.create(Tabular('|c|c|c|c|')) as tabular:
            tabular.add_hline()
            tabular.add_row(chaves)
            tabular.add_hline()
            for i in range(len(text)):
                tabular.add_row((text.iloc[i,0], text.iloc[i,1], text.iloc[i,2], text.iloc[i,3]))
            tabular.add_hline()

def criarfigura(doc, text=list):
    with doc.create(Figure(position='htp!')) as fig:
        for img in text:
            fig.add_image(img, width='600px')


def enviar_relatorio(gmail, enderecoeletronico=str, assuntodoenvio=str):
    try:
        gmail.pegar_arquivos(["Anexar/{nome}.pdf".format(nome='relatorio')])
        gmail.pegar_gmail(enderecoeletronico)
        gmail.pegar_assunto(assuntodoenvio)

        #gmail.pegar_conecao()
        
        gmail.enviar_gmail()
        removerarquivos()

        return True
    except Exception:
        print(Exception)
        return False

def removerarquivos():
    try:
        os.system('rm -r Anexar/*.csv')
        os.system('rm -r Anexar/*.pdf')
        os.system('rm -r Anexar/*.tex')
        os.system('rm -r Anexar/*.png')
        return True
    except Exception:
        return False

def imprimirlistas(doc, text:list, func):
    for i in text:
        func(doc, i)

def gerarrelatorio(nomedoarquivo=str):
    qualitativa = AnaliseQualitativa()
    quantitativa = AnaliseQuantitativa()

    oportunidades = pd.read_csv("Anexar/{nome}interna.csv".format(nome=nomedoarquivo))
    pontos = pd.read_csv("Anexar/{nome}externa.csv".format(nome=nomedoarquivo))
    chaves = pontos.keys()
    amostrastotalpontos, amostrapositivapontos, amostranegativapontos = quantitativa.geraramostras(pontos)
    amostrastotaloportunidade, amostrapositivaoportunidade, amostranegativaoportunidade = quantitativa.geraramostras(oportunidades)

    quantitativa.imprimirosgraficos(x=np.arange(0, len(amostrapositivapontos)), y=amostrapositivapontos[chaves[3]], legenda=["X", "Y"], nomegrafico="Pontos Positivos")
    quantitativa.imprimirosgraficos(x=np.arange(0, len(amostranegativapontos)), y=amostranegativapontos[chaves[3]], legenda=["X", "Y"], nomegrafico="Pontos Negativos")
    quantitativa.imprimirosgraficos(x=np.arange(0, len(amostrapositivaoportunidade)), y=amostrapositivaoportunidade[chaves[3]], legenda=["X", "Y"], nomegrafico="Oportunidade Positivos")
    quantitativa.imprimirosgraficos(x=np.arange(0, len(amostranegativaoportunidade)), y=amostranegativaoportunidade[chaves[3]], legenda=["X", "Y"], nomegrafico="Oportunidade Negativos")

    
    text = {
        "Resumo": [
                    "Este documento apresenta uma analise sobre o empreendimentos nos ",
                    "perfil de qualidade e quantidade, sendo apresentado por meio de ",
                    "grafícos os pontos em que precisam ser melhorados ou aperfeiçoados.",
                    "Dessa forma foi utilizado a linguagem de programação python e os pacotes ",
                    "numpy, pandas, nltx, textblob e pylatex para o desenvolvimento e implementação ",
                    "da analise."
        ],
        "Analise Qualitativa": [
                                "Das Tabelas acima foi realizado a separação dos dados, nas respectivas chaves das colunas, após isso, foi realizar a geração de amostras a qual pegava as colunas: grau; classificação; pergunta, para gerar as amostrar, depois utilizamos o texblob para realizar a analise de sentimentos das amostras.(A função utilizada foi Naive Bayers)."
                                ],
        "Analise Quantitativa": [
                                quantitativa.analisaramostras(amostrastotalpontos),
                                quantitativa.analisaramostras(amostrapositivapontos[chaves[3]]),
                                quantitativa.analisaramostras(amostranegativapontos[chaves[3]]),
                                quantitativa.analisaramostras(amostrastotaloportunidade),
                                quantitativa.analisaramostras(amostrapositivaoportunidade[chaves[3]]),
                                quantitativa.analisaramostras(amostranegativaoportunidade[chaves[3]])
                            ],
        "Analise Grafica": [
                                ["Pontos Positivos.png"],
                                ["Pontos Negativos.png"],
                                ["Oportunidade Positivos.png"],
                                ["Oportunidade Negativos.png"]
        ]
    }

    doc = Document('')
    doc.documentclass = Command(
        'documentclass',
        options=['12pt', 'oneside', 'a4paper', 'brazil', 'landscape'],
        arguments=['abntex2'],
    )
    criar_extrutura(doc)
    criarsection(doc, namesection="Resumo", text=text['Resumo'])
    criarsection(doc=doc, namesection="Analise", text=[""])
    criarsubsection(doc=doc, namesubsection="Matrix Swot", text=[""])
    criartabela(doc=doc, text=pontos)
    criartabela(doc=doc, text=oportunidades)
    criarsubsection(doc=doc, namesubsection="Analise Qualitativa", text=[""])
    criartabela(doc=doc, text=qualitativa.analisaramostras(pontos))
    criartabela(doc=doc, text=qualitativa.analisaramostras(oportunidades))
    criarsubsection(doc=doc, namesubsection="Analise Quantitativa", text=["Na analise quantitativa, realizamos as mesmas operaçõs que na analise qualitativa, todavia, com um analise númerica sobre o problema, ou seja, atráves da analise quantitativa podemos ver o crescimento da empressa, e definir uma familiar de função que ela está contida, dessa forma podemos averir a velocidade do crescimento da empressa."])
    criaritem(doc=doc,text=text['Analise Quantitativa'][1:])
    criarsubsection(doc=doc, namesubsection="Analise Grafíca", text=[""])
    imprimirlistas(doc=doc,text=text["Analise Grafica"], func=criarfigura)
    doc.generate_pdf(filepath='Anexar/relatorio', clean_tex=True)
    doc.dumps()
