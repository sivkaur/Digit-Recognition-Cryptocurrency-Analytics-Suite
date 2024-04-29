import streamlit as st
import requests
import pandas as pd
import plotly.graph_objs as go
from requests.exceptions import HTTPError

# Set page config to wide mode for a better layout
st.set_page_config(layout="wide")

# Custom CSS
st.markdown("""
<style>
/* Set the overall background of the page */
body {
    background-color: #0E1117;
}

/* Style for the main title */
h1 {
    color: #E1E8EB;
    text-align: center;
    margin-bottom: 30px;
}

/* Streamlit container for centralized content */
.streamlit-container {
    max-width: 75%;
    margin: auto;
}

/* Custom style for dropdown menus */
select {
    color: #000;
    background-color: #F0F2F6;
    border-radius: 10px;
}

/* Custom button styles */
.stButton>button {
    color: #FFFFFF;
    background-color: #FF4B4B;
    padding: 10px 24px;
    border-radius: 25px;
    border: none;
    font-size: 16px;
    font-weight: bold;
}

/* Custom style for the selectbox */
.stSelectbox .css-2trqyj {
    background-color: #202C33;
    color: #FFF;
    border-radius: 10px;
}

/* Style for error messages */
.stAlert {
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

st.title('CryptoPulse - Coin Comparison App')

# Function to get the list of coins
def get_coins_list():
    url = "https://api.coingecko.com/api/v3/coins/list"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return {coin['name']: coin['id'] for coin in response.json()}
    except HTTPError as http_err:
        if response.status_code == 429:
            st.error("Too many requests. Please wait a while before trying again.")
            return None
        else:
            st.error(f"HTTP error occurred: {http_err}")
            return None
    except Exception as err:
        st.error(f"An unexpected error occurred: {err}")
        return None

# Function to fetch historical price data for the selected coin
def fetch_price_history(coin_id, days):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart?vs_currency=usd&days={days}&interval=daily"
    try:
        response = requests.get(url)
        response.raise_for_status()
        prices = response.json()['prices']
        df = pd.DataFrame(prices, columns=['timestamp', 'price'])
        df['date'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('date', inplace=True)
        df.drop(columns=['timestamp'], inplace=True)
        return df
    except HTTPError as http_err:
        if response.status_code == 429:
            st.error("🚦 Too much traffic at the moment. Please try again in a few minutes.")
        else:
            st.error("😕 We encountered an error retrieving the data. Please try again later.")
        return pd.DataFrame()
    except Exception as err:
        st.error("🤯 Unexpected issue occurred. We're on it!")
        return pd.DataFrame()

# Main app flow
coins_dict = get_coins_list()
if coins_dict:
    col1, col2 = st.columns(2)
    with col1:
        coin_choice1 = st.selectbox("Choose the first cryptocurrency", list(coins_dict.keys()), index=0)
    with col2:
        coin_choice2 = st.selectbox("Choose the second cryptocurrency", list(coins_dict.keys()), index=1)

    # Time frame selection
    time_frames = {'1 week': 7, '1 month': 30, '1 year': 365, '5 years': 1825}
    time_frame = st.selectbox("Select time frame for comparison", list(time_frames.keys()))

    coin_id1 = coins_dict[coin_choice1]
    coin_id2 = coins_dict[coin_choice2]
    days = time_frames[time_frame]

    df1 = fetch_price_history(coin_id1, days)
    df2 = fetch_price_history(coin_id2, days)

    if not df1.empty and not df2.empty:
        df1_normalized = df1['price'] / df1['price'].iloc[0]
        df2_normalized = df2['price'] / df2['price'].iloc[0]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df1.index, y=df1_normalized, mode='lines', name=coin_choice1))
        fig.add_trace(go.Scatter(x=df2.index, y=df2_normalized, mode='lines', name=coin_choice2))
        fig.update_layout(
            title=f'Price Comparison of {coin_choice1} vs {coin_choice2}',
            xaxis_title='Date',
            yaxis_title='Normalized Price',
            template='plotly_dark',
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False)
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("Failed to fetch data for the selected cryptocurrencies.")
