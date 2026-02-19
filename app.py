import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from src.functions.cleaning import fillm
from src.functions.wrangling import get_date, new_data

@st.cache_data
def load_data():
    df = pd.read_csv('src/data/online_retail_II.csv')
    # -------------------- DATA CLEANING ---------------------------
    # Removendo os valores nulos da coluna 'Customer ID'.
    df = fillm(df, 'Customer ID', 'Country', get_dummies=True)
    # Removendo os valores nulos da coluna Description.
    df = fillm(df, 'Description', 'StockCode', get_dummies=True)

    # Alterando o tipo de dado da coluna 'Customer ID' de float64 para int64.
    df['Customer ID'] = df['Customer ID'].astype('int32')
    #Alterando o tipo de dado da coluna 'InvoiceDate' de str para datetime.
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    
    df = get_date(df, 'InvoiceDate', year=True, month=True)
    df = new_data(df, mcolumn='Quantity', auxcolumn='Price', newcolumn='Total Sales')
    return df

df = load_data()

# ------------------- CONFIGURAÇÃO DA PÁGINA ---------------------------
st.set_page_config(
    page_title='Overview Dashboard Clients',
    page_icon='',
    layout='wide'
)

# BARRA LATERAL PARA OS FILTROS:
st.sidebar.header('Filtros')
# FILTRO PAÍS
enable_countries = sorted(df['Country'].unique())
selected_country = st.sidebar.multiselect('Country', enable_countries, default=enable_countries)

# FILTRO ANO
enable_years = sorted(df['Year'].unique())
selected_year = st.sidebar.multiselect('Year', enable_years, default=enable_years)

df_filtered = df[
    (df['Country'].isin(selected_country)) &
    (df['Year'].isin(selected_year)) 
]

faturamento_total = df_filtered['Total Sales'].sum()
total_pedidos = df_filtered['Invoice'].nunique()
ticket_medio = faturamento_total / total_pedidos if total_pedidos > 0 else 0
qtd_clientes = df_filtered['Customer ID'].nunique()

col1, col2, col3, col4 = st.columns(4)
col1.metric('Faturamento Total', f'$ {faturamento_total:,.2f}')
col2.metric('Total de Pedidos', f'{total_pedidos}')
col3.metric('Ticket Médio', f'$ {ticket_medio:,.2f}')
col4.metric('Qtd Clientes', qtd_clientes)

tab1, tab2, tab3, tab4 = st.tabs(["📊 Visão Geral", "🛍️ Produtos (Pareto)", "👥 Clientes (Cohort)", "📊 RFM"])

with tab1:
    if not df_filtered.empty:
        # ------------------- WRANGLING SEASONALITY ------------------------
        # Criando o DataFrame 'seasonality_sales' para usar em gráfico e utilizando a função get_date() para coletar os anos e os meses da coluna InvoiceDate.
        df_filtrado = get_date(df_filtered, 'InvoiceDate', year=True, month=True)
        # Agrupando o DataFrame 'seasonality_sales' pelas colunas Year e Month, obtendo a soma da coluna 'Total Sales' por mês e ano, e ordenando por pela coluna Month.
        df_filtrado = df_filtrado.groupby(['Year', 'Month'])['Total Sales'].sum().reset_index().sort_values(by=['Month'])
        
        months_map = {
            1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr', 5: 'Mai', 6: 'Jun',
            7: 'Jul', 8: 'Ago', 9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez'
        }
        
        df_filtrado['Month_Name'] = df_filtrado['Month'].map(months_map)
        
        months_order = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
        df_filtrado['Month_Name'] = pd.Categorical(df_filtrado['Month_Name'], categories=months_order, ordered=True)
        
        # ------------------- GRAPH SEASONALITY ------------------------
        if not df_filtrado.empty:
            graph_seasonality_sales = px.line(
                df_filtrado,
                x='Month_Name',
                y='Total Sales',
                color='Year',
                markers=True, # Adiciona pontos nas linhas
                title='Sazonalidade Mensal: Comparativo de Vendas por Ano',
                labels={'Month_Name': 'Mês do Ano', 'Total Sales': 'Faturamento ($)', 'Year': 'Ano'},
                template='plotly_white',
                color_discrete_sequence=px.colors.qualitative.Prism # Uma paleta de cores mais elegante
            )

            # Ajustando para que o eixo X mostre todos os meses (1 a 12)
            graph_seasonality_sales.update_xaxes(dtick=1)

            # Formatando o eixo Y para milhares (k)
            graph_seasonality_sales.update_layout(
                yaxis_tickformat='$',
                hovermode='x unified' # Melhora a visualização ao passar o mouse
            )
            
            st.plotly_chart(graph_seasonality_sales, width='stretch')
        else:
            st.warning('Não há dados para serem exibidos.')
    else:
        st.warning('Nenhum filtro selecionado.')
        
with tab2:
    if not df_filtered.empty:
        sales_products = df_filtered.copy()
        # ------------------- WRANGLING PARETO ------------------------------
        # Através da função drop() removemos os valores de reembolso (menor que 0) identificados na coluna 'Total Sales'.
        sales_products = sales_products.drop(sales_products.loc[sales_products['Total Sales'] < 0].index)
        # Realizamos o agrupamento dos dados através da coluna 'StockCode', calculamos a soma do total das vendas por 'StockCode', e organizamos os valores de forma decrescente.
        sales_products = sales_products.groupby(['StockCode'])['Total Sales'].sum().sort_values(ascending=False).reset_index()
        # Criamos a coluna 'Accumulative Sales' através da soma aculativa da coluna 'Total Sales', e por fim arrendodamos para exibir somente dois números decimais.
        sales_products['Accumulative Sales'] = (sales_products['Total Sales'].cumsum()).round(2)
        # Criamos a coluna 'Accumulative Percentage' para coletar a porcentagem através da divisão da soma acumulativa (coluna 'Accumalative Sales') e da soma total (coluna 'Total Sales')
        sales_products['Accumulative Percentage'] = (sales_products['Accumulative Sales'] / sales_products['Total Sales'].sum()).round(4)
        # Configuramos para exibir somente alguns valores, pois a base de dados possui muitas informações.
        sales_products = sales_products.head(600)
        
        # ------------------- GRAPH PARETO ------------------------------
        if not sales_products.empty:
            # 1. Criar subplots com eixo Y secundário
            graph_sales_products = make_subplots(specs=[[{"secondary_y": True}]])

            # 2. Adicionar as Barras (Vendas Individuais)
            graph_sales_products.add_trace(
                go.Bar(
                    x=sales_products['StockCode'],
                    y=sales_products['Total Sales'],
                    name="Vendas Individuais",
                    marker_color='rgb(55, 83, 109)'
                ),
                secondary_y=False,
            )

            # 3. Adicionar a Linha (Percentual Acumulado)
            graph_sales_products.add_trace(
                go.Scatter(
                    x=sales_products['StockCode'],
                    y=sales_products['Accumulative Percentage'],
                    name="% Acumulado",
                    line=dict(color='red', width=3)
                ),
                secondary_y=True,
            )

            # 4. Ajustes Finais de Layout
            graph_sales_products.update_layout(
                title_text="Análise de Pareto: Produtos que Geram 80% da Receita",
                template="plotly_white"
            )

            # Definir o limite do eixo de porcentagem para 100%
            graph_sales_products.update_yaxes(title_text="Vendas ($)", secondary_y=False)
            graph_sales_products.update_yaxes(title_text="Percentual Acumulado (%)", secondary_y=True, range=[0, 1.05], tickformat=".0%")

            st.plotly_chart(graph_sales_products, width='stretch')

        else:
            st.warning('Não há dados para serem exibidos.')
    else:
        st.warning('Nenhum filtro selecionado.')

with tab3:
    # ------------------- WRANGLING COHORT -----------------------------
    if not df_filtered.empty:
        df_cohort = df_filtered.copy()
        
        # Criando a coluna 'Referencial Date', a qual recebe o período da coluna 'InvoiceDate'.
        df_cohort['Referencial Date'] = df_filtered['InvoiceDate'].dt.to_period('M')
        
        # Criando a coluna 'First Purchase', a qual recebe a menor data de compra por 'CustomerID'.
        df_cohort['First Purchase'] = df_cohort.groupby('Customer ID')['Referencial Date'].transform('min')
        
        # Criando a coluna 'Customer Age', recebendo a subtração entre as colunas 'Referencial Date' e 'First Purchase', a qual identifica a quanto tempo o cliente compra na loja.
        df_cohort['Customer Age'] = (df_cohort['Referencial Date'] - df_cohort['First Purchase']).apply(lambda x: x.n)
        
        # Agrupando o DataFrame pelas colunas 'First Purchase' e 'Customer Age' e coletando as vezes ÚNICAS que cada cliente (CustomerID) realizou uma compra.
        df_cohort = df_cohort.groupby(['First Purchase', 'Customer Age'])['Customer ID'].nunique().reset_index()
        
        # Transformando o DataFrame em uma tabela dinámica, a qual recebe o index como 'First Purchase', as colunas 'Customer Age', e os valores pela coluna 'Customer ID'.
        cohort_pivot = df_cohort.pivot(index='First Purchase', columns='Customer Age', values='Customer ID')
        
        # Nesta linha de código estamos dividindo todos os valores das linhas pelo primeiro valor da linha (First Purchase) para transformar em porcentagem.
        cohort_matrix = cohort_pivot.divide(cohort_pivot.iloc[:,0], axis=0)
        
        # Transformando o datatype do index da tabela dinâmica para str.
        cohort_matrix.index = cohort_matrix.index.astype(str)
        
        if not cohort_matrix.empty:
            cohort_graph = px.imshow(
                cohort_matrix,
                text_auto='.0%',
                color_continuous_scale='Blues',
                labels=dict(x="Meses após a 1ª Compra", y="Mês de Entrada", color="Taxa de Retenção"),
                title="Análise de Cohort: Retenção de Clientes por Safra"
            )

            # Ajustando o tamanho do gráfico e das fontes
            cohort_graph.update_layout(
                height=600,
                font=dict(size=14), # Aumenta o tamanho geral da fonte
                title_font_size=22  # Destaca o título
            )

            # Aumentando especificamente o texto dentro dos quadradinhos (.0%)
            cohort_graph.update_traces(textfont_size=16)
            cohort_graph.update_xaxes(dtick=1)

            st.plotly_chart(cohort_graph, width='stretch')
        else:
            st.warning('Não há dados para serem exibidos.')
    else:
        st.warning('Nenhum filtro selecionado.')
    
    # ------------------- GRAPH COHORT -----------------------------
    
with tab4:
    if not df_filtered.empty:
        rfm = df_filtered.copy()
        rfm.drop(rfm.loc[rfm['Total Sales'] < 0].index , inplace=True)

        snapshot_date = rfm['InvoiceDate'].max() + pd.Timedelta(days=1)

        rfm = rfm.groupby('Customer ID').agg({
            'InvoiceDate': lambda x: (snapshot_date - x.max()).days,
            'Invoice': 'nunique',
            'Total Sales': 'sum'
        })

        rfm.columns = ['Recency', 'Frequency', 'Monetary']

        rfm['R'] = pd.qcut(rfm['Recency'], q=5, labels=[5, 4, 3, 2, 1])
        rfm['F'] = pd.qcut(rfm['Frequency'].rank(method='first'), q=5, labels=[1, 2, 3, 4, 5])
        rfm['M'] = pd.qcut(rfm['Monetary'], q=5, labels=[1, 2, 3, 4, 5])

        rfm['RFM Score'] = rfm['R'].astype(str) + rfm['F'].astype(str) + rfm['M'].astype(str)

        segs = {
            r'[1-2][1-2]': 'Hibernando',
            r'[1-2][3-4]': 'Em Risco',
            r'[1-2]5': 'Não podemos perder',
            r'3[1-2]': 'Prestes a dormir',
            r'33': 'Precisa de atenção',
            r'[3-4][4-5]': 'Clientes Leais',
            r'41': 'Promissores',
            r'51': 'Novos Clientes',
            r'[4-5][2-3]': 'Potenciais Fiéis',
            r'5[4-5]': 'Campeões'
        }

        rfm['Segment'] = rfm['R'].astype(str) + rfm['F'].astype(str)
        rfm['Segment'] = rfm['Segment'].replace(segs, regex=True)

        # 1. Criando um resumo por segmento para facilitar o gráfico
        rfm_counts = rfm['Segment'].value_counts().reset_index()
        rfm_counts.columns = ['Segment', 'Count']
    
        if not rfm_counts.empty:
            rfm_graph = px.treemap(
                rfm_counts, 
                path=['Segment'], 
                values='Count',
                title='Distribuição dos Segmentos de Clientes (RFM)',
                color='Count',
                color_continuous_scale='RdBu', # Escala de cores profissional
                template='plotly_white'
            )
            st.plotly_chart(rfm_graph, width='stretch')
            
            st.subheader("Lista de Clientes por Segmento")
            selected_segment = st.selectbox("Selecione um segmento para ver os detalhes:", rfm['Segment'].unique())
            df_segment = rfm[rfm['Segment'] == selected_segment]
            st.dataframe(df_segment)
            
            csv = df_segment.to_csv(index=True).encode('utf-8')
            st.download_button(
                label="📥 Baixar lista de clientes (CSV)",
                data=csv,
                file_name=f'clientes_{selected_segment.lower()}.csv',
                mime='text/csv',
            )
        else:
            st.warning('Não há dados para serem exibidos.')
    else:
        st.warning('Nenhum filtro selecionado.')
        
        