import math

import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go


def fmt(v, dec=0):
    """1,500 -> 1.5K | 2,340,000 -> 2.34M | small numbers keep `dec` decimals."""
    a = abs(v)
    if a >= 1e6:
        s, u = f"{v / 1e6:.2f}", "M"
    elif a >= 1e3:
        s, u = f"{v / 1e3:.1f}", "K"
    else:
        return f"{v:,.{dec}f}"
    return s.rstrip("0").rstrip(".") + u


def nice_ticks(maxv, n=5):
    """Evenly spaced round tick values from 0 to just above maxv."""
    if maxv <= 0:
        return [0]
    raw = maxv / n
    mag = 10 ** math.floor(math.log10(raw))
    step = min(m * mag for m in (1, 2, 2.5, 5, 10) if m * mag >= raw)
    return list(np.arange(0, maxv + step, step))

# ─────────────────────────────────────────────────────────────
# 1. CONFIG: change only this line
# ─────────────────────────────────────────────────────────────
DATA_PATH = "../dataset/cleaned_data.csv"   # .csv or .xlsx

st.set_page_config(page_title="Retail Sales Dashboard", layout="wide",
                   initial_sidebar_state="collapsed")

# ─────────────────────────────────────────────────────────────
# 2. PALETTE (matched to the reference screenshot)
# ─────────────────────────────────────────────────────────────
C = dict(
    header="#0F4C97", bg="#F3F7FC", border="#DCE6F2", text="#1B2A41",
    muted="#5B6B82", blue="#1565C0", blue_l="#8CBBF1", orange="#F5A030",
    green="#1FA463", purple="#7B3FBF", up="#1E9E5A", down="#D64545",
    insight_bg="#EAF2FB",
)
TINTS = ["#E3EEF9", "#E2F6EC", "#EEE8F8", "#FDEBD8", "#E0F3F5"]
ICON_BG = ["#C9DFF5", "#C3EBD6", "#DDD1F1", "#FAD5AE", "#BFE6EA"]
BLUE_SHADES = ["#1565C0", "#1E7FE0", "#4F9BEA", "#6FB0F0", "#8CBBF1"]
GREEN_SHADES = ["#1FA463", "#2DB574", "#4CC58A", "#6FD3A2", "#95DFBA"]
ORANGE_SHADES = ["#E07E00", "#F0940F", "#F5A030", "#F7B45C", "#FAC988"]
DONUT = [C["blue"], C["green"], C["orange"], C["purple"], "#0F4C97", "#8CBBF1"]

# ─────────────────────────────────────────────────────────────
# 3. STYLING
# ─────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html, body, .stApp, [class*="st-"] {{ font-family: 'Inter', sans-serif; }}
.stApp {{ background: {C['bg']}; color: {C['text']}; }}
header[data-testid="stHeader"], footer, #MainMenu {{ display: none; }}
.block-container {{ padding: 0.6rem 1.5rem 1rem 1.5rem; max-width: 100%; }}
div[data-testid="stVerticalBlock"] {{ gap: 0.6rem; }}

/* Header band */
.st-key-header {{ background: {C['header']}; border-radius: 12px; padding: 14px 22px 10px 22px; }}
.st-key-header h1 {{ color: #fff; font-size: 1.9rem; font-weight: 700; margin: 0; padding: 0; line-height: 1.2; }}
.st-key-header .sub {{ color: #DCE8F7; font-size: .9rem; margin-top: 2px; }}
.st-key-header label p {{ color: #DCE8F7 !important; font-size: .8rem; }}
.st-key-header div[data-baseweb="select"] > div {{ background: #fff; color: {C['text']}; min-height: 38px; }}
.st-key-header div[data-baseweb="select"] * {{ color: {C['text']} !important; }}

/* Chart cards */
[class*="st-key-card_"] {{ background: #fff; border: 1px solid {C['border']} !important;
    border-radius: 12px; padding: 6px 10px; box-shadow: 0 1px 3px rgba(15,76,151,.06);
    display: flex; flex-direction: column; width: 100%; }}
.st-key-card_insights {{ background: {C['insight_bg']}; }}
.card-title {{ font-weight: 700; font-size: 1.02rem; color: {C['text']}; margin: 4px 0 0 4px; }}
.card-body {{ flex: 1; overflow-y: auto; }}

/* Row 3 (category table | customer chart | insights): shared height so they line up */
.st-key-card_table, .st-key-card_cust, .st-key-card_insights {{ min-height: 430px; }}

/* KPI cards */
.kpi {{ border-radius: 12px; padding: 16px 18px; border: 1px solid {C['border']}; min-height: 158px; }}
.kpi-top {{ display: flex; align-items: center; gap: 12px; }}
.kpi-icon {{ width: 42px; height: 42px; border-radius: 10px; display: flex;
    align-items: center; justify-content: center; font-size: 1.3rem; }}
.kpi-label {{ font-weight: 600; font-size: .95rem; color: {C['text']}; }}
.kpi-value {{ font-weight: 700; font-size: 1.9rem; margin: 8px 0 2px 0; color: {C['text']}; }}
.kpi-delta {{ font-size: .82rem; color: {C['muted']}; }}
.up {{ color: {C['up']}; font-weight: 600; }}
.down {{ color: {C['down']}; font-weight: 600; }}
.st-key-kpi_row {{ margin-bottom: 18px; }}

/* Table */
table.perf {{ width: 100%; border-collapse: collapse; font-size: .88rem; margin-top: 6px; }}
table.perf th {{ background: {C['bg']}; text-align: right; padding: 9px 10px; font-weight: 600;
    border-bottom: 1px solid {C['border']}; }}
table.perf td {{ text-align: right; padding: 8px 10px; border-bottom: 1px solid #EDF2F8; }}
table.perf th:first-child, table.perf td:first-child {{ text-align: left; }}
table.perf tr.total td {{ background: #E3EEF9; font-weight: 700; border-bottom: none; }}

/* Insights */
.insight {{ display: flex; gap: 12px; align-items: flex-start; margin: 16px 6px; font-size: 1rem; line-height: 1.45; }}
.tick {{ background: {C['green']}; color: #fff; border-radius: 50%; min-width: 22px; height: 22px;
    font-size: .8rem; display: flex; align-items: center; justify-content: center; margin-top: 1px; }}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# 4. DATA LOADING & CLEANING
# ─────────────────────────────────────────────────────────────
@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_excel(path) if path.lower().endswith((".xlsx", ".xls")) else pd.read_csv(path)
    df.columns = df.columns.str.strip()
    df = df.drop(columns=[c for c in df.columns if c.startswith("Unnamed")], errors="ignore")

    for c in ["Transaction ID", "Customer ID", "Category", "Item", "Payment Method", "Location"]:
        df[c] = df[c].astype(str).str.strip()
    for c in ["Price Per Unit", "Quantity", "Total Spent"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    # Fill missing totals from price x quantity, drop rows that are still unusable
    df["Total Spent"] = df["Total Spent"].fillna(df["Price Per Unit"] * df["Quantity"])
    df["Transaction Date"] = pd.to_datetime(df["Transaction Date"], format="%m/%d/%Y", errors="coerce")
    # Exclude incomplete 2025 data; analysis scope: 2022–2024
    df = df[df["Transaction Date"] <= "2024-12-31"]
    df = df.dropna(subset=["Transaction Date", "Total Spent"])

    df["Discount Applied"] = (df["Discount Applied"].astype(str).str.strip().str.upper()
                              .map({"TRUE": "Yes", "FALSE": "No"}).fillna("Unknown"))
    df["Month"] = df["Transaction Date"].dt.to_period("M")
    return df


try:
    df = load_data(DATA_PATH)
except Exception as e:
    st.error(f"Could not load data from DATA_PATH = {DATA_PATH!r}\n\n{e}")
    st.stop()

# ─────────────────────────────────────────────────────────────
# 5. HEADER + FILTERS
# ─────────────────────────────────────────────────────────────
months = sorted(df["Month"].unique(), reverse=True)
month_label = {m: m.strftime("%b %Y") for m in months}

with st.container(key="header"):
    h0, h1, h2, h3 = st.columns([2.6, 1, 1, 1])
    h0.markdown("<h1>Retail Sales Dashboard</h1>"
                "<div class='sub'>Sales Performance &nbsp;|&nbsp; Category Analysis &nbsp;|&nbsp; Customer Behaviour</div>",
                unsafe_allow_html=True)
    period = h1.selectbox("Month", ["All"] + [month_label[m] for m in months])
    loc = h2.selectbox("Location", ["All"] + sorted(df["Location"].unique()))
    cat = h3.selectbox("Category", ["All"] + sorted(df["Category"].unique()))

# base = location/category filtered, all dates (used for trend + previous-period lookups)
base = df.copy()
if loc != "All":
    base = base[base["Location"] == loc]
if cat != "All":
    base = base[base["Category"] == cat]

sel_month = next((m for m in months if month_label[m] == period), None)
cur = base if sel_month is None else base[base["Month"] == sel_month]
prev = None
if sel_month is not None:
    p = base[base["Month"] == sel_month - 1]
    prev = p if len(p) else None
prev_label = (sel_month - 1).strftime("%b %Y") if sel_month is not None else ""

if cur.empty:
    st.warning("No transactions match the selected filters. Try widening them.")
    st.stop()


# ─────────────────────────────────────────────────────────────
# 6. KPI CALCULATIONS
# ─────────────────────────────────────────────────────────────
def kpis(d: pd.DataFrame) -> dict:
    n = d["Transaction ID"].nunique()
    rev = d["Total Spent"].sum()
    return dict(rev=rev, txn=n, units=d["Quantity"].sum(),
                aov=rev / n if n else 0,
                disc=(d["Discount Applied"] == "Yes").mean() * 100 if len(d) else 0)


k = kpis(cur)
kp = kpis(prev) if prev is not None else None


def pct(a, b):
    return (a - b) / b * 100 if b else None


def delta_html(now, before, pp=False):
    if before is None:
        return "<span>Full selected period</span>"
    ch = (now - before) if pp else pct(now, before)
    if ch is None:
        return "<span>No prior data</span>"
    cls, arrow = ("up", "▲") if ch >= 0 else ("down", "▼")
    unit = " pp" if pp else "%"
    return f"<span class='{cls}'>{arrow} {abs(ch):.1f}{unit}</span> vs {prev_label}"


def kpi_card(i, icon, label, value, delta):
    return (f"<div class='kpi' style='background:{TINTS[i]}'>"
            f"<div class='kpi-top'><div class='kpi-icon' style='background:{ICON_BG[i]}'>{icon}</div>"
            f"<div class='kpi-label'>{label}</div></div>"
            f"<div class='kpi-value'>{value}</div><div class='kpi-delta'>{delta}</div></div>")


cards = [
    ("💰", "Total Revenue", fmt(k["rev"]), delta_html(k["rev"], kp and kp["rev"])),
    ("🧾", "Transactions", fmt(k["txn"]), delta_html(k["txn"], kp and kp["txn"])),
    ("📦", "Units Sold", fmt(k["units"]), delta_html(k["units"], kp and kp["units"])),
    ("🛒", "Avg Order Value", fmt(k["aov"], 1), delta_html(k["aov"], kp and kp["aov"])),
    ("🏷️", "Discount Usage", f"{k['disc']:.1f}%", delta_html(k["disc"], kp and kp["disc"], pp=True)),
]
with st.container(key="kpi_row"):
    for i, col in enumerate(st.columns(5)):
        col.markdown(kpi_card(i, *cards[i]), unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# 7. CHART HELPERS
# ─────────────────────────────────────────────────────────────
def style(fig, h=300, legend=False):
    fig.update_layout(height=h, margin=dict(l=8, r=8, t=8, b=8), paper_bgcolor="rgba(0,0,0,0)",
                      plot_bgcolor="rgba(0,0,0,0)", showlegend=legend,
                      font=dict(family="Inter", size=12, color=C["text"]),
                      legend=dict(font=dict(color=C["text"], size=12)))
    fig.update_layout(bargap=0.45)   # thinner bars leave room for labels
    # automargin grows the plot margin to fit labels; ticklen pushes labels away from the axis
    dark = dict(tickfont=dict(color=C["text"], size=12), linecolor=C["border"],
                automargin=True, ticks="outside", ticklen=10, tickcolor="rgba(0,0,0,0)")
    fig.update_xaxes(**dark)
    fig.update_yaxes(**dark)
    return fig


def show(fig):
    # theme=None stops Streamlit from overriding the dark label colors
    st.plotly_chart(fig, use_container_width=True, theme=None, config={"displayModeBar": False})


def title(t):
    st.markdown(f"<div class='card-title'>{t}</div>", unsafe_allow_html=True)


def hbar(series, shades, height=300):
    s = series.head(5)
    fig = go.Figure(go.Bar(x=s.values, y=s.index, orientation="h",
                           marker_color=shades[:len(s)], text=[fmt(v) for v in s.values],
                           textposition="outside", textfont=dict(color=C["text"], size=12),
                           cliponaxis=False))
    ticks = nice_ticks(s.max())
    fig.update_yaxes(autorange="reversed", showgrid=False)
    fig.update_xaxes(showgrid=True, gridcolor="#EDF2F8", range=[0, s.max() * 1.3],
                     tickvals=ticks, ticktext=[fmt(t) for t in ticks])
    return style(fig, height)


# ─────────────────────────────────────────────────────────────
# 8. ROW 2: TREND | PAYMENT DONUT | TOP 5 ITEMS BY VOLUME
# ─────────────────────────────────────────────────────────────
r2a, r2b, r2c = st.columns([1.55, 1.1, 1.25])

with r2a, st.container(border=True, key="card_trend"):
    title("Monthly Revenue Trend")
    m = (base.groupby("Month")["Total Spent"].sum().sort_index())
    labels = [x.strftime("%b %Y") for x in m.index]
    colors = [C["blue"] if (sel_month is None or x == sel_month) else C["blue_l"] for x in m.index]
    fig = go.Figure()
    fig.add_bar(x=labels, y=m.values, name="Revenue", marker_color=colors)
    fig.add_scatter(x=labels, y=m.rolling(3, min_periods=1).mean().values, name="3-Month Avg",
                    mode="lines+markers", line=dict(color=C["orange"], width=2.5))
    fig.update_xaxes(showgrid=False, tickangle=-45, nticks=12)
    yt = nice_ticks(m.max())
    fig.update_yaxes(gridcolor="#EDF2F8", tickvals=yt, ticktext=[fmt(t) for t in yt])
    fig.update_layout(legend=dict(orientation="h", y=1.12, x=1, xanchor="right"))
    show(style(fig, 250, legend=True))

with r2b, st.container(border=True, key="card_pay"):
    title("Revenue by Payment Method")
    pay = cur.groupby("Payment Method")["Total Spent"].sum().sort_values(ascending=False)
    fig = go.Figure(go.Pie(labels=pay.index, values=pay.values, hole=0.62, sort=False,
                           marker=dict(colors=DONUT[:len(pay)]), textinfo="percent",
                           textfont=dict(color="#fff", size=12)))
    fig.add_annotation(text=f"Total<br><b>{fmt(pay.sum())}</b>", showarrow=False,
                       font=dict(size=14, color=C["text"]))
    fig.update_layout(legend=dict(orientation="v", y=0.5, x=1.0))
    show(style(fig, 250, legend=True))

with r2c, st.container(border=True, key="card_items"):
    title("Top 5 Categories by Volume (Units Sold)")
    show(hbar(cur.groupby("Category")["Quantity"].sum().sort_values(ascending=False), ORANGE_SHADES, height=250))


# ─────────────────────────────────────────────────────────────
# 9. ROW 3: CATEGORY TABLE | TOP CUSTOMERS | INSIGHTS
# ─────────────────────────────────────────────────────────────
r3a, r3b, r3c = st.columns([1.55, 1.1, 1.25])

with r3a, st.container(border=True, key="card_table"):
    title("Category Performance (Top 5)")
    t = (cur.groupby("Category").agg(rev=("Total Spent", "sum"), txn=("Transaction ID", "nunique"),
                                     units=("Quantity", "sum")).sort_values("rev", ascending=False))
    t["aov"] = t["rev"] / t["txn"]
    t["share"] = t["rev"] / t["rev"].sum() * 100

    top5, rest = t.head(5), t.iloc[5:]
    rows = "".join(f"<tr><td>{i}</td><td>{fmt(r.rev)}</td><td>{fmt(r.txn)}</td><td>{fmt(r.units)}</td>"
                   f"<td>{fmt(r.aov, 1)}</td><td>{r.share:.1f}%</td></tr>" for i, r in top5.iterrows())
    if len(rest):
        o_rev, o_txn, o_units = rest.rev.sum(), rest.txn.sum(), rest.units.sum()
        rows += (f"<tr><td>Others ({len(rest)})</td><td>{fmt(o_rev)}</td><td>{fmt(o_txn)}</td>"
                 f"<td>{fmt(o_units)}</td><td>{fmt(o_rev / o_txn, 1)}</td><td>{rest.share.sum():.1f}%</td></tr>")
    rows += (f"<tr class='total'><td>Total</td><td>{fmt(t.rev.sum())}</td><td>{fmt(t.txn.sum())}</td>"
             f"<td>{fmt(t.units.sum())}</td><td>{fmt(t.rev.sum() / t.txn.sum(), 1)}</td><td>100%</td></tr>")
    st.markdown("<div class='card-body'><table class='perf'><tr><th>Category</th><th>Revenue</th>"
                f"<th>Transactions</th><th>Units</th><th>Avg Order</th><th>Share</th></tr>{rows}</table></div>",
                unsafe_allow_html=True)

with r3b, st.container(border=True, key="card_cust"):
    title("Top 5 Customers by Revenue")
    show(hbar(cur.groupby("Customer ID")["Total Spent"].sum().sort_values(ascending=False), GREEN_SHADES,
             height=350))


# Auto-generated insights (recomputed for every filter combination)
def top_of(col):
    s = cur.groupby(col)["Total Spent"].sum()
    known = s.drop(labels=["Unknown"], errors="ignore")
    s = known if len(known) else s
    s = s.sort_values(ascending=False)
    return s.index[0], s.iloc[0] / cur["Total Spent"].sum() * 100


ins = []
if kp is not None and pct(k["rev"], kp["rev"]) is not None:
    ch = pct(k["rev"], kp["rev"])
    ins.append(f"Revenue {'increased' if ch >= 0 else 'decreased'} by {abs(ch):.1f}% compared to {prev_label}.")
else:
    ins.append(f"Total revenue of {fmt(k['rev'])} across {fmt(k['txn'])} transactions in the selected period.")
name, sh = top_of("Category");        ins.append(f"{name} is the leading category with {sh:.1f}% of revenue.")
name, sh = top_of("Payment Method");  ins.append(f"{name} is the most used payment method, driving {sh:.1f}% of revenue.")
name, sh = top_of("Location");        ins.append(f"{name} transactions contribute {sh:.1f}% of revenue.")
item_rev = cur.groupby("Item")["Total Spent"].sum()
item_rev = (item_rev.drop(labels=["Unknown"], errors="ignore") if len(item_rev.drop(labels=["Unknown"], errors="ignore")) else item_rev).sort_values(ascending=False)
ins.append(f"{item_rev.index[0]} is the top item with {fmt(item_rev.iloc[0])} in revenue.")
d_yes = cur[cur["Discount Applied"] == "Yes"]
d_no = cur[cur["Discount Applied"] == "No"]
if len(d_yes) and len(d_no):
    ins.append(f"Discounted orders average {fmt(d_yes['Total Spent'].mean(), 1)} vs "
               f"{fmt(d_no['Total Spent'].mean(), 1)} without a discount.")

with r3c, st.container(border=True, key="card_insights"):
    title("💡 Key Insights")
    st.markdown("<div class='card-body'>" +
                "".join(f"<div class='insight'><div class='tick'>✔</div><div>{x}</div></div>" for x in ins) +
                "</div>", unsafe_allow_html=True)