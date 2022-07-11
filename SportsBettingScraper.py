# Sports Betting Best Value Scraper
# By: Alex Lindberg 
# I created a program that scrapes over 4 of the most popular sports betting
# websites in order to find the individual moneyline that has the best value
# in comparison to the moneylines for the same game on the other three sites

##############################################################################
# NECESSARY IMPORTS

from selenium import webdriver

from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.chrome.service import Service

from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup

import requests 

from time import sleep 

##############################################################################
# FUNCTIONS: 

# Needed a simple function that would change abbreviated team names to the full names
def change_name(name): 
    if name == 'TB Ra':
        return 'Tampa Bay Rays'
    elif name == 'CIN R': 
        return 'Cincinnati Reds'
    elif name == 'LA An':
        return 'Los Angeles Angels'
    elif name == 'BAL O':
        return 'Baltimore Orioles'
    elif name == 'MIA M':
        return 'Miami Marlins'
    elif name == 'NY Me': 
        return 'New York Mets'
    elif name == 'NY Ya': 
        return 'New York Yankees'
    elif name == 'BOS R': 
        return 'Boston Red Sox'
    elif name == 'WAS N': 
        return 'Washington Nationals'
    elif name == 'ATL B': 
        return 'Atlanta Braves'
    elif name == 'TEX R': 
        return 'Texas Rangers'
    elif name == 'PIT P': 
        return 'Pittsburgh Pirates'
    elif name == 'MIL B': 
        return 'Milwaukee Brewers'
    elif name == 'DET T': 
        return 'Detroit Tigers'
    elif name == 'CHI W': 
        return 'Chicago White Sox'
    elif name == 'CLE G': 
        return 'Cleveland Guardians'
    elif name == 'KC Ro': 
        return 'Kansas City Royals'
    elif name == 'PHI P': 
        return 'Philadelphia Phillies'
    elif name == 'STL C': 
        return 'St. Louis Cardinals'
    elif name == 'COL R': 
        return 'Colorado Rockies'
    elif name == 'ARI D': 
        return 'Arizona Diamondbacks'
    elif name == 'HOU A': 
        return 'Houston Astros'
    elif name == 'OAK A': 
        return 'Oakland Athletics'
    elif name == 'SF Gi': 
        return 'San Francisco Giants'
    elif name == 'SD Pa': 
        return 'San Diego Padres'
    elif name == 'CHI C': 
        return 'Chicago Cubs'
    elif name == 'LA Do': 
        return 'LA Dodgers'
    elif name == 'TOR B': 
        return 'Toronto Blue Jays'
    elif name == 'SEA M': 
        return 'Seattle Mariners'
    elif name == 'MIN T': 
        return 'Minnesota Twins'
    else:
        return ""

##############################################################################
# DRAFT KINGS SCRAPER 
draftkings_html = requests.get('https://sportsbook.draftkings.com/leagues/baseball/88670847').text
draftkings = BeautifulSoup(draftkings_html, 'lxml')
mlb_teams = {
    'ARI D', 'ATL B', 'BAL O', 'BOS R', 'CHI W', 'CHI C', 'CIN R', 
    'CLE G', 'COL R', 'DET T', 'HOU A', 'KC Ro', 'LA An', 'LA Do',
    'MIA M', 'MIL B', 'NY Ya', 'NY Me', 'OAK A', 'PHI P', 'PIT P', 
    'SD Pa', 'SF Gi', 'SEA M', 'STL C', 'TB Ra', 'TEX R', 'TOR B', 
    'WAS N'
    }
dk_games = draftkings.find_all('tr')
dk_dict = {}
for game in dk_games:   
    team_name = game.find('div', class_ = 'event-cell__name-text')
    team_ml = game.find('span', class_ = 'sportsbook-odds american no-margin default-color')
    if team_name != None: 
        team_name = team_name.text 
        team_name = team_name[0:5]
    if team_ml != None: 
        team_ml = team_ml.text
    if team_name != None and team_ml != None and team_name in mlb_teams: 
        mlb_teams.remove(team_name)
        dk_dict[team_name] = team_ml

##############################################################################
# BETONLINE SCRAPER

# betonline is a dynamic website so we must use selenium 
betonline_driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
betonline_driver.get('https://www.betonline.ag/sportsbook/baseball/mlb')
sleep(2) # ensure page is loaded 
bo_dict = {}
bo_teams = []
bo_mls = []
for team in betonline_driver.find_elements(by = By.CLASS_NAME, value = 'lines-row'):
    name = team.find_element(by = By.CLASS_NAME, value = 'lines-row__team-row')
    ml = team.find_element(by = By.CLASS_NAME, value = 'lines-row__money')
    bo_teams.append(name.find_element(by = By.TAG_NAME, value = 'span').text.replace(' - Game #1', ''))
    bo_mls.append(ml.find_element(by = By.CLASS_NAME, value = 'bet-pick__wager-line').text)
for name, ml in zip(bo_teams, bo_mls): 
    bo_dict[name] = ml
betonline_driver.close()

##############################################################################
# BOVADA SCRAPER 

# bovada is dynamic website so we have to use selenium and webdriver
bovada_driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
bovada_driver.get('https://www.bovada.lv/sports/baseball/mlb')
sleep(2) # ensure page is loaded 
bov_all = bovada_driver.find_element(by = By.CLASS_NAME, value = 'grouped-events')
bov_games = bov_all.find_elements(by = By.XPATH, value = '/html/body/bx-site/ng-component/div/sp-sports-ui/div/main/div/section/main/sp-path-event/div/div[2]/sp-next-events/div/div/div[2]/div/sp-coupon')
bov_dict = {}
bov_teams = []
bov_mls = []
for game in bov_games: 
    names = game.find_elements(by = By.CLASS_NAME, value = 'name')
    mls = game.find_elements(by = By.CLASS_NAME, value = 'bet-price')
    bov_teams.append(names[0])
    bov_teams.append(names[1])
    bov_mls.append(mls[1])
    bov_mls.append(mls[4])
sleep(5)
for team, ml in zip(bov_teams, bov_mls): 
    ml = ml.text 
    ml = ml[1:len(ml) - 1]
    bov_dict[team.text] = ml

bovada_driver.close()

##############################################################################
# BETUS SCRAPER

betus_html = requests.get('https://www.betus.com.pa/sportsbook/baseball/mlb/').text
betus = BeautifulSoup(betus_html, 'lxml') 
bu_dict = {}
bu_games = betus.find_all('div', class_ = 'normal')
bu_teams = []
bu_ml = []
# add teams and moneylines to respective sets 
for game in bu_games:
    away_team = game.find('span', id = 'awayName')
    home_team = game.find('span', id =  'homeName')
    if(away_team.a != None):
        bu_teams.append(away_team.a.text.replace(' G1', ''))
    if(home_team.a != None): 
        bu_teams.append(home_team.a.text)
    ml_away = game.find_all('div', class_ = 'g-ln col-3 col-lg-2 p-0 border-left-0 line-container')
    ml_home = game.find_all('div', class_ = 'g-ln col-3 p-0 col-lg-2 line-container border-bottom-0')
    bu_ml.append(ml_away[1].text.replace('\n', ''))
    bu_ml.append(ml_home[0].text.replace('\n', ''))
# iterate through both lists and add the values to the dictionary     
for team, ml in zip(bu_teams, bu_ml):
    team = team.replace(' G1', '')
    bu_dict[team] = ml

##############################################################################
# We need to find the average money line for each team 
ml_averages = {}
for team in dk_dict: 
    long_team = change_name(team)
    if long_team in bo_dict and long_team in bov_dict and long_team in bu_dict: 
        dk_score = (dk_dict[team])
        bo_score = (bo_dict[long_team])
        bov_score = (bov_dict[long_team])
        bu_score = (bu_dict[long_team])
        if 'E' in dk_score or 'v' in dk_score: 
            dk_score = 100.0
        else: 
            dk_score = float(dk_score)
        if 'E' in bo_score or 'v' in bo_score: 
            bo_score = 100.0
        else: 
            bo_score = float(bo_score)
        if 'E' in bov_score or 'v' in bov_score: 
            bov_score = 100.0
        else: 
            bov_score = float(bov_score)
        if 'E' in bu_score or 'v' in bu_score: 
            bu_score = 100.0
        else: 
            bu_score = float(bu_score)
        avg = (dk_score + bo_score + bov_score + bu_score) / 4
        ml_averages[long_team] = avg

##############################################################################
# We now need to compare each team's moneyline on each website to the averages
# find best bets on each site
dk_best = ' '
dk_best_diff = -100000
dk_best_team = ""
for dk_team in dk_dict: 
    if change_name(dk_team) in ml_averages: 
        ml = dk_dict[dk_team]
        ml_avg = ml_averages[change_name(dk_team)]
        diff = float(ml) - ml_avg
        if diff > dk_best_diff: 
            dk_best_diff = diff
            dk_best_team = change_name(dk_team)
bo_best_diff = -100000
bo_best_team = ""
for bo_team in bo_dict:
    if bo_team in ml_averages: 
        ml = bo_dict[bo_team]
        ml_avg = ml_averages[bo_team]
        diff = float(ml) - ml_avg
        if(diff > bo_best_diff):
            bo_best_diff = diff
            bo_best_team = bo_team
bov_best_diff = -100000
bov_best_team = ""
for bov_team in bov_dict: 
    if bov_team in ml_averages: 
        ml = bov_dict[bov_team]
        ml_avg = ml_averages[bov_team]
        diff = float(ml) - ml_avg
        if(diff > bov_best_diff): 
            bov_best_diff = diff
            bov_best_team = bov_team
bu_best_diff = -100000
bu_best_team = ""
for bu_team in bu_dict: 
    if bu_team in ml_averages: 
        ml = bu_dict[bu_team]
        ml_avg = ml_averages[bu_team]
        diff = float(ml) - ml_avg
        if diff > bu_best_diff: 
            bu_best_diff = diff
            bu_best_team = bu_team

##############################################################################
# Finally, we need to find the bet that has the greatest difference from the
# average and print it out in a readable format
if max(dk_best_diff, bo_best_diff, bov_best_diff, bu_best_diff) == dk_best_diff: 
    print("The best value bet is " + dk_best_team + " " + dk_dict[change_name(dk_best_team)] + " on Draft Kings")
elif max(dk_best_diff, bo_best_diff, bov_best_diff, bu_best_diff) == bo_best_diff: 
    print("The best value bet is " + bo_best_team + " " + bo_dict[bo_best_team] + " on Bet Online")
elif max(dk_best_diff, bo_best_diff, bov_best_diff, bu_best_diff) == bov_best_diff: 
    print("The best value bet is " + bov_best_team + " " + bo_dict[bov_best_team] + " on Bovada")
else: 
    print("The best value bet is " + bu_best_team + " " + bu_dict[bu_best_team] + " on BetUS")
                                                         
          
    
    
    
    
