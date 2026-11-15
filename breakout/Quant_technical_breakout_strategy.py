
#necessary packages
import yfinance as yf   #yahoo finance package
import pandas as pd      #package to work with tables
import os               #package to work with folders
import numpy as np    #package to work with arrays/maths

#create data folder
folder = os.path.dirname(os.path.abspath(__file__)) #find out where breakout folder is located
data_folder = os.path.join(folder, "data")   #define the path for the data folder as the same of breakout
os.makedirs(data_folder, exist_ok=True)   #create the data folder (whenever it is not created)

#download data
start_date = "2000-01-01"  #define the start date for the data
end_date = "2026-11-14"
index = "^GSPC"  
df= yf.download(index, start=start_date, end=end_date)  #download the data from yahoo finance


# check whether the data is correctly downloaded
print(df.head()) #print the first 5 rows of the dataframe
print(df.tail()) #shows the last 5 rows of the dataframe
print(df.columns) # shows the names for the collumns of the dataframe

 #put the data on the folder
df.to_csv(os.path.join(data_folder, "gspc.csv"))


#adding collumns for dayly returns, and Donchian Channel
df["Daily Return"] = df["Close"].pct_change() #calculate the daily return and add it to the dataframe
print(df.head()) #print the first 5 rows of the dataframe to check the daily return is correctly calculated

N = 20  
df["Up"] = df["High"].rolling(N).max()  #calculate the rolling high for the last N days and add it to the dataframe
df["Down"] = df["Low"].rolling(N).min()

df["Up"]= df["Up"].shift(1) #shifts the collumn down by one so we don't backtest with future data.
df["Down"]= df["Down"].shift(1)



#defining the trading strategy
def strategy (df, date, current):
    if df.loc[date,"Close"] > df.loc[date,"Up"]:
        return 1
    if df.loc[date,"Close"] < df.loc[date,"Down"]:
        return 0
    else:
        return current


#constructing the signal collumn
signal=0
df["Signal"]=0
for i in df.index:   #loop that defines the signal for each day
    df.loc[i,"Signal"]=strategy(df, i, signal)
    signal=df.loc[i,"Signal"]


