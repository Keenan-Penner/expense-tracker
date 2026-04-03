import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import date, timedelta


data = pd.read_excel("data/transactions.xlsx")
data['date'] = pd.to_datetime(data['date'], format= "%d-%m-%Y")

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="My Finances",
    page_icon="💶",
    layout="wide",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0f0f11;
    color: #e8e6e1;
}

h1, h2, h3 { font-family: 'DM Serif Display', serif; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #0F7039;
    border-right: 1px solid #2a2a2e;
}

/* KPI cards */
.kpi-card {
    background: #1c1c22;
    border: 1px solid #2a2a2e;
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 12px;
}
.kpi-label {
    font-size: 11px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #888;
    margin-bottom: 6px;
}
.kpi-value {
    font-family: 'DM Serif Display', serif;
    font-size: 28px;
    line-height: 1;
}
.kpi-positive { color: #6fcf97; }
.kpi-negative { color: #eb5757; }
.kpi-neutral  { color: #e8e6e1; }

/* Section headers */
.section-title {
    font-family: 'DM Serif Display', serif;
    font-size: 20px;
    margin: 28px 0 12px 0;
    color: #00000;
}

/* Plotly chart background override */
.js-plotly-plot .plotly .bg { fill: #FFFFFF !important; }

/* Streamlit metric delta */
[data-testid="stMetricDelta"] { font-size: 12px; }
</style>
""", unsafe_allow_html=True)

# ── Date Range ────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("## 💶 My Finances")
    st.markdown("---")

    st.markdown("**Date range**")
    col_a, col_b = st.columns(2)
    with col_a:
        start_date = st.date_input("From", value=data["date"].min().date())
    with col_b:
        end_date = st.date_input("To", value=data["date"].max().date())

    st.markdown("**Quick periods**")
    qp = st.radio("", ["Custom", "Last 30 days", "Last 3 months", "Last 6 months", "Last year", "This year"], label_visibility="collapsed")
    if qp != "Custom":
        today = date.today()
        if qp == "Last 30 days":
            start_date, end_date = today - timedelta(days=30), today
        elif qp == "Last 3 months":
            start_date, end_date = today - timedelta(days=90), today
        elif qp == "Last 6 months":
            start_date, end_date = today - timedelta(days=180), today
        elif qp == "Last year":
            start_date, end_date = today - timedelta(days=365), today
        elif qp == "This year":
            start_date, end_date = date(today.year, 1, 1), today

mask = (
    (data["date"].dt.date >= start_date) &
    (data["date"].dt.date <= end_date) 
    # &
    # (data["category"].isin(selected_cats)) 
    # &
    # (df["status"].isin(selected_statuses))
)
df = data[mask].copy()


# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(f"## My Finances &nbsp;·&nbsp; <span style='font-family:DM Sans;font-size:16px;color:#888'>{start_date.strftime('%d %b %Y')} → {end_date.strftime('%d %b %Y')}</span>", unsafe_allow_html=True)
st.markdown("")


#this is our income
income = df[df['amount'] > 0]
#some of the spending is actually going towards our savings account. We don't want to count it as an expense
negative = df[df['amount'] < 0]

savings = negative[negative['subcategory'] == 'Épargne']
spending = negative[negative['subcategory'] != 'Épargne']
spending['abs_amount'] = spending['amount'].abs()

total_income = income['amount'].sum()
total_spending = spending['amount'].sum()
total_savings = abs(savings['amount'].sum())



c1, c2, c3, c4 = st.columns(4)

def indicators(col, label, value, cls):
    col.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value {cls}">{value}</div>
    </div>""", unsafe_allow_html=True)

indicators(c1, "Total income",    f"+{total_income:,.2f} €",   "kpi-positive")
indicators(c2, "Total expenses",  f"{total_spending:,.2f} €",  "kpi-negative")
indicators(c3, "Net balance",     f"{total_income + total_spending:+,.2f} €",    "kpi-positive" if total_income + total_spending >= 0 else "kpi-negative")
indicators(c4, "To savings account",   f"{total_savings} €" ,          "kpi-positive" if total_savings >0 else "kpi-neutral")


# ── Pie charts ────────────────────────────────────────────────────────────────────

st.markdown('<div class="section-title">Overview</div>', unsafe_allow_html=True)
left, right = st.columns([2, 2])

with left:
    # Initialize session state for selected category
    if 'selected_category' not in st.session_state:
        st.session_state.selected_category = None

    if st.session_state.selected_category is None:
        chart_expense_df = spending.groupby('category').agg(abs_amount= ('abs_amount', 'sum'), count= ('abs_amount', 'count')).reset_index()
        # st.write(chart_expense_df)

        # Dropdown to drill down — sits right below the chart
        categories = chart_expense_df['category'].tolist()
        chosen = st.selectbox("🔍 Drill into a category:", ["— select —"] + categories, key="cat_select")
        if chosen != "— select —":
            st.session_state.selected_category = chosen
            st.rerun()
        fig = go.Figure(go.Pie(
        labels=chart_expense_df['category'],
        values=chart_expense_df['abs_amount'],
        customdata=chart_expense_df['count'],
        hovertemplate='%{label}<br>%{value} €<br>%{customdata} transactions<extra></extra>'))
        fig.update_layout(title='Spending by Category')
        st.plotly_chart(fig, use_container_width=True)
        
        # fig = px.pie(chart_expense_df, values='abs_amount', names='category', title='Spending by Category', custom_data=['count'])
        # fig.update_traces(hovertemplate='%{label}<br>%{value} €<br>%{custom_data}<extra></extra>')
        # st.plotly_chart(fig, use_container_width=True, key="category_chart")

        

    else:
        selected = st.session_state.selected_category
        filtered = spending[spending['category'] == selected]
        chart_sub_df = filtered.groupby('subcategory')['abs_amount'].sum().reset_index()

        if st.button("← Back to all categories"):
            st.session_state.selected_category = None
            st.rerun()

        fig = px.pie(chart_sub_df, values='abs_amount', names='subcategory', title=f'{selected} — Subcategories')
        fig.update_traces(hovertemplate='%{label}<br>%{value} €<extra></extra>')
        st.plotly_chart(fig, use_container_width=True, key="subcategory_chart")

        

with right:
    chart_revenue_df = income.groupby('subcategory')['amount'].sum().reset_index()
    fig = px.pie(chart_revenue_df, values='amount', names='subcategory', title='Revenue repartition')
    fig.update_traces(hovertemplate='%{label}<br>%{value} €<extra></extra>')
    st.plotly_chart(fig, use_container_width=True)