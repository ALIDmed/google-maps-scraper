import streamlit as st
from scraper import generate_leads
import pandas as pd

st.set_page_config(page_title="LGS", layout="wide", initial_sidebar_state="auto", menu_items=None)

with st.container():
    st.title("Lead Generation Scraper")

col1, col2, col3 = st.columns(3, gap='large')

with col1:
    business = st.text_input("Enter the type of business")

with col2:
    location = st.text_input("Enter the city/country")

with col3:
    max_results = st.slider("Max number of results", min_value=1, max_value=120, value=1)

_, generate_col, _ = st.columns(3)
with generate_col:
    generate = st.button("Generate Leads", use_container_width=True, type='primary')

if generate:
    with st.spinner('Generating leads...'):
        generate_leads(business, location, max_results)

    _, _, _,download_col = st.columns(4)
    with download_col:
        st.download_button('Download', './results.csv', file_name='results.csv', type="primary", use_container_width=1)
    _, _, download_col = st.columns(3)
    df = pd.read_csv('results.csv')
    st.dataframe(df, use_container_width=True)
