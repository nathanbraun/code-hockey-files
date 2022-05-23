##############
# basic python
##############

##########################
# how to read this chapter
##########################
1 + 1

##########
# comments
##########

# print the result of 1 + 1
print(1 + 1)

###########
# variables
###########

goals_scored = 2

goals_scored
3*goals_scored

goals_scored = goals_scored + 1
goals_scored

####################
# types of variables
####################

penalty_minutes = 15  # int
puck_speed = 82.5  # float

starting_lw = 'David Perron'
starting_c = "Ryan O'Reilly"

type(starting_lw)

type(penalty_minutes)

starters = f'{starting_c}, {starting_lw}, etc.'
starters

# string methods
'do you believe in miracles!?'.upper()

'Bernie Geoffrion'.replace('Bernie', 'Boom Boom')

####################################
# How to figure things out in Python
####################################
foo = 'sidney crosby'  # alt if 'sidnedy crosby'? doesn't work in REPL

'sidney crosby'.capitalize()

'  sidney crosby'
'sidney crosby'

'  sidney crosby'.lstrip()

#######
# bools
#######
team1_goals = 2
team2_goals = 1

# and these are all bools:
team1_won = team1_goals > team2_goals
team2_won = team1_goals < team2_goals
teams_tied = team1_goals == team2_goals
teams_did_not_tie = team1_goals != team2_goals

type(team1_won)
teams_did_not_tie

# error because test for equality is ==, not =
# teams_tied = (team1_pts = team2_pts)  # commented out since it throws an error

shootout = (team1_goals > 4) and (team2_goals > 4)
at_least_one_good_team = (team1_goals > 4) or (team2_goals > 3)
you_guys_are_bad = not ((team1_goals > 1) or (team2_goals > 1))
meh = not (shootout or at_least_one_good_team or you_guys_are_bad)

###############
# if statements
###############
if team1_won:
  message = "Nice job team 1!"
elif team2_won:
  message = "Way to go team 2!!"
else:
  message = "must have tied!"

message

#################
# container types
#################

# lists
first_line = ['alex ovechkin', 'nicklas backstrom', 'anthony mantha']

first_line[0]
first_line[0:2]
first_line[-2:]

# dicts
first_line_dict = {'lw': 'alex ovechkin',
                   'c': 'nicklas backstrom',
                   'rw': 'anthony mantha'}

first_line_dict['lw']
first_line_dict['rd'] = 'john carlson'

first_line_dict

pos = 'lw'
first_line_dict[pos]

# unpacking
lw, rw = ['alex ovechkin', 'anthony mantha']

lw = 'alex ovechkin'
c = 'nicklas backstrom'

# gives an error - n of variables doesn't match n items in list
# lw, c = ['alex ovechkin', 'nicklas backstrom', 'anthony mantha']  # commented out w/ error

#######
# loops
#######

# looping over a list
first_line = ['alex ovechkin', 'nicklas backstrom', 'anthony mantha']

first_line_upper = ['', '', '']
i = 0
for player in first_line:
    first_line_upper[i] = player.title()
    i = i + 1

first_line_upper

for x in first_line_dict:
    print(f"position: {x}")

for x in first_line_dict:
   print(f"position: {x}")
   print(f"player: {first_line_dict[x]}")

for x, y in first_line_dict.items():
    print(f"position: {x}")
    print(f"player: {y}")

################
# comprehensions
################

# lists
first_line
first_line_proper = [x.title() for x in first_line]
first_line_proper

first_line_proper_alt = [y.title() for y in first_line]

type([x.title() for x in first_line])
[x.title() for x in first_line][:2]

first_line_last_names = [full_name.split(' ')[1] for full_name in first_line]
first_line_last_names

full_name = 'alex ovechkin'
full_name.split(' ')
full_name.split(' ')[1]

first_line_a_only = [
    x for x in first_line if x.startswith('a')]
first_line_a_only

'alex ovechkin'.startswith('a')
'nicklas backstrom'.startswith('a')
'anthony mantha'.startswith('a')

first_line_a_only_title = [
    x.title() for x in first_line if x.startswith('a')]
first_line_a_only_title

# dicts
salary_per_player = {
    'alex ovechkin': 10000000 , 'nicklas backstrom': 12000000, 'anthony mantha': 5700000}

salary_m_per_upper_player = {
    name.upper(): salary/1000000 for name, salary in salary_per_player.items()}

salary_m_per_upper_player

sum([1, 2, 3])

sum([salary for _, salary in salary_per_player.items()])

###########
# functions
###########
len(['alex ovechkin', 'nicklas backstrom', 'anthony mantha'])

n_goals = len(['alex ovechkin', 'nicklas backstrom', 'anthony mantha'])
n_goals

4 + len(['alex ovechkin', 'nicklas backstrom', 'anthony mantha'])

def team_pts(wins, losses, ot_losses):
    """
    multi line strings in python are between three double quotes

    it's not required, but the convention is to put what the fn does in one of these multi line strings (called "docstring") right away in function

    this function takes number of wins, overtime losses, and regular season
    losses and returns team points
    """
    return 2*wins + 1*ot_losses

team_pts(62, 16, 4)

# this gives an error: wins is only defined inside team_pts
# print(wins)

def team_pts_noisy(wins, losses, ot_losses):
    """
    this function takes number of wins, overtime losses, and regular season
    losses and returns team points

    it also prints out wins
    """
    print(wins)  # works here since we're inside fn
    return 2*wins + 1*ot_losses

team_pts_noisy(62, 16, 4)

# side effects
def is_player_on_team(player, team):
    """
    take a player string and team list and check whether the player is on team

    do this by adding the player to the team, then returning True if the player
    shows up 2 or more times
    """
    team.append(player)
    return team.count(player) >= 2

roster_list = ['alex ovechkin', 'nicklas backstrom', 'anthony mantha']
is_player_on_team('sidney crosby', roster_list)

roster_list
is_player_on_team('sidney crosby', roster_list)

roster_list

# function arguments
## Positional vs Keyword Arguments

team_pts(62, 16, 4)
team_pts(62, 4, 16)  # order matters!

team_pts?

team_pts(wins=62, ot_losses=4, losses=16)  # keyword argumensts

team_pts(62, losses=16, ot_losses=4)

# error: keyword arguments can't come before positional arguments
# team_pts(ot_losses=4, 62, 16)

## Default Values for Arguments

# error: leaving off an argument
# team_pts(62, 16)

def team_pts_wdefault(wins, losses, ot_losses=0):
    """
    this function takes number of wins, overtime losses, and regular season
    losses and returns team points
    """
    return 2*wins + 1*ot_losses

team_pts_wdefault(62, 16)

# error: leaving out required argument
# team_pts_wdefault(62)

# error: required arguments need to come first
# def team_pts_wdefault_wrong(wins=0, losses, ot_losses=0):
#     """
#     this function takes number of wins, overtime losses, and regular season
#     losses and returns team points
#     """
#     return 2*wins + 1*ot_losses


#####################################
# functions that take other functions
#####################################

def do_to_list(working_list, working_fn, desc):
    """
    this function takes a list, a function that works on a list, and a
    description

    it applies the function to the list, then returns the result along with
    description as a string
    """

    value = working_fn(working_list)

    return f'{desc} {value}'

def last_elem_in_list(working_list):
    """
    returns the last element of a list.
    """
    return working_list[-1]

positions = ['LW', 'C', 'RW', 'LD', 'RD', 'GK']

do_to_list(positions, last_elem_in_list, "last element in your list:")
do_to_list([1, 2, 4, 8], last_elem_in_list, "last element in your list:")

do_to_list(positions, len, "length of your list:")

do_to_list([2, 3, 7, 1.3, 5], lambda x: 3*x[0], "first element in your list times 3 is:")

# normally imports like this would be at the top of the file
import os

os.cpu_count()

from os import path

# change this to the location of your data
DATA_DIR = '/Users/nathan/fantasybook/data'
path.join(DATA_DIR, 'adp_2017.csv')
os.path.join(DATA_DIR, 'adp_2017.csv')  # alt if we didn't want to import path
