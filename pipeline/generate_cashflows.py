import pandas as pd
import yaml
from pathlib import Path

CFG = yaml.safe_load(Path("pipeline/config.yaml").read_text())

START = pd.to_datetime(CFG["start_date"])
FIRST_DEP = pd.to_datetime(CFG["first_deposit_date"])
BAL0 = float(CFG["starting_balance"])
DEP = float(CFG["deposit_amount_biweekly"])
APY = float(CFG["apy_percent"]) / 100.0
GOAL = float(CFG["goal_amount"])
H = int(CFG["projection_horizon_months"])

def biweekly_dates(first_date, months):
    end = first_date + pd.DateOffset(months=months)
    dates = [first_date]
    while dates[-1] < end:
        dates.append(dates[-1] + pd.Timedelta(days=14))
    return pd.to_datetime(dates[:-1])

def monthly_periods(start, months):
    return pd.period_range(start=start, periods=months, freq="M").to_timestamp("M")

def run_projection():
    r = APY / 12.0
    depo_dates = set(biweekly_dates(FIRST_DEP, H))
    month_ends = monthly_periods(START, H)

    rows = []
    bal = BAL0

    current = START
    for m_end in month_ends:
        # deposits this month (count biweekly occurrences inside the month)
        month_days = pd.date_range(current, m_end, freq="D")
        dep_in_month = sum(DEP for d in month_days if d in depo_dates)

        interest = (bal + dep_in_month) * r
        bal_end = bal + dep_in_month + interest

        rows.append({
            "month_end": m_end.date(),
            "deposits": round(dep_in_month, 2),
            "interest": round(interest, 2),
            "balance_end": round(bal_end, 2),
        })
        bal = bal_end
        current = m_end + pd.Timedelta(days=1)

        if bal >= GOAL:
            break

    df = pd.DataFrame(rows)
    outdir = Path("data/outputs")
    outdir.mkdir(parents=True, exist_ok=True)
    df.to_csv(outdir / "cashflow_monthly.csv", index=False)
    return df

if __name__ == "__main__":
    df = run_projection()
    print(df.head(), "\n...\n", df.tail())
