import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="20K Savings Dashboard", layout="wide")

@st.cache_data
def load_cashflow():
    p = Path("data/outputs/cashflow_monthly.csv")
    if not p.exists():
        st.error("Run pipeline/generate_cashflows.py first.")
        st.stop()
    return pd.read_csv(p, parse_dates=["month_end"])

def kpi_row(df, goal):
    reached = df[df["balance_end"] >= goal]
    if len(reached):
        goal_month = reached.iloc[0]["month_end"].date()
        months_to_goal = df.index[df["balance_end"] >= goal][0] + 1
    else:
        goal_month, months_to_goal = "Not within horizon", len(df)

    total_contrib = df["deposits"].sum()
    total_interest = df["interest"].sum()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Months to Goal", int(months_to_goal) if isinstance(months_to_goal, (int,)) else months_to_goal)
    c2.metric("Projected Goal Month", f"{goal_month}")
    c3.metric("Total Contributions", f"${total_contrib:,.2f}")
    c4.metric("Total Interest", f"${total_interest:,.2f}")

st.sidebar.title("Parameters")
goal_default = 20000

def main():
    df = load_cashflow()
    goal = st.sidebar.number_input("Goal ($)", value=goal_default, step=500)
    st.title("20K Savings – Forecast & Tracking")
    st.caption("Bi-weekly deposits with monthly compounding (SQLite-backed)")

    # KPIs
    kpi_row(df, goal)

    # Charts
    st.subheader("Balance Projection")
    st.line_chart(df.set_index("month_end")["balance_end"])

    st.subheader("Monthly Deposits & Interest")
    st.bar_chart(df.set_index("month_end")[["deposits","interest"]])

    # Table
    st.subheader("Cashflow Table")
    st.dataframe(df, use_container_width=True)

    # Download
    st.download_button("Download cashflow CSV", data=df.to_csv(index=False), file_name="cashflow_monthly.csv", mime="text/csv")

if __name__ == "__main__":
    main()
