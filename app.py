import streamlit as st
import pandas as pd
import pickle
import plotly.express as px
import os.path
import os
import plotly.graph_objects as go
import numpy as np

CUR_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(CUR_DIR)
data = {'COMPLETE_topic_breakdown':None,'piedf':None}
for datum in data.keys():
    try:
        with open(os.path.join(data_path,f'{datum}.pickle'), 'rb') as f:
            data[datum] = pickle.load(f)
    except Exception as e:
        print(f"Error loading data file {datum}:{e}")

df_full = data['COMPLETE_topic_breakdown']
df_pie = data['piedf']

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
    five categories ([engine oils](https://www.mlperformance.co.uk/collections/engine-oil-recommender), 
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
    The {df_full.shape[0]} products are distributed as shown in the following sunburst chart:
    """
)

# types of product - sunburst chart
fig1 = px.sunburst(
    df_pie,
    values = 'percentage',
    path=['category','prod_type'],
    title = "Product Distribution - Sunburst Chart"
) 
st.plotly_chart(fig1)
    
# st.plotly_chart(fig1, theme='streamlit')
st.write(
    f"""
    From the pie chart above, it is noticeable that among the five categories, 
    the products listed on ML's website are mostly constituted by the tyre category.
    Meanwhile, the least product listed on the site is the tuning & remap.
    Next, if we take a look on the listing price of each category, the following 
    histogram can be observed.
    """
)

# # price of product - histogram
fig2 = px.histogram(df_full, x='price (MYR)',
                    color='category',
                    marginal='rug', title='Price distribution for each category - Histogram')
st.plotly_chart(fig2)

st.write(
    f"""
    From the histogram above, we can observe that between the tyre and the tuning/remap
    category, the range price of the later category is wider than the tyre category. However, although
    some price of the products in the tuning/remap category can exceed the tyre category, the price
    for the tuning/remap is concentrated on a cheaper price compared to the tyre category.
    This might suggest that the average price for tuning/remap products are are lower than the tyre products.
    """
)

# # rating of vendor - boxplot
fig3 = px.box(df_full,y='rating', x='vendor')
st.plotly_chart(fig3)

# # feedback from customer - spider chart/polar chart
grouped_df = df_full[['category','recommended_purchase','performance_vehicle_improve','delivery_time',
 'great_service_product_item','good_quality','excellent_customer_service',
 'fast_delivery']].replace('No Type', 0)
grouped_df = grouped_df.groupby('category',as_index=False)[['recommended_purchase','performance_vehicle_improve','delivery_time',
 'great_service_product_item','good_quality','excellent_customer_service',
 'fast_delivery']].mean()

topics = ['Recommended','Improve performance', 'Great Service/Product/Item',
          'Good Quality','Excellent Customer Service','Fast Delivery']
fig4 = go.Figure()
for idx, cat in enumerate(grouped_df.category):
    fig4.add_trace(go.Scatterpolar(
        r=list(grouped_df.iloc[idx,1:]),
        theta=topics,
        fill='toself',
        name=grouped_df.iloc[idx, 0]
    ))
fig4.update_layout(
    polar=dict(
        radialaxis=dict(visible=True, range=[0, max(grouped_df.iloc[0:,1:])])  # set range if values are normalized
    ),
    showlegend=True,
    title='Customer Feedback - Spider Chart'
)

st.plotly_chart(fig4, theme='streamlit')
