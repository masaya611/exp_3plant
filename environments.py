import sys
import numpy as np
import random

class Environment:
    """シミュレーションの実行環境を定義する"""

    def __init__(self,args):
        self.args = args
        self.n = args.num_pv # Agentの数
        self.money_reward = 0
        self.supply = 0
        self.total_cost = 0
        self.total_supply = 0
        self.flag = [0,0,0]
        self.config = {"SolarPV":[25, 25, 25, 25, 50, 50,
                                100, 100, 300, 300, 400, 400,
                                400, 400, 300, 300, 100, 100,
                                50, 50, 25, 25, 25, 25],
                        "Grid_price":10,
                        "agent1":[600,5],
                        "agent2":[25,9],
                        "agent3":[8,1]}
        
        """
        self.config = { "SolarPV":[150, 150, 150, 150, 150, 150,
                                    150, 150, 150, 150, 150, 150,
                                    150, 150, 150, 150, 150, 150,
                                    150, 150, 150, 150, 150, 150]}
        """
    @property
    def hour(self):
        """現在の時間を返す"""
        return self.steps % 24

    @property
    def next_hour(self):
        """次の状態の時間を返す"""
        return (self.steps + 1) % 24

    def reset(self):
        #state reset (time, num_activate)
        observations = [[0,1], [0,1], [0,1]]
        #reward reset
        self.total_cost = 0
        self.flag = [0,0,0]
        self.oper_time = [self.config["agent1"][0],self.config["agent2"][1],self.config["agent3"][2],]
        return observations

    def step(self, action_n, obs_n):
        self.total_supply += self.config["SolarPV"][self.steps]
        penalty = [0, 0, 0] # [0 for _ in range(self.num_agent)]
        done = [False for _ in range(self.n)]
        operate = [0, 0, 0] #len:agent
        for i in range(len(action_n)):
            if action_n[i][0] >= 0:
                operate[i] = 1 #ON
                self.flag[i] = 1
            else:
                operate[i] = 0 #OFF

#-----編集中2----------------------------------------------------------------
        
        # 報酬計算
        for i in range(len(obs_n)):
            if obs_n[i][1] == 0 and operate[i] == 1:
                """稼働不可の時に、稼働のアクションを出した場合"""
                cost = - 100000

            if self.oper_time[i]>0 and self.flag[i]== 1:

        if flag[0] == 1 and flag[1] == 1 and flag[2] == 1:
            total_demand = 600*operate[i] + 25*operate[i] + 1*operate[i]
            balance = self.config["SolarPV"][self.steps] - total_demand
            # print("balance", balance)
            if balance >= 0:
                if operate[0] == 0 and operate[1] == 0 and operate[2] == 0:
                    cost = -5000
                else:
                    cost = 0
            else:
                cost = balance * self.config["Grid_price"]
            reward_n = [cost, cost, cost]
        else:
            reward_n = [cost, cost, cost]

        # done条件1
        if self.steps!=0 and self.steps % 23==0:    
            done = [True for _ in range(self.n)]
        # next_obsの計算
        operation_time = [0, 0, 0]
        terminal = [1, 1, 1] #稼働時間分の稼働が終わったかどうか
        for i in range(len(obs_n)):
            operation_time[i] = obs_n[i][1]-operate[i]
            if operation_time[i] <= 0:
                operation_time[i] = 0
                terminal[i] = 0
        if self.steps+1 == 24:
            next_obs_n = [[0,5], [0,9], [0,8]]
        else:
            next_obs_n = [[(self.steps+1)*terminal[i], operation_time[i]] for i in range(self.n)]
        
        # done条件2
        if obs_n[0][1]==0 and obs_n[1][1]==0 and obs_n[2][1]==0:
            done = [True for _ in range(self.n)]
        #2reward
        return next_obs_n, reward_n, done, {}

    def render(self):
        pass
#-----編集中2'----------------------------------------------------------------
