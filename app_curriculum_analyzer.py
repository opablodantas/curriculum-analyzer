import streamlit as st
from phi.agent import Agent
from phi.model.groq import Groq
from dotenv import load_dotenv
import fitz  # PyMuPDF
import re
import os

# Carrega variáveis de ambiente
load_dotenv()

# Configuração da página
st.set_page_config(page_title="Currículo Analytics", layout="wide")
st.title("📄 Currículo Analytics - Triagem Inteligente com IA")
st.markdown("Auxílio ao RH na seleção de currículos com análise automatizada e comparativa.")

# === Funções ===
@st.cache_data
def extrair_texto_pdf_bytes(pdf_file_bytes):
    texto = ""
    if pdf_file_bytes:
        doc = fitz.open(stream=pdf_file_bytes, filetype="pdf")
        for page in doc:
            texto += page.get_text()
    return texto

@st.cache_data
def extrair_texto_pdf_arquivo(caminho):
    texto = ""
    doc = fitz.open(caminho)
    for page in doc:
        texto += page.get_text()
    return texto

# === Vaga: carregar PDF da pasta ===
pasta_vagas = "vagas"
arquivos_vaga = [f for f in os.listdir(pasta_vagas) if f.endswith(".pdf")]

st.sidebar.title("🧾 Seleção de Vaga")
arquivo_vaga = st.sidebar.selectbox("Selecione a vaga (PDF):", arquivos_vaga)

vaga_titulo = os.path.splitext(arquivo_vaga)[0].replace("_", " ").title()
vaga_caminho = os.path.join(pasta_vagas, arquivo_vaga)
vaga_descricao = extrair_texto_pdf_arquivo(vaga_caminho)

# === Upload de currículos ===
st.sidebar.markdown("---")
st.sidebar.markdown("📤 Faça upload de até **3 currículos em PDF** para análise")

col1, col2, col3 = st.columns(3)
with col1:
    pdf1 = st.file_uploader("PDF 1", type="pdf", key="pdf1")
with col2:
    pdf2 = st.file_uploader("PDF 2", type="pdf", key="pdf2")
with col3:
    pdf3 = st.file_uploader("PDF 3", type="pdf", key="pdf3")

# === Currículos: carregar texto ===
curriculos = []
for idx, pdf in enumerate([pdf1, pdf2, pdf3]):
    if pdf:
        texto = extrair_texto_pdf_bytes(pdf.read())
        curriculos.append((f"Candidato {idx+1}", texto))

# === Agente IA ===
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

            prompt = f"""Você é um assistente de RH. Abaixo está a descrição da vaga seguida dos currículos. Analise e compare:

Título da vaga: {vaga_titulo}
Descrição da vaga:
{vaga_descricao}

Agora, avalie os currículos abaixo:
"""
            for nome, texto in curriculos:
                prompt += f"\nCurrículo de {nome}:\n{texto}\n"

            resposta = agente.run(prompt)
            texto_limpo = re.sub(r"<[^>]+>", "", resposta.content).strip()

            st.markdown("### 🧠 Resultado da IA")
            st.markdown(texto_limpo)

else:
    st.info("Selecione uma vaga da lista e envie pelo menos um currículo.")

# === Sobre o Projeto ===
st.markdown("## ℹ️ Sobre o Projeto")
st.markdown("""
Enquanto estudava sobre agentes de inteligência artificial, percebi que muitos colegas de trabalho gastavam um tempo considerável analisando currículos individualmente — uma tarefa que, em teoria, deveria ser simples. Essa análise manual, repetitiva e demorada, frequentemente se tornava um gargalo no processo de seleção.

Pensando em tornar essa etapa mais prática e eficiente, criei este projeto como uma ferramenta de suporte à equipe de RH. A proposta é oferecer uma solução que auxilie na triagem inicial de currículos, reduzindo o tempo de análise e aumentando as chances de encontrar o candidato ideal com mais agilidade e assertividade.
""")

# === Rodapé ===
st.markdown("---")
st.markdown(
    'Projeto desenvolvido por [Pablo Dantas](https://www.linkedin.com/in/pablodantasevangelista/)', 
    unsafe_allow_html=True
)
