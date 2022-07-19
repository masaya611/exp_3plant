import tqdm
import numpy as np
import argparse
from environments import Environment
from maddpg import MaddpgAgents

# -------------------------------------------------------------------------
"""
obs_n: n個のAgentのobservation
"""
# -----編集中1----------------------------------------------------------------
# ------args-------------------------------------------------------------------
parser = argparse.ArgumentParser(description='Set parameters.')
parser.add_argument('--num_episode', default=20000, type=int, help='Number of episode')
parser.add_argument('--max_steps', default=200, type=int, help='Number of max steps')
parser.add_argument('--memory_size', default=10000, type=int, help='Number of memory size')
parser.add_argument('--initial_memory_size', default=100000, type=int, help='Number of initial memory size')
parser.add_argument('--lr', default=0.01, type=float, help='Learning rate of Agents')

# agent config
parser.add_argument('--num_pv', default=3, type=int, help='Number of PV Agents')
parser.add_argument('--observation_space', default=2, type=int, help='Number of PV Agents')
# demand config
parser.add_argument('--demand', default="constant", type=str, help='type of Demand')

args = parser.parse_args()
# -------------------------------------------------------------------------

# 各種設定
# num_episode = 20000  #学習エピソード数（論文では25000）
# max_steps = 200  # エピソードの最大ステップ数
# memory_size = 10000  #replay bufferの大きさ
# initial_memory_size = 100000  #最初貯める数
# ログ用の設定
episode_rewards = []
num_average_epidodes = 100

env = Environment(args)
# env.n=3 -> env.n=2 (no building)
# agent = MaddpgAgents(observation_space=1, action_space=2, num_agent=env.n, memory_size=memory_size)
agent = MaddpgAgents(observation_space=args.observation_space, action_space=1, num_agent=args.num_pv, lr=args.lr,
                     memory_size=args.memory_size)

"""
省略
#最初にreplay bufferにノイズのかかった行動をしたときのデータを入れる
obs_n = env.reset()
for step in range(initial_memory_size):
    if step % max_steps == 0:
        obs_n = env.reset()
    actions = agent.get_action(state)
    next_state, reward, done, _ = env.step(actions)
    agent.buffer.cache(state,next_state,actions,reward,done)
    state = next_state
print('%d Data collected' % (initial_memory_size))
"""
# -----編集中1'----------------------------------------------------------------

# -------- plot用 ----------
reward_log = []
episode_reward_log = []

config_nums = []
agent1_log = []
agent2_log = []
agent3_log = []
# -------- plot用' ----------


for episode in tqdm.trange(args.num_episode):
    obs_n = env.reset()
    episode_reward = 0
    reward_sum = [0]

    # -------- plot用 ----------
    agent1_episode_log = []
    agent2_episode_log = []
    agent3_episode_log = []
    # -------- plot用' ----------
    # print("env.config_epi", env.config["solar_insolations"][-3:])
    for t in range(args.max_steps):
        assert len(obs_n) == args.num_pv
        total_reward = []
        env.steps = t
        action_n = agent.get_action(obs_n)
        assert len(action_n) == args.num_pv
        next_obs_n, reward_n, done, _ = env.step(action_n, obs_n)
        # ----- 編集中2 ----------------------------------------------------------------

        # -------- total reward learning --------

        for i in range(args.num_pv):
            total_reward.append(sum(reward_n))
        episode_reward += sum(total_reward)

        reward_sum = [x + y for (x, y) in zip(reward_sum, total_reward)]  # plot用
        num_steps = t  # plot用
        agent.buffer.cache(obs_n, next_obs_n, action_n, total_reward, done)
        obs_n = next_obs_n

        # -------- plot用 ----------
        agent1_episode_log.append(action_n[0][0])
        agent2_episode_log.append(action_n[1][0])
        agent3_episode_log.append(action_n[2][0])
        # -------- plot用' ----------

        if all(done):
            # -------- total reward learning --------
            reward_sum = [x / num_steps for x in reward_sum]  # plot用
            reward_log.append(reward_sum)  # plot用
            episode_reward_log.append(episode_reward / num_steps)  # plot用

            agent1_log.append(agent1_episode_log)
            agent2_log.append(agent2_episode_log)
            agent3_log.append(agent3_episode_log)
            break

    np.save('./reward_log/reward_log_{0}'.format("0620"), reward_log)  # plot用
    np.save('./reward_log/episode_reward_log_{0}'.format("0620"), episode_reward_log)  # plot用
    np.save('./config_nums', config_nums)  # plot用

    np.save('./action_log/agent1_action_price_log_{0}'.format("0620"), agent1_log)  # plot用
    np.save('./action_log/agent2_action_price_log_{0}'.format("0620"), agent2_log)  # plot用
    np.save('./action_log/agent3_action_price_log_{0}'.format("0606"), agent3_log)  # plot用

    if episode > 40 and episode % 4 == 0:
        agent.update()
        # print(agent.target_actor_group[0].state_dict())
    episode_rewards.append(episode_reward)
    if episode % 200 == 0:
        print("Episode %d finished | Episode reward %f" % (episode, episode_reward))

print("args", args)
# -----編集中2'----------------------------------------------------------------
