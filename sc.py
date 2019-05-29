
import pandas as pd
from bs4 import BeautifulSoup
import urllib.request
import re

#scraper


def scraper(url):

    content = urllib.request.urlopen(url).read()

    # use BeautifulSoup to find the tag named table with wikitable sortable class
    soup = BeautifulSoup(content, features="html.parser")
    table = soup.find('table', {"class": "wikitable sortable"})

    # extract the header of table and modify
    dataheaders = [header.text for header in table.find_all('th')]
    words = [re.sub("\n|\[c\]", "", w) for w in dataheaders]
    words.insert(7, '2016 land area(sq km)')
    words.insert(9, '2016 population density(sq km)')

    # extract the table body and save as dataframe
    rows = []
    for row in table.find_all('tr'):
        rows.append([val.text.strip() for val in row.find_all('td')])

    rows.remove([])
    df = pd.DataFrame(rows, columns=words)

    # extract the links behind the column of city save as a list
    links = list(map(lambda x: 'https://en.wikipedia.org' + table.find_all('tr')[x].find_all('td')[1].a['href'],
                     list(range(1, len(table.find_all('tr'))))))

    # extract every city's zipcode through the different links
    zipcode = []
    for link in links:
        content_city = urllib.request.urlopen(link).read()
        soup_city = BeautifulSoup(content_city, features="html.parser")
        try:
            code = soup_city.find('table', {"class": "infobox geography vcard"}).find('div', {
                "class": "postal-code"}).get_text()
        except:
            print('err')
        zipcode.append(code)

    df["Zipcode"] = zipcode

    return df

url="https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population"
df = scraper(url)

# content = urllib.request.urlopen(url).read()
#
# #use BeautifulSoup to find the tag named table with wikitable sortable class
# soup = BeautifulSoup(content,features="html.parser")
# table = soup.find('table',{"class":"wikitable sortable"})
#
# #extract the header of table and modify
# dataheaders = [header.text for header in table.find_all('th')]
# words = [re.sub("\n|\[c\]","",w) for w in dataheaders]
# words.insert(7,'2016 land area(sq km)')
# words.insert(9,'2016 population density(sq km)')
#
# #extract the table body and save as dataframe
# rows=[]
# for row in table.find_all('tr'):
#     rows.append([val.text.strip() for val in row.find_all('td')])
#
# rows.remove([])
# df = pd.DataFrame(rows, columns= words)
#
# #extract the links behind the column of city save as a list
# links = list(map(lambda x:'https://en.wikipedia.org' + table.find_all('tr')[x].find_all('td')[1].a['href'],list(range(1,len(table.find_all('tr'))))))
#
# #extract every city's zipcode through the different links
# zipcode = []
# for link in links:
#     content_city = urllib.request.urlopen(link).read()
#     soup_city = BeautifulSoup(content_city,features="html.parser")
#     try:
#         code = soup_city.find('table',{"class":"infobox geography vcard"}).find('div',{"class":"postal-code"}).get_text()
#     except:
#         print('err')
#     zipcode.append(code)
#
#
# df["Zipcode"] = zipcode


#Data clean

#delete the [] behind the city
df['City']=df['City'].str.split('[').str.get(0)

#convert the string to int
df['2018estimate'] = df['2018estimate'].str.replace(',','').astype('int')
df['2010Census'] = df['2010Census'].str.replace(',','').astype('int')

#convert the string to float and delete the percentage sign
df['Change'] = df['Change'].str.replace('%','')
df['Change'] = df['Change'].str.replace('NA\[ab\]','0')
df['Change'] = df['Change'].str.replace('−','-').map(float)
#change the name of columns
df = df.rename(columns={'Change': 'Change(%)'})

#convert the string to float
df['2016 land area'] = df['2016 land area'].str.replace(',','')
df['2016 land area'] = df['2016 land area'].str.extract('(\d+.\d)').astype('float')
df = df.rename(columns={'2016 land area': '2016 land area(sq mi)'})

#convert the string to float
df['2016 land area(sq km)'] = df['2016 land area(sq km)'].str.replace(',','')
df['2016 land area(sq km)'] = df['2016 land area(sq km)'].str.extract('(\d+.\d)').astype('float')

#convert the string to int
df['2016 population density'] = df['2016 population density'].str.replace(',','')
df['2016 population density'] = df['2016 population density'].str.extract('(\d+)').astype('int')
df = df.rename(columns={'2016 population density': '2016 population density(sq mi)'})

#convert the string to int
df['2016 population density(sq km)'] = df['2016 population density(sq km)'].str.replace(',','')
df['2016 population density(sq km)'] = df['2016 population density(sq km)'].str.extract('(\d+)').astype('int')

#save as csv
df.to_csv("/Users/wuqiying/Desktop/df.csv", sep='\t', encoding='utf-8')