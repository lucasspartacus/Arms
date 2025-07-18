import google.generativeai as genai
import json
import re
from functools import lru_cache

# Configuração da API do Gemini
genai.configure(api_key="AIzaSyCq5KGI1At419D8010MNHsM-2b4nghLfxc") 

model = genai.GenerativeModel("gemini-1.5-flash")

# Função com cache 
@lru_cache(maxsize=256)
def avaliar_candidato_cached(candidato_json: str):
    candidato = json.loads(candidato_json)
    return avaliar_candidato(candidato)

# Função principal de avaliação
def avaliar_candidato(candidato):
    prompt = f"""
        Você é um assistente avaliador de RH. Responda com **apenas** um JSON válido.

        Perfil do candidato:
        Nome: {candidato['nome']}
        Habilidades: {', '.join(candidato['habilidades'])}
        Experiência: {candidato['experiencia']} anos
        Valores: {', '.join(candidato['valores'])}

        Critérios:
        - Técnicos: experiência com Python e versionamento (Git)
        - Culturais: colaboração e aprendizado contínuo

        Responda **somente** com um JSON no seguinte formato:
        {{
        "nota_tecnica": int (0 a 10),
        "nota_cultural": int (0 a 10),
        "justificativa": str,
        "aprovado": bool
        }}
    """.strip()

    try:
        response = model.generate_content(prompt)
        content = response.text.strip()

        # Regex para extrair JSON seguro
        match = re.search(r'\{.*\}', content, re.DOTALL)
        if match:
            json_text = match.group()
            resultado = json.loads(json_text)
            return resultado
        else:
            raise ValueError("Nenhum JSON encontrado na resposta.")

    except Exception as e:
        print("Erro ao interpretar resposta da IA:", str(e))
        return {
            "nota_tecnica": 0,
            "nota_cultural": 0,
            "justificativa": "Erro ao processar IA.",
            "aprovado": False
        }
