import numpy as np
from matplotlib import pyplot
import datetime
import argparse
parser = argparse.ArgumentParser(description='Set parameters.')
parser.add_argument('--fig_save', default="non_save", type=str, help='type of Demand')
args = parser.parse_args()


n = 1

reward_log = np.load('./reward_log/reward_log_0620.npy',allow_pickle=True)
episode_reward_log = np.load('./reward_log/episode_reward_log_0620.npy',allow_pickle=True)


reward_log1 = [x[0] for x in reward_log]

print(len(reward_log1))

print("reward_log1", reward_log1[0:10])

#移動平均
ave_n = 1000
reward_moving_ave = np.convolve(reward_log1,np.ones(ave_n)/ave_n, mode='valid')
epi_reward_moving_ave = np.convolve(episode_reward_log,np.ones(ave_n)/ave_n, mode='valid')



#moving ave
pyplot.plot(range(len(reward_moving_ave)), reward_moving_ave)
# pyplot.ylim(-7, 0)
pyplot.show()

pyplot.plot(range(len(epi_reward_moving_ave)), epi_reward_moving_ave)
if args.fig_save == "save":
    pyplot.savefig("reward{0}.png".format(datetime.datetime.now()))
# pyplot.ylim(-11, 0)
pyplot.show()

"""
pyplot.plot(range(len(reward_log1_ave)), reward_log1_ave)
pyplot.ylim(-1, 1)
pyplot.show()
"""