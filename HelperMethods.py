import pandas as pd
import statistics
import re

def divide_team(team):
    qbs = pd.DataFrame(columns=["Player", "Team", "Bye", "POS"])
    rbs = pd.DataFrame(columns=["Player", "Team", "Bye", "POS"])
    wrs = pd.DataFrame(columns=["Player", "Team", "Bye", "POS"])
    tes = pd.DataFrame(columns=["Player", "Team", "Bye", "POS"])

    if len(team.index) == 0:
        return qbs, rbs, wrs, tes

    for idx in team.index:
        pos = team.at[idx, 'POS']
        #print(pos)
        if pos == 'QB':
            qbs = pd.concat([qbs, team.loc[[idx]]])
        if pos == 'RB':
            rbs = pd.concat([rbs, team.loc[[idx]]])
        if pos == 'TE':
            tes = pd.concat([tes, team.loc[[idx]]])
        if pos == 'WR':
            wrs = pd.concat([wrs, team.loc[[idx]]])

    return qbs, rbs, wrs, tes

def team_strength(team,replacements):
    qbs, rbs, wrs, tes = divide_team(team)
    QB = qb_strength(qbs,replacements)
    RB = rb_strength(rbs,replacements)
    WR = wr_strength(wrs,replacements)
    TE = te_strength(tes,replacements)
    return QB + RB + WR + TE

def qb_strength(qbs,replacements):
    qb_replacements = [replacements['QB1'],replacements['QB2'],replacements['QB3']]
    ranks = qbs.index
    num_cloggers = len(ranks) - 2

    qb1 = -25
    qb2 = -10
    ratings = [qb1, qb2]

    if len(ranks) < 3:
        for idx in range(0,len(ranks)):
            ratings[idx] = qb_replacements[idx] - ranks[idx]
    else:
        for idx in range(0,2):
            ratings[idx] = qb_replacements[idx] - ranks[idx]

    strength = 0

    for rating in ratings:
        strength += rating

    if num_cloggers > 0:
        strength = strength - num_cloggers * 30

    return strength

def te_strength(tes,replacements):
    te_replacements = [replacements['TE1'],replacements['TE2'],replacements['TE3']]
    ranks = tes.index
    num_cloggers = len(ranks) - 2

    te1 = -25
    te2 = -10
    ratings = [te1, te2]

    if len(ranks) < 3:
        for idx in range(0, len(ranks)):
            ratings[idx] = te_replacements[idx] - ranks[idx]
    else:
        for idx in range(0, 2):
            ratings[idx] = te_replacements[idx] - ranks[idx]

    strength = 0

    for rating in ratings:
        strength += rating

    if num_cloggers > 0:
        strength = strength - num_cloggers * 30

    return strength

def rb_strength(rbs,replacements):
    rb_replacements = [replacements['RB1'],replacements['RB2'],replacements['RB3'],replacements['RB4'],replacements['RB5'],replacements['RB6'],replacements['RB7']]
    ranks = rbs.index
    num_cloggers = len(ranks) - 6

    rb1 = -55
    rb2 = -45
    rb3 = -35
    rb4 = -25
    rb5 = -15
    rb6 = -5

    ratings = [rb1, rb2, rb3, rb4, rb5, rb6]

    if len(ranks) < 7:
        for idx in range(0, len(ranks)):
            ratings[idx] = rb_replacements[idx] - ranks[idx]
    else:
        for idx in range(0, 6):
            ratings[idx] = rb_replacements[idx] - ranks[idx]

    strength = 0

    for rating in ratings:
        strength += rating

    if num_cloggers > 0:
        strength = strength - num_cloggers * 20

    return strength

def wr_strength(wrs,replacements):
    wr_replacements = [replacements['WR1'],replacements['WR2'],replacements['WR3'],replacements['WR4'],replacements['WR5'],replacements['WR6'],replacements['WR7'],replacements['WR8']]
    ranks = wrs.index

    num_cloggers = len(ranks) - 7

    wr1 = -50
    wr2 = -40
    wr3 = -30
    wr4 = -20
    wr5 = -10
    wr6 = 0
    wr7 = 0

    ratings = [wr1, wr2, wr3, wr4, wr5, wr6, wr7]

    if len(ranks) < 8:
        for idx in range(0, len(ranks)):
            ratings[idx] = wr_replacements[idx] - ranks[idx]
    else:
        for idx in range(0, 7):
            ratings[idx] = wr_replacements[idx] - ranks[idx]

    strength = 0

    for rating in ratings:
        strength += rating

    if num_cloggers > 0:
        strength = strength - num_cloggers * 20

    return strength

def replacement_adp(adp):
    qbs, rbs, wrs, tes = divide_team(adp)
    replacements = {}
    qb_indices = qbs.index
    replacements['QB1'] = statistics.mean([qb_indices[8],qb_indices[9],qb_indices[10],qb_indices[11]])
    replacements['QB2'] = statistics.mean([qb_indices[18], qb_indices[19], qb_indices[20], qb_indices[21]])
    replacements['QB3'] = statistics.mean([qb_indices[28], qb_indices[29], qb_indices[30], qb_indices[31]])
    rb_indices = rbs.index
    replacements['RB1'] = statistics.mean([rb_indices[8],rb_indices[9],rb_indices[10],rb_indices[11]])
    replacements['RB2'] = statistics.mean([rb_indices[18],rb_indices[19],rb_indices[20],rb_indices[21]])
    replacements['RB3'] = statistics.mean([rb_indices[28], rb_indices[29], rb_indices[30], rb_indices[31]])
    replacements['RB4'] = statistics.mean([rb_indices[38], rb_indices[39], rb_indices[40], rb_indices[41]])
    replacements['RB5'] = statistics.mean([rb_indices[48], rb_indices[49], rb_indices[50], rb_indices[51]])
    replacements['RB6'] = statistics.mean([rb_indices[58], rb_indices[59], rb_indices[60], rb_indices[61]])
    replacements['RB7'] = statistics.mean([rb_indices[68], rb_indices[69], rb_indices[70], rb_indices[71]])
    wr_indices = wrs.index
    replacements['WR1'] = statistics.mean([wr_indices[8],wr_indices[9],wr_indices[10],wr_indices[11]])
    replacements['WR2'] = statistics.mean([wr_indices[18],wr_indices[19],wr_indices[20],wr_indices[21]])
    replacements['WR3'] = statistics.mean([wr_indices[28], wr_indices[29], wr_indices[30], wr_indices[31]])
    replacements['WR4'] = statistics.mean([wr_indices[38], wr_indices[39], wr_indices[40], wr_indices[41]])
    replacements['WR5'] = statistics.mean([wr_indices[48], wr_indices[49], wr_indices[50], wr_indices[51]])
    replacements['WR6'] = statistics.mean([wr_indices[58], wr_indices[59], wr_indices[60], wr_indices[61]])
    replacements['WR7'] = statistics.mean([wr_indices[68], wr_indices[69], wr_indices[70], wr_indices[71]])
    replacements['WR8'] = statistics.mean([wr_indices[78], wr_indices[79], wr_indices[80], wr_indices[81]])
    te_indices = tes.index
    replacements['TE1'] = statistics.mean([te_indices[8],te_indices[9],te_indices[10],te_indices[11]])
    replacements['TE2'] = statistics.mean([te_indices[18], te_indices[19], te_indices[20], te_indices[21]])
    replacements['TE3'] = statistics.mean([te_indices[28], te_indices[29], te_indices[30], te_indices[31]])
    return replacements

# returns best QB available and position on remaining draft board
def get_best_QB(adp):
    for i in adp.index.values.tolist():
        if adp.at[i,'POS'] == 'QB':
            return adp.loc[[i]], i

# returns best RB available and position on remaining draft board
def get_best_RB(adp):
    for i in adp.index.values.tolist():
        if adp.at[i,'POS'] == 'RB':
            return adp.loc[[i]], i

# returns best WR available and position on remaining draft board
def get_best_WR(adp):
    for i in adp.index.values.tolist():
        if adp.at[i,'POS'] == 'WR':
            return adp.loc[[i]], i

# returns best TE available and position on remaining draft board
def get_best_TE(adp):
    for i in adp.index.values.tolist():
        if adp.at[i,'POS'] == 'TE':
            return adp.loc[[i]], i

# removes a player from adp and returns adp
def removeFromBoard(adp,player):
    adp = adp.drop(player.index)
    return adp

def new_adp():
    adp = pd.read_csv("FantasyPros_2022_Overall_ADP_Rankings.csv", index_col="Rank")
    adp = dropCols(adp)
    adp = adp.dropna()
    adp = removeDigits(adp)
    adp = dropPos(adp)
    return adp

def dropCols(adp):
    adp = adp.drop("MFL",axis=1)
    adp = adp.drop("Fantrax",axis=1)
    adp = adp.drop("FFC",axis=1)
    adp = adp.drop("ESPN",axis=1)
    adp = adp.drop("RTSports",axis=1)
    adp = adp.drop("Sleeper",axis=1)
    adp = adp.drop("AVG",axis=1)
    return adp

# removes digits from position
def removeDigits(adp):
    ranks = adp.index.values.tolist()

    pattern = r'[0-9]'

    for rank in ranks:
        pos = adp.at[rank, 'POS']
        no_digits = re.sub(pattern, '', pos)
        adp.at[rank, 'POS'] = no_digits
    return adp

# drops player with invalid positions (Kicker/Defense)
def dropPos(adp):
    ranks = adp.index.values.tolist()
    for rank in ranks:
        pos = adp.at[rank, 'POS']
        if pos == "K" or pos == "DST" or pos == "LB" or pos == "DE":
            adp = adp.drop(rank)
    return adp

def draft_player(adp,team,player):
    adp = removeFromBoard(adp, player)
    #print("team columns: " + str(team.columns))
    #print("player columns: " + str(player.columns))
    #team.iloc[player.index[0]] = player
    team.loc[player.index[0]] = [player['Player'].iloc[0], player['Team'].iloc[0], player['Bye'].iloc[0], player['POS'].iloc[0]]
    #team = team.append(player)
    #team = pd.concat([team, player],axis = 1)    # , ignore_index=True
    return adp, team

def create_teams():
    team1 = pd.DataFrame(columns=["Player", "Team", "Bye", "POS"])
    team2 = pd.DataFrame(columns=["Player", "Team", "Bye", "POS"])
    team3 = pd.DataFrame(columns=["Player", "Team", "Bye", "POS"])
    team4 = pd.DataFrame(columns=["Player", "Team", "Bye", "POS"])
    team5 = pd.DataFrame(columns=["Player", "Team", "Bye", "POS"])
    team6 = pd.DataFrame(columns=["Player", "Team", "Bye", "POS"])
    team7 = pd.DataFrame(columns=["Player", "Team", "Bye", "POS"])
    team8 = pd.DataFrame(columns=["Player", "Team", "Bye", "POS"])
    team9 = pd.DataFrame(columns=["Player", "Team", "Bye", "POS"])
    team10 = pd.DataFrame(columns=["Player", "Team", "Bye", "POS"])
    return team1,team2,team3,team4,team5,team6,team7,team8,team9,team10

def separate_teams(teams):
    team1 = teams[0]
    team2 = teams[1]
    team3 = teams[2]
    team4 = teams[3]
    team5 = teams[4]
    team6 = teams[5]
    team7 = teams[6]
    team8 = teams[7]
    team9 = teams[8]
    team10 = teams[9]
    return team1,team2,team3,team4,team5,team6,team7,team8,team9,team10

def get_teams(adp):
    team1, team2, team3, team4, team5, team6, team7, team8, team9, team10 = create_teams()
    teams = [team1, team2, team3, team4, team5, team6, team7, team8, team9, team10]

    for round in range(1, 17):       #17
        for team_idx in range(0,10):
            team = teams[team_idx]
            target = adp.iloc[:1]
            adp, teams[team_idx] = draft_player(adp, team, target)
        print("Round " + str(round) + " Complete")
        teams.reverse()

        team1, team2, team3, team4, team5, team6, team7, team8, team9, team10 = separate_teams(teams)
    return team1, team2, team3, team4, team5, team6, team7, team8, team9, team10

def getBPA(adp):
    return adp.iloc[0]

def cpu_draft(adp,team,player):
    adp = cpu_remove_from_board(adp,player)
    #team = team.append(player)
    #print(player)
    team.loc[len(team.index)] = player
    #team = pd.concat([team, player],axis = 1)    # , ignore_index=True
    return adp, team

def cpu_remove_from_board(adp,player):
    adp = adp.drop(player.name)
    return adp