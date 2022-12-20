
#Author: Md.Fazlul Hoque
#Source: Stackoverflow and answered by the author
#Source link: https://stackoverflow.com/questions/73394922/give-me-attribute-error-using-beautifulsoup


from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.chrome.options import Options
import pandas as pd


options = Options()
options.add_argument("--no-sandbox")
options.add_argument("start-maximized")
#options.add_experimental_option("detach", True)
s = Service("./chromedriver") #Your chromedriver path

driver = webdriver.Chrome(service= s, options=options)
base_url='https://www.avocats-lille.com/'
url = 'https://www.avocats-lille.com/fr/annuaire/avocats-du-tableau-au-barreau-de-lille?view=entries'

driver.get(url)
time.sleep(1)

soup = BeautifulSoup(driver.page_source, "html.parser")
tra = soup.find_all('h2',class_='title')
data = []
productlinks=[]
for links in tra:
    for link in links.find_all('a',href=True):
        comp=base_url+link['href']
        productlinks.append(comp)
        
for link in productlinks:
    driver.get(link)
    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    t=soup.select_one('p:-soup-contains("Tél.")')
    tel = t.next_element.replace('Tél.', '').strip() if t else None
    mail=soup.select_one('.contact + div > p:nth-child(1) > span > a')
    email = mail.text if mail else None
    #print(tel,email)
    data.append({'email': email})

df = pd.DataFrame(data)
#print(df)
