
from datetime import date
from service import download_stock, git_update
from stock import upload

class Stock:
    def __init__(self, name, id):
        self.id = id
        self.name = name

        today = date.today()
        today = str(today)
        date_info = today.split("-")
        date_info[0] = str(int(date_info[0]) - 1)
        start_date = ""
        for i in range(len(date_info)):
            if i == len(date_info) - 1:
                today += date_info[i]
            else:
                today += date_info[i] + "-"
        
        csv, i = download_stock(self.id, start_date)
        self.data = upload(csv, 1, True)

        self.last_timeseries = None
        self.close_price = self.data[len(self.data) - 1]
        self.percentage = 0.00
        self.shares = 0
    def set_rebalance_info(self, percentage, shares):
        self.percentage = percentage
        self.shares = shares
    def stock_id(self):
        return self.id
    def stock_percentage(self):
        return self.percentage

class Portfolio:
    def __init__(self, stocks=None, percentage=None, shares=None, d2_asset=0.00):
        self.d2_asset = d2_asset
        self.stocks = stocks
        if self.stocks != None:
            for i in range(len(stocks)):
                stocks[i].set_rebalance_info(percentages[i], shares[i])
    def create_portfolio(self, portfolio_name):
        etf_stock_list = open(portfolio_name + "_etf_stock_list.txt", "w+")
        etf_stock_balance = open(portfolio_name + "_etf_balance.txt", "w+")
        for i in range(len(stocks)):
            etf_stock_list.write(stocks[i].stock_id() + ",")
            etf_stock_balance.write(str(stocks[i].stock_percentage()) + ",")
        etf_stock_balance.write(str(self.d2_asset))
        etf_stock_list.close()
        etf_stock_balance.close()
    def load(self, portfolio_name):
        self.d2_asset, self.stocks = 0, []
        # read stock list, balance (i.e., percentages), shares, and assets
        try:
            etf_stock_list = open(portfolio_name + "_etf_stock_list.txt", "r")
            etf_stock_balance = open(portfolio_name + "_etf_balance.txt", "r")
            stock_list = etf_stock_list.read().split(",")
            stock_balance = etf_stock_balance.read().split(",")
            for i in range(len(stock_list) - 1):
                self.stocks.append(Stock(stock_list[i], stock_list[i]))
                self.stocks[len(self.stocks) - 1].set_rebalance_info(int(stock_balance[i]))
            self.d2_asset = int(stock_balance[len(stock_balance) - 1])
        except IOError:
            print("Cannot find ETF info named, '{}'" .format(portfolio_name))

# create ETF portfolio using this module
if __name__ == "__main__":
    latin = Stock('TIGER Latin 35', '105010.KS')
    government_bond3 = Stock('Government Bond 3 Years', '114260.KS')
    gold = Stock('Gold', '132030.KS')
    s_and_p = Stock('S&P 500', '^gspc')
    government_bond10 = Stock('Government Bond 3 Years', '148070.KS')
    china_a50 = Stock("KODEX China A50", '169950.KS')
    vietnam_vn30 = Stock("KINDEX Vietnam VN30", '279540.KS')
    russia_msci = Stock("Russias MSCI", '265690.KS')
    volatility = Stock("KODEX Volatility", '279540.KS')
    usa_bond30 = Stock('USA Bond 30 years', '304660.KS')
    battery = Stock("TIGER Secondary Battery", '305540.KS')
    ultra_government_bond = Stock("HANARO KAP Government Bond", '346000.KS')

    stocks = [china_a50, vietnam_vn30, volatility, battery, s_and_p, latin, russia_msci, usa_bond30, ultra_government_bond, government_bond10, government_bond3]
    percentages = [8, 8, 8, 8, 8, 4, 2, 2, 12, 12, 16, 10]
    shares = [72, 46, 65, 95, 100, 12, 30, 7, 94, 23, 13, 18]

    etf = Portfolio(stocks, percentages, shares, 429121)
    etf.create_portfolio("junyoung")
    git_update()