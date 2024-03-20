import pandas as pd
import numpy

##Pobranie danych
url = 'https://raw.githubusercontent.com/WKirejew/Backtesting_StockStrats/main/2401-Longstrider/WTI.f1440.csv'

dataframe = pd.read_csv(url, sep=";", usecols=['date','high','low'])
print(dataframe)
def ATR(n, t):
    atr = 0
    for i in range (n):
        atr = atr + dataframe.high[t-n] - dataframe.low[t-n]
    atr = atr / n
    return atr

class Pozycja:
    def __init__(self, t, war_otw) -> None:
        self.open_date = dataframe.date[t]
        self.time = t
        self.open_price = war_otw
        self.stop_loss = war_otw - 2* ATR(20, t)
        self.status = 'open'
        self.close_price = None
    def sl(self, index):
        self.close_price = self.stop_loss
        z[index] = self
        return
    def close(self, index, war_zamk):
        self.close_price = war_zamk
        z[index] = self
        return
index = 1
z_count = 0
x = {}
z = {}
for i in range (20, len(dataframe)):
    #wyznaczanie warunku otwarcia i zamknięcia:
    last_20 = []
    last_10 = []
    for l in range (20):
        last_20.append(dataframe.high[i-20+l])
    for l in range (10):
        last_10.append(dataframe.high[i-10+l])
    war_otw = max(last_20)
    war_zamkn = min(last_10)
    #Jeśli warunek otwarcia jest spełniony, otwieramy pozycję:
    if dataframe.high[i] >= war_otw:
        if index < 6:
            x[index] = Pozycja(i, war_otw)
            index = index + 1
    #Jeśli wybito stoploss, zamykamy pozycję od najnowszej:
    elif index > 1:
            for poz in range(index-1, 1 , -1):
                if dataframe.low[i] <= x[poz].stop_loss:
                    x[poz].sl(z_count)
                    z_count = z_count + 1
                    index = index - 1
                elif i > x[poz].time + 10:
                    if dataframe.low[i] <= war_zamkn:
                        x[poz].close(z_count, war_zamkn)
                        z_count = z_count + 1
                        index = index - 1

suma=0
for key in z:
    print(z[key].close_price -z[key].open_price)
    suma = suma + z[key].close_price -z[key].open_price
print("Sumaryczny wynik backtestu:", suma)