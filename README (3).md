#  University Student Analytics Dashboard

**Activity I – Data Visualization and Dashboard Deployment**  
Data Mining · Universidad de La Costa  
Prof. José Escorcia Gutiérrez, Ph.D.

---

##  group 
juan david villada ureche

---

##  Purpose

This dashboard provides interactive visualizations over a university's student admission, enrollment, retention, and satisfaction data (2015–2024). It supports data-driven decision-making by surfacing trends across academic years, terms, and departments.

---

##  Features

| Visualization | Type | Description |
|---|---|---|
| KPI Cards | Metric cards | Avg retention, satisfaction, total apps & enrollment |
| Retention Rate Trend | Line chart | Spring vs Fall over time |
| Satisfaction by Year | Bar chart | Annual average satisfaction scores |
| Spring vs Fall Comparison | Grouped bar chart | Applications, admitted, enrolled per term |
| Department Enrollment | Pie/donut chart | Share per department |
| Department Trends | Multi-line chart | Per-department enrollment over time |
| Correlation Heatmap | Heatmap | Pearson correlations between key indicators |

### Interactive Filters
- **Year range** – slider to select a time window
- **Term** – Spring, Fall, or both
- **Department** – select which programs to display

---

##  How to Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the dashboard
streamlit run app.py
```

The app will open at `http://localhost:8501`.

---

##  Deployed App

 **Live dashboard:** [https://your-app.streamlit.app](https://your-app.streamlit.app)

---

##  Repository Structure

```
├── app.py               # Streamlit dashboard
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

---

##  Key Findings

- Retention rates improved steadily from **85 % (2015)** to **90 % (2024)**.
- Student satisfaction rose from **78 %** to **88 %** over the same period.
- Engineering is consistently the largest department; Science enrollment declined after 2019.
- Spring and Fall terms show nearly identical figures, suggesting stable year-round demand.
- **Actionable insight:** The drop in Science enrollment after 2019 warrants targeted recruitment and program review to reverse the trend.
