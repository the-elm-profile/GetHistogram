import io
import math
import pandas as pd
import streamlit as st  
import matplotlib.pyplot as plt

@st.cache_resource
def load_csv(file):
    return pd.read_csv(file)
        
st.set_page_config(page_title='Get Histogram', layout='wide')  
st.title('Get Histogram')

with st.expander("Project info"):
    st.markdown("Made for study proposes only. | GitHub: https://github.com/the-elm-profile/GetHistogram | Under The Gnu General Public License v3.0.")

with st.sidebar:
    st.header('Load .csv')
    uploaded = st.file_uploader('Choose a .csv file', type='csv')
    if uploaded is not None:
        try:
            df = load_csv(uploaded)
            st.session_state['df']= df
            st.session_state['filename'] = uploaded.name
            st.success(f"Loaded {len(df)} rows from '{uploaded.name}'")
        except pd.errors.EmptyDataError:
            st.error('Empty file. Try other.')
        except Exception as e:
            st.error(f'Error: {e}')

if 'df' not in st.session_state or st.session_state['df'] is None:
    st.info('This application creates histograms from CSV datasets, allowing you to explore data distributions and uncover patterns.')
    st.info('Upload a .csv file from the side bar to begin.')
    st.stop()

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

    st.header('Configure')
    with st.sidebar.expander('Title, X and Y axis'):
        title = st.text_input('Title', 'Histogram')
        title_size = st.slider('Title Font Size', 8, 32, 20)
        xlabel = st.text_input('X-label', 'Value')
        xlabel_size = st.slider('X-label Font Size', 8, 24, 12)
        ylabel = st.text_input('Y-label', 'Frequency')
        ylabel_size = st.slider('Y-label font Size', 8, 24, 12)
        density = st.checkbox('Normalize Density', False, help='Show propability density insted of counts')
        logscale = st.checkbox('Log Scale (Y axis)', False)

    with st.sidebar.expander('Appearance'):
        col1, col2 = st.columns(2)
        with col1:
            color = st.color_picker('Bar Color', '#4682B4')
        with col2:
            edgecolor = st.color_picker('Edge Color', '#000000')
        alpha = st.slider('Transparency', 0.1, 1.00, 0.85)
        show_grid = st.checkbox('Show Grid', True)

    with st.sidebar.expander('Binnig'):
            bin_mode = st.selectbox('Bin Mode', ['Fixed', 'Auto Sqrt', 'Auto Sturges'])
            if bin_mode == 'Fixed':
                bins = st.slider('Bins', 1, 50, 10)
            elif bin_mode == 'Auto Sqrt':
                bins = int(len(df[column].dropna()) ** 0.5)
                st.caption(f"Auto Bins Sqrt: **{bins}**")
            else:
                bins = 'sturges'
                st.caption(f'Auto Bins: Sturges rule')
            st.caption(f"{len(df[column].dropna())} data points → {bins} bins")

    with st.sidebar.expander('Statistics in Histogram'):
        con1 = st.container(border=True)
        con2 = st.container(border=True)
        con3 = st.container(border=True)
        with con1:
            median_line = st.checkbox('Include the median in the histogram')
            median_color = st.color_picker('Median-line color', '#FF0000')
        with con2:    
            mean_line = st.checkbox('Include the mean in the histogram')
            mean_color = st.color_picker('Mean-line color', '#FFFF00')
        with con3:    
            std_line = st.checkbox('Include the standard deviation in the histogram')
            std_color = st.color_picker('Std-line color', '#008000')
        
def histogram():
    st.subheader('Histogram')
    fig,ax = plt.subplots()
    data = df[column].dropna()
    
    ax.set_title(title, fontsize=title_size)
    ax.set_xlabel(xlabel, fontsize=xlabel_size)
    ax.set_ylabel(ylabel, fontsize=ylabel_size)
    ax.hist(df[column].dropna(), 
            bins=bins, 
            color=color, 
            edgecolor=edgecolor, 
            alpha=alpha,
            density=density,) 
    median = data.median()
    mean = data.mean()
    std = data.std()
    if show_grid:
        ax.grid(True, axis='y', alpha=alpha)
    if logscale is True:
        ax.set_yscale('log')
    if median_line:
        ax.axvline(median, color=median_color, linestyle='dashed', linewidth=2, label=f'Median: {median:.4f}')
    if mean_line:
        ax.axvline(mean, color=mean_color, linestyle='dashed', linewidth=2, label=f'Mean: {mean:.4f}')
    if std_line:
        ax.axvline(mean + std, color=std_color, linestyle='dotted', linewidth=2, label=f'Mean + Std Dev: {mean + std:.4f}')
        ax.axvline(mean - std, color=std_color, linestyle='dotted', linewidth=2, label=f'Mean - Std Dev: {mean - std:.4f}')
    if median_line or mean_line or std_line:
        ax.legend()
    st.pyplot(fig)
    plt.close(fig)
    return fig

def statistics(fig):
    st.subheader('Summary Statistics')
    data = df[column].dropna()
    median = data.median()
    mean = data.mean()
    std = data.std()
    uncert = std/math.sqrt(len(data))
    min_val = data.min()
    max_val = data.max()

    col1, col2 = st.columns(2)
    col1.metric('Count', f'{len(data)}')
    col1.metric('Mean', f'{mean:.4f}')
    col1.metric('Median', f'{median:.4f}')
    col2.metric('Std. Dev', f'{std:.4f}')
    col2.metric('Uncertanty', f'{uncert:.4f}')
    col2.metric('Min. Value', f'{min_val:.4f}')
    col2.metric('Max. Value', f'{max_val:.4f}')

    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    st.download_button(
        'Download histogram',
        data=buf,
        file_name=f'{title}.png',
        mime='image/png',
)

left, right = st.columns([2, 1])
with left:
    fig = histogram()

with right:
    statistics(fig)

st.subheader('Data view')
df = st.session_state['df']
st.dataframe(df, height=250) 
