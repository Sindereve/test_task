import random
import datetime


def generation_time (lastTime):
    change = datetime.timedelta(milliseconds = 5000)
    time = lastTime + change
    return time

def generation_price (lastPrice):
    r = random.random()
    if  r <= 0.4:
        price = round(random.uniform(lastPrice,lastPrice+0.2),1)
        activity = 'BUY'
    if 0.4 < r <= 0.8:
        price = round(random.uniform(lastPrice,lastPrice-0.2),1)
        activity = 'SELL'
    if 0.8 < r <= 0.9:
        price = round(random.uniform(lastPrice,lastPrice-0.1),1)
        activity = 'SELL'
    if 0.9 < r <= 1:
        price = round(random.uniform(lastPrice,lastPrice+0.1),1)
        activity = 'BUY'

    return price, activity
   

def generation_V():
    return round(random.random() * 5,0) + 1
    
    
def generation(lastPrice):
    time = datetime.datetime(2024, 1, 1, 0, 0, 0, 0)
    price = lastPrice
    kol = 0
    timeStr = None

    file = open('trades.txt','w')

    while True:
        time = generation_time (time)
        timeStr = time.strftime('%H:%M:%S.%f')[:-3] 
        
        if time > datetime.datetime(2024, 1, 1, 23, 59, 59, 999):
            file.close()
            break
        
        kol+=1
        price, activity = generation_price(price)
        V = generation_V()

        file.write(f"{timeStr};{activity};{price};{V}\n")

    print("Файл 'trades.txt' успешно создан.")        
    print (f" - Конечное время:{timeStr}\n - Количество операций:{kol}")


#  00:00:00.001;BUY;100.0;1.0

    