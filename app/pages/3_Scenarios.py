import streamlit as st
import pandas as pd
from pathlib import Path
import pandas as pd

st.title("Scenarios (What-if)")

# Inputs
start_balance = st.number_input("Starting balance ($)", value=143.24, step=10.0)
biweekly = st.number_input("Bi-weekly deposit ($)", value=100.0, step=25.0)
apy = st.number_input("APY (%)", value=3.8, step=0.1)
months = st.slider("Projection horizon (months)", 12, 180, 120)
goal = st.number_input("Goal ($)", value=20000, step=500)

# Simple recompute inline (monthly compounding, bi-weekly deposits)
r = apy/100/12

import datetime as dt
today = pd.Timestamp.today().normalize()
first_dep = today + pd.Timedelta(days=(7 - today.weekday()) % 14)  # next "deposit-ish" anchor

def biweekly_dates(first_date, months):
    end = first_date + pd.DateOffset(months=months)
    dates = [first_date]
    while dates[-1] < end:
        dates.append(dates[-1] + pd.Timedelta(days=14))
    return pd.to_datetime(dates[:-1])

def monthly_periods(start, months):
    return pd.period_range(start=start, periods=months, freq="M").to_timestamp("M")

depo_dates = set(biweekly_dates(first_dep, months))
month_ends = monthly_periods(today, months)

rows = []
bal = start_balance
current = today
for m_end in month_ends:
    month_days = pd.date_range(current, m_end, freq="D")
    dep_in_month = sum(biweekly for d in month_days if d in depo_dates)
    interest = (bal + dep_in_month) * r
    bal_end = bal + dep_in_month + interest
    rows.append({"month_end": m_end.date(), "deposits": round(dep_in_month,2), "interest": round(interest,2), "balance_end": round(bal_end,2)})
    bal = bal_end
    current = m_end + pd.Timedelta(days=1)

df = pd.DataFrame(rows)

# KPIs
reached = df[df["balance_end"] >= goal]
if len(reached):
    goal_month = reached.iloc[0]["month_end"]
    months_to_goal = df.index[df["balance_end"] >= goal][0] + 1
    st.metric("Months to Goal", int(months_to_goal))
    st.metric("Projected Goal Month", f"{goal_month}")
else:
    st.info("Goal not reached within horizon. Increase deposit or horizon.")

st.line_chart(df.set_index("month_end")["balance_end"])
st.bar_chart(df.set_index("month_end")[["deposits","interest"]])
st.dataframe(df, use_container_width=True)
