import streamlit as st
from dotenv import load_dotenv
from groq import Groq
import fitz  # PyMuPDF
import os
import re

# =========================
# Configurações iniciais
# =========================
load_dotenv()

st.set_page_config(page_title="Currículo Analytics", layout="wide")
st.title("📄 Currículo Analytics - Triagem Inteligente com IA")
st.markdown("Auxílio ao RH na seleção de currículos com análise automatizada e comparativa.")

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# =========================
# Funções
# =========================
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

def analisar_curriculos(vaga_titulo, vaga_descricao, curriculos):
    prompt = f"""
Você é um especialista em recrutamento e seleção.

Fale apenas em português.
Não use marcações como <think>, <system> ou código.
Se possível, apresente os resultados em formato de tabela.

TÍTULO DA VAGA:
{vaga_titulo}

DESCRIÇÃO DA VAGA:
{vaga_descricao}

TAREFA:
- Avalie cada currículo
- Compare com os requisitos da vaga
- Atribua uma nota de 0 a 100
- Liste pontos fortes e pontos fracos

CURRÍCULOS:
"""

    for nome, texto in curriculos:
        prompt += f"\n---\nCurrículo de {nome}:\n{texto}\n"

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "Você é um assistente de RH."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4,
        max_tokens=2000
    )

    return response.choices[0].message.content.strip()

# =========================
# Vagas
# =========================
pasta_vagas = "vagas"
arquivos_vaga = [f for f in os.listdir(pasta_vagas) if f.endswith(".pdf")]

st.sidebar.title("🧾 Seleção de Vaga")
arquivo_vaga = st.sidebar.selectbox("Selecione a vaga (PDF):", arquivos_vaga)

vaga_titulo = os.path.splitext(arquivo_vaga)[0].replace("_", " ").title()
vaga_caminho = os.path.join(pasta_vagas, arquivo_vaga)
vaga_descricao = extrair_texto_pdf_arquivo(vaga_caminho)

# =========================
# Upload de currículos
# =========================
st.sidebar.markdown("---")
st.sidebar.markdown("📤 Faça upload de até **3 currículos em PDF**")

col1, col2, col3 = st.columns(3)
with col1:
    pdf1 = st.file_uploader("PDF 1", type="pdf")
with col2:
    pdf2 = st.file_uploader("PDF 2", type="pdf")
with col3:
    pdf3 = st.file_uploader("PDF 3", type="pdf")

curriculos = []
for idx, pdf in enumerate([pdf1, pdf2, pdf3]):
    if pdf:
        texto = extrair_texto_pdf_bytes(pdf.read())
        curriculos.append((f"Candidato {idx+1}", texto))

# =========================
# Execução da IA
# =========================
if vaga_descricao and curriculos:
    if st.button("🔍 Analisar Currículos"):
        with st.spinner("Analisando com IA..."):
            resultado = analisar_curriculos(
                vaga_titulo,
                vaga_descricao,
                curriculos
            )

            resultado = re.sub(r"<[^>]+>", "", resultado)

            st.markdown("### 🧠 Resultado da IA")
            st.markdown(resultado)
else:
    st.info("Selecione uma vaga e envie pelo menos um currículo.")



st.markdown("---")
st.markdown(
    'Projeto desenvolvido por [Pablo Dantas](https://www.linkedin.com/in/pablodantasevangelista/)',
    unsafe_allow_html=True
)
