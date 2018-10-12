import sys
import os
import re
from bs4 import BeautifulSoup
import requests
import pandas as pd
import ssl
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

def get_text_from_elements(elements):

    return [e.text.strip() for e in elements]


def main():
    # get each record from for loop
    street_ =[]
    zip_=[]
    price_=[]
    bed_=[]
    bath_=[]

    for i in range(30):
        n=i+1
        url = "https://www.foundmydreamhomewithmarkay.com/listings/areas/46865/pgn/"+str(n)+"/minprice/275000/beds/1/sort/price+asc/?dynkw=Real%20Estate%20Broker%20Pittsburgh%20Pennsylvania/"
        headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
               'accept-encoding': 'gzip, deflate, sdch, br',
               'accept-language': 'en-GB,en;q=0.8,en-US;q=0.6,ml;q=0.4',
               'cache-control': 'max-age=0',
               'upgrade-insecure-requests': '1',
               'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
        req = requests.get(url,headers=headers)
        soup = BeautifulSoup(req.content,'html.parser')
        #street
        stree = soup.select(".street")
        street = get_text_from_elements(stree)
        for i in range(len(street)):
            s=str(street[i])
            street_.append(s)
        #zip
        csz = soup.select(".csz")
        city = get_text_from_elements(csz)
        zip=[]
        for i in range(len(city)):
            cs = str(city[i]).replace("PITTSBURGH, PA ", "")
            zip.append(cs)
        for i in range(len(zip)):
            z=str(zip[i])
            zip_.append(z)
        #price
        pric = soup.select('h5[class^="price "]')
        price = get_text_from_elements(pric)
        prices=[]
        for i in range(len(price)):
            pr=str(price[i].replace("$","").replace(",",""))
            prices.append(pr)
        for i in range(len(prices)):
            p=str(prices[i])
            price_.append(p)
        #bed
        bds = soup.select(".beds")
        bed = get_text_from_elements(bds)
        beds = []
        for i in range(len(bed)):
            be = str(bed[i]).replace(" bds", "")
            beds.append(be)
        for i in range(len(beds)):
            b=str(beds[i])
            bed_.append(b)
        #bath
        ba = soup.select(".baths")
        bath = get_text_from_elements(ba)
        baths = []
        for i in range(len(bath)):
            bat = str(bath[i]).replace(" ba", "")
            baths.append(bat)
        for i in range(len(baths)):
            b=str(baths[i])
            bath_.append(b)

    # from str to int and float
    prices_=[]
    for i in range(len(price_)):
        p=int(price_[i])
        prices_.append(p)
    beds_=[]
    for i in range(len(bed_)):
        b=int(bed_[i])
        beds_.append(b)
    baths_=[]
    for i in range(len(bath_)):
        b=float(bath_[i])
        baths_.append(b)

    cut = pd.cut(prices_, 5, precision=2)
    d={'Street':street_,'ZIP':zip_,'Price':prices_,'Price Group(differs by 22000)':cut.codes,'Bed':beds_,'Bath':baths_}
    f={'ZIP':zip_,'Price':prices_,'Bed':beds_,'Bath':baths_}
    df = pd.DataFrame(data=d)
    df_=pd.DataFrame(data=f)
    
    hou_count=pd.crosstab(df['ZIP'],df['Price Group(differs by 22000)'])
    hou_count = hou_count.loc[:, :]
    pcts = hou_count.div(hou_count.sum(1), axis=0)
    pc=pcts.plot.bar()
    plt.show(pc)

    sn=sns.pairplot(df_, diag_kind='kde', plot_kws={'alpha': 0.2})
    plt.show(sn)


main()
