import streamlit as st
import pandas as pd
from datetime import datetime
import time

st.set_page_config(page_title="BI da Minha Vida", layout="wide", page_icon="📊")

st.title("📊 BI da Minha Vida — Dashboard Geral")
st.markdown("---")

# 1. PUXAR DADOS DOS SECRETS SEGURAMENTE
# 1. PUXAR DADOS DOS SECRETS SEGURAMENTE (VERSÃO DETETIVE)
try:
    url_financeiro = st.secrets["LINK_CSV_FINANCEIRO"]
    url_projetos = st.secrets["LINK_CSV_PROJETOS"]
    
    # Criamos um "carimbo de tempo" para forçar o Google a atualizar
    carimbo = int(time.time())
    
    # Adicionamos o carimbo no final do link com um parâmetro falso (&_cb=)
    df_fin = pd.read_csv(f"{url_financeiro}&_cb={carimbo}", on_bad_lines='skip')
    df_proj = pd.read_csv(f"{url_projetos}&_cb={carimbo}", on_bad_lines='skip')
    
except Exception as e:
    st.error(f"❌ Ocorreu um erro real no sistema:")
    st.exception(e)
    st.stop()
# st.write("🕵️‍♂️ As colunas que o Pandas encontrou foram:", df_fin.columns.tolist())
# --- CONVERSÃO DE DADOS ---
if not df_fin.empty:
    # 1. Transforma em texto para poder manipular
    df_fin["Valor"] = df_fin["Valor"].astype(str)
    # 2. Arranca as vírgulas (ex: 2,104 vira 2104)
    df_fin["Valor"] = df_fin["Valor"].str.replace(',', '', regex=False)
    # 3. Agora sim, converte para número matemático
    df_fin["Valor"] = pd.to_numeric(df_fin["Valor"], errors='coerce')
if not df_proj.empty:
    df_proj['Prazo'] = pd.to_datetime(df_proj['Prazo'], errors='coerce')

# =====================================================================
# SEÇÃO 1: ALERTAS CRÍTICOS (EIXO 2)
# =====================================================================
if not df_proj.empty:
    hoje = pd.to_datetime(datetime.now().date())
    df_proj['Dias_Restantes'] = (df_proj['Prazo'] - hoje).dt.days
    
    # Alertas: Vence em até 5 dias OU prioridade é "fudeu" (e não está concluído)
    alertas = df_proj[
        ((df_proj['Dias_Restantes'] <= 5) & (df_proj['Dias_Restantes'] >= 0) | (df_proj['Prioridade'] == "fudeu")) 
        & (df_proj['Status'] != "Concluído")
    ]
    
    if not alertas.empty:
        st.error("🚨 **ALERTAS CRÍTICOS DE PROJETOS:**")
        for _, row in alertas.iterrows():
            st.write(f"• **{row['Nome']}** ({row['Tipo']}) — Prazo: {row['Prazo'].strftime('%d/%m/%Y')} (**{row['Dias_Restantes']} dias restantes!**) | Prioridade: `{row['Prioridade']}`")
        st.markdown("---")

# =====================================================================
# SEÇÃO 2: METRICAS FINANCEIRAS DO MÊS (EIXO 1)
# =====================================================================
st.subheader("💰 Resumo Financeiro Geral")
if not df_fin.empty:
    entradas = df_fin[df_fin['Tipo'] == 'Entrada']['Valor'].sum()
    saidas = df_fin[df_fin['Tipo'] == 'Saída']['Valor'].sum()
    saldo = entradas - saidas
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Total de Entradas", f"R$ {entradas:,.2f}")
    c2.metric("Total de Saídas", f"R$ {saidas:,.2f}", delta=f"-R$ {saidas:,.2f}", delta_color="inverse")
    c3.metric("Balanço / Saldo", f"R$ {saldo:,.2f}")
    
    # Cálculos de Maior e Menor Gasto (Apenas Saídas)
    df_saidas = df_fin[df_fin['Tipo'] == 'Saída']
    if not df_saidas.empty:
        # Agrupa por categoria para saber o maior acumulado
        gastos_por_cat = df_saidas.groupby("Categoria")["Valor"].sum()
        maior_gasto_cat = gastos_por_cat.idxmax()
        maior_gasto_val = gastos_por_cat.max()
        
        menor_gasto_cat = gastos_por_cat.idxmin()
        menor_gasto_val = gastos_por_cat.min()
        
        st.markdown("#### 🔍 Insights de Consumo")
        col_in1, col_in2 = st.columns(2)
        with col_in1:
            st.info(f"🔺 **Maior foco de gasto:** {maior_gasto_cat} (R$ {maior_gasto_val:,.2f})")
        with col_in2:
            st.success(f"🔻 **Menor foco de gasto:** {menor_gasto_cat} (R$ {menor_gasto_val:,.2f})")
else:
    st.info("Nenhum dado financeiro encontrado para calcular os indicadores.")

# =====================================================================
# SEÇÃO 3: VISÃO DE ÁGUIA (PROJETOS)
# =====================================================================
st.markdown("---")
st.subheader("🚀 Projetos em Andamento")
if not df_proj.empty:
    # Filtra apenas o que não está concluído nem pausado
    df_ativos = df_proj[~df_proj['Status'].isin(['Concluído', 'Pausado'])]
    if not df_ativos.empty:
        st.dataframe(df_ativos[['Nome', 'Status', 'Prioridade', 'Prazo']], use_container_width=True)
    else:
        st.write("Tudo limpo! Nenhum projeto ativo no momento.")