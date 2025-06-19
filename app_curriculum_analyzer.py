import streamlit as st

col1, col2, col3 = st.columns(3)

with col1:
    pdf1 = st.file_uploader("PDF 1", type="pdf", key="pdf1")

with col2:
    pdf2 = st.file_uploader("PDF 2", type="pdf", key="pdf2")

with col3:
    pdf3 = st.file_uploader("PDF 3", type="pdf", key="pdf3")
