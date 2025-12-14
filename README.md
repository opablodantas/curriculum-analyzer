

# Currículo Analytics - Triagem Inteligente com IA

Currículo Analytics é uma aplicação de triagem de currículos desenvolvida para auxiliar equipes de RH na seleção de candidatos. O projeto utiliza **Inteligência Artificial** para analisar currículos em PDF (mas podendo facilmente adaptado para outros formatos caso seja necessário), comparando-os com os requisitos da vaga e gerando uma avaliação automatizada com notas, pontos fortes e fracos.

---

## Tecnologias Utilizadas

* **Python**: Linguagem principal do projeto.
* **Streamlit**:Framework para criação de interfaces web interativas.
* **PyMuPDF (fitz)**: Biblioteca para leitura e extração de texto de arquivos PDF.
* **Groq API**: Plataforma de IA utilizada para análise de currículos (modelo `llama-3.1-8b-instant`).
* **python-dotenv**: Gerenciamento de variáveis de ambiente (como `GROQ_API_KEY`).
* **re (Regex)**: Limpeza de texto gerado pela IA.

---

## Estrutura do Projeto

```
curriculo-analytics/
│
├─ vagas/                           # PDFs das vagas disponíveis
├─ app_curriculum_analyzer.py       # Aplicação principal Streamlit
├─ .env                             # Variáveis de ambiente (ex: GROQ_API_KEY)
├─ requirements.txt                 # Dependências do projeto
└─ README.md                        # Este arquivo
```

---

## Funcionalidades

1. **Upload de Vagas e Currículos**

   * Upload de PDFs de vagas para análise.
   * Upload de até 3 currículos simultaneamente.

2. **Extração de Texto de PDFs**

   * Extração de texto via **PyMuPDF**, suportando upload de arquivos ou leitura local.

3. **Análise de Currículos com IA**

   * Avaliação automática comparando currículos com os requisitos da vaga.
   * Geração de notas de 0 a 100, pontos fortes e pontos fracos de cada candidato.
   * Resultados apresentados diretamente na interface Streamlit.

---

## Como Rodar o Projeto

1. **Clone o repositório**

```bash
git clone https://github.com/seu-usuario/curriculo-analytics.git
cd curriculo-analytics
```

2. **Instale as dependências**

```bash
pip install -r requirements.txt
```

3. **Configure a API Key do Groq**

Crie um arquivo `.env` na raiz do projeto:

```
GROQ_API_KEY=sua_chave_aqui
```

4. **Execute a aplicação Streamlit**

```bash
streamlit run app_curriculum_analyzer.py
```

5. **Acesse no navegador**
   A aplicação estará disponível em `http://localhost:8501`.

---

## Observações

* O projeto está configurado para análise de currículos em português.
* É necessário ter uma conta e **API Key válida da Groq** para que a análise funcione.
* A IA retorna os resultados em formato textual, que é processado e exibido no Streamlit.

---

## Autor

Desenvolvido por [Pablo Dantas](https://www.linkedin.com/in/pablodantasevangelista/)

---
