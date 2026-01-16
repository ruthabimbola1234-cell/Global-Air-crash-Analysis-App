import streamlit as st

import pandas as pd

import plotly.express as px

import plotly.graph_objects as go



#--Page configuration---
st.set_page_config(
    page_title="✈ Over Aircrash Analysis Dashboard (1908–2024)",
    page_icon="✈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM STYLES ---
st.markdown("""
    <style>
        .main {background-color:#(#1f1f2e;}
        .stMetric {background-color:white; border-radius:15px; padding:10px;}
        h1, h2, h3, h4 {color:#1f3c88;}
    </style>
""", unsafe_allow_html=True)



def load_data():
    df = pd.read_csv("cleaned_aircrashes_2024.csv")
    return df

df = load_data()

# --- HEADER ---

st.markdown(" ## ✈ Global Air Crash Analysis (1908-2024)")
st.caption(
    "### Interactive exploration of air crash patterns, fatalities, and survival trends."
)

# --- SIDEBAR FILTERS ---
st.sidebar.header("🔎 Filter Crashes")
# --- Year Dropdown ---
year = st.sidebar.selectbox(
    "Select Year:",
    options= ["All"] + sorted(df["Year"].dropna().unique())
)
# --- Country Dropdown ---
country = st.sidebar.selectbox(
    "Select Country:",
    options= ["All"] + sorted(df["Country/Region"].dropna().unique())
)
# --- Continent Dropdown ---
continent = st.sidebar.selectbox(
    "Select Continent:",
    options= ["All"] + sorted(df["Continent"].dropna().unique())
)
# --- Quarter Dropdown ---
quarter = st.sidebar.selectbox(
    "Select Quarter:",
    options= ["All"] + sorted(df["Quarter"].dropna().unique())
)
# --- APPLY FILTERS ---
filtered_df = df[
    (df["Country/Region"] == country) &
    (df["Year"] == year) &
    (df["Quarter"] == quarter) &
    (df["Continent"] == continent)
]


# KPI section
# --- KPI SECTION (Overall and Filtered) ---


# --- Overall totals ---
total_aboard_all = int(df["Aboard"].sum())
total_fatalities_all = int(df["Fatalities (air)"].sum())
ground_fatalities_all = int(df["Ground"].sum())
total_crashes_all = len(df)
survivors_all = int(df["Survivors"].sum())

# --- Filtered totals ---
filtered_df = df.copy()
if country != "All":
    filtered_df = filtered_df[filtered_df["Country/Region"] == country]
if year != "All":
    filtered_df = filtered_df[filtered_df["Year"] == year]
if quarter != "All":
    filtered_df = filtered_df[filtered_df["Quarter"] == quarter]
if continent != "All":
    filtered_df = filtered_df[filtered_df["Continent"] == continent]  

total_aboard_filt = int(filtered_df["Aboard"].sum())
total_fatalities_filt = int(filtered_df["Fatalities (air)"].sum())
ground_fatalities_filt = int(filtered_df["Ground"].sum())
total_crashes_filt = len(filtered_df)
survivors_filt = int(filtered_df["Survivors"].sum())
# KPI data and colors
kpis_overall = [
    {"label":"🧍 Total Aboard", "value": total_aboard_all, "color":"#00BCD4"},  # Cyan
    {"label":"💀 Air Fatalities", "value": total_fatalities_all, "color":"#E91E63"},  # Pink
    {"label":"🏠 Ground Fatalities", "value": ground_fatalities_all, "color":"#FFC107"}, # Amber
    {"label":"✈ Total Crashes", "value": total_crashes_all, "color":"#3F51B5"},  # Indigo
    {"label":"🕊 Survivors", "value": survivors_all, "color":"#4DD0E1"},  # Light Cyan
]
kpis_filtered = [
    {"label":"🧍 Total Aboard", "value": total_aboard_filt, "color":"#00BCD4"},  # Cyan
    {"label":"💀 Air Fatalities", "value": total_fatalities_filt, "color":"#E91E63"},  # Pink
    {"label":"🏠 Ground Fatalities", "value": ground_fatalities_filt, "color":"#FFC107"}, # Amber
    {"label":"✈ Total Crashes", "value": total_crashes_filt, "color":"#3F51B5"},  # Indigo
    {"label":"🕊 Survivors", "value": survivors_filt, "color":"#4DD0E1"},  # Light Cyan
]
# Overall totals
st.markdown("### 🌍 Overall Totals")
cols = st.columns(5)
for col, kpi in zip(cols, kpis_overall):
    col.markdown(f"""
        <div style="
            background-color:{kpi['color']};
            color:white;
            padding:20px;
            border-radius:10px;
            text-align:center;
            font-size:16px;
            font-weight:bold;">
            {kpi['label']}<br>
            <span style="font-size:24px;font-weight:bold;">{kpi['value']:,}</span>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Filtered view
st.markdown("### 🎯 Filtered View")
cols = st.columns(5)
for col, kpi in zip(cols, kpis_filtered):
    col.markdown(f"""
        <div style="
            background-color:{kpi['color']};
            color:white;
            padding:20px;
            border-radius:10px;
            text-align:center;
            font-size:16px;
            font-weight:bold;">
            {kpi['label']}<br>
            <span style="font-size:24px;font-weight:bold;">{kpi['value']:,}</span>
        </div>
    """, unsafe_allow_html=True)


    
st.markdown("### *1. How have global air crashes occurrences changed over time from 1908–2024 ?*")

# Use filtered data
data = filtered_df.copy()
 # Group by Year
yearly_trend = data.groupby("Year").size().reset_index(name="Crash_Count")

fig = px.line(
    yearly_trend,
    x="Year",
    y="Crash_Count",
    title="📈 Global Air Crash Occurrences (1908–2024)",
    markers=True,
    line_shape='linear',
)


fig.update_traces(line=dict(color='#3F51B5', width=3), marker=dict(color='#00BCD4', size=6))

# Style layout
fig.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    xaxis_title="Year",
    yaxis_title="Number of Crashes",
    title_font_size=20,
)

st.plotly_chart(fig, use_container_width=True)


st.markdown("### *2. Which decades recorded the highest number of air crash fatalities worldwide ?*")

# Use filtered data
data = filtered_df.copy()
# Create Decade column
data["Decade"] = (data["Year"] // 10) * 10

# Total fatalities (air + ground)
data["Total_Fatalities"] = data["Fatalities (air)"] + data["Ground"]

# Group by Decade
decade_fatalities = (
    data.groupby("Decade")["Total_Fatalities"]
    .sum()
    .reset_index()
)

# Plot bar chart
fig = px.bar(
    decade_fatalities,
    x="Decade",
    y="Total_Fatalities",
    title="💀 Worldwide air crash fatalities by decades ",
)

# Color styling (fatalities-focused, clear and readable)
fig.update_traces(
    marker=dict(color="#E91E63")  # Pink / Fatalities color
)

# Layout styling for Streamlit
fig.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    xaxis_title="Decade",
    yaxis_title="Total Fatalities (Air + Ground)",
    title_font_size=20,
    yaxis=dict(showgrid=True, gridcolor="#E0E0E0"),
    xaxis=dict(showgrid=False),
)

st.plotly_chart(fig, use_container_width=True)



st.markdown("### *3. Is there a signicant relationship between the day of the week and air crash occurrences?*")

# Use filtered data
data = filtered_df.copy()
# Ensure date column is datetime
data["Date"] = pd.to_datetime(data["Date"])

# Extract day of week
data["Day_of_Week"] = data["Date"].dt.day_name()

# Order days properly
day_order = [
    "Monday", "Tuesday", "Wednesday",
    "Thursday", "Friday", "Saturday", "Sunday"
]

# Count crashes per day
day_counts = (
    data["Day_of_Week"]
    .value_counts()
    .reindex(day_order)
    .reset_index()
)

day_counts.columns = ["Day_of_Week", "Crash_Count"]

# Donut chart
fig = px.pie(
    day_counts,
    names="Day_of_Week",
    values="Crash_Count",
    title="Air Crash Occurrences by Day of the Week",
    hole=0.45
)

# KPI-consistent colors
fig.update_traces(
    marker=dict(colors=[
        "#3F51B5",  # Indigo
        "#00BCD4",  # Cyan
        "#FFC107",  # Amber
        "#E91E63",  # Pink
        "#4DD0E1",  # Light Cyan
        "#9C27B0",  # Purple
        "#2196F3"   # Blue
    ]),
    textinfo="percent+label"
)

# Layout styling
fig.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    title_font_size=20,
    legend_title_text="Day of the Week"
)

st.plotly_chart(fig, use_container_width=True)


st.markdown("### *4. Which countries or regions have experienced the highest number of air crashes since 1908?*")

# Use filtered data
data = filtered_df.copy()
# Count crashes by Country/Region
country_counts = (
    data["Country/Region"]
    .value_counts()
    .head(10)
    .reset_index()
)

country_counts.columns = ["Country/Region", "Crash_Count"]

# Horizontal bar chart
fig = px.bar(
    country_counts,
    x="Crash_Count",
    y="Country/Region",
    orientation="h",
    title="Top 10 Countries by Number of Air Crashes (Since 1908)",
)

# KPI-consistent colors
fig.update_traces(
    marker=dict(color="#3F51B5")  # Indigo
)

# Layout styling
fig.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    xaxis_title="Number of Air Crashes",
    yaxis_title="Country / Region",
    title_font_size=20,
    yaxis=dict(autorange="reversed"),  # Highest at top
    xaxis=dict(showgrid=True, gridcolor="#E0E0E0"),
)

st.plotly_chart(fig, use_container_width=True)


st.markdown("### *5. Which aircraft manufacturers are most frequently involved in air crashes globally?*")

# Count crashes per aircraft manufacturer
manufacturer_counts = (
    data["Aircraft Manufacturer"]
    .value_counts()
    .head(5)
    .reset_index()
)

manufacturer_counts.columns = ["Manufacturer", "Crash_Count"]

# Define a colorful KPI-inspired palette
colors = [
    "#3F51B5",  # Indigo
    "#00BCD4",  # Cyan
    "#FFC107",  # Amber
    "#E91E63",  # Pink
    "#4DD0E1",  # Light Cyan
    "#9C27B0",  # Purple
    "#2196F3",  # Blue
    "#FF9800",  # Orange
    "#8BC34A",  # Green
    "#FF5722",  # Deep Orange
]

# Funnel chart
fig = px.funnel(
    manufacturer_counts,
    x="Crash_Count",
    y="Manufacturer",
    title="Top 5 Aircraft Manufacturers by Number of Air Crashes Globally"
)

fig.update_traces(marker=dict(color=colors))

# Layout styling
fig.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    title_font_size=20,
)

st.plotly_chart(fig, use_container_width=True)


st.markdown("### *6. Do specific aircraft models tend to be involved in crashes with higher numbers of fatalities or survivors?*")

# Use filtered data
data = filtered_df.copy()
# Aggregate total fatalities and survivors by aircraft model
model_stats = (
    data.groupby("Aircraft")
    .agg({"Fatalities (air)": "sum", "Survivors": "sum"})
    .reset_index()
)

# Sort by total fatalities to get top 10 models
top_models = model_stats.sort_values(by="Fatalities (air)", ascending=False).head(10)

top_models_melted = top_models.melt(
    id_vars="Aircraft",
    value_vars=["Fatalities (air)", "Survivors"],
    var_name="Outcome",
    value_name="Count"
)

# Grouped horizontal bar chart
fig = px.bar(
    top_models_melted,
    x="Count",
    y="Aircraft",
    color="Outcome",
    orientation="h",
    text="Count",
    title="Top 10 Aircraft Models by Total Fatalities and Survivors",
    color_discrete_map={
        "Fatalities (air)": "#E91E63",  # Pink for fatalities
        "Survivors": "#00BCD4"          # Cyan for survivors
    }
)

# Layout styling
fig.update_traces(textposition="outside")
fig.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    yaxis=dict(autorange="reversed"),  # Highest at top
    xaxis_title="Count",
    yaxis_title="Aircraft Model",
    title_font_size=20
)

# Display in Streamlit
st.plotly_chart(fig, use_container_width=True)


st.markdown("### *7.  Do air crash occurrences and survival rates vary across different quarters or months of the year worldwide?*")

# Use filtered data
data = filtered_df.copy()
# Ensure date column is datetime
data["Date"] = pd.to_datetime(data["Date"])

# Extract month info
data["Month"] = data["Date"].dt.month_name()
data["Month_Num"] = data["Date"].dt.month

# Total onboard
data["Total_Aboard"] = data["Survivors"] + data["Fatalities (air)"]

# Aggregate monthly data
monthly_stats = (
    data.groupby(["Month", "Month_Num"])
    .agg(
        Crash_Count=("Month", "size"),
        Survivors=("Survivors", "sum"),
        Total_Aboard=("Total_Aboard", "sum")
    )
    .reset_index()
    .sort_values("Month_Num")
)

# Survival rate
monthly_stats["Survival_Rate (%)"] = (
    monthly_stats["Survivors"] / monthly_stats["Total_Aboard"] * 100
)

# Create figure
fig = go.Figure()

# Bar chart: Crash occurrences
fig.add_trace(
    go.Bar(
        x=monthly_stats["Month"],
        y=monthly_stats["Crash_Count"],
        name="Crash Occurrences",
        marker_color="#26C6DA",  # Bright Teal
        yaxis="y1"
    )
)

# Line chart: Survival rate
fig.add_trace(
    go.Scatter(
        x=monthly_stats["Month"],
        y=monthly_stats["Survival_Rate (%)"],
        name="Survival Rate (%)",
        mode="lines+markers",
        line=dict(color="#FF5252", width=4),  # Coral Red
        marker=dict(size=8),
        yaxis="y2"
    )
)

# Layout with dual y-axes
fig.update_layout(
    title="Seasonal Variation in Air Crash Occurrences and Survival Rates",
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    xaxis=dict(title="Month"),
    yaxis=dict(
        title="Number of Crashes",
        showgrid=True,
        gridcolor="#E0E0E0"
    ),
    yaxis2=dict(
        title="Survival Rate (%)",
        overlaying="y",
        side="right",
        showgrid=False
    ),
    legend=dict(x=0.01, y=0.99),
    title_font_size=20
)

st.plotly_chart(fig, use_container_width=True)



st.markdown("### *8. How are air crash occurrences geographically distributed across countries and regions worldwide?*")

# Use filtered data
data = filtered_df.copy()
# Aggregate crash counts by country/region
country_crashes = (
    data.groupby("Country/Region")
    .size()
    .reset_index(name="Crash_Count")
)

# Choropleth map
fig = px.choropleth(
    country_crashes,
    locations="Country/Region",
    locationmode="country names",
    color="Crash_Count",
    hover_name="Country/Region",
    color_continuous_scale="Turbo",  # Vibrant & attractive
    title="Global Distribution of Air Crash Occurrences"
)

# Layout styling
fig.update_layout(
    geo=dict(
        showframe=False,
        showcoastlines=True,
        projection_type="natural earth"
    ),
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    title_font_size=20,
    coloraxis_colorbar=dict(
        title="Number of Crashes"
    )
)

st.plotly_chart(fig, use_container_width=True)



st.markdown("### *9. Aircraft manufacturer, total fatalities and survival rate*")

# We aggregate the key metrics by Manufacturer
manufacturer_stats = data.groupby("Aircraft").agg(
    Total_Incidents=("Aircraft", "count"),
    Total_Fatalities=("Fatalities (air)", "sum"),
    Total_Survivors=("Survivors", "sum")
).reset_index()

#  Calculate Survival Rate (%)
# Survival Rate = (Survivors / (Survivors + Fatalities)) * 100
manufacturer_stats['Survival Rate (%)'] = (
    (manufacturer_stats['Total_Survivors'] / 
    (manufacturer_stats['Total_Survivors'] + manufacturer_stats['Total_Fatalities'])) * 100
).fillna(0).round(2)

# 3. Filter for Top 15 Manufacturers (to keep the table readable)
# Sorting by Total Incidents to show the most prominent manufacturers
top_manufacturers = manufacturer_stats.nlargest(15, "Total_Incidents")


colorscale = px.colors.sequential.Greens
max_rate = top_manufacturers['Survival Rate (%)'].max() or 1
cell_colors = [
    px.colors.sample_colorscale("Greens", [val/100])[0] 
    for val in top_manufacturers['Survival Rate (%)']
]
fig = go.Figure(data=[go.Table(
    header=dict(
        values=['<b>Manufacturer</b>', '<b>Total Fatalities</b>', '<b>Total Survivors</b>', '<b>Survival Rate</b>'],
        fill_color='#2c3e50',
        align='left',
        font=dict(color='white', size=12)
    ),
    cells=dict(
        values=[
            top_manufacturers['Aircraft'],
            top_manufacturers['Total_Fatalities'],
            top_manufacturers['Total_Survivors'],
            top_manufacturers['Survival Rate (%)'].apply(lambda x: f"{x}%")
        ],
        # Only the Survival Rate column gets the green gradient
        fill_color=[
            'white', 
            'white', 
            'white', 
            cell_colors
        ],
        align='left',
        font=dict(color='black', size=11),
        height=30
    )
)])

fig.update_layout(
    title="Aircraft Manufacturer Safety Performance (Top 15 by Incidents)",
    margin=dict(l=0, r=0, t=40, b=0)
)

st.plotly_chart(fig, use_container_width=True)


st.markdown("### *10. What proportion of air crashes result in ground fatalities, and how has this changed over time?*")

# Convert Date and extract Year
data['Date'] = pd.to_datetime(data['Date'])
data['Year'] = data['Date'].dt.year

# Logic: Count an incident if 'Ground' fatalities > 0
data['Has_Ground_Fatalities'] = data['Ground'] > 0

# Aggregate data by Year
yearly_data = data.groupby('Year').agg(
    Total_Crashes=('Has_Ground_Fatalities', 'count'),
    Crashes_With_Ground_Fatalities=('Has_Ground_Fatalities', 'sum')
).reset_index()

# Calculate the actual Proportion (%)
yearly_data['Proportion (%)'] = (
    (yearly_data['Crashes_With_Ground_Fatalities'] / yearly_data['Total_Crashes']) * 100
).round(2)

st.subheader("Evolution of Ground Fatality Proportions")

fig = px.area(
    yearly_data,
    x="Year",
    y="Proportion (%)",
    title="Percentage of Air Crashes Involving Ground Fatalities",
    labels={"Proportion (%)": "Proportion of Total Crashes (%)", "Year": "Year of Incident"},
    color_discrete_sequence=["#EF553B"], # A warm, alert red-orange
    template="plotly_white"
)

fig.update_layout(
    hovermode="x unified",
    xaxis=dict(showgrid=False),
    yaxis=dict(ticksuffix="%", showgrid=True, gridcolor='rgba(0,0,0,0.1)'),
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)"
)

# Add a trend line (Optional: smoothing out the noise)
fig.update_traces(line_color="#B22222", line_width=2, fillcolor="rgba(239, 85, 59, 0.3)")

st.plotly_chart(fig, use_container_width=True)

# Contextual Metrics ---
col1, col2 = st.columns(2)
with col1:
    peak_year = yearly_data.loc[yearly_data['Proportion (%)'].idxmax()]
    st.metric("Highest Proportion Year", f"{int(peak_year['Year'])}", f"{peak_year['Proportion (%)']}%")

with col2:
    recent_avg = yearly_data.tail(10)['Proportion (%)'].mean()
    st.metric("Avg. Proportion (Last 10 Years)", f"{recent_avg:.2f}%")



    st.markdown("### *FINDINGS*")

    st.markdown("###  1.   Totals include people 156,625 aboard, 111,872 air fatalities, 8,582 ground fatalities, and 44,753 survivors. ")
    st.markdown("###  2.   Total deaths due to air crashes amount to 5,035.")
    st.markdown("###  3.   The crashes from 1908–2024 climbs slowly at first, rises sharply then trends downward after, reaching very low single‑digit levels after 2010.")
    st.markdown("###  4.	Fatalities by decade shows the highest total deaths in the 1970s, after which fatalities drop significantly in the 2000s and even more in the 2010s and early 2020s.")
    st.markdown("###  5.	From the donut chart, crashes are evenly distributed across the week with percentage range between 12% and 15.3%.")
    st.markdown("###  6.	United States recorded the highest number of air crashes.")
    st.markdown("###  7.	McDonnell Douglas have the highest number of plane crashes among manufacturers.")
    st.markdown("###  8.	Some aircraft models have much higher death tolls: older aircraft have high fatalities and low survival, while some modern jets have higher survival numbers, this shows crashes survivability has improved dramatically in newer aircraft.")
    st.markdown("###  9.	Highest crashes occurrences stay between 350-450 per month. This simply shows there is a seasonal effect driven by weather, heavy travel and Congested airports and pilot workload.")
    st.markdown("###  10.	Crashes cluster in high-traffic or developing aviation nations, but not uniformly global.")
    st.markdown("###  11.	Manufacturers shows high survival rates (>85%), with fatalities linked to incident volume.")
    st.markdown("###  12.	Ground fatalities are rare (<5% average), trending downward long-term.")



    st.markdown("###  RECOMMENDATIONS ")

    st.markdown("###  1.	Sustain, strengthens safety regulations and inspection should be done frequently. ")
    st.markdown("###  2.	Invest in technology and infrastructure especially in places where historical risk has been higher.")
    st.markdown("###  3.	Strengthens pilot scheduling during high-risk months and increase simulator training for emergency scenarios.")
    st.markdown("###  4.	Predictive analytical measures should be used to monitor aircraft model risk, weather patterns, seasonal traffic spikes.")
    st.markdown("###  5.	Aircrafts with poor survival records should be phased out.")