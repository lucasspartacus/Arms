from flask import Flask, render_template, request
import json
import os

from feedback import gerar_feedback
from concurrent.futures import ThreadPoolExecutor
from process import avaliar_candidato_cached
from flask_compress import Compress

app = Flask(__name__)
Compress(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/processar', methods=['POST'])
def processar():
    # Caminho fixo para o arquivo de candidatos
    filepath = 'candidatos.json'

    if not os.path.exists(filepath):
        return "Arquivo candidatos.json não encontrado.", 400

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
            reprovados.append((resultado, candidato))
        else:
            resultado["feedback"] = f"Parabéns {candidato['nome']}! Você foi aprovado no processo seletivo. Sua combinação de competências técnicas e valores culturais é exatamente o que buscamos."

        resultados.append(resultado)

    # Gerar feedbacks para reprovados em paralelo
    def gerar_feedback_para_reprovado(par):
        resultado, candidato = par
        if not resultado["aprovado"]:
            resultado["feedback"] = gerar_feedback(candidato, resultado["justificativa"])
        return resultado

    with ThreadPoolExecutor(max_workers=5) as executor:
        reprovados_atualizados = list(executor.map(gerar_feedback_para_reprovado, reprovados))

    # Substituir reprovados com feedback atualizado
    for atualizado in reprovados_atualizados:
        for i in range(len(resultados)):
            if resultados[i]["nome"] == atualizado["nome"]:
                resultados[i] = atualizado

    # Ordenar aprovados por nota
    shortlist = sorted(
        [c for c in resultados if c["aprovado"]],
        key=lambda x: x["nota_tecnica"] + x["nota_cultural"],
        reverse=True
    )

    return render_template("resultado.html", resultados=resultados, shortlist=shortlist)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
