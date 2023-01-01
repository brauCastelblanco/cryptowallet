# importing the libraries
import pandas as pd
import streamlit as st
import datetime
from datetime import date
import dateutil.relativedelta
import plotly.express as px
import plotly.graph_objects as go
pd.set_option('display.float_format', '{:.11f}'.format)


currencies = pd.read_csv("currencies.csv")
raw_balance = pd.read_csv("balance.csv")
transactions_history = pd.read_csv("transactions_history.csv")
with open("readme.md") as f:
    readme = f.read()
currencies['timestamp'] = pd.to_datetime(currencies['timestamp'],format='%Y-%m-%d')
currencies['month'] = currencies['timestamp'].dt.strftime('%Y-%m')
today = datetime.datetime(2022,12,31)
last_month = (datetime.datetime(2022,12,31) + dateutil.relativedelta.relativedelta(months=-1)).strftime('%Y-%m')

#calculating my cryptowallet balance
current_month_prices = currencies[currencies['month']== today.strftime('%Y-%m')].groupby(['from_currency']).mean()
current_month_prices.reset_index(inplace=True)
current_month_prices.rename(columns={'from_currency':'currency'},inplace=True)
balance = pd.merge(raw_balance, current_month_prices[['currency','close']], on='currency',how='left')
balance['balance_usd'] = balance.available * balance.close
balance.fillna(0,inplace=True)
own_crypto_list = balance['currency'].to_list()



#STREAMLIT
st.title('My Cryptocurrency Portfolio Dashboard')
with st.expander('read.me'):
    st.markdown(readme)

#TABS
tab1, tab2 = st.tabs(['Portfolio Dashboard','Exchange Rates'])
with tab1:
    #PORTFOLIO SECTION
    options = st.multiselect(label='Choose the cryptos from your portfolio:',
        options=own_crypto_list,default=own_crypto_list,)

    #Creating dataset for portfolio evolution
    portfolio = currencies[currencies['from_currency'].isin(options)].join(
        raw_balance.set_index(['currency']),how='left',on=['from_currency'])
    portfolio['amount_usd'] = portfolio['close'] * portfolio['available']
    portfolio_evolution = portfolio.groupby('timestamp')['amount_usd'].sum()
    portfolio_evolution = portfolio_evolution.to_frame()
    portfolio_evolution.reset_index(inplace=True)
    portfolio_evolution['day'] = portfolio_evolution['timestamp'].dt.strftime('%Y-%m-%d')
    def past_value(month):
        past_value = round(portfolio_evolution[portfolio_evolution['day'] == pd.to_datetime((datetime.datetime(2022,12,31) + dateutil.relativedelta.relativedelta(months=month))).strftime('%Y-%m-%d')].amount_usd.values[0],3)
        return past_value
    current_value = round(portfolio_evolution.iloc[-1:, 1].values[0],3)

    #PLOTTING
    st.subheader('Current Portfolio Evolution')
    col4portfolio, col1_portfolio, col2_portfolio, col3_portfolio = st.columns(4)
    col4portfolio.metric('Current Value', current_value)
    col1_portfolio.metric(label='Value 1 month ago',
        value=past_value(-1),
        delta=round((current_value - past_value(-1))/past_value(-1),3))
    col2_portfolio.metric(label='Value 3 months ago',
        value=past_value(-3),
        delta=round((current_value - past_value(-3))/past_value(-3),3))
    col3_portfolio.metric(label='Value 6 months ago',
        value=past_value(-6),
        delta=round((current_value - past_value(-6))/past_value(-6),3))
    st.line_chart(portfolio_evolution,x='timestamp',y='amount_usd')
    fig_current_balance = px.bar(balance[balance['currency'].isin(options)],x='balance_usd',y='currency', orientation='h',color='currency')
    fig_current_balance.update_layout(barmode='stack', yaxis={'categoryorder':'total ascending'}, showlegend=False)
    st.subheader('Portfolio Composition')
    with st.expander('See the Details'):
        st.dataframe(balance)
    st.plotly_chart(fig_current_balance,use_container_width=True)
    st.text('You can also see your Transactions')
    with st.expander('Transactions'):
        st.dataframe(transactions_history)


    




with tab2:
    #CRYPTOCURRENCY EVOLUTION
    select_item = st.selectbox(
        "Choose a crypto",
        own_crypto_list)


    # CALCULATING AND CREATING THE BULLET POINTS
    query = "from_currency == '" + select_item + "' and month == '"+today.strftime('%Y-%m') +"' "
    query_last_month = "from_currency == '" + select_item + "' and month == '"+last_month+"' "
    mean_month = currencies.query(query)['close'].mean()
    mean_last_month = currencies.query(query_last_month)['close'].mean()
    max_month = currencies.query(query)['max'].max()
    max_last_month = currencies.query(query_last_month)['max'].max()
    min_month = currencies.query(query)['min'].min()
    min_last_month = currencies.query(query_last_month)['min'].min()
    col1, col2, col3 = st.columns(3)
    col1.metric(
        label='Current month price',
        value= round(mean_month),
        delta = round((mean_month - mean_last_month)/mean_last_month,4))
    col2.metric(
        label='Max price current month',
        value= round(max_month),
        delta = round((max_month - max_last_month)/max_last_month,4))
    col3.metric(
        label='Min price current month',
        value= round(min_month),
        delta = round((min_month - min_last_month)/min_last_month,4))
    mycryptos = currencies[currencies['from_currency'].isin([select_item])]
    fig_candle = go.Figure(data=[go.Candlestick(x= currencies[currencies['from_currency'].isin([select_item])].timestamp,
        open=currencies[currencies['from_currency'].isin([select_item])].open,
        high=currencies[currencies['from_currency'].isin([select_item])]['max'],
        low=currencies[currencies['from_currency'].isin([select_item])]['min'],
        close=currencies[currencies['from_currency'].isin([select_item])].close)])
    st.plotly_chart(fig_candle,use_container_width=True)
