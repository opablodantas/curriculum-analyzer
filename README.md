

# 📄 Curriculum Analyzer — Triagem Inteligente com IA

O **Currículo Analytics** é uma aplicação web que utiliza **Inteligência Artificial** para apoiar equipes de **Recursos Humanos** na triagem inicial de currículos.
A ferramenta compara currículos em PDF com uma vaga específica e gera uma análise clara, objetiva e automatizada, ajudando a ganhar tempo e reduzir vieses no processo seletivo.

A proposta do projeto é **simplificar decisões* e ajudar na tomada de decisões**, não substituí-las: a IA atua como apoio estratégico ao recrutador.

---

## 🚀 O que a aplicação faz:

* Analisa currículos em PDF de forma automática
* Compara cada currículo com os requisitos da vaga
* Atribui notas de compatibilidade (0 a 100)
* Destaca pontos fortes e pontos de atenção de cada candidato
* Apresenta os resultados diretamente na interface, de forma clara e organizada

Tudo isso acontece em poucos segundos, sem necessidade de conhecimento técnico por parte do usuário.

---

## 🧠 Como funciona (visão geral)

1. O recrutador seleciona uma vaga (nesse caso, as vagas estão em formato PDF)
2. Faz upload de até **3 currículos**
3. A IA analisa os documentos com base nos critérios da vaga
4. O sistema retorna uma avaliação comparativa dos candidatos

A análise é feita utilizando um **modelo de linguagem de grande porte (LLM)**, focado em leitura e interpretação de texto profissional.

---

## 🛠️ Tecnologias utilizadas

* **Python** — linguagem principal do projeto
* **Streamlit** — interface web interativa
* **PyMuPDF (fitz)** — extração de texto de arquivos PDF
* **Groq API** — motor de IA responsável pela análise dos currículos
* **Regex (re)** — limpeza e organização do texto gerado

A aplicação foi preparada para rodar localmente e também em **ambiente de produção no Streamlit Cloud**.

---

## 📂 Estrutura do projeto

```
curriculo-analytics/
│
├─ vagas/                     # PDFs das vagas disponíveis
├─ app_curriculum_analyzer.py # Aplicação principal
├─ requirements.txt           # Dependências do projeto
└─ README.md                  # Documentação geral
```

---

## ☁️ Configuração de ambiente

A aplicação utiliza **variáveis de ambiente seguras** para acessar a API de IA.

* Em ambiente local ou produção, a chave deve ser fornecida como:

  * `GROQ_API_KEY`

No **Streamlit Cloud**, essa variável é configurada diretamente em **Settings → Secrets**, sem necessidade de arquivos `.env`.

---

## ▶️ Executando a aplicação

Após instalar as dependências, execute:

```bash
streamlit run app_curriculum_analyzer.py
```

A aplicação ficará disponível no navegador em:

```
http://localhost:8501
```

---

## 📌 Observações importantes

* A análise é realizada **em português**
* Os resultados são sugestões baseadas em IA, não decisões finais
* O projeto pode ser facilmente expandido para:

  * mais currículos
  * outros formatos de arquivo
  * novos critérios de avaliação
  * novo comportamento do LLM

---

## 👨‍💻 Autor

Desenvolvido por **Pablo Dantas**
🔗 [LinkedIn](https://www.linkedin.com/in/pablodantasevangelista/)

