# Cryptocurrency Analytics and Image Classification Suite

This repository contains a suite of applications developed to provide insights into cryptocurrency trends and an image classification tool for digit recognition.

## Contents
1. [StockDetailsApp.py](#stockdetailsapppy) - Cryptocurrency details viewer.
2. [CoinComparisonApp.py](#coincomparisonapppy) - Comparative analysis of cryptocurrencies.
3. [Classifier.py & ImageClassifier.py](#classifierpy--imageclassifierpy) - Image classification for digit recognition.

### StockDetailsApp.py
This Streamlit application leverages the CoinGecko API to allow users to view detailed information about cryptocurrencies. Users can search for a cryptocurrency (e.g., Bitcoin, Ethereum) to see its price trend over the last year, including maximum and minimum prices and the dates on which these occurred.

#### Features
- Fetch cryptocurrency data using: https://api.coingecko.com/api/v3/coins/list
- Plot the price trend over the last year.
- Display the maximum and minimum trading prices and their respective dates.

### CoinComparisonApp.py
A Streamlit application that extends the functionalities of `StockDetailsApp.py` by allowing users to compare the price performance of two selected cryptocurrencies over specified time frames (1 week, 1 month, 1 year, 5 years).

#### Features
- Compare two cryptocurrencies.
- Interactive graphs showing price performance over user-selected time frames.

### Classifier.py & ImageClassifier.py
These scripts are part of an image classification application built using Streamlit, capable of recognizing digits from 0 to 9.

#### Classifier.py
Trains a classifier using a predefined model (details on saving and loading the model are available at https://keras.io/api/models/model_saving_apis/).

#### ImageClassifier.py
A Streamlit application that allows users to upload an image of a digit, which is then classified by the trained model.

#### Features
- Users can upload square images of digits for classification.
- The application handles resizing and classification of the images.
- Image data for training can be found at: http://bit.ly/smu-files-2

## Usage
To run each app, navigate to the app's directory and execute the following command:
```bash
streamlit run <filename.py>
```

# Streamlit App Urls
- StockDetailsApp: https://pythonassignment-stockdetailsapp.streamlit.app/
- CoinComparisonApp: https://pythonassignment-coincomparisonapp.streamlit.app/
- Classifier: https://pythonassignment-imageclassifier.streamlit.app/
