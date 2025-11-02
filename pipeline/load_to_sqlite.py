import sqlite3, pandas as pd
from pathlib import Path

p = Path("data/outputs/cashflow_monthly.csv")
if not p.exists():
    raise SystemExit("Run pipeline/generate_cashflows.py first.")

cf = pd.read_csv(p, parse_dates=["month_end"])
con = sqlite3.connect("data/outputs/savings.db")
cf.to_sql("cashflow_monthly", con, if_exists="replace", index=False)
con.executescript("""
CREATE INDEX IF NOT EXISTS idx_month ON cashflow_monthly(month_end);
""")
con.commit()
con.close()
print("Loaded to data/outputs/savings.db")
