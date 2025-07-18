from flask import Flask, render_template, request
import json
import os

from feedback import gerar_feedback
from werkzeug.utils import secure_filename
from concurrent.futures import ThreadPoolExecutor
from process import avaliar_candidato_cached
from flask_compress import Compress


app = Flask(__name__)
Compress(app)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5 MB

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/processar', methods=['POST'])
def processar():
    file = request.files.get('candidatos_json')
    if not file:
        return "Nenhum arquivo enviado", 400

    # Salvar o arquivo no servidor
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Carregar dados JSON
    with open(filepath, 'r', encoding='utf-8') as f:
        candidatos = json.load(f)

    # Avaliar candidatos em paralelo
    with ThreadPoolExecutor(max_workers=5) as executor:
        avaliacoes = list(executor.map(
            lambda c: avaliar_candidato_cached(json.dumps(c, sort_keys=True)),
            candidatos
    ))

    # Construir os resultados
    resultados = []
    reprovados = []

    for candidato, avaliacao in zip(candidatos, avaliacoes):
        resultado = {
            "nome": candidato["nome"],
            "nota_tecnica": avaliacao["nota_tecnica"],
            "nota_cultural": avaliacao["nota_cultural"],
            "justificativa": avaliacao["justificativa"],
            "aprovado": avaliacao["aprovado"]
        }

        if not avaliacao["aprovado"]:
            reprovados.append((resultado, candidato))  # salvar para gerar feedback depois
        else:
            # Feedback positivo direto
            resultado["feedback"] = f"Parabéns {candidato['nome']}! Você foi aprovado no processo seletivo. Sua combinação de competências técnicas e valores culturais é exatamente o que buscamos."

    # Gerar feedbacks para reprovados 
    def gerar_feedback_para_reprovado(par):
        resultado, candidato = par
        if not resultado["aprovado"]:  # segurança extra
            resultado["feedback"] = gerar_feedback(candidato, resultado["justificativa"])
        return resultado

    with ThreadPoolExecutor(max_workers=5) as executor:
        reprovados_atualizados = list(executor.map(gerar_feedback_para_reprovado, reprovados))

    # Atualizar lista final com os feedbacks
    for atualizado in reprovados_atualizados:
        if not atualizado.get("aprovado"):
            for i in range(len(resultados)):
                if resultados[i]["nome"] == atualizado["nome"]:
                    resultados[i] = atualizado

    # Shortlist ordenada dos aprovados
    shortlist = sorted(
        [c for c in resultados if c["aprovado"]],
        key=lambda x: x["nota_tecnica"] + x["nota_cultural"],
        reverse=True
    )

    return render_template("resultado.html", resultados=resultados, shortlist=shortlist)

if __name__ == '__main__':
    app.run(debug=True)
