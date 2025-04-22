import streamlit as st
import pandas as pd
import pickle
import plotly.express as px
import os.path
import os
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title=None, page_icon=None, layout="centered", initial_sidebar_state="expanded", menu_items=None)

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(CUR_DIR)
data = {'COMPLETE_topic_breakdown':None,
        'piedf':None,
        'spiderdf':None,
        'hist_Car Batteries': None,
        'hist_Engine Oil Recommender': None,
        'hist_Tuning Remap': None,
        'hist_Tyre Recommender': None,
        'hist_Wiper Blades': None,}
for datum in data.keys():
    try:
        with open(os.path.join(data_path,f'{datum}.pickle'), 'rb') as f:
            data[datum] = pickle.load(f)
    except Exception as e:
        print(f"Error loading data file {datum}:{e}")

df_full = data['COMPLETE_topic_breakdown']
df_pie = data['piedf']
df_spider = data['spiderdf']

# @st.cache_data
# def get_data():
#     df = pd.DataFrame(df_full)
#     return df

# @st.cache_data(hash_funcs={np.ndarray: str})
# def show_data(data):
#     time.sleep(1)
#     return data

# # SIDEBAR
st.sidebar.write(
    f"""
    __About__\n 
    # ML Performance app
    This is the app that visualize the products sold at the [ML Performance](https://www.mlperformance.co.uk) website.\n
    The analysis were performed using {df_full.shape[0]} products from 
    five categories 
    ([engine oils](https://www.mlperformance.co.uk/collections/engine-oil-recommender), 
    [batteries](https://www.mlperformance.co.uk/collections/car-batteries), 
    [tyres](https://www.mlperformance.co.uk/collections/tyre-recommender), 
    [wiper blades](https://www.mlperformance.co.uk/collections/wiper-blades), 
    [tuning and remap](https://www.mlperformance.co.uk/collections/tuning-remap)).

    """
)

# # BODY CONTENT
st.write(
    f"""
    # Overview
    Among five categories, the {df_full.shape[0]} products are distributed as shown in the following sunburst chart:
    """
)

# types of product - sunburst chart
fig1 = px.sunburst(
    df_pie,
    values = 'percentage',
    path=['category','prod_type'],
    title = "Product Distribution - Sunburst Chart"
) 
st.plotly_chart(fig1, theme='streamlit')
    
st.write(
    f"""
    From the pie chart above, it is noticeable that among the five categories, 
    the products are mostly constituted by the tyre category.
    Meanwhile, the least product listed on the site is the tuning & remap.
    Now, let us see what is the feedback that our customer provide when they bought products from ML Performance.
    \n The following spider/polar chart summarise the topic modelling that customer mentioned when they leave review to us.
    """
)

val = ['Engine Oil Recommender','Car Batteries','Tyre Recommender','Wiper Blades','Tuning Remap']
labs = ['Engine Oils','Batteries','Tyres','Wiper Blades','Tuning & Remap']

filter_data = ['All','Engine Oil Recommender','Car Batteries','Tyre Recommender','Wiper Blades','Tuning Remap']

def check_All():
    if st.session_state['checkboxAll']:
        for i in st.session_state.keys():
            if i.startswith('checkbox_') and not st.session_state[i]:
                st.session_state[i] = True
    else:
        for i in st.session_state.keys():
            if i.startswith('checkbox_') and st.session_state[i]:
                st.session_state[i] = False

def checkbox_container():
    cols = st.columns(6)
    for idx in range(len(filter_data)):
        if idx == 0:
            cols[idx].checkbox('All', value=False, key=f'checkboxAll', on_change=check_All)
            continue
        if idx == 3 or idx == 5:
            cols[idx].checkbox(labs[idx-1], value=True, key=f'checkbox_{val[idx-1]}')
            continue
        cols[idx].checkbox(labs[idx-1], value=False, key=f'checkbox_{val[idx-1]}')

def get_checkbox():
    selected = [i.replace('checkbox_','') for i in st.session_state.keys() if i.startswith('checkbox_') and st.session_state[i]]
    return selected

checkbox_container()
count_select = get_checkbox()

# # feedback from customer - spider chart/polar chart
topics = ['Recommended','Improve performance', 'Great Service/Product/Item',
          'Good Quality','Excellent Customer Service','Fast Delivery']

fig4 = go.Figure()

for idx in count_select:
    fig4.add_trace(go.Scatterpolar(
        r=list(df_spider[df_spider['category']==idx].iloc[0,[1,2,3,5,6,7]]),
        theta=topics,
        fill='toself',
        name=idx
    ))
fig4.update_layout(
    polar=dict(
        radialaxis=dict(visible=False, range=[0, max(df_spider[df_spider['category'].isin(count_select)].iloc[0,[1,2,3,5,6,7]]) + 0.003])  # set range if values are normalized
    ),
    showlegend=True,
    title=f'Customer Feedback - spider chart'
)
st.plotly_chart(fig4)

st.write('''Next, if we take a look on the listing price of each category, the following 
    price histogram can be observed.''')


# # price of product - histogram

for fil in count_select:
    fig2 = px.histogram(data[f'hist_{fil}'], x='price (MYR)',
                        color='vendor',
                        marginal='rug',title=f'Price distribution for {fil}')
    st.plotly_chart(fig2)

st.write(
    f"""
    From the histogram above, we can observe that between the tyre and the tuning/remap
    category, the range price of the later category is wider than the tyre category. However, although
    some price of the products in the tuning/remap category can exceed the tyre category, the price
    for the tuning/remap is concentrated on a cheaper price compared to the tyre category.
    This might suggest that the average price for tuning/remap products are are lower than the tyre products.
    \n Nonetheless, since most customer provide good reviews to the products listed on the website, let us also check which 
    vendor have the best rating in terms of the quality of its products.
    """
)

# # rating of vendor - boxplot
for cat in val:
    filtered_df = df_full[(df_full['category'] == cat) & (df_full['rating'] != 0)]
    fig3 = px.box(filtered_df,y='rating', x='vendor', title = f"Rating for {cat} category")
    st.plotly_chart(fig3)

