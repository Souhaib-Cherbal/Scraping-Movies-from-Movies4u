# %%
from bs4 import BeautifulSoup
import pandas as pd
import re
import requests
from itertools import zip_longest 


# %%
name                    = []
category                = []
rate                    = []
link                    = []
quality                 = []
date                    = []
movie_lenght            = []
production_countries    = []
download_sd_size        = []
download_hd_size        = []
download_fullHD_size    = []
download_sd_link        = []
download_hd_link        = []
download_fullHD_link    = []

# %% [markdown]
# ## For the first page (name, rate, link)

# %%

def main_page_scraping():
    html = requests.get(page_link).content
    soup = BeautifulSoup(html,"lxml")
    name_pre = soup.find_all("h3", class_="card__title")
    category_pre = soup.find_all("div", class_="card__category")
    rate_pre = soup.find_all("div", class_="card__rate card__rate--green")
    for i in range(len(name_pre)):
        #for name 
        try:    
            a = name_pre[i].text
            b = a.replace("مترجم","")
            b = b.replace("مشاهدة فيلم","").strip() 
        except:
            continue
        name.append(b)
        #for the links
        link_pre = name_pre[i].a['href']
        link.append(link_pre)
        #for the rate
        rate.append(rate_pre[i].text)
        #for the category 
        category.append(category_pre[i].text)

# %%
def inner_page_scraping():
    html = requests.get(page_link).content
    soup = BeautifulSoup(html,"lxml")
    try:
            #quality
        quality_pre = soup.find_all(text = re.compile("جودة الفيلم:"))
        quality.append(quality_pre[0].parent.parent.text.replace("جودة الفيلم:","").strip())


            #date
        date_pre = soup.find_all(text = re.compile("سنة الإنتاج:"))
        date.append(date_pre[0].parent.parent.text.replace("سنة الإنتاج:","").strip())

            #Movie Lenght
        movie_lenght_pre = soup.find_all(text = re.compile("مدة الفيلم:"))
        movie_lenght_pre = movie_lenght_pre[0].parent.parent.text.replace("مدة الفيلم:","").replace("دقيقة","").strip()
        movie_lenght.append(movie_lenght_pre)
            #production_countries
        production_countries_pre = soup.find_all(text = re.compile("دول الأنتاج:"))
        production_countries_pre = production_countries_pre[0].parent.parent.text.replace("دول الأنتاج:","").strip()
        production_countries.append(production_countries_pre)

    
        # sd = soup.find_all(text=re.compile("480"))[0].parent.parent.find_all("td")
        # sd_size = sd[2].text
        # sd_link = sd[3].a['href']
        # download_sd_size.append(sd_size)
        # download_sd_link.append(sd_link)

        # hd = soup.find_all(text=re.compile("720"))[0].parent.parent.find_all("td")
        # hd_size = hd[2].text
        # hd_link = hd[3].a['href']
        # download_hd_size.append(hd_size)
        # download_hd_link.append(hd_link)

        # full_hd = soup.find_all(text=re.compile("1080p"))[1].parent.parent.find_all("td")
        # full_hd_size = full_hd[2].text
        # full_hd_link = full_hd[3].a['href']
        # download_fullHD_size.append(full_hd_size)
        # download_fullHD_link.append(full_hd_link)
    except:
        print("error")
        error_number = error_number + 1
        print("Total errors : "+srt(error_number))




# %% [markdown]
# ## Structure

# %%
error_number = 0
page_link = "https://movie4u.watch/movies"
html = requests.get(page_link).content
soup = BeautifulSoup(html,"lxml")
last_page = soup.find_all('li', class_="paginator__item")
for page_number in range(1,int(last_page[-2].text)+1):
    print("page "+str(page_number)+" of "+str(int(last_page[-2].text)))
    page_link = f"https://movie4u.watch/movies?page={page_number}"
    main_page_scraping()
i = 1
for movie_link in link:
    print("Link "+str(i)+ "of "+str(len(link)))
    page_link = movie_link
    inner_page_scraping()
    i = i+1




# %%


# %%

for i in range(len(category)):
    category[i] = category[i].replace("\n","")
data = (name, category, rate, movie_lenght, date, quality, movie_lenght, production_countries, download_sd_size, download_hd_size, download_fullHD_size, download_sd_link, download_hd_link, download_fullHD_link)
a = zip_longest(*data)
b = pd.DataFrame(a)
b.to_csv('/Users/client/Desktop/PHYTON/MY PROJECTS/reasults.csv')
print(b)


