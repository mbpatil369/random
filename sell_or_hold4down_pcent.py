#!/usr/bin/python3
#mbpatil

import argparse

parser = argparse.ArgumentParser(description='sell or hold your stocks given a potential down_pcent for stock')
parser.add_argument('-c', '--capital', help='capital amount', type=float, default=100)
parser.add_argument('-t', '--taxrate_pcent', help='taxrate percent amount', type=float, default=25)
parser.add_argument('-d', '--down_pcent', help='potential stock down percent amount', type=float, default=25)
parser.add_argument('-gm', '--gain_pcent_min', help='minimum gain percent amount', type=int, default=10)
parser.add_argument('-gM', '--gain_pcent_max', help='maximum gain percent amount', type=int, default=1000)
parser.add_argument('-gi', '--gain_pcent_interval', help='interval between gain percent amount', type=int, default=5)

parser.add_argument('-v', '--verbose', help='dump values before plotting', action="store_true")
parser.add_argument('-r', '--reverse', help='exchange x and y axis in plot. Applicable to plotext only', action="store_true")
parser.add_argument('-f', '--full', help='do not restrict plotsize. Applicable to plotext only', action="store_true")
parser.add_argument('-m', '--matplotlib', help='plot using matplotlib. Useful in gui env', action="store_true")
parser.add_argument('-o', '--outfile', help='save matplotlib plot as svg file')
args = parser.parse_args()

capital = args.capital
taxrate_pcent = args.taxrate_pcent
down_pcent = args.down_pcent

#initialize
gain_pcent4sell = []
diff4sell = []
gain_pcent4hold = []
diff4hold = []

def populate_data():
    for gain_pcent in range(args.gain_pcent_min, args.gain_pcent_max+1, args.gain_pcent_interval):
        #sell now
        profit = capital * gain_pcent/100
        tax = profit * taxrate_pcent/100
        sell_amount = capital + profit - tax

        # hold till stock price go down
        loss = (capital + profit) * down_pcent/100
        down_amount = capital + profit - loss

        if sell_amount >= down_amount:
            decision="SELL"
            diff = sell_amount - down_amount
            gain_pcent4sell.append(gain_pcent)
            diff4sell.append(diff)
        else:
            decision="HOLD"
            diff = down_amount - sell_amount
            gain_pcent4hold.append(gain_pcent)
            diff4hold.append(diff)

        if args.verbose:
            print("capital={:.2f} taxrate%={:.2f} down%={:.2f} gain%={:.2f} sell={:.2f} hold={:.2f} {} [{:.2f}]".
                format(capital, taxrate_pcent, down_pcent, gain_pcent, sell_amount, down_amount, decision, diff))
    #for
#def populate_data

#plot on terminal with plotext
def plotext_plot() :
        import plotext as plt

        plt.title("SELL/HOLD plot with captial={} taxrate={} down_pcent={}".format(capital, taxrate_pcent, down_pcent))

        if args.reverse:
                plt.ylabel("gain_pcent")
                plt.xlabel("amount saved")
                if len(diff4sell): plt.plot(diff4sell, gain_pcent4sell, label="SELL")
                if len(diff4hold): plt.plot(diff4hold, gain_pcent4hold, label="HOLD")
        else:
                plt.xlabel("gain_pcent")
                plt.ylabel("amount saved")
                if len(diff4sell): plt.plot(gain_pcent4sell, diff4sell, label="SELL")
                if len(diff4hold): plt.plot(gain_pcent4hold, diff4hold, label="HOLD")

        if not args.full:
                plt.plotsize(100, 30)

        plt.show()
#def plotext_plot() :

#plot using matplotlib
def matplotlib_plot():
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(8, 6))
        fig.autofmt_xdate()

        ax.set_title("SELL/HOLD plot with captial={} taxrate={} down_pcent={}".format(capital, taxrate_pcent, down_pcent))
        ax.set_xlabel("gain_pcent")
        ax.set_ylabel("amount saved")
        if len(diff4sell): ax.plot(gain_pcent4sell, diff4sell, label="SELL")
        if len(diff4hold): ax.plot(gain_pcent4hold, diff4hold, label="HOLD")
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
