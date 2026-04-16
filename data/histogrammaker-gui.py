import io
import pandas as pd
import streamlit as st  
import matplotlib.pyplot as plt

@st.cache_data
def load_csv(file):
    return pd.read_csv(file)

st.set_page_config(page_title='Histogram Maker', layout='wide')  
st.title('Histogram Maker')

with st.sidebar:
    st.header('Load .csv')
    uploaded = st.file_uploader('Choose a .csv file', type='csv')
    if uploaded is not None:
        try:
            df = load_csv(uploaded)
            st.session_state['df'] = df
            st.session_state['filename'] = uploaded.name
            st.success(f"Loaded {len(df)} rows from '{uploaded.name}'")
        except pd.errors.EmptyDataError:
            st.error('Empty file. Try other.')
        except Exception as e:
            st.error(f'Error: {e}')

if 'df' not in st.session_state or st.session_state['df'] is None:
    st.info('Upload a .csv file from the side bar to begin.')
    st.stop()

st.subheader('Preview')
df = st.session_state['df']
st.dataframe(df.head())

with st.sidebar:
    st.header('Data')
    numeric_cols = [col for col in df.columns
                    if pd.api.types.is_numeric_dtype(df[col])]
    if not numeric_cols:
        st.error(f"No numeric columns found in {st.session_state['filename']}")
        st.stop()
    column = st.selectbox('Column', numeric_cols)
    missing = df[column].isna().sum()
    if missing > 0:
        st.warning(f'{missing} missing values ignored.')
    st.header("Configure")
    title = st.text_input('Title', 'Histogram')
    title_size = st.slider('Title Font Size', 8, 32, 20)
    xlabel = st.text_input('X-label', 'Value')
    xlabel_size = st.slider('X-label Font Size', 8, 24, 12)
    ylabel = st.text_input('Y-label', 'Frequency')
    ylabel_size = st.slider('Y-label font Size', 8, 24, 12)
    bins = st.slider('Bins', 1, 50, 10)
    density = st.checkbox('Normalize Density', False)
    bin_mode = st.selectbox('Bin Mode', ['Fixed', 'Auto Sqrt', 'Auto Sturges'])
    color = st.color_picker('Bar Color', '#4682B4')
    edgecolor = st.color_picker('Edge Color', '#000000')
    alpha = st.slider('Transparency', 0.1, 1.00, 0.85)
    logscale = st.checkbox('Log Scale (Y axis)', False)
    show_grid = st.checkbox('Show Grid', True)
    
def histogram():
    st.subheader('Histogram')
    fig, ax = plt.subplots()
    ax.set_title(title, fontsize=title_size)
    ax.set_xlabel(xlabel, fontsize=xlabel_size)
    ax.set_ylabel(ylabel, fontsize=ylabel_size)
    ax.hist(df[column].dropna(), 
            bins=bins, 
            color=color, 
            edgecolor=edgecolor, 
            alpha=alpha,
            density=density,)
    if show_grid is True:
        ax.grid(True, axis='y', alpha=alpha)
    if logscale is True:
        ax.set_yscale('log')
    st.pyplot(fig)
    plt.close(fig)
    return fig

def statistics(fig):
    data = df[column].dropna()
    count = data.count()
    mean = data.mean()
    median = data.median()
    std = data.std()
    min_val = data.min()
    max_val = data.max()

    if bin_mode == 'Auto (sqrt)':
        bins = int(len(data) ** 0.5)
    elif bin_mode == 'Auto (sturges)':
        bins = 'sturges'

    st.subheader('Summary Statistics')
    col1, col2 = st.columns(2)
    col1.metric('Count', f'{count}')
    col1.metric('Mean', f'{mean:.0f}')
    col1.metric('Median', f'{median:.2f}')
    col2.metric('Std. Dev', f'{std:.3f}')
    col2.metric('Min. Value', f'{min_val:.0f}')
    col2.metric('Max. Value', f'{max_val:.0f}')
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    st.download_button(
        'Download histogram',
        data=buf.getvalue(),
        file_name=f'{title}.png',
        mime='image/png'
    )

left, right = st.columns([2, 1])
with left:
    fig = histogram()

with right:
    statistics(fig)
    