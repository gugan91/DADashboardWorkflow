# Install needed packages:
# pip install streamlit pandas gspread gspread_dataframe google-auth streamlit-aggrid

import pandas as pd
import streamlit as st
import gspread
from google.oauth2 import service_account
from gspread_dataframe import get_as_dataframe
from st_aggrid import AgGrid, GridOptionsBuilder

# Setup credentials from Streamlit Secrets
scopes = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=scopes
)

gc = gspread.authorize(credentials)

# Connect to Google Sheet
spreadsheet = gc.open_by_url('https://docs.google.com/spreadsheets/d/1T6HbMBJRHgsZFWJiVqwJeEHUE-oVKQ0BvZTRyfPN964/edit?usp=sharing')
worksheet = spreadsheet.sheet1
df = get_as_dataframe(worksheet).dropna()

# Build Streamlit app
st.set_page_config(page_title="DA Workflow Tracker", page_icon=":clipboard:", layout="wide")
st.title('Data Associate Live Workflow Tracker')

st.markdown('**Hover or click on DA names to view their current workflow assignment.**')

# Create Interactive Table
gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, editable=False)
gridOptions = gb.build()

AgGrid(df, gridOptions=gridOptions, enable_enterprise_modules=False, theme='streamlit')
