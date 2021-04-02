import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import timedelta, date
import time

# Type represents whether you would like a Dataframe of names, bref_id, mlb_id
def getLineups(date, dfType):
    # sample url https://www.baseballpress.com/lineups/2021-03-19
    # Scrape data for given days lineups
    url = "https://www.baseballpress.com/lineups/"+date
    raw_data = requests.get(url)

    # Set arrays
    df = pd.DataFrame()
    players = []
    away = []
    home = []
    teams = []
    pitchers = []

    # Use lxml because html misses players
    soup = BeautifulSoup(raw_data.text, 'lxml')
    for lineupCard in soup.findAll('div', {'class': 'lineup-card'}):
        header = lineupCard.find('div', {'class': 'lineup-card-header'})
        for team_tags in header.findAll('div', {'class': 'col col--min c'}):
            a = team_tags.find('a')
            if (a != None):
                team_div = a.find('div')
                teams.append(team_div.getText())
        for pitcher_nodes in header.findAll('div', {'class': 'col col--min player'}):
            pitcher = pitcher_nodes.find('a')
            if pitcher is None:
                pitchers.append('TBD')
            else:
                if dfType == 'names':
                    comp_name = pitcher.find('span', {'class': 'desktop-name'})
                    if comp_name != None:
                        pitchers.append(comp_name.getText())
                    else:
                        pitchers.append(pitcher.getText())
                elif dfType == 'mlb':
                    pitchers.append(pitcher['data-mlb'])
                elif dfType == 'bref':
                    pitchers.append(pitcher['data-bref'])
        body = lineupCard.find('div', {'class': 'lineup-card-body'})
        for item in body.select(".player > a.player-link"):
            # player_name = item.get('data-mlb') #.split("/")[-2].replace("+"," ")
            if dfType == 'names':
                comp_name = item.find('span', {'class': 'desktop-name'})
                if comp_name != None:
                    players.append(comp_name.getText())
                else:
                    players.append(item.getText())
            elif dfType == 'mlb':
                players.append(item['data-mlb'])
            elif dfType == 'bref':
                players.append(item['data-bref'])
        if len(players) != 18:
            away = [pitchers[0], 'TBA', 'TBA', 'TBA', 'TBA', 'TBA', 'TBA', 'TBA', 'TBA', 'TBA']
            home = [pitchers[1], 'TBA', 'TBA', 'TBA', 'TBA', 'TBA', 'TBA', 'TBA', 'TBA', 'TBA']
        else:
            away = [pitchers[0], players[0], players[1], players[2], players[3], players[4], players[5], players[6],
                    players[7], players[8]]
            home = [pitchers[1], players[9], players[10], players[11], players[12], players[13], players[14],
                    players[15], players[16], players[17]]
        df[teams[0]] = away
        df[teams[1]] = home
        players = []
        away = []
        home = []
        teams = []
        pitchers = []
    return df