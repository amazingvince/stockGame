from random import shuffle, uniform, gauss, random

class Game():
    def __init__(self, startMoney, numStocks, numWeeks , stockNames):
        self.stockMarket = self.StockMarket(stockNames,numStocks)
        self.player = self.Player(startMoney, self.stockMarket.stockNames)
        self.numWeeks = numWeeks
        self.week = 1

    def start(self):
        print "Welcome to the stock simulator game"
        print "You selected to play {} weeks".format(self.numWeeks)
        print ""
        self.stockMarket.printCurrentWeek()
        while True:
            print "Would you like to buy any stock? Y or N"
            response = raw_input("> ")
            if response.upper() == "Y":
                self.buyStocks()
                break
            if response.upper() == "N":
                break

    def end(self):
        self.stockMarket.nextWeek()
        self.stockMarket.printMarketHistory()
        for name in self.player.portfolio:
            self.player.sell(name, self.player.portfolio[name], self.stockMarket)
        print ""
        print "After selling your stocks. You have $ {0:.2f}".format(self.player.cash)

    def play(self):
        self.start()
        while self.week <= self.numWeeks:
            print ""
            self.stockMarket.nextWeek()
            self.stockMarket.printCurrentWeek()
            self.sellStocks()
            self.buyStocks()
            self.week += 1
        print ""
        self.end()

    def buyStocks(self):
        while True:
            print "Type the name of the stock you would like to buy. If you are finished type DONE"
            name = raw_input("> ")
            name = name.upper()
            if name == "DONE":
                break
            name = name.lower()
            if name in self.stockNames:
                print "How many shares would you like?"
                numShares = int(raw_input("> "))
                print self.player.buy(name, numShares, self.stockMarket)
            else:
                print "Sorry stock name not found."

    def sellStocks(self):
        self.player.printPortfolio()
        while True:
            print "Type the name of the stock you would like to sell. If you are finished type DONE"
            name = raw_input("> ")
            if name == "DONE":
                break
            name = name.lower()
            if name in self.stockNames:
                print "How many shares would you like to sell?"
                numShares = int(raw_input("> "))
                print self.player.sell(name, numShares, self.stockMarket)
            else:
                print "Sorry stock name not found."


    class Player(object):
        def __init__(self, startMoney, stockNames):
            self.cash = startMoney
            self.portfolio = {}
            for name in stockNames:
                self.portfolio[name] = 0

        def printPortfolio(self):
            for stock in self.portfolio:
                print "{}: {}".format(stock, self.portfolio[stock])
            print ""
        
        def buy(self, name, numShares, stockMarket):
            price = stockMarket.market[name].price
            cost = price * numShares
            if self.cash < cost:
                return "Not enough cash! \n"
            else:
                self.cash -= cost
                self.portfolio[name] += numShares
                cash = "{0:.2f}".format(self.cash)
                cost = "{0:.2f}".format(cost)
                return "You bought {} shares of {} stock for {}. \nYou now have $ {} left. \n".format(numShares, name, cost, cash)

        def sell(self, name, numShares, stockMarket):
            price = stockMarket.market[name].price
            if self.portfolio[name] < numShares:
                return "You do not have enough stock! \n"
            else:
                self.portfolio[name] -= numShares
                profit = price * numShares
                self.cash += profit
                cash = "{0:.2f}".format(self.cash)
                profit = "{0:.2f}".format(profit)
                return "You sold {} shares of {} stock for {}. \nYou now have $ {}. \n".format(numShares, name, profit, cash)


    class StockMarket(object):

        def __init__(self, stockNames, numStocks):
            shuffle(stockNames)
            self.stockNames = stockNames[:numStocks]
            self.market = {}
            self.week = 1
            for stockName in self.stockNames:
                stock = self.Stock(stockName)
                self.market[stockName] = stock 
        
        def printCurrentWeek(self):
            marketHistory = self.marketHistory()
            week = "Week {}".format(self.week - 1)
            print week
            for name in self.stockNames:
                price = "{0:.2f}".format(marketHistory[name][week])
                print "{}  $ {}".format(name, price)
            print ""

        def nextWeek(self):            
            for name in self.market:
                self.market[name].nextWeek(self.week)
            self.week += 1

        def stockHistory(self, name):
            stock = self.market[name]
            return stock.history

        def marketHistory(self):
            marketHistory = {}
            for name in self.stockNames:
                marketHistory[name] = self.stockHistory(name)
            return marketHistory

        def printMarketHistory(self):
            marketHistory = self.marketHistory()
            for name in self.stockNames:
                print name
                for week in range(len(marketHistory[name])):
                    week = "Week {}".format(week)
                    price = "{0:.2f}".format(marketHistory[name][week])
                    print "{}  $ {}".format(week, price)
                print ""
                
        
        class Stock(object):
        
            def __init__(self, name):
                self.name = name
                self.minPrice = 20
                self.maxPrice = 100
                self.mu = 0
                self.price = next(self.gen_price())
                self.history = {'Week 0': self.price}

            def nextWeek(self, weeknum):
                self.price = next(self.gen_price())
                week = 'Week {}'.format(weeknum)
                self.history[week] = self.price


            def gen_price(self):
                price= uniform(self.minPrice, self.maxPrice)
                yield price
                
                while True:
                    price += gauss(self.mu, gauss(0, price/4))
                    if price <=0:
                        break 
                    yield price
                    
                while True:
                    yield 0


def main():
    print "For this game of guessing the stock market,"
    startMoney = int(raw_input("How much money would you like to start with? $")) 
    numStocks = int(raw_input("How many stocks would you like there to be? > "))
    numWeeks = int(raw_input("How many weeks would you like to play?? > "))
    print ""

    stockNames = ['apple','bookface', 'softmicro', 'bluebull', 'pokemon', 'tinder', 'oogle', 
                    'askjeeves', 'spotify', 'wire', 'hbo', 'troll', 'wish', 'zippy']

    stockGame = Game(startMoney, numStocks, numWeeks , stockNames) 
    stockGame.play()


if __name__ == '__main__':
    main()


