import requests
from parsel import Selector
import pandas as pd

for i in range(2017, 2021):
    # url = 'https://en.wikipedia.org/wiki/'+str(i)+"_UCI_Track_Cycling_World_Championships_–_Men%27s_sprint"
    url = 'https://en.wikipedia.org/wiki/'+str(i)+"_UCI_Track_Cycling_World_Championships_–_Women%27s_sprint"
    text = requests.get(url).text
    selector = Selector(text=text)
    if i > 2018:
        df = pd.read_html(selector.xpath('//*[@id="mw-content-text"]/div[1]/table[3]').getall()[0])[0].to_csv('data/'+str(i)+"_qualifying.csv")
        df = pd.read_html(selector.xpath('//*[@id="mw-content-text"]/div[1]/table[4]').getall()[0])[0].to_csv('data/'+str(i)+"_sixteenth.csv")
        df = pd.read_html(selector.xpath('//*[@id="mw-content-text"]/div[1]/table[5]').getall()[0])[0].to_csv('data/'+str(i)+"_eight.csv")
        df = pd.read_html(selector.xpath('//*[@id="mw-content-text"]/div[1]/table[6]').getall()[0])[0].to_csv('data/'+str(i)+"_quarter.csv")
        df = pd.read_html(selector.xpath('//*[@id="mw-content-text"]/div[1]/table[7]').getall()[0])[0].to_csv('data/'+str(i)+"_semi.csv")
        df = pd.read_html(selector.xpath('//*[@id="mw-content-text"]/div[1]/table[8]').getall()[0])[0].to_csv('data/'+str(i)+"_final.csv")
    else:
        df = pd.read_html(selector.xpath('//*[@id="mw-content-text"]/div[1]/table[2]').getall()[0])[0].to_csv('data/'+str(i)+"_qualifying.csv")
        df = pd.read_html(selector.xpath('//*[@id="mw-content-text"]/div[1]/table[3]').getall()[0])[0].to_csv('data/'+str(i)+"_sixteenth.csv")
        df = pd.read_html(selector.xpath('//*[@id="mw-content-text"]/div[1]/table[4]').getall()[0])[0].to_csv('data/'+str(i)+"_eight.csv")
        df = pd.read_html(selector.xpath('//*[@id="mw-content-text"]/div[1]/table[5]').getall()[0])[0].to_csv('data/'+str(i)+"_quarter.csv")
        df = pd.read_html(selector.xpath('//*[@id="mw-content-text"]/div[1]/table[6]').getall()[0])[0].to_csv('data/'+str(i)+"_semi.csv")
        df = pd.read_html(selector.xpath('//*[@id="mw-content-text"]/div[1]/table[7]').getall()[0])[0].to_csv('data/'+str(i)+"_final.csv")