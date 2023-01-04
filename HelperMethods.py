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
    qb_replacement = [replacements['QB1'],replacements['QB2'],replacements['QB3']]
    qbs_indices = qbs.index
    if len(qbs_indices) == 0:
        return 0
    elif len(qbs_indices) == 1:
        return qb_replacement[0] - qbs_indices[0]
    elif len(qbs_indices) == 2:
        qb1 = qb_replacement[0] - qbs_indices[0]
        qb2 = qb_replacement[1] - qbs_indices[1]
        strength = qb1 * 0.67 + qb2 * 0.3
        return strength
    else:
        qb1 = qb_replacement[0] - qbs_indices[0]
        qb2 = qb_replacement[1] - qbs_indices[1]
        qb3 = qb_replacement[2] - qbs_indices[2]
        strength = qb1 * 0.67 + qb2 * 0.3 + qb3 * 0.03
        return strength

def te_strength(tes,replacements):
    te_replacement = [replacements['TE1'],replacements['TE2'],replacements['TE3']]
    tes_indices = tes.index
    if len(tes_indices) == 0:
        return 0
    elif len(tes_indices) == 1:
        return te_replacement[0] - tes_indices[0]
    elif len(tes_indices) == 2:
        te1 = te_replacement[0] - tes_indices[0]
        te2 = te_replacement[1] - tes_indices[1]
        strength = te1 * 0.67 + te2 * 0.3
        return strength
    else:
        te1 = te_replacement[0] - tes_indices[0]
        te2 = te_replacement[1] - tes_indices[1]
        te3 = te_replacement[2] - tes_indices[2]
        strength = te1 * 0.67 + te2 * 0.3 + te3 * 0.03
        return strength

def rb_strength(rbs,replacements):
    rb_replacement = [replacements['RB1'],replacements['RB2'],replacements['RB3'],replacements['RB4'],replacements['RB5'],replacements['RB6'],replacements['RB7']]
    rbs_indices = rbs.index
    if len(rbs_indices) == 0:
        return 0.0
    rb1 = rb_replacement[0] - rbs_indices[0]
    if len(rbs_indices) == 1:
        return rb1 * 0.4
    rb2 = rb_replacement[1] - rbs_indices[1]
    if len(rbs_indices) == 2:
        strength = rb1 * 0.4 + rb2 * 0.25
        return strength
    rb3 = rb_replacement[2] - rbs_indices[2]
    if len(rbs_indices) == 3:
        strength = rb1 * 0.4 + rb2 * 0.25 + rb3 * 0.15
        return strength
    rb4 = rb_replacement[3] - rbs_indices[3]
    if len(rbs_indices) == 4:
        strength = rb1 * 0.4 + rb2 * 0.25 + rb3 * 0.15 + rb4 * 0.10
        return strength
    rb5 = rb_replacement[4] - rbs_indices[4]
    if len(rbs_indices) == 5:
        strength = rb1 * 0.4 + rb2 * 0.25 + rb3 * 0.15 + rb4 * 0.10 + rb5 * 0.06
        return strength
    rb6 = rb_replacement[5] - rbs_indices[5]
    if len(rbs_indices) == 6:
        strength = rb1 * 0.4 + rb2 * 0.25 + rb3 * 0.15 + rb4 * 0.10 + rb5 * 0.06 + rb6 * 0.03
        return strength
    rb7 = rb_replacement[6] - rbs_indices[6]
    strength = rb1 * 0.4 + rb2 * 0.25 + rb3 * 0.15 + rb4 * 0.10 + rb5 * 0.06 + rb6 * 0.03 + rb7 * 0.01
    return strength

def wr_strength(wrs,replacements):
    wr_replacement = [replacements['WR1'],replacements['WR2'],replacements['WR3'],replacements['WR4'],replacements['WR5'],replacements['WR6'],replacements['WR7'],replacements['WR8']]
    wrs_indices = wrs.index
    if len(wrs_indices) == 0:
        return 0.0
    wr1 = wr_replacement[0] - wrs_indices[0]
    if len(wrs_indices) == 1:
        return wr1 * 0.4
    wr2 = wr_replacement[1] - wrs_indices[1]
    if len(wrs_indices) == 2:
        strength = wr1 * 0.4 + wr2 * 0.25
        return strength
    wr3 = wr_replacement[2] - wrs_indices[2]
    if len(wrs_indices) == 3:
        strength = wr1 * 0.4 + wr2 * 0.25 + wr3 * 0.15
        return strength
    wr4 = wr_replacement[3] - wrs_indices[3]
    if len(wrs_indices) == 4:
        strength = wr1 * 0.4 + wr2 * 0.25 + wr3 * 0.15 + wr4 * 0.10
        return strength
    wr5 = wr_replacement[4] - wrs_indices[4]
    if len(wrs_indices) == 5:
        strength = wr1 * 0.4 + wr2 * 0.25 + wr3 * 0.15 + wr4 * 0.10 + wr5 * 0.05
        return strength
    wr6 = wr_replacement[5] - wrs_indices[5]
    if len(wrs_indices) == 6:
        strength = wr1 * 0.4 + wr2 * 0.25 + wr3 * 0.15 + wr4 * 0.10 + wr5 * 0.05 + wr6 * 0.03
        return strength
    wr7 = wr_replacement[6] - wrs_indices[6]
    if len(wrs_indices) == 7:
        strength = wr1 * 0.4 + wr2 * 0.25 + wr3 * 0.15 + wr4 * 0.10 + wr5 * 0.05 + wr6 * 0.03 + wr7 * 0.01
        return strength
    wr8 = wr_replacement[7] - wrs_indices[7]
    strength = wr1 * 0.4 + wr2 * 0.25 + wr3 * 0.15 + wr4 * 0.10 + wr5 * 0.05 + wr6 * 0.03 + wr7 * 0.01 + wr8 * 0.01
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
    print(team)
    print(player)
    team.loc[player.index[0]] = player
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