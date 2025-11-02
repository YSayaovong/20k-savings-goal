# 20K Savings Dashboard – How to Run & What It Solves

This project is a **senior-level data analyst dashboard** built with **Python, Streamlit, SQLite, and VS Code**.

It models your **bi-weekly $100 deposits**, applies **monthly compounding**, and projects exactly **when you will reach $20,000**.  
It includes KPIs, charts, a scenario tool, and a downloadable cashflow table.

---

## ✅ What This Solves

This dashboard answers:

- *When will I reach my savings goal?*  
- *How much interest will I earn?*  
- *How do different APYs or deposit amounts change the timeline?*  
- *How do contributions compare to interest over time?*

It turns your savings into a **data-driven model**, just like what analysts build in banking and fintech.

---

## ✅ How to Run the Project (VS Code)

### **1. Go to your project folder**
```powershell
cd "E:\Career Projects\Data Analyst Projects\20k-savings-dashboard"
```

### **2. Create and activate your virtual environment**
```powershell
py -m venv venv
.env\Scriptsctivate
```

### **3. Install dependencies**
```powershell
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

### **4. Generate data**
```powershell
py pipeline\generate_cashflows.py
py pipeline\load_to_sqlite.py
```

### **5. Run the dashboard**
```powershell
py -m streamlit run app\app.py
```

Your dashboard will open in your browser.

---

## ✅ Dashboard Previews

### **Forecast & KPIs**
Shows goal date, months to goal, contribution totals, and interest totals.
![Forecast Tracking](forecast_tracking.PNG)

---

### **Monthly Cashflows**
Shows deposits, interest, and ending balance month by month.
![Cashflow Table](cashflow.PNG)

---

### **Scenario Analysis**
Adjust deposit, APY, or projection length and see new results instantly.
![Scenarios Page](scenarios.PNG)

---

## ✅ Project Structure
```
20k-savings-dashboard/
 ├─ app/
 │   ├─ app.py
 │   └─ pages/
 ├─ pipeline/
 │   ├─ generate_cashflows.py
 │   └─ load_to_sqlite.py
 ├─ data/
 │   └─ outputs/
 ├─ sql/
 ├─ tests/
 ├─ requirements.txt
 └─ README.md
```

---

## ✅ Summary
- Real financial forecasting tool  
- SQL + Python + Streamlit  
- Professional data analyst workflow  
- Perfect for GitHub and your portfolio  

