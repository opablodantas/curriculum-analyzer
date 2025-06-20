import streamlit as st
from phi.agent import Agent
from phi.model.groq import Groq
from dotenv import load_dotenv
import fitz  # PyMuPDF
import re

# Carrega variáveis de ambiente
load_dotenv()

# Configuração da página
st.set_page_config(page_title="Currículo Analytics", layout="wide")
st.title("📄 Currículo Analytics - Triagem Inteligente com IA")
st.markdown("Auxílio ao RH na seleção de currículos com análise automatizada e comparativa.")

st.sidebar.title("🧾 Detalhes da Vaga")
vaga_titulo = st.sidebar.text_input("Título da Vaga", placeholder="Ex: Cientista de Dados")
vaga_descricao = st.sidebar.text_area("Descrição da Vaga", placeholder="Inclua requisitos, habilidades, etc.")

st.sidebar.markdown("---")
st.sidebar.markdown("📤 Faça upload de até **3 currículos em PDF** para análise")

# Upload de currículos
col1, col2, col3 = st.columns(3)
with col1:
    pdf1 = st.file_uploader("PDF 1", type="pdf", key="pdf1")
with col2:
    pdf2 = st.file_uploader("PDF 2", type="pdf", key="pdf2")
with col3:
    pdf3 = st.file_uploader("PDF 3", type="pdf", key="pdf3")

# Função para extrair texto do PDF
def extrair_texto_pdf(pdf_file):
    texto = ""
    if pdf_file:
        doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
        for page in doc:
            texto += page.get_text()
    return texto

# Carregando currículos enviados
curriculos = []
for idx, pdf in enumerate([pdf1, pdf2, pdf3]):
    if pdf:
        texto = extrair_texto_pdf(pdf)
        curriculos.append((f"Candidato {idx+1}", texto))

# Define o Agente de IA em português
if vaga_descricao and curriculos:
    agente = Agent(
        name="IA de RH",
        role="Especialista em Recursos Humanos",
        model=Groq(id="deepseek-r1-distill-llama-70b"),
        instructions=[
            "Fale em português.",
            "Analise cada currículo comparando com a vaga descrita.",
            "Atribua uma pontuação de 0 a 100 de acordo com a compatibilidade.",
            "Destaque pontos fortes e fracos de cada candidato.",
            "Mostre o resultado em forma de tabela se possível.",
            "Não use marcações como <think> ou <sistem>."
        ],
        markdown=True
    )

    if st.button("🔍 Analisar Currículos"):
        with st.spinner("Analisando com IA..."):

            # Monta o prompt em português
            prompt = f"""Você é um assistente de RH. Abaixo está a descrição da vaga seguida dos currículos. Analise e compare:

Título da vaga: {vaga_titulo}
Descrição da vaga:
{vaga_descricao}

Agora, avalie os currículos abaixo:

"""
            for nome, texto in curriculos:
                prompt += f"\nCurrículo de {nome}:\n{texto}\n"

            resposta = agente.run(prompt)

            # Remove possíveis tags como <think>
            texto_limpo = re.sub(r"<[^>]+>", "", resposta.content).strip()

            st.markdown("### 🧠 Resultado da IA")
            st.markdown(texto_limpo)

else:
    st.info("Preencha a descrição da vaga e envie pelo menos um currículo.")
