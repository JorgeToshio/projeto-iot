import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

# 1. Configuração da página (deve ser a primeira linha do Streamlit)
st.set_page_config(page_title="Dashboard IoT - UNIFECAF", layout="wide")

# 2. Conexão com o banco de dados PostgreSQL (Docker)
# Se você alterou a senha no Docker, ajuste aqui: 'postgresql://usuario:senha@localhost:5432/nome_do_banco'
engine = create_engine('postgresql://admin:admin@localhost:5432/iot_db')

# 3. Função para carregar os dados das Views SQL
def load_data(view_name):
    try:
        return pd.read_sql(f"SELECT * FROM {view_name}", engine)
    except Exception as e:
        st.error(f"Erro ao carregar a view {view_name}: {e}")
        return pd.DataFrame()

# --- TÍTULO DO DASHBOARD ---
st.title('🌡️ Dashboard de Monitoramento de Temperaturas IoT')
st.markdown("---")

# --- GRÁFICO 1: MÉDIA DE TEMPERATURA POR DISPOSITIVO ---
st.header('1. Média de Temperatura por Dispositivo')
df_avg = load_data('avg_temp_por_dispositivo')

if not df_avg.empty:
    # Ordenar pela temperatura para o gráfico ficar em escada
    df_avg = df_avg.sort_values('avg_temp', ascending=False)
    
    fig1 = px.bar(
        df_avg, 
        x='device_id', 
        y='avg_temp', 
        color='avg_temp',
        color_continuous_scale='RdYlBu_r',
        labels={'device_id': 'ID do Dispositivo', 'avg_temp': 'Temperatura Média (°C)'},
        title="Média por Dispositivo (Ordenado)"
    )
    st.plotly_chart(fig1, use_container_width=True)
else:
    st.warning("Dados da View 'avg_temp_por_dispositivo' não encontrados.")


# --- GRÁFICO 2: LEITURAS POR HORA (VOLUME DE DADOS) ---
st.header('2. Volume de Leituras por Hora do Dia')
df_hora = load_data('leituras_por_hora')

if not df_hora.empty:
    # IMPORTANTE: Ordenar pela hora para a linha não "voltar para trás"
    df_hora = df_hora.sort_values('hora')
    
    fig2 = px.line(
        df_hora, 
        x='hora', 
        y='contagem', 
        markers=True,
        labels={'hora': 'Data e Hora', 'contagem': 'Qtd de Leituras'},
        title="Frequência de Ingestão de Dados"
    )
    st.plotly_chart(fig2, use_container_width=True)


# --- GRÁFICO 3: TEMPERATURAS MÁXIMAS E MÍNIMAS POR DIA ---
st.header('3. Oscilação Térmica Diária (Máx vs Mín)')
df_max_min = load_data('temp_max_min_por_dia')

if not df_max_min.empty:
    # IMPORTANTE: Ordenar pela data para a linha seguir a cronologia correta
    df_max_min = df_max_min.sort_values('data')
    
    fig3 = px.line(
        df_max_min, 
        x='data', 
        y=['temp_max', 'temp_min'], 
        markers=True,
        labels={'data': 'Data', 'value': 'Temperatura (°C)', 'variable': 'Tipo'},
        title="Temperaturas Extremas por Dia"
    )
    # Personalizando as cores das linhas
    fig3.update_traces(line_color='#ef553b', selector=dict(name='temp_max')) # Vermelho para Máx
    fig3.update_traces(line_color='#636efa', selector=dict(name='temp_min')) # Azul para Mín
    
    st.plotly_chart(fig3, use_container_width=True)

# --- RODAPÉ ---
st.markdown("---")
st.caption("Projeto de Pipeline de Dados IoT - Disciplina: Disruptive Architectures")