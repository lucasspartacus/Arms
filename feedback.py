import google.generativeai as genai

genai.configure(api_key="AIzaSyCq5KGI1At419D8010MNHsM-2b4nghLfxc")

model = genai.GenerativeModel("models/gemini-1.5-flash")

def gerar_feedback(candidato, justificativa):
    prompt = f"""
    Gere um feedback respeitoso para o candidato {candidato['nome']}, que não foi aprovado no processo seletivo.

    Perfil:
    Habilidades: {', '.join(candidato['habilidades'])}
    Experiência: {candidato['experiencia']} anos
    Valores: {', '.join(candidato['valores'])}

    Motivo da não aprovação: {justificativa}

    O feedback deve ser construtivo, motivador e breve.
    """

    response = model.generate_content(prompt)
    return response.text

import google.generativeai as genai

genai.configure(api_key="AIzaSyCq5KGI1At419D8010MNHsM-2b4nghLfxc")

model = genai.GenerativeModel("models/gemini-1.5-flash")

def gerar_feedback(candidato, justificativa):
    prompt = f"""
    Gere um feedback respeitoso e construtivo para o candidato {candidato['nome']}, que não foi aprovado no processo seletivo.

    Perfil:
    Habilidades: {', '.join(candidato['habilidades'])}
    Experiência: {candidato['experiencia']} anos
    Valores: {', '.join(candidato['valores'])}

    Motivo da não aprovação: {justificativa}

    O feedback deve ser breve, motivador e educado.
    """

    response = model.generate_content(prompt)
    return response.text.strip()
