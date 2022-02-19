import pandas as pd
import streamlit as st

data = pd.read_csv('data.csv.gz')

st.title('PLUS Explorer')
st.write('In December 2021')
