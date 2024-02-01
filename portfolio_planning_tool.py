import yfinance as yf
import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
import time

#a dictionary mapping stock tickers (strings) to investment values (double)
global portfolio
portfolio = {}

#create the GUI window
root = tk.Tk()
root.geometry('1000x1000')
root.title("Niti's Portfolio Planning Tool")
root.resizable(width=1,height=1)

#headings
tk.Label(root, text="Niti's Portfolio Planning Tool", font='arial 30 bold').pack()
tk.Label(root, text="Add Stock To Portfolio", font='arial 20 bold').pack()

investments = tk.StringVar()
stock_ticker_var = tk.StringVar()
investment_value_var = tk.DoubleVar()


def update_portfolio():
    global portfolio
    stock_ticker = stock_ticker_var.get().upper()
    investment = investment_value_var.get()
    portfolio.update({stock_ticker: investment})
    portfolio_text = ''.join(f"{key} --- {portfolio[key]}\n" for key in portfolio.keys())
    investments.set(portfolio_text)
    text_widget.delete(1.0, tk.END)  # Clear existing content
    text_widget.insert(tk.END, investments.get())  # Insert new content


tk.Label(root, text="Enter Stock Ticker: ", font='arial 15 bold').pack()
tk.Entry(root, font='arial 15',textvariable=stock_ticker_var).pack()
tk.Label(root, text="Enter Investment ($): ", font='arial 15 bold').pack()
tk.Entry(root, font='arial 15', textvariable=investment_value_var).pack()
tk.Button(root, font='arial 20 bold', text="Add To Portfolio", command=update_portfolio).pack()

text_widget = tk.Text(root, height=10, width=40)
text_widget.pack()


def calculate(showGraph = False):
    plt.clf()
    # the beta value is the 5Y monthly beta value from Yahoo Finance
    total_investment=0.0

    # Calculate Total Investment
    for key in portfolio.keys():
        total_investment += (portfolio[key])

    getInfoText = f"Portfolio Value = ${total_investment}"

    # A DataFrame whose columns contain the Closing Price
    # of each stock in the portfolio over the last month
    portfolio_month_history = pd.DataFrame()

    # Calculate Beta: Summation of each stock's beta multiplied by the portfolio weight
    running_beta = 0.0
    for ticker in portfolio.keys():
        running_beta += (yf.Ticker(ticker).info["beta"]*(portfolio[ticker]/total_investment))

    getInfoText += f"\nPortfolio Beta = {round(running_beta, 3)}"
    getInfoText+="\n\nNumber of Shares at Current Market Price:"

    for key in portfolio.keys():
        hist = yf.Ticker(key).history(period='1mo')

        # Get number of stocks bought
        currentPrice = yf.Ticker(key).info['currentPrice']
        numShares = portfolio[key]/currentPrice

        print(hist['Close'])
        getInfoText+=(f"\n{key}: {round(numShares, 3)} Shares")

        #Scale the Close Price column by number of shares
        hist['Close'] = hist['Close'].apply(lambda x: x * numShares)
        portfolio_month_history[f'Close{key}'] = hist['Close']

    info_text.delete(1.0, tk.END)  # Clear existing content
    info_text.insert(tk.END, getInfoText)  # Insert new content

    if showGraph:
        # Graph

        firstColumn = True
        for column in portfolio_month_history.columns:
            if firstColumn:
                portfolio_month_history['Close_PortfolioSum'] = portfolio_month_history[column]
                firstColumn = False
            else:
                portfolio_month_history['Close_PortfolioSum'] \
                    = (portfolio_month_history['Close_PortfolioSum']
                       + portfolio_month_history[column])

        print(portfolio_month_history)

        plt.plot(portfolio_month_history['Close_PortfolioSum'])
        plt.title("Portfolio 1 Month History")
        plt.xlabel('Date') # from before
        plt.ylabel('Closing Price') #from before
        plt.show()


tk.Button(root, font='arial 20 bold', text="Get Portfolio Info", command = calculate).pack()
info_text = tk.Text(root, height=10, width=50)
info_text.pack()
tk.Button(root, font='arial 20 bold', text="View Past Performance", command = lambda:calculate(showGraph = True)).pack()


root.mainloop()

# name = input("Enter Stock Ticker: ")
# ticker = yf.Ticker(name).info
# #print(ticker) #print what info yahoo finance can give me
# market_price = ticker['currentPrice']
# previous_close_price = ticker['regularMarketPreviousClose']
# print(f'Ticker: {name.upper()}')
# print('Market Price:', market_price)
# print('Previous Close Price:', previous_close_price)


#Ideas:
#can do NLP on ticker['longBusinessSummary']
#can do ticker['beta']
# can do 'trailingPE' and 'forwardPE'
#Maybe can do a program where you enter your portfolio
#stocks and investments
#and it calculates portfolio beta