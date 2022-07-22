"""
Answers to the end of chapter exercises for Python chapter.

Questions with written (not code) answers are inside triple quotes.
"""

###############################################################################
# 2.1
###############################################################################
"""
a) `_throwaway_data`. Valid. Python programmers often start variables with `_`
   if they're throwaway or temporary, short term variables.
b) `n_shots`. Valid.
c) `1st_period`. Not valid. Can't start with a number.
d) `shotsOnGoal`. Valid, though convention is to split words with `_`, not camelCase.
e) `made_2022_playoffs`. Valid. Numbers OK as long as they're not in the first
    spot
f) `player position`. Not valid. No spaces
g) `@home_or_away`. Not valid. Only non alphanumeric character allowed is `_`
h) `'num_penalties'`. Not valid. A string (wrapped in quotes), not a variable
    name. Again, only non alphanumeric character allowed is `_`
"""

###############################################################################
# 2.2
###############################################################################
penalty_minutes = 0
penalty_minutes = penalty_minutes + 2
penalty_minutes = penalty_minutes + 5

penalty_minutes # 7

###############################################################################
# 2.3
###############################################################################
def commentary(player, play):
    return f'{player} with the {play}!'

commentary('Crosby', 'goal')

###############################################################################
# 2.4
###############################################################################
"""
It's a string method, so what might `islower()` in the context of a string?
I'd say it probably returns whether or not the string is lowercase.

A function "is *something*" usually returns a yes or no answer (is it
something or not), which would mean it returns a boolean.

We can test it like:
"""

'sidney crosby'.islower()  # should return True
'Sidney Crosby'.islower()  # should return False

###############################################################################
# 2.5
###############################################################################
def is_oreilly(player):
    return player.replace("'", '').lower() == 'ryan oreilly'

is_oreilly('sidney crosby')
is_oreilly("Ryan O'Reilly")
is_oreilly("RYAN OREILLY")

###############################################################################
# 2.6
###############################################################################
def a_lot_of_goals(goals):
    if goals >= 4:
        return f'{goals} is a lot of goals!'
    else:
        return f"{goals} is not that many goals"

a_lot_of_goals(2)
a_lot_of_goals(6)

###############################################################################
# 2.7
###############################################################################
roster = ['alex ovechkin', 'nicklas backstrom', 'anthony mantha']

roster[0:2]
roster[:2]
roster[:-1]
[x for x in roster if x != 'anthony mantha']
[x for x in roster if x in ['alex ovechkin', 'nicklas backstrom']]

###############################################################################
# 2.8
###############################################################################
shot_info = {'shooter': 'Connor McDavid', 'is_slap': False, 'went_in': False}

# a
shot_info['shooter'] = 'Nathan MacKinnon'
shot_info

# b
def toggle_slap(info):
    info['is_slap'] = not info['is_slap']
    return info

shot_info
toggle_slap(shot_info)

###############################################################################
# 2.9
###############################################################################
"""
a) No. `'is_penalty_shot'` hasn't been defined.
b) No, `shooter` is a variable that hasn't been defined, the key is
`'shooter'`.
c) Yes.
"""

###############################################################################
# 2.10
###############################################################################
roster = ['alex ovechkin', 'nicklas backstrom', 'anthony mantha']

# a
for x in roster:
  print(x.split(' ')[-1])

# b
{player: len(player) for player in roster}

###############################################################################
# 2.11
###############################################################################
roster_dict = {'lw': 'alex ovechkin',
               'c': 'nicklas backstrom',
               'rw': 'anthony mantha',
               'rd': 'john carlson'}

# a
[pos for pos in roster_dict]

# b
[player for _, player in roster_dict.items()
    if player.split(' ')[-1][0] in ['b', 'm']]

###############################################################################
# 2.12
###############################################################################
# a
def mapper(my_list, my_function):
    return [my_function(x) for x in my_list]

# b
shots = [48, 40, 38, 39, 40, 52]

mapper(shots, lambda x: round(x*0.09))
