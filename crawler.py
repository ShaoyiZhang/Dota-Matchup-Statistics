import re
import requests
import json
from bs4 import BeautifulSoup

# # url = 'http://dotamax.com/hero/detail/match_up_comb/spectre/'
# # url = 'http://dotamax.com/hero/detail/match_up_anti/spectre/'
# url = 'http://dotamax.com/hero/rate/'

# headers = { 'Referer':'http://dotamax.com/hero/rate/',
#             'Accept-Language':'en-us',
#             'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.113 Safari/537.36'}
# req = requests.get(url,headers=headers)
# print(req.status_code)
# # with open('./match_up_comb_spectre.html','w') as f:
# # with open('./match_up_anti_spectre.html','w') as f:
# with open('./winrate.html','w') as f:
#     f.write(req.text)

getHeroName = re.compile('name-list">([A-Za-z_\']+?)</span>')
ratePatt = re.compile('10px">(.*)%</div>')

with open('./winrate.html','r') as f:
    text = f.read()
    soup = BeautifulSoup(text, 'html.parser')
    trlist = soup.find_all('tr')
    FavoredHeroDict = {}
    for i in range(1,len(trlist)):
        tdlist = trlist[i].find_all('td')
        print(tdlist)
        if len(tdlist) != 3:
            print('Irregular tdlist:\n',tdlist)
            break
        # try:
        heroName = getHeroName.search(re.sub(r'\ ','_',str(tdlist[0]))).group(1)
        # cooperationIndex = ratePatt.search(str(tdlist[1])).group(1)
        targetHeroWinRate = ratePatt.search(str(tdlist[1])).group(1)
        # ignore total battles for now, will be trivial to add later
        FavoredHeroDict[heroName] = {'winRate':targetHeroWinRate}
        # except:
        #     print(tdlist)

    out = json.dumps(FavoredHeroDict, sort_keys=True,indent=4, separators=(',', ': '))
    with open('winrate.json','w') as js:
        js.write(out)





# ANTI
'''
getHeroName = re.compile('"/hero/detail/([A-Za-z_]+?)"')
ratePatt = re.compile('10px">(.*)%</div>')

with open('./match_up_anti_spectre.html','r') as f:
    text = f.read()
    soup = BeautifulSoup(text, 'html.parser')
    trlist = soup.find_all('tr')
    FavoredHeroDict = {}
    for i in range(1,len(trlist)):
        tdlist = trlist[i].find_all('td')
        if len(tdlist) != 4:
            print('Irregular tdlist:\n',tdlist)
            break
        try:
            heroName = getHeroName.search(str(tdlist[0])).group(1)
            cooperationIndex = ratePatt.search(str(tdlist[1])).group(1)
            targetHeroWinRate = ratePatt.search(str(tdlist[2])).group(1)
            # ignore total battles for now, will be trivial to add later
            FavoredHeroDict[heroName] = {'co-opIndex':cooperationIndex,'winRateAsAlly':targetHeroWinRate}
        except:
            print(tdlist)

    out = json.dumps(FavoredHeroDict, sort_keys=True,indent=4, separators=(',', ': '))
    with open('spectre_anti.json','w') as js:
        js.write(out)
'''

# ALLY
'''
getHeroName = re.compile('"/hero/detail/([A-Za-z_]+?)"')
ratePatt = re.compile('10px">(.*)%</div>')

with open('./match_up_comb_spectre.html','r') as f:
    text = f.read()
    soup = BeautifulSoup(text, 'html.parser')
    trlist = soup.find_all('tr')
    FavoredHeroDict = {}
    for i in range(1,len(trlist)):
        tdlist = trlist[i].find_all('td')
        if len(tdlist) != 4:
            print('Irregular tdlist:\n',tdlist)
            break
        try:
            heroName = getHeroName.search(str(tdlist[0])).group(1)
            cooperationIndex = ratePatt.search(str(tdlist[1])).group(1)
            targetHeroWinRate = ratePatt.search(str(tdlist[2])).group(1)
            # ignore total battles for now, will be trivial to add later
            FavoredHeroDict[heroName] = {'co-opIndex':cooperationIndex,'winRateAsAlly':targetHeroWinRate}
        except:
            print(tdlist)

    out = json.dumps(FavoredHeroDict, sort_keys=True,indent=4, separators=(',', ': '))
    with open('spectre.json','w') as js:
        js.write(out)
'''
        