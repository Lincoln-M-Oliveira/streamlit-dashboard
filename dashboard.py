import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração inicial
st.set_page_config(layout='wide', page_title="Dashboard Supermercado")

# Carregando dados
df = pd.read_csv('supermarket_sales.csv', sep=',', decimal='.')
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values('Date')
df['Month'] = df['Date'].dt.to_period('M').astype(str)

# Filtros
st.sidebar.header("Filtros")
month = st.sidebar.selectbox("Mês", df['Month'].unique())
cities = st.sidebar.multiselect("Cidade", df['City'].unique(), default=df['City'].unique())

# Filtrando dados
df_filtered = df[(df['Month'] == month) & (df['City'].isin(cities))]

# KPIs
st.title("Dashboard de Vendas - Supermercado")

colA, colB, colC = st.columns(3)
colA.metric("Faturamento Total", f"R$ {df_filtered['Total'].sum():,.2f}")
colB.metric("Ticket Médio", f"R$ {df_filtered['Total'].mean():,.2f}")
colC.metric("Nº de Vendas", f"{len(df_filtered)}")

st.markdown("---")

# ====================

# Gráficos de Vendas
st.subheader("Vendas")

col1, col2 = st.columns(2)

# Faturamento diário
fig_date = px.bar(df_filtered, x='Date', y='Total',
                  color='City', title='Faturamento diário (R$)')
col1.plotly_chart(fig_date, use_container_width=True)

# Faturamento por categoria de produto
prod_total = (df_filtered.groupby('Product line')['Total']
              .sum().reset_index()
              .sort_values('Total', ascending=False))
fig_prod = px.bar(prod_total, x='Product line', y='Total', color='Product line',
                  title='Faturamento por categoria de produto (R$)')
col2.plotly_chart(fig_prod, use_container_width=True)

# ==============

# Gráficos por Cidade
st.subheader("Cidades")

col3, col4 = st.columns(2)

# Faturamento por cidade
city_total = (df_filtered.groupby('City')['Total']
              .sum().reset_index()
              .sort_values('Total', ascending=False))
fig_city = px.bar(city_total, x='City', y='Total',
                  title='Faturamento por cidade (R$)')
col3.plotly_chart(fig_city, use_container_width=True)

# Avaliação média por cidade
city_rating = df_filtered.groupby('City')['Rating'].mean().round(1).reset_index()
fig_rating = px.bar(city_rating, x='City', y='Rating',
                    title='Média de avaliação por cidade')
col4.plotly_chart(fig_rating, use_container_width=True)

# ===============

# Formas de Pagamento
st.subheader("Métodos de Pagamento")

pay_total = (df_filtered.groupby('Payment')['Total']
             .sum().reset_index()
             .sort_values('Total', ascending=True))
fig_payment = px.bar(pay_total, x='Total', y='Payment', orientation='h',
                     title='Distribuição de faturamento por forma de pagamento (R$)')
st.plotly_chart(fig_payment, use_container_width=True)
# teste
#teste 
#teste