import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import math
import data_generation

def data_read():
    data_generation.generation(10000)
    times = []
    prices = []
    with open('trades.txt','r') as file:
        for line in file:
            parts=line.strip().split(';')
            timeStr=parts[0]
            price=float(parts[2])
            time=datetime.datetime.strptime(timeStr, '%H:%M:%S.%f')

            times.append(time)
            prices.append(price)

    return times, prices


def create_BB(prices,period):
    middlePrices = []
    sumPrice = 0

    for k in range(period):
        sumPrice+=prices[k]
        middlePrice=sumPrice/(k+1)
        middlePrices.append(middlePrice)

    for k in range(period,len(prices)):
        sumPrice+=prices[k]-prices[k-period]
        middlePrice=sumPrice/period
        middlePrices.append(middlePrice)

    upBBs = []
    downBBs = []
    sumStdOne = 0

    upBBs.append(middlePrices[1])
    downBBs.append(middlePrices[1])

    for k in range(1,period):
        sumStdOne = 0
        for i in range (k+1):
            sumStdOne += (prices[i]-middlePrices[i])**2
        stdDev = math.sqrt(sumStdOne/k+1)

        upBBs.append(middlePrices[k]+2*stdDev)
        downBBs.append(middlePrices[k]-2*stdDev)

    for k in range(period,len(prices)):
        sumStdOne = 0
        for i in range(k-period, k):
            sumStdOne+=(prices[i]-middlePrices[i])**2
        stdDev=math.sqrt(sumStdOne/period)

        upBBs.append(middlePrices[k]+2*stdDev)
        downBBs.append(middlePrices[k]-2*stdDev)

    return middlePrices, upBBs, downBBs

def create_treade(prices, upBBs, downBBs):
    buyMarker = [] 
    sellMarker = []
    for k in range(len(prices)):
        if prices[k]>upBBs[k]:
            sellMarker.append(k)
        if prices[k]<downBBs[k]:
            buyMarker.append(k)
    return buyMarker, sellMarker 


def build(times, prices, middlePrices, upBBs, downBBs, sellMarker, buyMarker):
    
    plt.figure(figsize=(10, 5))
    plt.plot(times, prices, color='g', label='Цена')
    plt.plot(times, middlePrices, color='r', label='ср. цена')
    plt.plot(times, upBBs, color='k', label='линии огр.')
    plt.plot(times, downBBs, color='k' )
    plt.xlabel('Время')
    plt.ylabel('Цена')   
    
    plt.scatter([times[k] for k in buyMarker], [prices[k] for k in buyMarker], color='b', label='Покупка', marker='^', alpha=1)
    plt.scatter([times[k] for k in sellMarker], [prices[k] for k in sellMarker], color='m', label='Продажа', marker='v', alpha=1)

    ax = plt.gca()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    plt.gcf().autofmt_xdate()

    plt.title('График цены за день')
    plt.legend()
    plt.grid(True)
    plt.show()
    

times, prices = data_read()
middlePrices, upBBs, downBBs = create_BB( prices,20)
sellMarker, buyMarker= create_treade(prices, upBBs, downBBs)
build(times, prices, middlePrices, upBBs, downBBs, sellMarker, buyMarker)
