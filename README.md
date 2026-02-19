📊 E-commerce Analytics Dashboard: Do ETL à Segmentação RFM

Este projeto é uma aplicação de Business Intelligence desenvolvida em Python que transforma dados brutos de transações de um e-commerce em insights estratégicos. A ferramenta permite analisar o faturamento, a retenção de clientes e a saúde da base de produtos em tempo real.
🚀 [Acesse o Dashboard Online Aqui] (Link do seu Streamlit Cloud)
🎯 Objetivo do Projeto

O objetivo principal é fornecer a um gestor de e-commerce uma visão 360º da operação, respondendo a perguntas como:

    Quais produtos geram 80% do faturamento? (Pareto)

    Qual é a taxa de retorno dos clientes mês a mês? (Cohort)

    Quem são os nossos melhores clientes e quem estamos prestes a perder? (RFM)

🛠️ Tecnologias e Metodologias

    Linguagem: Python 3.x

    Interface: Streamlit (Web App)

    Processamento de Dados: Pandas e NumPy

    Visualização: Plotly Express e Plotly Graph Objects

    Metodologias de Negócio:

        RFM (Recency, Frequency, Monetary): Segmentação comportamental de clientes.

        Análise de Cohort: Estudo de retenção por safra de entrada.

        Princípio de Pareto (80/20): Identificação de produtos críticos para a receita.

📋 Funcionalidades Principais
1. Visão Geral e Sazonalidade

    KPIs em Tempo Real: Faturamento, Total de Pedidos, Ticket Médio e Clientes Únicos que reagem aos filtros de País e Ano.

    Comparativo Anual: Gráfico de linhas comparando o desempenho mensal entre os anos selecionados.

2. Análise de Pareto (Produtos)

    Identificação visual dos "produtos estrela". O gráfico combina barras de vendas individuais com uma linha de percentual acumulado, permitindo focar no estoque e marketing do que realmente importa.

3. Análise de Cohort (Retenção)

    Mapa de calor que rastreia grupos de clientes desde sua primeira compra. Essencial para medir a fidelidade e identificar em qual mês a retenção costuma cair.

4. Segmentação RFM

    Treemap Interativo: Visualização da distribuição da base de clientes entre segmentos como "Campeões", "Leais", "Em Risco" e "Hibernando".

    Exportação de Dados: Tabela detalhada por segmento com opção de download para ações de marketing direto.

📁 Estrutura do Repositório
Plaintext

├── data/               # Arquivo de dados (CSV)
├── functions/          # Funções modulares de Limpeza e Wrangling
│   ├── cleaning.py     # Tratamento de nulos e tipos de dados
│   └── wrangling.py    # Cálculos de datas e transformações
├── app.py              # Arquivo principal do Streamlit
├── requirements.txt    # Dependências do projeto
└── README.md           # Documentação

⚙️ Como executar localmente

    Clone o repositório:
    Bash

    git clone https://github.com/seu-usuario/nome-do-repositorio.git

    Instale as dependências:
    Bash

    pip install -r requirements.txt

    Execute o Streamlit:
    Bash

    streamlit run app.py

Desenvolvido por Guilherme Lapa Baioni

    https://www.linkedin.com/in/guilhermelapabaioni/
