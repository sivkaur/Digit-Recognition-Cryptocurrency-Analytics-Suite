import streamlit as st
import requests
import pandas as pd

# Custom CSS
st.markdown("""
    <style>
    body {
        background-image: url("https://cdn.pixabay.com/photo/2016/11/10/05/09/bitcoin-1813503_1280.jpg");
        background-size: cover;
    }
    .reportview-container .main .block-container {
        padding-top: 5rem;
        padding-bottom: 5rem;
    }
    .reportview-container .main {
        color: #ffffff;
        background-color: transparent;
    }
    .error-message {
        color: red;
        font-weight: bold;
    }
    .big-font {
        font-size:20px !important;
        font-weight: bold !important;
    }
    .stSelectbox .css-2trqyj {
        background-color: rgba(255, 255, 255, 0.8);
    }
    .stButton>button {
        border: 2px solid #4CAF50;
        color: white;
        background-color: #4CAF50;
        padding: 10px 24px;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: white;
        color: #4CAF50;
    }
    .st-bd {
        border: 2px solid #4CAF50;
    }
    </style>
""", unsafe_allow_html=True)

st.title('CryptoPulse - The Heartbeat of Cryptocurrency')

# Display the error
def show_error_message(message):
    st.markdown(f'<p class="error-message">{message}</p>', unsafe_allow_html=True)

# Function to get the list of coins
def get_coins_list():
    url = "https://api.coingecko.com/api/v3/coins/list"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises HTTPError if the response code was unsuccessful
        return {coin['name']: coin['id'] for coin in response.json()}
    except requests.exceptions.HTTPError as http_err:
        if http_err.response.status_code == 429:
            show_error_message("Rate limit exceeded. Please try again later.")
        else:
            show_error_message(f"HTTP error occurred: {http_err}. Please check the CoinGecko API status.")
        return {}
    except Exception as err:
        show_error_message(f"An error occurred: {err}")
        return {}

#Function to fetch historical price data for the selected coin
def fetch_price_history(coin_id):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart?vs_currency=usd&days=365"
    try:
        response = requests.get(url)
        response.raise_for_status()
        prices = response.json()['prices']
        df = pd.DataFrame(prices, columns=['timestamp', 'price'])
        df['date'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df
    except requests.exceptions.HTTPError as http_err:
        if http_err.response.status_code == 429:
            show_error_message("Rate limit exceeded. Please try again later.")
        else:
            show_error_message(f"HTTP error occurred when fetching data for {coin_choice}: {http_err}")
        return pd.DataFrame()
    except Exception as err:
        show_error_message(f"An unexpected error occurred when fetching data for {coin_choice}: {err}")
        return pd.DataFrame()

try:
    coins_dict = get_coins_list()
    if coins_dict:
        coin_choice = st.selectbox("Choose a cryptocurrency", list(coins_dict.keys()), index=0)
        if st.button('Show Details'):
            df = fetch_price_history(coins_dict[coin_choice])
            if not df.empty:
                st.line_chart(df.set_index('date')['price'])
                max_price = df['price'].max()
                min_price = df['price'].min()
                max_date = df[df['price'] == max_price]['date'].dt.strftime('%Y-%m-%d').iloc[0]
                min_date = df[df['price'] == min_price]['date'].dt.strftime('%Y-%m-%d').iloc[0]
                st.markdown(f"**Maximum price** of {coin_choice} was ${max_price:.10f} on {max_date}")
                st.markdown(f"**Minimum price** of {coin_choice} was ${min_price:.10f} on {min_date}")
            else:
                show_error_message("Failed to display the cryptocurrency data.")
except Exception as err:
    show_error_message(f"An unexpected error occurred: {err}")
