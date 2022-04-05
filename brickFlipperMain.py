def availableSizes(url = "https://www.nike.com/t/air-vapormax-plus-mens-shoes-nC0dzF/924453-004"):
    import requests
    import json
    from bs4 import BeautifulSoup
    import pandas as pd
    import re

    #Headers are highly recommended
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0',
        'Accept': 'image/webp,*/*',
        'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
    }
    url = url
    page = requests.get(url,headers = headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    #The web page is populated with data contained in a script tag which we will look for
    #It is json data
    data = json.loads(soup.find('script',text=re.compile('INITIAL_REDUX_STATE')).text.replace('window.INITIAL_REDUX_STATE=','')[0:-1])

    #The Sku we are searching for
    product_id = url[-10:]

    #In the json file, the following will give us the possible SKUs list
    skus = data['Threads']['products'][product_id]['skus']
    #And the following their availability
    available_skus = data['Threads']['products'][product_id]['availableSkus']

    #Let's use pandas to cross both tables
    df_skus = pd.DataFrame(skus)
    df_available_skus = pd.DataFrame(available_skus)

    #Here is finally the table with the available skus and their sizes
    final = df_skus.merge(df_available_skus[['skuId','available']], on ='skuId')
    # which can be saved in any format you want (xl, txt, csv, json...)
    return (final)
def hasSize(size,url="https://www.nike.com/t/air-vapormax-plus-mens-shoes-nC0dzF/924453-004"):
    available_sizes = []
    for x in (availableSizes(url)['nikeSize']):
        available_sizes.append(x)
    return (size in available_sizes)
def stockx(url = 'https://stockx.com/nike-air-vapormax-plus-triple-black'): #I have been banned on stockx (need the human verification)
    import pandas as pd
    import requests
    from bs4 import BeautifulSoup
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0'}
    url = url
    page = requests.get(url,headers = headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    bext = soup.find_all(text=True)
    #bext = str(bext)
    print(bext[151])

    #size = text[160] #these only work when the url used is the default one. They also sometimes dont work.
    #it changes the index every output, but if you use the default link and run it a few times it should work
    #size = str(size)
    #price = text[161] #would love to be able to find a way of locating this without hardcoding
    #price = str(price)
    done = False
    failcount= 0
    orAskIndex = (bext.index('Place Bid'))
    while done == False and failcount<50:
        try:
            orAskIndex=(bext.index('Place Bid'))
            print(orAskIndex)#FOUND IT, use this to index. The price will be the one after this
            done = True
        except:
            failcount+=1
            print(failcount)
            #retry
    if failcount >= 50:
        #print('max retries reached, please re-run')
        return('none')
    else:
        size = bext[orAskIndex + 1]
        price = bext[orAskIndex + 2]
        TransactionFee = 10.0
        PaymentProc = 3
        total = int(price[1:]) - (int(price[1:]) * (TransactionFee/100)) - (int(price[1:])*(PaymentProc/100))
        return(size,total)
        #stockx('https://stockx.com/air-jordan-1-retro-high-white-black-volt-university-gold') #run a couple of times if it doesnt work

def getPrice(url='https://www.nike.com/t/air-vapormax-plus-mens-shoes-nC0dzF/924453-004',discount=20):
    import requests
    from bs4 import BeautifulSoup
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0'}
    url = url
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    price = soup.find(class_='product-price css-11s12ax is--current-price css-tpaepq').find(text=True)
    price = int(price[1:])
    adjustedPrice = price - (price * (discount/100))
    return(adjustedPrice)

def highestBids(url = 'https://stockx.com/sell/nike-air-vapormax-plus-white'):
    #need to add proxy support for when we are banned on this IP
    import requests
    from bs4 import BeautifulSoup
    import time
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    # object of ChromeOptions class
    c = webdriver.ChromeOptions()
    # incognito parameter passed
    c.add_argument("--incognito")
    driver = webdriver.Chrome(options=c)
    driver.get(url)
    suc = False
    fail = 0
    while suc == False and fail < 5:
        try: #the problem is stockx now asks for human verification at this step. Lets see if we can get bids any other way
            time.sleep(3)
            try:
                element = driver.find_element(By.XPATH,'//*[@id="chakra-modal-3"]/footer/div/button[2]')
                element.click()
                print('clicked understand 1\n')
                suc = True
            except:
                element = driver.find_element(By.XPATH, '//*[@id="bottom-bar-root"]/div/div/button[2]') #dont think this works, xpath for the button is being spotty
                element.click()
                print('clicked understand 2\n')
                suc = True
        except:
            driver.refresh()
            time.sleep(5.5)
            fail += 1
            pass
    if fail >= 10:
        return('none')
        driver.close()
    else:
        output = []
        for x in range(1,24):
            try:
                element = driver.find_element(By.XPATH,'//*[@id="main-content"]/div/div/div[2]/div/div[2]/div['+str(x)+']/div').text #banned, so cant tell if this works, but should be the element of the first size, this second element should be the second size and price
                output.append(element)
            except:
                break

        return output
        driver.close()
        #now we throw all these in a list and iterate through and see if any of them are above the retail (minus discount) price
def check(lzt=['4\n$157', '4.5\n$185', '5\n$200', '5.5\n$170', '6\n$176', '6.5\n$230', '7\n$182', '7.5\n$178', '8\n$116', '8.5\n$171', '9\n$160', '9.5\n$133', '10\n$140', '10.5\n$155', '11\n$175'],url='https://www.nike.com/t/air-vapormax-plus-womens-shoes-xbt7zf/DQ4695-001',number=10,discount=20):
    import time
    temp = lzt
    transactionFee = 0.1 #CAN BE CHANGED IF YOU ARE A HIGH LEVEL STOCKX ACCOUNT
    paymentProc = 0.03 #same with this one
    checkDict = {}
    for x in lzt:
        size = x[0:int(x.index('\n'))]
        price = x[x.index('$')+1:]
        price = int(price)
        price = price-(price*paymentProc)-(price*transactionFee) #These are to include the fees, so the price will be what the payout price would be
        checkDict[size] = price
    sortedSize = sorted(checkDict.items(), key=lambda x: x[1])
    sortdict = dict(sortedSize)
    productPrice = getPrice(url,discount)
    output={}
    for x in sortdict:
        if sortdict[x]>productPrice:
            output[x]=sortdict[x]
        else:
            pass
    buyList = {}
    for x in output:
        if hasSize(x,url):
            buyList[x]=output[x]-productPrice #in the format of size:potential profit
    return buyList
#right now the dictionary is size:price, might want to change that in the future who knows

    #needs to get an input of one nike url and the size and price dictionary from stockx then:
    #1) needs to sort the inputted dictionary from largest to smallest
    #2) check the price of the nike product
    #3) remove all items in the stockx dictionary that are below the retail/getPrice() price
    #4) iterate through the remaining stockx prices/sizes and check (with the hasSize()) to see if any of the sizes are available



def getNikes(url='https://www.nike.com/w/mens-nik1?q=airmax',number=10):
    import requests
    from bs4 import BeautifulSoup
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0'}
    url = url
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    text = soup.find_all(text=True)
    text = str(text)
    if len(text)<100:
        return ('retry')
    else:
         #I think all of the products are in here as a dictionary, but cant access them as dictionary
        temp = text
        prefix = 'https://www.nike.com/t/'
        urlz=[]
        for x in range (number):
            temp = temp[temp.index('pdpUrl'):]
            pdUrl = temp[temp.index('pdpUrl')+9:temp.index(',')-1]
            pdUrl = (prefix+pdUrl[26:])
            pdUrl=pdUrl.replace('u002F','')
            temp = temp[temp.index(':'):]
            urlz.append(pdUrl)
        return urlz
def getStockx(url = 'https://www.nike.com/t/blazer-mid-77-vintage-mens-shoes-nw30B2/BQ6806-002'):
    import requests
    from bs4 import BeautifulSoup
    pid = url[-10:]
    url = 'https://stockx.com/search?s='+pid
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0'}
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    name = soup.find(class_='chakra-text css-3lpefb')
    name = str(name)[34:-4]
    name = name.replace(' ','-')
    return('https://stockx.com/'+name)
def main(number = 20,url='https://www.nike.com/w/mens-best-76m50znik1'):
    success = False
    print('getting nike links')
    while success == False:
        nikes = getNikes(url,number)
        if len(nikes)>=number:
            success = True
            print('got nike links')
    stockx = []
    s = False
    print('getting stockx links')
    for x in nikes:
        stock = (getStockx(x))
        stockx.append(stock)
    print(stockx)
    print('got stockx links')
    s = False
    print('checking links')
    buyDict = {}
    for x in range(len(nikes)):
        bids = (highestBids(stockx[x]))
        buyDict[nikes[x]]=check(bids,nikes[x],number)

    return buyDict
print(main(1))
#main does not work, getting problems wherever the fuck "short" is.

#the problem is stockx banned me, need human verify

#create a nike account bot to get discounts. Use domains, might need several to not get banned in long run. They send at beginning of each month
#so we create them now (today is 4/4/22) and they will be available/emails will go out (5/1/22)

#add proxy support to the stockx selenium highestBids function
#nike code: USCS10PANKN1H5SE
#jamesmicheal@brainmail.net,8649Password! (should have 10% code by 5/1/22)