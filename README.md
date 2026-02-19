This is a professional version of your README in English, optimized for GitHub. It highlights your technical skills in data engineering, statistical analysis, and dashboard development.
📊 E-commerce Analytics Dashboard: From ETL to RFM Segmentation

This Business Intelligence application transforms raw e-commerce transactional data into actionable strategic insights. Built with Python, it allows stakeholders to analyze revenue trends, customer retention, and database health in real-time.

🚀 [Access the Live Dashboard Here] 
(https://ecommerceanalyticsdashboard.streamlit.app/)

🎯 Project Objective

The goal is to provide e-commerce managers with a 360º view of their operations, answering critical business questions:

    Which products drive 80% of my revenue? (Pareto Principle).

    What is the customer retention rate month-over-month? (Cohort Analysis).

    Who are my best customers, and who am I about to lose? (RFM Segmentation).

🛠️ Tech Stack & Methodologies

    Language: Python 3.x.

    Interface: Streamlit (Web App).

    Data Processing: Pandas and NumPy.

    Visualization: Plotly Express and Plotly Graph Objects.

    Performance: Optimized with @st.cache_data to ensure fluid data loading.

    Business Methodologies:

        RFM (Recency, Frequency, Monetary): Behavioral customer segmentation.

        Cohort Analysis: Retention study by acquisition "vintage".

        Pareto Analysis (80/20): Identification of critical products for revenue.

📋 Key Features
1. Dynamic KPIs & Seasonality

    Real-time Metrics: Revenue, Unique Orders (using nunique), Average Ticket, and Unique Customers that react instantly to Sidebar filters.

    Yearly Comparison: A comparative line chart showing monthly sales performance across selected years.
   <img width="1499" height="566" alt="image" src="https://github.com/user-attachments/assets/a7eb940c-e781-4063-880e-707cf6c8e872" />

3. Pareto Analysis (Product Health)

    Identification of "Star Products." The chart combines individual sales bars with a cumulative percentage line, allowing focus on inventory and marketing for high-impact items.
    <img width="1507" height="436" alt="image" src="https://github.com/user-attachments/assets/6908a241-44c3-4705-b4f6-6bbcffdc09cd" />

4. Cohort Analysis (Retention)

    A heatmap tracking customer groups from their first purchase month. This is essential for measuring loyalty and identifying the specific month where churn typically increases.
    <img width="1480" height="564" alt="image" src="https://github.com/user-attachments/assets/cc1d47fd-042f-4e71-b731-ce86b281a447" />

5. RFM Segmentation

    Interactive Treemap: Visualizes the distribution of the customer base into segments such as "Champions," "Loyal," "At Risk," and "Hibernating".
    <img width="1498" height="356" alt="image" src="https://github.com/user-attachments/assets/cdb492ce-0b79-46d8-a593-f9716dd3a45f" />

    Actionable Data: Includes a detailed table per segment with the ability to view specific customer IDs for targeted marketing campaigns.
    <img width="1508" height="605" alt="image" src="https://github.com/user-attachments/assets/63bf9cab-936a-4664-b291-97d4aa33aa98" />

📁 Repository Structure
Plaintext

├── data/               # CSV data storage
├── functions/          # Modular ETL functions
│   ├── cleaning.py     # Data cleaning and type conversion
│   └── wrangling.py    # Date calculations and transformations
├── app.py              # Main Streamlit application
├── requirements.txt    # Project dependencies
└── README.md           # Documentation

⚙️ How to Run Locally

    Clone the repository:
    Bash

    git clone https://github.com/your-username/your-repo-name.git

    Install dependencies:
    Bash

    pip install -r requirements.txt

    Run the App:
    Bash

    streamlit run app.py

💡 Key Business Insights

    Revenue Concentration: 20% of StockCodes account for the vast majority of total sales.

    Retention Trends: The Cohort matrix reveals the "decay" rate of new customers, providing a baseline for re-engagement strategies.

    Customer Health: Segmenting by RFM identifies "At Risk" customers who haven't purchased recently but were historically high-value.

Developed by Guilherme Lapa Baioni

    [LinkedIn] https://www.linkedin.com/in/guilhermelapabaioni/)
