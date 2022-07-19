import sys
import numpy as np
import random


class Environment:
    """シミュレーションの実行環境を定義する"""
    total_supply: int

    def __init__(self, args):
        self.finish_oper = None
        self.steps = None
        self.oper_time = None
        self.args = args
        self.n = args.num_pv  # Agentの数
        self.money_reward = 0
        self.supply = 0
        self.total_consumption = 0
        self.total_supply = 0
        self.flag = [0, 0, 0]
        self.config = {"SolarPV": (25, 25, 25, 25, 50, 50,
                                   100, 100, 300, 300, 400, 400,
                                   400, 400, 300, 300, 100, 100,
                                   50, 50, 25, 25, 25, 25),
                       "Grid_price": 10,
                       "agent1": [600, 5, 19],  # [kWh/h, operation time, operation limit]
                       "agent2": [25, 9, 15],
                       "agent3": [1, 8, 16]}

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

    def _reset_total_supply(self, balance):
        if 0 <= balance:
            return
        self.total_supply = 0

    def reset(self):
        # state reset (time, num_activate)
        observations = [[0, 1], [0, 1], [0, 1]]
        # reward reset
        self.total_consumption = 0
        self.total_supply = 0
        self.flag = [0, 0, 0]
        self.finish_oper = [1, 1, 1]
        self.oper_time = [self.config["agent1"][1], self.config["agent2"][1], self.config["agent3"][1]]
        return observations

    def step(self, action_n, obs_n):
        self.total_supply += self.config["SolarPV"][self.steps]
        penalty = [0, 0, 0]  # [0 for _ in range(self.num_agent)]
        done = [False for _ in range(self.n)]
        operate = [0, 0, 0]  # len:agent
        for i in range(len(action_n)):
            if 0 <= action_n[i][0]:
                operate[i] = 1  # ON
                self.flag[i] = 1
            else:
                operate[i] = 0  # OFF

        # 報酬計算
        cost: int = 0
        for i in range(len(obs_n)):
            if obs_n[i][1] == 0 and operate[i] == 1:
                """稼働不可の時に、稼働のアクションを出した場合"""
                cost -= 100000
            if self.oper_time[i] > 0 and self.flag[i] == 1:
                """残り可能稼働時間"""
                self.oper_time[i] -= 1
                if self.oper_time[i] == 0:
                    self.finish_oper[i] = 0

        balance = self.total_supply - (
                600 * self.flag[0] * self.finish_oper[0] + 25 * self.flag[1] * self.finish_oper[1] + 1 * self.flag[2] *
                self.finish_oper[2])
        self._reset_total_supply(balance)
        cost += - balance ** 2
        rew_n = [cost, cost, cost]

        if (self.steps == self.config["agent1"][2] and self.flag[0] != 1) or (
                self.steps == self.config["agent2"][2] and self.flag[1] != 1) or (
                self.steps == self.config["agent3"][2] and self.flag[2] != 1):
            """done条件1: 規定の時間を過ぎても実行せずに時間が過ぎてしまった時"""
            done = [True for _ in range(self.n)]

        if self.steps != 0 and self.steps % 23 == 0:
            """done条件2: 23時になった時"""
            done = [True for _ in range(self.n)]

        # next_obsの計算
        operation_time = [0, 0, 0]
        terminal = [1, 1, 1]  # 稼働時間分の稼働が終わったかどうか
        for i in range(len(obs_n)):
            if operation_time[i] == 0:
                break
            operation_time[i] = obs_n[i][1] - operate[i]
            terminal[i] -= operate[i]

        next_obs_n = [[(self.steps + 1) * terminal[i], operation_time[i]] for i in range(self.n)]

        return next_obs_n, rew_n, done, {}

    def render(self):
        pass
