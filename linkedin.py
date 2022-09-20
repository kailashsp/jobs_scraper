from cgitb import html
import re
import cloudscraper
from bs4 import BeautifulSoup
import pandas as pd

scraper = cloudscraper.create_scraper()

def extract(page):
    url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Web%20Development&location=India&geoId=102713980&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start={page}"
    r = scraper.get(url=url,headers={'User-Agent' :'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrohttpsme/83.0.4103.97 Safari/537.36'})
    soup = BeautifulSoup(r.content,'html.parser')
    return soup

def transform(soup):
    divs = soup.find_all('div',class_='base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card')
    for item in divs:
        title = item.find('h3','base-search-card__title').text.strip()
        company = item.find('h4','base-search-card__subtitle').text.strip()
        location = item.find('span','job-search-card__location').text.strip()

        # posted = item.find('time',class_ = 'job-search-card__listdate').text.strip()
        posted = item.time.attrs['datetime']

        link = item.find('a', class_='base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]')['href']+'/'

        job = {
            'Title':title,
            'Company':company,
            'location':location,
            'date_posted':posted,
            'Links':link
        }
        joblist.append(job)

    return

joblist = []



for i in range(0,40): 
    print(f'getting page {i}')                   #looping through the different pages and applying extract and tranform function
    
    c = extract(i)
    transform(c)



df = pd.DataFrame(joblist)

df.to_csv('linkedin_jobs.csv')


# c = extract(0)
# print(c)
