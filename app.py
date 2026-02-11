import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------
# Page Config
# ----------------------------
st.set_page_config(
    page_title="NFHS Dashboard",
    layout="wide"
)

st.title("📊 National Family Health Survey (NFHS) Dashboard")

# ----------------------------
# Load Data
# ----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("All India National Family Health Survey.csv")
    return df

df = load_data()

# ----------------------------
# Sidebar Filters
# ----------------------------
st.sidebar.header("🔍 Filters")

states = st.sidebar.multiselect(
    "Select State/UT",
    options=sorted(df["India/States/UTs"].unique()),
    default=["India"]
)

survey = st.sidebar.multiselect(
    "Select Survey Round",
    options=df["Survey"].unique(),
    default=df["Survey"].unique()
)

area = st.sidebar.multiselect(
    "Select Area",
    options=df["Area"].unique(),
    default=["Total"]
)

# Filter dataframe
filtered_df = df[
    (df["India/States/UTs"].isin(states)) &
    (df["Survey"].isin(survey)) &
    (df["Area"].isin(area))
]

# ----------------------------
# Indicator Selection
# ----------------------------
non_indicator_cols = ["India/States/UTs", "Survey", "Area"]
indicators = [col for col in df.columns if col not in non_indicator_cols]

indicator = st.selectbox("📌 Select Indicator", indicators)

# ----------------------------
# KPI Display (if single value)
# ----------------------------
if len(filtered_df) == 1:
    value = filtered_df[indicator].values[0]
    st.metric(label=indicator, value=value)

# ----------------------------
# Visualization
# ----------------------------
st.subheader("📈 Visualization")

if len(states) > 1:
    fig = px.bar(
        filtered_df,
        x="India/States/UTs",
        y=indicator,
        color="Survey",
        barmode="group",
        title=indicator
    )
else:
    fig = px.line(
        filtered_df,
        x="Survey",
        y=indicator,
        markers=True,
        title=indicator
    )

st.plotly_chart(fig, use_container_width=True)

# ----------------------------
# Raw Data Section
# ----------------------------
with st.expander("📄 View Filtered Data"):
    st.dataframe(filtered_df)
