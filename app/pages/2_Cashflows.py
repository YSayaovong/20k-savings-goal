import streamlit as st
import pandas as pd
from pathlib import Path

st.title("Cashflows")
p = Path("data/outputs/cashflow_monthly.csv")
if not p.exists():
    st.error("Run pipeline/generate_cashflows.py first.")
else:
    df = pd.read_csv(p, parse_dates=["month_end"])
    st.dataframe(df, use_container_width=True)
    st.download_button("Download cashflow CSV", data=df.to_csv(index=False), file_name="cashflow_monthly.csv", mime="text/csv")
