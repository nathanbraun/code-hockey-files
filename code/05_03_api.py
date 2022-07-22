import requests
import json
from pandas import DataFrame, Series
import pandas as pd

#######
# teams
#######

# after looking at url in browser, get what you need in python
teams_url = 'https://statsapi.web.nhl.com/api/v1/teams'
teams_resp = requests.get(teams_url)

teams_json = teams_resp.json()

# with open('./data/json/teams.json') as f:
#     teams_json = json.load(f)

teams_json
teams_json.keys()

type(teams_json['teams'])

teams_json['teams'][0]

nj_nested = teams_json['teams'][0]

nj_flat = {key: value for key, value in nj_nested.items()
    if type(value) is not dict}
nj_flat

nj_nested['venue']

nj_flat['venue_name'] = nj_nested['venue']['name']
nj_flat['venue_city'] = nj_nested['venue']['city']

nj_flat['franchise_id'] = nj_nested['franchise']['franchiseId']
nj_flat['division_id'] = nj_nested['division']['id']
nj_flat['convference_id'] = nj_nested['conference']['id']

nj_flat

def flatten_team(nested):
    flat = {key: value for key, value in nested.items() if type(value) is not dict}

    flat['venue_name'] = nested['venue']['name']
    flat['venue_city'] = nested['venue']['city']
    flat['franchise_id'] = nested['franchise']['franchiseId']
    flat['division_id'] = nested['division']['id']
    flat['convference_id'] = nested['conference']['id']

    return flat

df_teams = DataFrame([flatten_team(x) for x in teams_json['teams']])
df_teams.head()

#########
# rosters
#########
rosters_url = 'https://statsapi.web.nhl.com/api/v1/teams?expand=team.roster'
rosters_resp = requests.get(rosters_url)
rosters_json = rosters_resp.json()

# with open('./data/json/rosters.json') as f:
#     rosters_json = json.load(f)

# specific instance
nj = rosters_json['teams'][0]
nj_roster = nj['roster']['roster']
jb = nj_roster[0]

jb

jb_flat = {}
jb_flat['person_id'] = jb['person']['id']
jb_flat['name'] = jb['person']['fullName']
jb_flat['jersey'] = jb['jerseyNumber']
jb_flat['position'] = jb['position']['code']

jb_flat

def flatten_player(nested):
    flat = {}
    flat['person_id'] = nested['person']['id']
    flat['name'] = nested['person']['fullName']
    flat['position'] = nested['position']['code']
    return flat

df_nj = DataFrame([flatten_player(x) for x in nj_roster])

def process_roster1(team_dict):
    roster = team_dict['roster']['roster']
    df = DataFrame([flatten_player(x) for x in roster])
    return df

df_nj2 = process_roster1(nj)
df_nj2.head()

df_sea = process_roster1(rosters_json['teams'][-1])
df_sea.head()

def process_roster2(team_dict):
    roster = team_dict['roster']['roster']
    df = DataFrame([flatten_player(x) for x in roster])
    df['team_id'] = team_dict['id']
    df['team_name'] = team_dict['name']
    return df

df_nj3 = process_roster2(nj)
df_nj3.head()

league_rosters = pd.concat([process_roster2(x) for x in rosters_json['teams']],
        ignore_index=True)

league_rosters.sample(5)

###################
# player stats data
###################
player_id = 8471675  # sidney crosby
stats_url = f'https://statsapi.web.nhl.com/api/v1/people/{player_id}/stats?stats=yearByYear'

crosby_resp = requests.get(stats_url)
crosby_json = crosby_resp.json()

# with open('./data/json/crosby.json') as f:
#     crosby_json = json.load(f)

crosby_stats_0 = crosby_json['stats'][0]['splits'][0]
crosby_stats_0

def flatten_player_year_stats(stats_dict):
    stats_flat = stats_dict['stat']
    stats_flat['season'] = stats_dict['season']
    stats_flat['team'] = stats_dict['team']['name']
    stats_flat['league'] = stats_dict['league']['name']
    return stats_flat

flatten_player_year_stats(crosby_stats_0)

crosby_stats_all = DataFrame([flatten_player_year_stats(x) for x in
    crosby_json['stats'][0]['splits']])
crosby_stats_all[['season', 'team', 'league', 'assists', 'goals', 'games']]

def hist_stats_by_player_year(player_id):
    stats_url = f'https://statsapi.web.nhl.com/api/v1/people/{player_id}/stats?stats=yearByYear'
    stats_resp = requests.get(stats_url)
    stats_json = stats_resp.json()
    return DataFrame([flatten_player_year_stats(x) for x in stats_json['stats'][0]['splits']])

ovechkin_stats = hist_stats_by_player_year(8471214)
ovechkin_stats[['season', 'team', 'league', 'assists', 'goals', 'games']].head()
