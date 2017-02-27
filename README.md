   SuperSimpleStocks
=======================
Code assessment task for JP Morgan recruitment process.

# Problem
Provide working source code that will :
+ For a given stock,
    - Given a market price as input, calculate the dividend yield.
    - Given a market price as input,  calculate the P/E Ratio.
    - Record a trade, with timestamp, quantity of shares, buy or sell indicator and trade price.
    - Calculate Volume Weighted Stock Price based on trades in past 15 minutes.
+ Calculate the GBCE All Share Index using the geometric mean of prices for all stocks.

# Requirements
+ The code has been tested on Python 2.7.10 and Python 3.6.0.
+ The mock library is required for Python 2.

# Assumptions made
The following assumptions have been made:
+ To calculate the Price-Earnings ratio, the dividend yield is used in the formula.
+ If the dividend yield is zero, the Price-Earnings ratio returns zero.
+ To calculate the All Shares Index, the stock price used is the stock Volume Weighted Price calculated over the last 15 minutes.

# How to use
+ The unit tests can be run by running:
    ```
    python test_supersimplestocks.py
    ```
+ The main program using GBCE sample data can be run by running:
    ```
    python supersimplestocks.py
    ```
