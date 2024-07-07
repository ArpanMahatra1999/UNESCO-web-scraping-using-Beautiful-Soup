# libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd

# creating soup using url
main_url = "https://whc.unesco.org"
page = requests.get(main_url+"/en/list/&order=year")
soup = BeautifulSoup(page.content, "html.parser")

# finding years and list sites
card_body = soup.find("div", id="acc").findChild()
years = card_body.find_all('h4')
list_sites = card_body.find_all('div', class_="list_site")

# creating empty dataframe
df = pd.DataFrame()

# creating rows
for i in range(len(years)):
    year = int(years[i].text)
    ulist = list_sites[i].find_all("li")
    for item in ulist:
        heritage_type = item['class'][0].strip()
        df = df.append({
            'site': item.find('a').text.strip(),
            'natural': 'natural' in heritage_type or 'mixed' in heritage_type,
            'cultural': 'cultural' in heritage_type or 'mixed' in heritage_type,
            'danger': 'danger' in heritage_type,
            'url': main_url + item.find('a')['href'],
            'country': item.text.split("(")[-1].strip().split(")")[0],
            'year': year
        }, ignore_index=True)

# check dataframe
print(df.sample(10))

# create csv file from dataframe
df.to_csv('unesco.csv', index=False)