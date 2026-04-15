import pandas as pd
import streamlit as st 
import matplotlib.pyplot as plt
import matplotlib.colors as clr

cend = '\033[0m'
bold = '\033[1m'
bred = '\033[1;31m'
bblue = '\033[1;34m'
bgreen = '\033[1;32m'
byellow = '\033[1;33m'
inval = f'{bred}Invalid! {cend}'

st.set_page_config(page_title='Histogram Maker', layout='wide')  
st.title('Histogram Maker')

if 'df' not in st.session_state:
    st.session_state.df = None
if 'filename' not in st.session_state:
    st.session_state.filename = None

with st.sidebar:
    st.header('Load .csv')
    uploaded = st.file_uploader('Choose a .csv file', type='csv')
    if uploaded is not None:
        try:
            df = pd.read_csv(uploaded)
            print(f'{bgreen}File loaded.{cend}')
            if 'df' not in st.session_state:
                st.session_state = 'df'
            filename = uploaded.name
            if 'filename' not in st.session_state:
                st.session_state = 'filename' 
            st.session_state.filename = True
        except pd.errors.EmptyDataError:
            st.error('Empty file. Try other.')
        except Exception as e:
            st.error(f'Error: {e}')