import random
import pandas as pd
from HelperMethods import *

class envr():
    def __init__(self):
        super(envr, self).__init__()
        self.action_space = ['QB','RB','WR','TE']
        self.team = pd.DataFrame(columns=["Player", "Team", "Bye", "POS"])
        self.adp = new_adp()
        self.power = 0.0
        self.state = []
        self.te_power = 0.0
        self.wr_power = 0.0
        self.qb_power = 0.0
        self.rb_power = 0.0
        self.pos_breakdown = [0,0,0,0]
    def sample(self):
        p = random.randint(0,3)
        return p
    def reset(self):
        self.adp = new_adp()
        self.replacements = replacement_adp(self.adp)
        best_qb, qb_index = get_best_QB(self.adp)
        best_rb, rb_index = get_best_RB(self.adp)
        best_wr, wr_index = get_best_WR(self.adp)
        best_te, te_index = get_best_TE(self.adp)
        self.state = [0, 0, 0, 0, 0.0, 0.0, 0.0, 0.0, qb_index, rb_index, wr_index, te_index]
        self.team = pd.DataFrame(columns=["Player", "Team", "Bye", "POS"])
        self.power = 0.0
        self.pos_breakdown = [0,0,0,0]
        return self.state
    def step(self,action):
        best_qb, qb_index = get_best_QB(self.adp)
        best_rb, rb_index = get_best_RB(self.adp)
        best_wr, wr_index = get_best_WR(self.adp)
        best_te, te_index = get_best_TE(self.adp)

        if action == 0:
            self.adp, self.team = draft_player(self.adp,self.team,best_qb)
        elif action == 1:
            self.adp, self.team = draft_player(self.adp, self.team, best_rb)
        elif action == 2:
            self.adp, self.team = draft_player(self.adp, self.team, best_wr)
        elif action == 3:
            self.adp, self.team = draft_player(self.adp, self.team, best_te)

        qbs, rbs, wrs, tes = divide_team(self.team)
        self.pos_breakdown = [len(qbs), len(rbs), len(wrs), len(tes)]

        self.qb_power = qb_strength(qbs, self.replacements)
        self.rb_power = rb_strength(rbs, self.replacements)
        self.wr_power = wr_strength(wrs, self.replacements)
        self.te_power = te_strength(tes, self.replacements)
        old_power = self.power
        new_power = self.qb_power + self.rb_power + self.wr_power + self.te_power
        reward = new_power - old_power
        self.power = new_power
        self.state = [self.pos_breakdown[0], self.pos_breakdown[1], self.pos_breakdown[2], self.pos_breakdown[3],
                      self.qb_power, self.rb_power, self.wr_power, self.te_power, qb_index, rb_index, wr_index, te_index]
        return self.state, reward

    def cpu_draft(self):
        bpa = getBPA(self.adp)
        dummy_team = pd.DataFrame(columns=["Player", "Team", "Bye", "POS"])
        self.adp, dummy_team = cpu_draft(self.adp, dummy_team, bpa)

        best_qb, qb_index = get_best_QB(self.adp)
        best_rb, rb_index = get_best_RB(self.adp)
        best_wr, wr_index = get_best_WR(self.adp)
        best_te, te_index = get_best_TE(self.adp)

        self.state = [self.pos_breakdown[0], self.pos_breakdown[1], self.pos_breakdown[2], self.pos_breakdown[3],
                      self.qb_power, self.rb_power, self.wr_power, self.te_power, qb_index, rb_index, wr_index, te_index]
        return self.state

    def get_team(self):
        return self.team

    def get_power(self):
        return self.power
