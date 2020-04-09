#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import time
import requests
from bs4 import BeautifulSoup


# In[6]:


data = pd.read_excel('Zipcode_data.xlsx',converters={'ZipCode': lambda x: str(x), 'CountyFIPS': lambda x: str(x), 'StateFIPS': lambda x: str(x)})


# In[7]:


len(data)


# In[8]:


data.head()


# In[9]:


# testing
url = 'https://www.zip-codes.com/zip-code/09316/zip-code-09316.asp'
print(url)
website_url = requests.get(url)

print(website_url.status_code)   # This should print 200


# In[15]:


#this loop will iterrate over each row and use zip code for extracting data
lst = []
for i,j in data.iterrows():
    
    temp_row =[]
    
    zc =j['ZipCode']
    cn = j['CityName']
    ct =  j['CityType']
    con = j['CountyName'] 
    sa = j['StateName']
    sp = j['StateAbbr']
    sf = j ['StateFIPS']
    
    
    temp_row.append(zc)
    temp_row.append(cn)
    temp_row.append(ct)
    temp_row.append(con)
    temp_row.append(sa)
    temp_row.append(sp)
    temp_row.append(sf)
    
    zipcode=zc
    #append 0 so that every zip code length is 5
    if len(zipcode) == 3:
        zipcode = '00'+zipcode
        
    elif len(zipcode) == 4:
        zipcode = '0'+zipcode
        
    #website which will be use to scrap data of a zip code
    url = 'https://www.zip-codes.com/zip-code/'+str(zipcode) + '/zip-code-'+str(zipcode) +'.asp'
    print(url)
    website_url = requests.get(url)

    print(website_url.status_code)   # This should print 200
    if(website_url.status_code == 200):
        soup = BeautifulSoup(website_url.content, 'html.parser')

        gdp_table = soup.find("table", attrs={"class": "statTable"})
        
        if gdp_table is None:
            print('hi')
        else:
            rows = gdp_table.find_all('tr')
            for row in rows:

                count = 0
                tds = list(row.find_all('td'))

                for ele in tds:

                    if ele.text == 'Latitude:':
                        #print(ele.text)
                        lat = ele.text
                        val = tds[1].text
                        print(lat, val)
                        temp_row.append(val)
                    elif ele.text == 'Longitude:':
                        #print(ele.text)
                        long = ele.text
                        val = tds[1].text
                        print(long, val)
                        temp_row.append(val)
            tup = tuple(temp_row)
            lst.append(tup) # append each tuple or rows in list
            time.sleep(20)
    


# In[ ]:


scrap_data= pd.DataFrame(lst, columns=['ZipCode', 'CityName', 'CityType', 'CountyName','StateName', 'StateAbbr', 'StateFIPS', 'Lat', 'Lng'])
scrap_data.to_excel('scrap_data.xlsx', index=False)

