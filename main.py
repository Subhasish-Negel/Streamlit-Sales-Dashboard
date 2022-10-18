import pandas as pd  # pip install pandas openpyxl
import streamlit as st  # pip install streamlit
import plotly.express as px  # pip install plotly-express

st.set_page_config(page_title='Sales Dashboard', page_icon='📊', layout='wide')


# Read Excel File
@st.cache
def get_data_from_excel():
    dframe = pd.read_excel(io='supermarket_sales.xlsx',
                           sheet_name='Sales',
                           skiprows=3,
                           usecols='B:R',
                           nrows=1000)
    # Getting the Hour Column in the DataFrame
    dframe['Hour'] = pd.to_datetime(dframe['Time'], format='%H:%M:%S').dt.hour
    return dframe


df = get_data_from_excel()

st.sidebar.header('Select Filters Here:')
city = st.sidebar.multiselect(
    'Select Your City:',
    options=df['City'].unique(),
    default=df['City'].unique()
)

customer_type = st.sidebar.multiselect(
    'Select Customer Type:',
    options=df['Customer_type'].unique(),
    default=df['Customer_type'].unique()
)
gender = st.sidebar.multiselect(
    'Select Gender',
    options=df['Gender'].unique(),
    default=df['Gender'].unique()
)

df_selection = df.query(
    'City == @city & Customer_type == @customer_type & Gender == @gender'
)

# Main_page

st.title('📊 Sales Insights')
st.markdown('##')
st.markdown('##')

# KPIs

total_sales = round(df_selection['Total'].sum(), 2)
average_ratings = round(df_selection['Rating'].mean(), 1)
rating_star = '⭐' * int(round(average_ratings, 0))
average_sale_per_transaction = round(df_selection['Total'].mean(), 2)

# making columns for alignment

left_column, middle_column, right_column = st.columns(3)

with left_column:
    st.subheader('Total Sales:')
    st.subheader(f'US $ {total_sales:,}')

with middle_column:
    st.subheader('Average Rating:')
    st.subheader(f'{rating_star}{average_ratings}')

with right_column:
    st.subheader('Average Sale per Transaction:')
    st.subheader(f'US $ {average_sale_per_transaction}')

# separating section with a line
st.markdown('---')

# Sales by Product Line

sales_by_product_line = df_selection.groupby(by=['Product line']).sum()[['Total']].sort_values(by='Total')

# Creating the figure
product_sale_figure = px.bar(sales_by_product_line,
                             x='Total',
                             y=sales_by_product_line.index,
                             orientation='h',
                             title='<b>Sales by Product Line</b>',
                             color_discrete_sequence=['#804CF9'] * len(sales_by_product_line),
                             template='simple_white')

# Figure layout Update

product_sale_figure.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(showgrid=False)
)

# Sales by Time(Hour)

sales_by_hour = df_selection.groupby(by=['Hour']).sum()[['Total']]

# Creating the Figure
sale_figure_byHour = px.bar(sales_by_hour,
                            y='Total',
                            x=sales_by_hour.index,
                            orientation='v',
                            title='<b>Sales by Hour</b>',
                            color_discrete_sequence=['#d24f70'] * len(sales_by_hour),
                            template='simple_white')

# Figure layout Update

sale_figure_byHour.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(tickmode='linear'),
    yaxis=dict(showgrid=False)
)

# Separating the charts by Column

col_1, col_2 = st.columns(2)

col_1.plotly_chart(sale_figure_byHour, use_container_width=True)
col_2.plotly_chart(product_sale_figure, use_container_width=True)
