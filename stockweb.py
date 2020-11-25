#import necessary libraries

import streamlit as st
import pandas as pd
from PIL import Image


#Add title and an image

st.title("Stock Market Web Application: AMZN/TSLA/GOOG")

# open the image
image = Image.open("Bull-and-Stock-Market-iStock.jpg")
st.image(image, use_column_width=True)

# Create a sidebar header
st.sidebar.header('User Input')

#Create a function to get the user input
def get_input():
    start_date = st.sidebar.text_input("Start Date", "2019-11-25")
    end_date = st.sidebar.text_input("end Date", "2020-11-23")
    stock_symbol = st.sidebar.text_input("stock symbol", "AMZN")
    return start_date, end_date, stock_symbol

#Create a function to get the company name
def get_company_name(symbol):
    if symbol == 'AMZN':
        return 'Amazon'
    elif symbol == 'TSLA':
        return 'Tesla'
    elif symbol == 'GOOG':
        return 'Alphabet'
    else:
        'None'
        
#Create a function to get the proper company data and the proper timeframe from the user start and end time 
def get_data(symbol, start, end):

    # load the  data
    if symbol.upper() == 'AMZN':
        df = pd.read_csv("AMZN.csv")
    elif symbol.upper() == 'TSLA':
        df = pd.read_csv("TSLA.csv")
    elif symbol.upper() == 'GOOG':
        df = pd.read_csv("GOOG.csv")
    else:
        df = pd.DataFrame(columns = ['Date','Open','High','Low','Close','Adj Close', 'Volume'])

    #get the date range
    start = pd.to_datetime(start)
    end = pd.to_datetime(end)

    #  set the  start and end index to both 0
    start_row = 0
    end_row = 0

    # start looking at the date from the top of the data set and go down to see if the users start date less than  or equal to the  date  of the dataset
    for i in range(0,len(df)):
        if start <= pd.to_datetime(df['Date'][i]):
            start_row = i
            break
    # start looking at the date from the   bottom of the dataset and go up to see if the  user  end date is  greater than or equal to date in the  dataset
    for j in range(0,len(df)):
        if end >= pd.to_datetime(df['Date'][len(df)-1-j]):
            end_row = len(df) -1 -j
            break
    # set the  index to be the date
    df = df.set_index(pd.DatetimeIndex(df['Date'].values))

    return df.iloc[start_row:end_row +1, :]

# get the users input

start, end, symbol = get_input()

# get the data 
df = get_data(symbol, start, end)

# get the company  name
company_name = get_company_name(symbol.upper())

# display the close price
st.header(company_name + " Close\n")
st.line_chart(df['Close'])

# display the Adj  Close
st.header(company_name + "Volume\n")
st.line_chart(df['Volume'])

# display statistics on the  data

st.header('Data Statistics')
st.write(df.describe())
