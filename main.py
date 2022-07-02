import json
import requests
from bs4 import BeautifulSoup
import pandas as pd

def getTitle(soup):
    try:
        title = soup.find("span",attrs={"id": 'productTitle'})
        title_string = str(title.string)
        title_string=title_string.rstrip().lstrip()
            
    except AttributeError:
            title_string = None

    return title_string

def getImage(soup,title):
    try:
        if(soup.find("img",attrs={"id":"imgBlkFront"})!=None):
            
            img = soup.find("img",attrs={"id":"imgBlkFront"})
        
        elif(soup.find("img",attrs={"id":"landingImage"})!=None):
            
            img=soup.find("img",attrs={"id":"landingImage"})
        
        elif(soup.find("img",attrs={"alt":title})!=None):
            
            img=img=soup.find("img",attrs={"id":"landingImage"})
        else:
            return(None)
        
        return(img.attrs["src"])
    
    except:
        return(None)


def getPrice(soup):
    try:
        price_string=None
        if(soup.find("span",attrs={"class": 'a-offscreen'})!=None):
            price = soup.find("span",attrs={"class": 'a-offscreen'})
            price_string = str(price.string)
            string_unicode = price_string
            string_encode = string_unicode.encode("ascii", "ignore")
            price_string = string_encode.decode().rstrip().lstrip()
            
            if("€" not in price_string):
                
                if(soup.find("span",attrs={"class": 'a-size-base a-color-price a-color-price'})!=None):
                    price = soup.find("span",attrs={"class": 'a-size-base a-color-price a-color-price'})
                    price_string = str(price.string)
                    string_unicode = price_string
                    string_encode = string_unicode.encode("ascii", "ignore")
                    price_string = string_encode.decode().rstrip().lstrip()

                    if("€" not in price_string):
                        price_string=None
                else:
                    price_string=None
    except :
        price_string = None
    
    return price_string



def getDetails(soup):
    if(soup.find("table",attrs={"id": 'productDetails_techSpec_section_1'})!=None):
        desTable = soup.find("table",attrs={"id": 'productDetails_techSpec_section_1'})
        try:
            details={}
            for i in desTable.findAll('tr'):
                
                try:
                    a=str(i.th.string)
                    b=str(i.td.string).lstrip()
                    string_unicode = b
                    string_encode = string_unicode.encode("ascii", "ignore")
                    string_decode = string_encode.decode().rstrip().lstrip()
                    details[a]=string_decode
                
                except:
                    pass
        except :
            details=None

    elif(soup.find("div",attrs={"id": 'detailBullets_feature_div'})!=None):
        desDiv = soup.find("div",attrs={"id": 'detailBullets_feature_div'})
        try:
            details={}
            for i in desDiv.ul.findAll('li'):
                try:
                    a=str(i.span.findAll('span')[0].string)
                    a = (" ".join(a.split()))[0:-3].rstrip()
                    string_unicode = a
                    string_encode = string_unicode.encode("ascii", "ignore")
                    string_decode = string_encode.decode().rstrip().lstrip()
                    b=str(i.span.findAll('span')[1].string)
                    details[string_decode]=b
                except:
                    pass
        except :
            details=None
    else:
        details=None
    
    return details


outputDict={"data":[]}
countLink=0
linksCSV= pd.read_csv("AmazonScraping.csv",on_bad_lines='skip')
for i in range(0,1000):
    country=linksCSV["country"][i]
    Asin=linksCSV["Asin"][i]

    url= f'https://www.amazon.{country}/dp/{Asin}'

    HEADERS=({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36','Accept-Language': 'en-US, en;q=0.5'})
    reqData = requests.get(url, headers=HEADERS)

    if(reqData.status_code==200):
        html=reqData.content
        soup= BeautifulSoup(html,"html.parser")

        Ptitle=getTitle(soup)
        Pimg=getImage(soup,Ptitle)
        Pprice=getPrice(soup)
        Pdetails=getDetails(soup)

        linkDict={
            "Product_Title":Ptitle,
            "Product_Image_URL":Pimg,
            "Price of the Product":Pprice,
            "Product Details":Pdetails
        }
        outputDict["data"].append(linkDict)



    elif(reqData.status_code==404):
        print(url,"not available")
    else:
        print("Error occured :",reqData.status_code)
    
    countLink+=1

    if(countLink%100==0):
        print(countLink,"are done")

outFile=open("OutputFile.json",'w')
json.dump(outputDict, outFile)