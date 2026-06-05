import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import time

st.title("💰 Eixo 1: Gestão Financeira")

URL_LEITURA_FINANCEIRO = st.secrets["LINK_CSV_FINANCEIRO"]
URL_ESCRITA_SCRIPT = st.secrets["URL_ESCRITA_SCRIPT"]

# 1. LER OS DADOS DA PLANILHA (Via CSV Público com Destruidor de Cache)
try:
    carimbo = int(time.time())
    df_existente = pd.read_csv(f"{URL_LEITURA_FINANCEIRO}&_cb={carimbo}", on_bad_lines='skip')
except Exception:
    df_existente = pd.DataFrame(columns=["Data", "Tipo", "Categoria", "Natureza", "Valor", "Descricao"])

categorias = ["Salário", "Freelance", "Vale Alimentação/Refeição", "Vale Transporte", "Moradia", 
              "Assinaturas", "Saúde", "Investimentos", "Educação", "Aluguel", "Moto", 
              "Conta de Luz", "Conta de Água", "Pet", "Imposto de Renda", "Outros"]

# 2. FORMULÁRIO DE ESCRITA
with st.form("novo_gasto"):
    st.subheader("📝 Registrar Movimentação")
    col1, col2 = st.columns(2)
    with col1:
        tipo = st.selectbox("Tipo", ["Saída", "Entrada"])
        categoria = st.selectbox("Categoria", categorias)
        natureza = st.selectbox("Natureza", ["Despesa Fixa", "Despesa Variável", "N/A"])
    with col2:
        valor_str = st.text_input("Valor (R$)", placeholder="Ex: 2800,90 ou 2.800,90")
        data = st.date_input("Data")
        descricao = st.text_input("Descrição/Detalhe")
        
    submit = st.form_submit_button("Salvar Registro")
    
    if submit:
        # PASSO 1: Limpa e traduz o número que você digitou
        try:
            if not valor_str:
                valor_final = 0.0 # Salva 0 se você esquecer de digitar
            else:
                valor_limpo = valor_str.replace(".", "").replace(",", ".")
                valor_final = float(valor_limpo)
        except ValueError:
            st.error("🚨 Formato de valor inválido! Digite apenas números, ponto ou vírgula.")
            st.stop() # Para o código aqui se der erro
            
        # PASSO 2: Prepara os dados para o Google com o número certinho
        dados_envio = {
            "aba": "Financeiro",
            "valores": [str(data), tipo, categoria, natureza, valor_final, descricao]
        }
        
        # PASSO 3: Envia os dados para a planilha
        resposta = requests.post(URL_ESCRITA_SCRIPT, json=dados_envio)
        
        # PASSO 4: Avisa que deu certo e recarrega
        if resposta.status_code == 200:
            st.success("✅ Salvo com sucesso no Sheets!")
            st.rerun()
        else:
            st.error("Erro ao salvar os dados. Verifique a URL do Script.")

# --- 3. GRÁFICOS E BI ---
st.markdown("---")
st.subheader("📊 Análise de Gastos Reais")

if not df_existente.empty:
    # Tratamento para garantir que a tabela exiba e calcule certo
    df_existente["Valor"] = df_existente["Valor"].astype(str)
    df_existente["Valor"] = df_existente["Valor"].str.replace(',', '', regex=False)
    df_existente["Valor"] = pd.to_numeric(df_existente["Valor"], errors='coerce')

    # Mostrar tabela
    st.dataframe(df_existente, use_container_width=True)
    
    # Gráfico de Pizza (Apenas saídas)
    df_saidas = df_existente[df_existente["Tipo"] == "Saída"]
    if not df_saidas.empty:
        fig = px.pie(df_saidas, values='Valor', names='Categoria', title="Maiores Gastos por Categoria", hole=0.4)
        st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Nenhum dado registrado ou aguardando sincronização.")