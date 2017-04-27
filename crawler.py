import re
import requests
import json
import time
from bs4 import BeautifulSoup

# # url = 'http://dotamax.com/hero/detail/match_up_comb/spectre/'
# # url = 'http://dotamax.com/hero/detail/match_up_anti/spectre/'
# url = 'http://dotamax.com/hero/rate/'

headers = { 'Referer':'http://dotamax.com/hero/rate/',
            'Accept-Language':'en-us',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.113 Safari/537.36'}
# req = requests.get(url,headers=headers)
# print(req.status_code)
# # with open('./match_up_comb_spectre.html','w') as f:
# # with open('./match_up_anti_spectre.html','w') as f:
# with open('./winrate.html','w') as f:
#     f.write(req.text)
'''
# download
with open('herolist.txt') as heros:
    herolist = heros.read().split(',')
    herolist.append("furion")
    herolist.append('spectre')
    for hero in herolist:
        # Ally
        url = 'http://dotamax.com/hero/detail/match_up_comb/' + hero + '/'
        req = requests.get(url,headers=headers)
        print(req.status_code,hero)        
        with open('./html/comb/'+hero,'w') as f:
            f.write(req.text)
        time.sleep(0.5)

        # Enemy
        url = 'http://dotamax.com/hero/detail/match_up_anti/' + hero + '/'
        req = requests.get(url,headers=headers)
        print(req.status_code, hero)        
        if (req.status_code != 200):
            print(url)
        with open('./html/anti/'+hero,'w') as f:
            f.write(req.text)
        time.sleep(0.5)
        
    # WinRate
    url = 'http://dotamax.com/hero/rate'
    req = requests.get(url,headers=headers)
    print(req.status_code,'winRate')        
    if (req.status_code != 200):
        print(url)
    with open('./html/winRate/winRate','w') as f:
        f.write(req.text)
    time.sleep(0.5)

'''
def WinRate(fileDescriptor):
    # getHeroName = re.compile('name-list">([A-Za-z_\'-]+?)</span>')
    getHeroName = re.compile("/hero/detail/([A-Za-z_\'-]+?)'")
    # '/hero/detail/doom_bringer')
    ratePatt = re.compile('10px">(.*)%</div>')

    
    text = fileDescriptor.read()
    # print(text)
    soup = BeautifulSoup(text, 'html.parser')
    trlist = soup.find_all('tr')
    WinRateDict = {}
    print(len(trlist))
    # for i in range(0,len(trlist)):
    for i in range(0,len(trlist)):    
        # print(i)
        tdlist = trlist[i].find_all('td')
        # tdlist = trlist[i].find_all('tr')
        # print(trlist[i])
        # (r"DoNav('/hero/detail/([A-Za-z_\'-]+?)")
        nameRaw = re.sub(r'\ ','_',str(trlist[i]))
        if 'natural' in nameRaw and 'prophet' in nameRaw:
            heroName = 'nature_prophet'
        else:
            heroName = getHeroName.search(nameRaw).group(1)
        if len(tdlist) != 3:
            print('Irregular tdlist:\n',tdlist)
            break
        # print(tdlist)
        # try:
        # heroName = 'gg'
        # heroName = getHeroName.search(re.sub(r'\ ','_',str(tdlist[0]))).group(1)
        # print(tdlist)
        # print(heroName)
        # cooperationIndex = ratePatt.search(str(tdlist[1])).group(1)
        targetHeroWinRate = ratePatt.search(str(tdlist[1])).group(1)
        # ignore total battles for now, will be trivial to add later
        WinRateDict[heroName.lower()] = {'winRate':targetHeroWinRate}
        # except:
        #     print(tdlist)
    # print(WinRateDict)
    
    return WinRateDict



# ANTI
def Enemy(fileDescriptor):
    getHeroName = re.compile('/hero/detail/([A-Za-z_\']+?)"')
    ratePatt = re.compile('10px">(.*)%</div>')

    
    text = fileDescriptor.read()
    soup = BeautifulSoup(text, 'html.parser')
    trlist = soup.find_all('tr')
    EnemyHeroDict = {}
    for i in range(1,len(trlist)):
        tdlist = trlist[i].find_all('td')
        if len(tdlist) != 4:
            print('Irregular tdlist:\n',tdlist)
            break
        try:
            # heroName = getHeroName.search(str(tdlist[0])).group(1)
            nameRaw = re.sub(r'\ ','_',str(tdlist[0])).lower()
            if 'natural' in nameRaw and 'prophet' in nameRaw:
                heroName = 'furion'
            else:
                heroName = getHeroName.search(nameRaw).group(1)
            # if (heroName == 'furion'):
            #     continue
            cooperationIndex = ratePatt.search(str(tdlist[1])).group(1)
            targetHeroWinRate = ratePatt.search(str(tdlist[2])).group(1)
            # ignore total battles for now, will be trivial to add later
            EnemyHeroDict[heroName.lower()] = {'co-opIndex':cooperationIndex,'winRateAsAlly':targetHeroWinRate}
        except:
            print(tdlist)
    return EnemyHeroDict

# ALLY
def Ally(fileDescriptor):
    # getHeroName = re.compile('"/hero/detail/([A-Za-z_]+?)"')
    getHeroName = re.compile('/hero/detail/([A-Za-z_\']+?)"')
    ratePatt = re.compile('10px">(.*)%</div>')

    text = fileDescriptor.read()
    soup = BeautifulSoup(text, 'html.parser')
    trlist = soup.find_all('tr')
    FavoredHeroDict = {}
    for i in range(1,len(trlist)):
        tdlist = trlist[i].find_all('td')
        if len(tdlist) != 4:
            print('Irregular tdlist:\n',tdlist)
            break
        try:
            nameRaw = re.sub(r'\ ','_',str(tdlist[0])).lower()
            if 'natural' in nameRaw and 'prophet' in nameRaw:
                heroName = 'furion'
            else:
                heroName = getHeroName.search(nameRaw).group(1)
            # heroName = getHeroName.search(str(tdlist[0])).group(1)
            # if (heroName == 'furion'):
                # continue
            cooperationIndex = ratePatt.search(str(tdlist[1])).group(1)
            targetHeroWinRate = ratePatt.search(str(tdlist[2])).group(1)
            # ignore total battles for now, will be trivial to add later
            FavoredHeroDict[heroName.lower()] = {'co-opIndex':cooperationIndex,'winRateAsAlly':targetHeroWinRate}
        except:
            print(tdlist)

    return FavoredHeroDict


# parse
with open('herolist.txt') as heros:
    herolist = heros.read().split(',')
    TopLayerDict = {}

    with open('./html/winRate/winRate','r') as f:
        TopLayerDict = WinRate(f)
    
    # print('good')
    # special for nature's prophet
    herolist.append('furion')
    herolist.append('spectre')
    
    for hero in herolist:
        print('Processing ', hero,'')
        # if (hero == 'furion'):
        #     continue
        AllyDict = {}
        EnemyDict = {}
        # Ally
        with open('./html/comb/'+hero,'r') as f1:
            AllyDict[hero] = Ally(f1)
    
        # Enemy

        with open('./html/anti/'+hero,'r') as f2:
            EnemyDict[hero] = Enemy(f2)
    
        TopLayerDict[hero.lower()]['Ally'] = AllyDict
        # print(AllyDict.values())
        # break
        # print(TopLayerDict)
        TopLayerDict[hero.lower()]['Enemy'] = EnemyDict
        # print(hero)  
        
             
    out = json.dumps(TopLayerDict, sort_keys=True,indent=4, separators=(',', ': '))
    with open('Dota_STAT.json','w') as js:
        js.write(out)

        
'''
getHeroName = re.compile('name-list">([A-Za-z_\']+?)</span>')
ratePatt = re.compile('10px">(.*)%</div>')

with open('./winrate.html','r') as f:
    text = f.read()
    soup = BeautifulSoup(text, 'html.parser')
    trlist = soup.find_all('tr')
    FavoredHeroDict = {}
    for i in range(1,len(trlist)):
        tdlist = trlist[i].find_all('td')
        # print(tdlist)
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


'''

'''
# ANTI

# getHeroName = re.compile('"/hero/detail/([A-Za-z_]+?)"')
getHeroName = re.compile('/hero/detail/([A-Za-z_\']+?)"')
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
            # heroName = getHeroName.search(str(tdlist[0])).group(1)
            heroName = getHeroName.search(re.sub(r'\ ','_',str(tdlist[0]))).group(1)
            cooperationIndex = ratePatt.search(str(tdlist[1])).group(1)
            targetHeroWinRate = ratePatt.search(str(tdlist[2])).group(1)
            # ignore total battles for now, will be trivial to add later
            FavoredHeroDict[heroName] = {'co-opIndex':cooperationIndex,'winRateAsAlly':targetHeroWinRate}
        except:
            print(tdlist)

    out = json.dumps(FavoredHeroDict, sort_keys=True,indent=4, separators=(',', ': '))
    with open('spectre_anti.json','w') as js:
        js.write(out)
    # with open('herolist.txt','w') as hero:
    #     hero.write(str(sorted(FavoredHeroDict.keys())))
'''
# ALLY

'''
# getHeroName = re.compile('"/hero/detail/([A-Za-z_]+?)"')
getHeroName = re.compile('/hero/detail/([A-Za-z_\']+?)"')
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

    # with open('herolist.txt','w') as hero:
    #     hero.write(str(sorted(FavoredHeroDict.keys())))
'''