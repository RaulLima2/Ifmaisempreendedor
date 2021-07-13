from flask import request, Flask, render_template
from jinja2 import Template
from src.scripts.matrix_swot import respontaswotexternoclassificacao, respostaswotexternoimportancia, respontaswotinternoclassificacao, respostaswotinternoimportancia, questaoswotexterno, questaoswotinterno, swot

app = Flask(__name__, template_folder='template', static_folder='static')

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")


@app.route('/SwotInterno', methods=['GET', 'POST'])
def swotinterno():
    return render_template('interno.html', respontaswotinternoclassificacao=respontaswotinternoclassificacao, respostaswotinternoimportancia=respostaswotinternoimportancia, questaoswotinterno=questaoswotinterno)


@app.route('/SwotExterno', methods=['GET', 'POST'])
def swot_externo():

    if request.method == "POST":
        resposta_interno = request.form.to_dict(flat=False)
        swot.dicionario_interno = resposta_interno
        swot.pegar_pontosfortesefracosda_interna(dicionario_derepostas=swot.dicionario_interno)
    

    return render_template('externo.html', respontaswotexternoclassificacao=respontaswotexternoclassificacao, respostaswotexternoimportancia=respostaswotexternoimportancia, questaoswotexterno=questaoswotexterno)


@app.route('/MatrixSwot', methods=['GET', 'POST'])
def matrix_swot():
    if request.method == 'POST':
        resposta_externo = request.form.to_dict(flat=False)
        swot.dicionario_externo = resposta_externo
        swot.pegar_pontosamecaeoportunidadesda_externa(dicionario_derepostas=swot.dicionario_externo)
        swot.prepar_arquivo()
        swot.enviar_matrixswot(endereco_eletronico="raulbrunoslimagmail.com", assunto_doenvio="Dados das Empreendedoras")

        return "Enviado"
    


if __name__ == '__main__':
    app.run(debug=True)