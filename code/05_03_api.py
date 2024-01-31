import requests
import json
from pandas import DataFrame, Series
import pandas as pd

#################
# teams/standings
#################

# after looking at url in browser, get what you need in python
standings_url = 'https://api-web.nhle.com/v1/standings/2024-01-21'
standings_resp = requests.get(standings_url)

standings_json = standings_resp.json()

# with open('./data/json/standings.json') as f:
#     standings_json = json.load(f)

standings_json
standings_json.keys()

type(standings_json['standings'])
standings_json['standings'][0]

canucks_nested = standings_json['standings'][0]

canucks_flat = {key: value for key, value in canucks_nested.items() if
    type(value) not in (dict, list)}
canucks_flat

canucks_nested['teamName']

canucks_flat['teamName'] = canucks_nested['teamName']['default']

{key: value for key, value in canucks_nested.items() if
    type(value) in (dict, list)}

canucks_flat['placeName'] = canucks_nested['placeName']['default']
canucks_flat['teamCommonName'] = canucks_nested['teamCommonName']['default']
canucks_flat['teamAbbrev'] = canucks_nested['teamAbbrev']['default']

def flatten_team(nested):
    flat = {key: value for key, value in nested.items() if type(value) not in (dict, list)}
    flat['teamName'] = nested['teamName']['default']
    flat['placeName'] = nested['placeName']['default']
    flat['teamCommonName'] = nested['teamCommonName']['default']
    flat['teamAbbrev'] = nested['teamAbbrev']['default']

    return flat

df_teams = DataFrame([flatten_team(x) for x in standings_json['standings']])
df_teams[['teamAbbrev', 'wins', 'losses', 'ties', 'goalFor', 'goalAgainst']].head(10)

#########
# rosters
#########

tor_roster_url = 'https://api-web.nhle.com/v1/roster/TOR/20232024'
tor_roster_resp = requests.get(tor_roster_url)
tor_roster_json = tor_roster_resp.json()

# with open('./data/json/tor_roster.json') as f:
#     teams_json = json.load(f)

tor_roster_json.keys()

forward1 = tor_roster_json['forwards'][0]
forward1

forward1_flat = {key: value for key, value in forward1.items()
                 if type(value) not in (dict, list)}
forward1_flat['firstName'] = forward1['firstName']['default']
forward1_flat['lastName'] = forward1['lastName']['default']
forward1_flat['birthCity'] = forward1['birthCity']['default']
forward1_flat['birthStateProvince'] = forward1['birthStateProvince']['default']

forward1_flat

def flatten_player(nested):
    flat = {key: value for key, value in nested.items() if type(value) not in
        (dict, list)}
    flat['firstName'] = nested['firstName']['default']
    flat['lastName'] = nested['lastName']['default']
    flat['birthCity'] = nested['birthCity']['default']
    flat['birthStateProvince'] = nested['birthStateProvince']['default']

    return flat

# commented out because it returns an error
# df_fwd = DataFrame([flatten_player(x) for x in tor_roster_json['forwards']])

def flatten_player2(nested):
    flat = {key: value for key, value in nested.items() if type(value) not in
        (dict, list)}
    flat['firstName'] = nested['firstName']['default']
    flat['lastName'] = nested['lastName']['default']
    flat['birthCity'] = nested['birthCity']['default']

    if 'birthStateProvince' in nested.keys():
        flat['birthStateProvince'] = nested['birthStateProvince']['default']

    return flat

df_fwd = DataFrame([flatten_player2(x) for x in tor_roster_json['forwards']])

def roster_by_team1(team):
    roster_url = f'https://api-web.nhle.com/v1/roster/{team}/20232024'
    roster_resp = requests.get(roster_url)
    roster_json = roster_resp.json()

    df_fwd = DataFrame([flatten_player2(x) for x in roster_json['forwards']])
    df_def = DataFrame([flatten_player2(x) for x in roster_json['defensemen']])
    df_g = DataFrame([flatten_player2(x) for x in roster_json['goalies']])

    return pd.concat([df_fwd, df_def, df_g], ignore_index=True)
    
df_tor = roster_by_team1('TOR')
df_tor.drop('headshot', axis=1)

df_chi = roster_by_team1('CHI')
df_chi.drop('headshot', axis=1).head()

def roster_by_team2(team):
    roster_url = f'https://api-web.nhle.com/v1/roster/{team}/20232024'
    roster_resp = requests.get(roster_url)
    roster_json = roster_resp.json()

    df_fwd = DataFrame([flatten_player2(x) for x in roster_json['forwards']])
    df_def = DataFrame([flatten_player2(x) for x in roster_json['defensemen']])
    df_g = DataFrame([flatten_player2(x) for x in roster_json['goalies']])

    df_all = pd.concat([df_fwd, df_def, df_g], ignore_index=True)
    df_all['team'] = team
    return df_all

df_sea = roster_by_team2('SEA')
df_sea.drop('headshot', axis=1).head()

league_rosters = pd.concat([roster_by_team2(x) for x in
    df_teams['teamAbbrev']], ignore_index=True)

league_rosters[['id', 'firstName', 'lastName', 'positionCode', 'team']].sample(5)

###################
# player stats data
###################
player_id = 8471675  # sidney crosby
stats_url = f'https://api-web.nhle.com/v1/player/{player_id}/game-log/20232024/2'

crosby_resp = requests.get(stats_url)
crosby_json = crosby_resp.json()

# with open('./data/json/crosby.json') as f:
#     crosby_json = json.load(f)

crosby_stats_0 = crosby_json['gameLog'][0]
crosby_stats_0

def flatten_game_log(nested):
    flat = {key: value for key, value in nested.items()
        if type(value) is not dict}
    return flat

flatten_game_log(crosby_stats_0)

crosby_stats_all = DataFrame([flatten_game_log(x) for x in
    crosby_json['gameLog']])

crosby_stats_all[['gameDate', 'opponentAbbrev', 'goals', 'assists', 'plusMinus']].head(10)


def games_by_player(player_id):
    stats_url = f'https://api-web.nhle.com/v1/player/{player_id}/game-log/20232024/2'
    stats_resp = requests.get(stats_url)
    stats_json = stats_resp.json()
    return DataFrame([flatten_game_log(x) for x in stats_json['gameLog']])

mcdavid_stats = games_by_player(8478402)
mcdavid_stats[['gameDate', 'opponentAbbrev', 'goals', 'assists', 'plusMinus']].head()

################################################################################
################################################################################

## note: this part isn't meant to be run
## i (nate) am running this Wed 1/31/24 to save data we'll load above
## 
## including here to make it clearer this saved data above just comes from APIs

# standings_url = 'https://api-web.nhle.com/v1/standings/2024-01-21'
# tor_roster_url = 'https://api-web.nhle.com/v1/roster/TOR/20232024'
# stats_url = f'https://api-web.nhle.com/v1/player/{player_id}/game-log/20232024/2'

# standings_resp = requests.get(standings_url)
# tor_roster_resp = requests.get(tor_roster_url)
# crosby_resp = requests.get(stats_url)

# standings_json = standings_resp.json()
# tor_roster_json = tor_roster_resp.json()
# crosby_json = crosby_resp.json()

# with open('./data/json/standings.json', 'w') as f:
#     json.dump(standings_json, f)

# with open('./data/json/tor_roster.json', 'w') as f:
#     json.dump(tor_roster_json, f)

# with open('./data/json/crosby.json', 'w') as f:
#     json.dump(crosby_json, f)

