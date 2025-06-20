import streamlit as st
from phidata.agent import Agent
from phidata.model.groq import Groq
import fitz  # PyMuPDF
import re

st.set_page_config(page_title="Currículo Analytics", layout="wide")
st.title("📄 Currículo Analytics - Triagem Inteligente com IA")
st.markdown("Auxílio ao RH na seleção de currículos com análise automatizada e comparativa.")

# Sidebar: detalhes da vaga
st.sidebar.title("🧾 Detalhes da Vaga")
vaga_titulo = st.sidebar.text_input("Título da Vaga", placeholder="Ex: Cientista de Dados")
vaga_descricao = st.sidebar.text_area("Descrição da Vaga", placeholder="Inclua requisitos, habilidades, etc.")

st.sidebar.markdown("---")
st.sidebar.markdown("📤 Faça upload de até **3 currículos em PDF** para análise")

col1, col2, col3 = st.columns(3)
with col1:
    pdf1 = st.file_uploader("PDF 1", type="pdf", key="pdf1")
with col2:
    pdf2 = st.file_uploader("PDF 2", type="pdf", key="pdf2")
with col3:
    pdf3 = st.file_uploader("PDF 3", type="pdf", key="pdf3")

def extrair_texto_pdf(pdf_file):
    texto = ""
    if pdf_file:
        # Rewind o arquivo antes da leitura, importante para upload streamlit
        pdf_file.seek(0)
        doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
        for page in doc:
            texto += page.get_text()
    return texto

# Extrai textos dos currículos enviados
curriculos = []
for idx, pdf in enumerate([pdf1, pdf2, pdf3]):
    if pdf:
        texto = extrair_texto_pdf(pdf)
        curriculos.append((f"Candidato {idx+1}", texto))

# Verifica se há dados para análise
if vaga_descricao and curriculos:

    # Verifica se a chave da API está configurada nos secrets
    if "groq_api_key" not in st.secrets:
        st.error("⚠️ Chave da API Groq não configurada em secrets.")
        st.stop()

    groq_api_key = st.secrets["groq_api_key"]

    agente = Agent(
        name="IA de RH",
        role="Especialista em Recursos Humanos",
        model=Groq(id="deepseek-r1-distill-llama-70b", api_key=groq_api_key),
        instructions=[
            "Sempre responda em português, nunca em inglês.",
            "Analise cada currículo comparando com a vaga descrita.",
            "Atribua uma pontuação de 0 a 100 de acordo com a compatibilidade.",
            "Destaque pontos fortes e fracos de cada candidato.",
            "Compare os candidatos entre si.",
            "Mostre o resultado em forma de tabela se possível.",
            "Não use marcações como <think> ou <system>."
        ],
        markdown=True
    )

    if st.button("🔍 Analisar Currículos"):
        with st.spinner("Analisando com IA..."):
            prompt = f"""Você é um assistente de RH especializado. Abaixo está a descrição da vaga seguida dos currículos. Sua tarefa é analisar cada currículo comparando com a vaga, atribuir pontuações e destacar pontos fortes e fracos de cada candidato. Sempre escreva em português.

Título da vaga: {vaga_titulo}
Descrição da vaga:
{vaga_descricao}

Agora, analise os seguintes currículos:
"""
            for nome, texto in curriculos:
                prompt += f"\nCurrículo de {nome}:\n{texto}\n"

            resposta = agente.run(prompt)
            # Limpa tags HTML, caso haja
            texto_limpo = re.sub(r"<[^>]+>", "", resposta.content).strip()
            st.markdown("### 🧠 Resultado da IA")
            st.markdown(texto_limpo)

else:
    st.info("Preencha a descrição da vaga e envie pelo menos um currículo para análise.")
