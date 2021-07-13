from flask import request, Flask, render_template
from jinja2 import Template
from src import MatrixSwot, Gmail
from src.scripts.matrix_swot import respontaswotexternoclassificacao, respostaswotexternoimportancia, respontaswotinternoclassificacao, respostaswotinternoimportancia, questaoswotexterno, questaoswotinterno

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
        MatrixSwot().dicionario_interno = resposta_interno
        MatrixSwot().pegar_pontosfortesefracosda_interna(dicionario_derepostas=MatrixSwot().dicionario_interno)
    

    return render_template('externo.html', respontaswotexternoclassificacao=respontaswotexternoclassificacao, respostaswotexternoimportancia=respostaswotexternoimportancia, questaoswotexterno=questaoswotexterno)


@app.route('/MatrixSwot', methods=['GET', 'POST'])
def matrix_swot():
    if request.method == 'POST':
        resposta_externo = request.form.to_dict(flat=False)
        MatrixSwot().dicionario_externo = resposta_externo
        MatrixSwot().pegar_pontosamecaeoportunidadesda_externa(dicionario_derepostas=MatrixSwot().dicionario_externo)
        MatrixSwot().prepar_arquivo()
        MatrixSwot().enviar_matrixswot(gmail=Gmail(),endereco_eletronico="raulbrunoslimagmail.com", assunto_doenvio="Dados das Empreendedoras")

        return "Enviado"
    
@app.route('/favicon', methods=['GET', 'POST'])
def favicon():
    return "ok"

if __name__ == '__main__':
    app.run(debug=True)