import streamlit as st
import pandas as pd
import requests
from datetime import datetime

st.title("🚀 Eixo 2: Projetos e Atividades")

URL_LEITURA_PROJETOS = st.secrets["LINK_CSV_PROJETOS"]

URL_ESCRITA_SCRIPT = st.secrets["URL_ESCRITA_SCRIPT"]

# 1. LER OS DADOS DA PLANILHA
try:
    df_projetos = pd.read_csv(URL_LEITURA_PROJETOS)
except Exception:
    df_projetos = pd.DataFrame(columns=["Nome", "Status", "Prioridade", "Tipo", "Prazo"])

# 2. FORMULÁRIO DE CADASTRO
with st.form("novo_projeto"):
    st.subheader("🆕 Cadastrar Novo Projeto/Atividade")
    
    nome = st.text_input("Nome do Projeto/Atividade")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        status = st.selectbox("Status", ["Em estruturação", "Em desenvolvimento", "Pausado", "Concluído"])
    with c2:
        prioridade = st.selectbox("Prioridade", ["Baixa", "Média", "Alta", "Urgente", "fudeu"])
    with c3:
        tipo = st.selectbox("Tipo", ["Sistema", "TCC", "Pesquisa", "Startup", "Design", "Projeto Social"])
        
    prazo = st.date_input("Prazo Final")
    
    submit = st.form_submit_button("Adicionar Projeto")
    
    if submit and nome:
        dados_envio = {
            "aba": "Projetos",
            "valores": [nome, status, prioridade, tipo, str(prazo)]
        }
        
        resposta = requests.post(URL_ESCRITA_SCRIPT, json=dados_envio)
        if resposta.status_code == 200:
            st.success("✅ Projeto adicionado com sucesso!")
            st.rerun()
        else:
            st.error("Erro ao conectar com a planilha.")

# 3. EXIBIÇÃO E ALERTAS (BI LOCAL)
st.markdown("---")
st.subheader("📋 Seus Projetos Ativos")

if not df_projetos.empty:
    # Garantir que a coluna Prazo é formato data
    df_projetos['Prazo'] = pd.to_datetime(df_projetos['Prazo'], errors='coerce')
    hoje = pd.to_datetime(datetime.now().date())
    
    # Cálculo de dias restantes
    df_projetos['Dias_Restantes'] = (df_projetos['Prazo'] - hoje).dt.days
    
    # Função para colorir a prioridade na tabela
    def colorir_prioridade(val):
        if val == 'fudeu':
            return 'background-color: #ff4b4b; color: white; font-weight: bold;'
        elif val == 'Urgente':
            return 'background-color: #ffa500; color: black;'
        return ''

    # Mostrar a tabela bonita
    st.dataframe(
        # Como deve ficar
        df_projetos.style.map(colorir_prioridade, subset=['Prioridade']), 
        use_container_width=True
    )
else:
    st.info("Nenhum projeto cadastrado.")