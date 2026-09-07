import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Gapminder Dashboard", layout="wide")

@st.cache_data
def load_data():
    return px.data.gapminder()

df = load_data()

st.title("Country Development Dashboard")

#---- Filter panel (sidebar) ----
st.sidebar.header("Filters")
years = sorted(df["year"].unique())
selected_year = st.sidebar.select_slider("Year", options=years, value=years[-1])
continents= sorted(df["continent"].unique())
selected_continents = st.sidebar.multiselect("Continent", continents, default=continents)
filtered = df[(df["year"] == selected_year) & (df["continent"].isin(selected_continents))]
col1, col2,col3 =st.columns(3)
col1.metric("Countries shown", f"{filtered['country'].nunique()}")
col2.metric("Avg life expectancy", f"{filtered['lifeExp'].mean():.1f} yrs")
col3.metric("Total population",f"{filtered['pop'].sum()/1e9:.2f} B")

#---- Main chart ----
fig = px.scatter(filtered, x="gdpPercap", y="lifeExp", size="pop", color="continent", hover_name="country", log_x=True, size_max=60,
title=f"GDP per Capita vs Life Expectancy in {selected_year}"
)
st.plotly_chart(fig, use_container_width= True)

# ---- Drill-down ----
st.subheader("Drill down into a country")
country_pick= st.selectbox("Choose a country", sorted(filtered["country"].unique()))
country_hist = df[df["country"]== country_pick]
fig2 = px.line(country_hist, x="year", y="lifeExp",markers= True, title=f"Life Expectancy Over Time - {country_pick}")
st.plotly_chart(fig2, use_container_width=True)
