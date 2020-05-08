from throttle import Throttle
from download import download,search_codes
from string import ascii_lowercase
import re
import csv
import itertools

throttle = Throttle(0)

"""
So, money.rediff.com has the simplest structure of scripcodes I found. All scrips are categorized by the first alphabet. In this code I am first finding out how many stocks are there starting with each alphabet. The count of the stocks is being recorded in the list 'index' below
"""
index=[]
for x in ascii_lowercase:
    throttle.wait('https://money.rediff.com')
    html=str(download('https://money.rediff.com/companies/{}'.format(x)))
    len=re.search('>Showing 1 - (.*?) of (.*?) ',html)
    index.append(int(len.group(2)))

"""
Once I have all the stocks by their alphabet, I am iterating through every page on the structure to find the regex for scripcode, which is a 6 digit number. I know the variables look ugly, but the code is fucntional, and will only be run once in a blue moon. I'll improve on it later on, if I get time. Basically, this is an unintelligent iterative crawler.
"""

ctr=0
b=[]
prod=[]
for x in ascii_lowercase:
    throttle.wait('https://money.rediff.com')
    for i in itertools.count(1,200):
        limit=index[ctr]
        if(i>limit):
            break
        b=search_codes('https://money.rediff.com/companies/{}/{}-{}'.format(x,i,i+199))
        for item in b:
            prod.append(int(item))
    ctr+=1
b=search_codes('https://money.rediff.com/companies/others')
for item in b:
    prod.append(int(item))

#now I am writing the contents of prod into a csv file. I have to set up a method to make a database out of this.
with open('Scripcodes\\scripcode.csv','w') as f:
    writer=csv.writer(f)
    writer.writerow(prod)
f.close()