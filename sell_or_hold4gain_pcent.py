#!/usr/bin/python3
#mbpatil

'''
[root@mbpatil stocks]# ./sell_or_hold4gain_pcent.py -h
usage: sell_or_hold4gain_pcent.py [-h] [-c CAPITAL] [-t TAXRATE_PCENT]
                                  [-g GAIN_PCENT] [-v] [-hs] [-r] [-f] [-m]
                                  [-o OUTFILE]

sell or hold your stocks

optional arguments:
  -h, --help            show this help message and exit
  -c CAPITAL, --capital CAPITAL
                        capital amount
  -t TAXRATE_PCENT, --taxrate_pcent TAXRATE_PCENT
                        taxrate percent amount
  -g GAIN_PCENT, --gain_pcent GAIN_PCENT
                        current stock gain percent amount
  -v, --verbose         dump values before plotting
  -hs, --hold_sell      include hold and sell when stock is down in verbose
                        mode
  -r, --reverse         exchange x and y axis in plot. Applicable to plotext
                        only
  -f, --full            do not restrict plotsize. Applicable to plotext only
  -m, --matplotlib      plot using matplotlib. Useful in gui env
  -o OUTFILE, --outfile OUTFILE
                        save matplotlib plot as svg file

[root@mbpatil stocks]# ./sell_or_hold4gain_pcent.py -v | head
capital=100.00 taxrate%=25.00 down%=1.00 gain%=25.00 sell=118.75 hold=123.75 HOLD [5.00]
capital=100.00 taxrate%=25.00 down%=2.00 gain%=25.00 sell=118.75 hold=122.50 HOLD [3.75]
capital=100.00 taxrate%=25.00 down%=3.00 gain%=25.00 sell=118.75 hold=121.25 HOLD [2.50]
capital=100.00 taxrate%=25.00 down%=4.00 gain%=25.00 sell=118.75 hold=120.00 HOLD [1.25]
capital=100.00 taxrate%=25.00 down%=5.00 gain%=25.00 sell=118.75 hold=118.75 SELL [0.00]
capital=100.00 taxrate%=25.00 down%=6.00 gain%=25.00 sell=118.75 hold=117.50 SELL [1.25]
capital=100.00 taxrate%=25.00 down%=7.00 gain%=25.00 sell=118.75 hold=116.25 SELL [2.50]
capital=100.00 taxrate%=25.00 down%=8.00 gain%=25.00 sell=118.75 hold=115.00 SELL [3.75]
capital=100.00 taxrate%=25.00 down%=9.00 gain%=25.00 sell=118.75 hold=113.75 SELL [5.00]
capital=100.00 taxrate%=25.00 down%=10.00 gain%=25.00 sell=118.75 hold=112.50 SELL [6.25]

Explaination:
capital=100.00 taxrate%=25.00 down%=5.00 gain%=25.00 sell=118.75 hold=118.75 SELL [0.00]
with capital of 100 and effective tax rate of 25, a 25% gain is equivalent to stock losing its value by 5%.
If stock looses >= 5%, it is better to SELL right now and pay 25% taxes
If stock looses < 5%, it is better to HOLD on to your stocks and not pay 25% taxes on it.
Assumption here is that, if you HOLD until your growth offsets the taxes or you no longer pay taxes.
'''

import argparse

parser = argparse.ArgumentParser(description='sell or hold  your stocks')
parser.add_argument('-c', '--capital', help='capital amount', type=float, default=100)
parser.add_argument('-t', '--taxrate_pcent', help='taxrate percent amount', type=float, default=25)
parser.add_argument('-g', '--gain_pcent', help='current stock gain percent amount', type=float, default=25)
parser.add_argument('-v', '--verbose', help='dump values before plotting', action="store_true")
parser.add_argument('-hs', '--hold_sell', help='include hold and sell when stock is down in verbose mode', action="store_true")
parser.add_argument('-r', '--reverse', help='exchange x and y axis in plot. Applicable to plotext only', action="store_true")
parser.add_argument('-f', '--full', help='do not restrict plotsize. Applicable to plotext only', action="store_true")
parser.add_argument('-m', '--matplotlib', help='plot using matplotlib. Useful in gui env', action="store_true")
parser.add_argument('-o', '--outfile', help='save matplotlib plot as svg file')
args = parser.parse_args()

capital = args.capital
taxrate_pcent = args.taxrate_pcent
gain_pcent = args.gain_pcent

#initialize
down_pcent4sell = []
diff4sell = []
down_pcent4hold = []
diff4hold = []

def populate_data():
    for down_pcent in range(1, 100, 1):
        #sell now
        profit = capital * gain_pcent/100
        tax = profit * taxrate_pcent/100
        sell_amount = capital + profit - tax

        # hold till stock price go down
        loss = (capital + profit) * down_pcent/100
        down_amount = capital + profit - loss

        #hold and sell when stock is down
        profit = down_amount - capital
        tax = profit * taxrate_pcent/100
        hold_sell_amount = capital + profit -tax

        if sell_amount >= down_amount:
            decision="SELL"
            diff = sell_amount - down_amount
            down_pcent4sell.append(down_pcent)
            diff4sell.append(diff)
        else:
            decision="HOLD"
            diff = down_amount - sell_amount
            down_pcent4hold.append(down_pcent)
            diff4hold.append(diff)

        if args.verbose:
            print("capital={:.2f} taxrate%={:.2f} down%={:.2f} gain%={:.2f} sell={:.2f} hold={:.2f} {} [{:.2f}]".
                format(capital, taxrate_pcent, down_pcent, gain_pcent, sell_amount, down_amount, decision, diff), end=' ')
            if args.hold_sell:
                print("hold_sell={:.2f} hold_sell-sell={:.2f} hold_sell-hold={:.2f}".
                        format(hold_sell_amount, hold_sell_amount-down_amount, hold_sell_amount-sell_amount), end='')
            print()
    #for
#def populate_data

#plot on terminal with plotext
def plotext_plot() :
        import plotext as plt

        plt.title("SELL/HOLD plot with captial={} taxrate={} gain_pcent={}".format(capital, taxrate_pcent, gain_pcent))

        if args.reverse:
                plt.ylabel("down_pcent")
                plt.xlabel("amount saved")
                if len(diff4sell): plt.plot(diff4sell, down_pcent4sell, label="SELL")
                if len(diff4hold): plt.plot(diff4hold, down_pcent4hold, label="HOLD")
        else:
                plt.xlabel("down_pcent")
                plt.ylabel("amount saved")
                if len(diff4sell): plt.plot(down_pcent4sell, diff4sell, label="SELL")
                if len(diff4hold): plt.plot(down_pcent4hold, diff4hold, label="HOLD")

        if not args.full:
                plt.plotsize(100, 30)

        plt.show()
#def plotext_plot() :

#plot using matplotlib
def matplotlib_plot():
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(8, 6))
        fig.autofmt_xdate()

        ax.set_title("SELL/HOLD plot with captial={} taxrate={} gain_pcent={}".format(capital, taxrate_pcent, gain_pcent))
        ax.set_xlabel("down_pcent")
        ax.set_ylabel("amount saved")
        if len(diff4sell): ax.plot(down_pcent4sell, diff4sell, label="SELL")
        if len(diff4hold): ax.plot(down_pcent4hold, diff4hold, label="HOLD")
        ax.legend()
        plt.grid()

        if args.outfile:
                plt.savefig(args.outfile, format="svg")

        plt.show()
#def matplotlib_plot():

#main
populate_data()

if args.matplotlib: 
    matplotlib_plot()
else:
    plotext_plot()
