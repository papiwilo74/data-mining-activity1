import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import io

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="University Student Analytics",
    page_icon="🎓",
    layout="wide",
)

# ── Team banner ────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div style='background:#1a237e;padding:18px 28px;border-radius:10px;margin-bottom:8px'>
        <h1 style='color:white;margin:0;font-size:2rem'>🎓 University Student Analytics Dashboard</h1>
        <p style='color:#90caf9;margin:4px 0 0'>Data Mining · Universidad de La Costa · Prof. José Escorcia Gutiérrez, Ph.D.</p>
        <p style='color:#bbdefb;margin:2px 0 0;font-size:0.85rem'><b>Team members:</b> [Member 1] · [Member 2] · [Member 3] · [Member 4]</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Load data ──────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    data = {
        "Year": [2015,2015,2016,2016,2017,2017,2018,2018,2019,2019,
                 2020,2020,2021,2021,2022,2022,2023,2023,2024,2024],
        "Term": ["Spring","Fall"]*10,
        "Applications":   [2500,2500,2600,2600,2700,2700,2800,2800,3000,3000,
                            2900,2900,3100,3100,3250,3250,3350,3350,3500,3500],
        "Admitted":       [1500,1500,1550,1550,1600,1600,1650,1650,1750,1750,
                           1700,1700,1800,1800,1900,1900,2000,2000,2100,2100],
        "Enrolled":       [600,600,625,625,650,650,675,675,700,700,
                           690,690,725,725,750,750,775,775,800,800],
        "Retention Rate (%)":       [85,85,86,86,87,87,86,86,88,88,
                                     85,85,87,87,88,88,89,89,90,90],
        "Student Satisfaction (%)": [78,78,79,79,80,80,82,82,83,83,
                                     81,81,84,84,85,85,86,86,88,88],
        "Engineering Enrolled": [200,200,210,210,225,225,235,235,250,250,
                                 240,240,260,260,275,275,285,285,300,300],
        "Business Enrolled":    [150,150,160,160,165,165,175,175,185,185,
                                 180,180,195,195,200,200,210,210,225,225],
        "Arts Enrolled":        [125,125,130,130,135,135,140,140,145,145,
                                 140,140,150,150,160,160,165,165,175,175],
        "Science Enrolled":     [125,125,125,125,125,125,125,125,120,120,
                                 130,130,120,120,115,115,115,115,100,100],
    }
    return pd.DataFrame(data)

df = load_data()

# ── Sidebar filters ────────────────────────────────────────────────────────────
st.sidebar.header("🔍 Filters")

years = sorted(df["Year"].unique())
selected_years = st.sidebar.slider(
    "Year range",
    min_value=int(min(years)),
    max_value=int(max(years)),
    value=(int(min(years)), int(max(years))),
)

terms = st.sidebar.multiselect(
    "Term",
    options=["Spring", "Fall"],
    default=["Spring", "Fall"],
)

departments = st.sidebar.multiselect(
    "Department (for enrollment chart)",
    options=["Engineering", "Business", "Arts", "Science"],
    default=["Engineering", "Business", "Arts", "Science"],
)

# ── Filter dataframe ───────────────────────────────────────────────────────────
mask = (
    df["Year"].between(*selected_years) &
    df["Term"].isin(terms if terms else ["Spring", "Fall"])
)
fdf = df[mask].copy()

if fdf.empty:
    st.warning("No data matches the current filters.")
    st.stop()

# ── KPI cards ──────────────────────────────────────────────────────────────────
st.markdown("### 📊 Key Performance Indicators")
k1, k2, k3, k4, k5 = st.columns(5)

avg_ret  = fdf["Retention Rate (%)"].mean()
avg_sat  = fdf["Student Satisfaction (%)"].mean()
tot_app  = fdf["Applications"].sum()
tot_enr  = fdf["Enrolled"].sum()
adm_rate = (fdf["Admitted"].sum() / fdf["Applications"].sum() * 100)

def kpi(col, label, value, fmt="{:.1f}", suffix=""):
    col.metric(label, f"{fmt.format(value)}{suffix}")

with k1:
    st.metric("Avg Retention Rate", f"{avg_ret:.1f}%")
with k2:
    st.metric("Avg Satisfaction", f"{avg_sat:.1f}%")
with k3:
    st.metric("Total Applications", f"{tot_app:,}")
with k4:
    st.metric("Total Enrolled", f"{tot_enr:,}")
with k5:
    st.metric("Avg Admission Rate", f"{adm_rate:.1f}%")

st.markdown("---")

# ── Colour palette ─────────────────────────────────────────────────────────────
BLUE   = "#1565c0"
ORANGE = "#e65100"
GREEN  = "#2e7d32"
PURPLE = "#6a1b9a"
DEPT_COLORS = {"Engineering": BLUE, "Business": ORANGE, "Arts": GREEN, "Science": PURPLE}

# ── Row 1: Retention trend + Satisfaction trend ────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 📈 Retention Rate Trend Over Time")
    ret_data = fdf.groupby(["Year", "Term"])["Retention Rate (%)"].mean().reset_index()
    fig, ax = plt.subplots(figsize=(6, 3.5))
    for term, color, ls in [("Spring", BLUE, "-o"), ("Fall", ORANGE, "-s")]:
        sub = ret_data[ret_data["Term"] == term]
        if not sub.empty:
            ax.plot(sub["Year"], sub["Retention Rate (%)"], ls, color=color,
                    label=term, linewidth=2, markersize=6)
    ax.set_xlabel("Year"); ax.set_ylabel("Retention Rate (%)")
    ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.0f%%"))
    ax.legend(); ax.grid(axis="y", linestyle="--", alpha=0.4)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

with col2:
    st.markdown("#### 😊 Student Satisfaction Scores by Year")
    sat_data = fdf.groupby("Year")["Student Satisfaction (%)"].mean().reset_index()
    fig, ax = plt.subplots(figsize=(6, 3.5))
    bars = ax.bar(sat_data["Year"], sat_data["Student Satisfaction (%)"],
                  color=BLUE, edgecolor="white", width=0.6)
    ax.bar_label(bars, fmt="%.1f%%", padding=3, fontsize=8)
    ax.set_xlabel("Year"); ax.set_ylabel("Satisfaction (%)")
    ax.set_ylim(70, 95)
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

# ── Row 2: Spring vs Fall + Department pie ──────────────────────────────────────
col3, col4 = st.columns(2)

with col3:
    st.markdown("#### 🔄 Spring vs Fall Comparison")
    metrics = ["Applications", "Admitted", "Enrolled"]
    comp = fdf.groupby("Term")[metrics].mean().reset_index()
    x = range(len(metrics))
    width = 0.35
    fig, ax = plt.subplots(figsize=(6, 3.5))
    for i, (term, color) in enumerate(zip(["Spring", "Fall"], [BLUE, ORANGE])):
        sub = comp[comp["Term"] == term]
        if not sub.empty:
            vals = [sub[m].values[0] for m in metrics]
            bars = ax.bar([xi + i*width for xi in x], vals, width,
                          label=term, color=color, edgecolor="white")
            ax.bar_label(bars, fmt="%.0f", padding=2, fontsize=7)
    ax.set_xticks([xi + width/2 for xi in x])
    ax.set_xticklabels(metrics)
    ax.set_ylabel("Avg Students")
    ax.legend(); ax.grid(axis="y", linestyle="--", alpha=0.4)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

with col4:
    st.markdown("#### 🏫 Enrollment by Department")
    dept_cols = [f"{d} Enrolled" for d in departments if f"{d} Enrolled" in fdf.columns]
    if dept_cols:
        dept_totals = fdf[dept_cols].sum()
        dept_labels = [c.replace(" Enrolled", "") for c in dept_cols]
        colors = [DEPT_COLORS[d] for d in dept_labels]
        fig, ax = plt.subplots(figsize=(5, 3.5))
        wedges, texts, autotexts = ax.pie(
            dept_totals, labels=dept_labels, autopct="%1.1f%%",
            colors=colors, startangle=140,
            wedgeprops=dict(edgecolor="white", linewidth=1.5),
        )
        for at in autotexts:
            at.set_fontsize(9)
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)
    else:
        st.info("Select at least one department.")

# ── Row 3: Department enrollment trend (line chart) ────────────────────────────
st.markdown("#### 📉 Department Enrollment Trends")
dept_trend = fdf.groupby("Year")[[f"{d} Enrolled" for d in departments
                                   if f"{d} Enrolled" in fdf.columns]].sum().reset_index()
fig, ax = plt.subplots(figsize=(10, 3.5))
for d in departments:
    col_name = f"{d} Enrolled"
    if col_name in dept_trend.columns:
        ax.plot(dept_trend["Year"], dept_trend[col_name], "-o",
                label=d, color=DEPT_COLORS[d], linewidth=2, markersize=5)
ax.set_xlabel("Year"); ax.set_ylabel("Students Enrolled")
ax.legend(loc="upper left"); ax.grid(axis="y", linestyle="--", alpha=0.4)
fig.tight_layout()
st.pyplot(fig)
plt.close(fig)

# ── Row 4: Heatmap correlation ──────────────────────────────────────────────────
st.markdown("#### 🔥 Correlation Heatmap")
num_cols = ["Applications", "Admitted", "Enrolled",
            "Retention Rate (%)", "Student Satisfaction (%)"]
corr = fdf[num_cols].corr()
fig, ax = plt.subplots(figsize=(7, 3.5))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="Blues",
            linewidths=0.5, ax=ax, cbar_kws={"shrink": 0.8})
ax.set_title("Pearson Correlation between Key Indicators", fontsize=10)
fig.tight_layout()
st.pyplot(fig)
plt.close(fig)

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("---")
st.caption("📌 Activity I — Data Visualization and Dashboard Deployment · Data Mining · Universidad de La Costa")
