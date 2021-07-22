from bs4 import BeautifulSoup
from os import walk, path
import typer
import codecs
import pandas as pd
# data = ['bmx_athletes.html', 'MTB_athletes.html', 'pentathlon.html', 'Road_cycling.html', ]

# app = typer.Typer()

for cp,dir,files in walk('.'):    
        for i in files:
            if i.endswith('.html'):
                file = codecs.open(i, 'r', 'utf-8')
                soup = BeautifulSoup(file)
                athletes = []
                for j in soup.find_all('li'):
                    
                    athlete = {}                                            
                    soup_li = BeautifulSoup(str(j))
                    
                    # <span class="athlete--name">Daniel</span>
                    athlete['name'] = soup_li.find('span', {'class':'athlete--name'}).getText()
                    
                    # <span class="athlete--surname">FONTANA</span></h1></div></a>
                    if soup_li.find('span', {'class':'athlete--surname'}):
                        athlete['name'] += ' '+soup_li.find('span', {'class':'athlete--surname'}).getText()

                    
                    # <span class="country--name" data-triname="Argentina">ARG, </span></span>
                    athlete['country'] = soup_li.find('span', {'class':'country--name'}).getText()
                    
                    # <span class="discipline--name">Triathlon</span></div>
                    athlete['discipline'] = soup_li.find('span', {'class':'discipline--name'}).getText()
                    
                    athletes.append(athlete)

                df = pd.DataFrame(athletes)
                df.to_csv(i[:i.find('.')]+'.csv')
# print(athletes[0])