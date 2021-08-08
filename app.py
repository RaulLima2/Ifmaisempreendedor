from flask import request, Flask, render_template
from jinja2 import Template
from src import swot, gmail, gerarrelatorio, enviar_relatorio, empreendedor
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
        empreendedor.getnome(request.form['Nomeempreendedora'])
        dados_internos = swot.pegar_pontosfortesefracosda_interna(dicionario_derepostas=resposta_interno)
        swot.prepar_arquivo(nomedoarquivo=empreendedor.setnome()+"interna",dicionario=dados_internos)

    return render_template('externo.html', respontaswotexternoclassificacao=respontaswotexternoclassificacao, respostaswotexternoimportancia=respostaswotexternoimportancia, questaoswotexterno=questaoswotexterno)


@app.route('/MatrixSwot', methods=['GET', 'POST'])
def matrix_swot():
    if request.method == 'POST':
        resposta_externo = request.form.to_dict(flat=False)
        dados_externos = swot.pegar_pontosamecaeoportunidadesda_externa(dicionario_derepostas=resposta_externo)
        swot.prepar_arquivo(nomedoarquivo=empreendedor.setnome()+"externa", dicionario=dados_externos)

        swot.enviar_matrixswot(gmail=gmail,nomedoarquivo=[empreendedor.setnome()+"externa", empreendedor.setnome()+"interna"], enderecoeletronico="raulbrunoslima@gmail.com", assuntodoenvio="Dados das Empreendedoras")
        
        gerarrelatorio(swot.retornarnomedoarquivo())
        enviar_relatorio(gmail=gmail,enderecoeletronico="raulbrunoslima@gmail.com", assuntodoenvio="Dados das Empreendedoras")

        return "Enviado"
    
@app.route('/favicon', methods=['GET', 'POST'])
def favicon():
    return "ok"

if __name__ == '__main__':
    app.run(debug=True)