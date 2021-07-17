from flask import request, Flask, render_template
from jinja2 import Template
from src import MatrixSwot, gmail
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
    interno = MatrixSwot()
    if request.method == "POST":
        resposta_interno = request.form.to_dict(flat=False)
        reesposta_interno = resposta_interno.pop('submit')
        dados_internos, nomde_arquivo = interno.pegar_pontosfortesefracosda_interna(dicionario_derepostas=resposta_interno)
        interno.nome_doarquivo = nomde_arquivo
        interno.prepar_arquivo(dicionario=dados_internos)

    return render_template('externo.html', respontaswotexternoclassificacao=respontaswotexternoclassificacao, respostaswotexternoimportancia=respostaswotexternoimportancia, questaoswotexterno=questaoswotexterno)


@app.route('/MatrixSwot', methods=['GET', 'POST'])
def matrix_swot():

    externo = MatrixSwot()

    if request.method == 'POST':
        resposta_externo = request.form.to_dict(flat=False)
        dados_externos, nomede_arquivo = externo.pegar_pontosamecaeoportunidadesda_externa(dicionario_derepostas=resposta_externo)
        externo.nome_doarquivo = nomede_arquivo
        externo.prepar_arquivo(dicionario=dados_externos)
        externo.enviar_matrixswot(gmail=gmail,endereco_eletronico="raulbrunoslimagmail.com", assunto_doenvio="Dados das Empreendedoras")

        return "Enviado"
    
@app.route('/favicon', methods=['GET', 'POST'])
def favicon():
    return "ok"

if __name__ == '__main__':
    app.run(debug=True)