import numpy as np
from matplotlib import pyplot
import datetime
import argparse
import statistics as stat
parser = argparse.ArgumentParser(description='Set parameters.')
parser.add_argument('--fig_save', default="non_save", type=str, help='type of Demand')
args = parser.parse_args()
n = 300


agent1_action_price_log = np.load('./action_log/agent1_action_price_log_0620.npy',allow_pickle=True)
agent1_action_amount_log = np.load('./action_log/agent1_action_amount_log_0620.npy',allow_pickle=True)
agent2_action_price_log = np.load('./action_log/agent2_action_price_log_0620.npy',allow_pickle=True)
agent2_action_amount_log = np.load('./action_log/agent2_action_amount_log_0620.npy',allow_pickle=True)

# print(agent2_action_amount_log)

agent1_price1 = []
agent2_price1 = []
agent1_amount1 = []
agent2_amount1 = []
for i in range(len(agent1_action_price_log)):
    agent1_price1.append((agent1_action_price_log[i][1]+1.0)*0.5 * 100 + 1e-6)
    agent2_price1.append((agent2_action_price_log[i][1]+1.0)*0.5 * 100 + 1e-6)

    agent1_amount1.append((agent1_action_amount_log[i][1]+1.0)*0.5 * 10 + 1e-6) # *10 *0.1
    agent2_amount1.append((agent2_action_amount_log[i][1]+1.0)*0.5 * 10 + 1e-6) # *10 *0.1

# print("agent2_price", agent2_amount0)

total_sell = [(w*x) + (y*z) for (w,x,y,z) in zip(agent1_price1, agent1_amount1, agent2_price1, agent2_amount1) ]
total_amount = [(w + x) for (w,x) in zip(agent1_amount1, agent2_amount1) ]

#移動平均
ave_n = 1000
agent1_price_ave = np.convolve(agent1_price1,np.ones(ave_n)/ave_n, mode='valid')
agent1_amount_ave = np.convolve(agent1_amount1,np.ones(ave_n)/ave_n, mode='valid')

agent2_price_ave = np.convolve(agent2_price1,np.ones(ave_n)/ave_n, mode='valid')
agent2_amount_ave = np.convolve(agent2_amount1,np.ones(ave_n)/ave_n, mode='valid')


#############################################
# price
"""
    #variance
agent1_price_stdev = [stat.stdev(agent1_price1[i:(i+ave_n)]) for i in range(len(agent1_price_ave))]
print("done")
agent2_price_stdev = [stat.stdev(agent2_price1[i:(i+ave_n)]) for i in range(len(agent2_price_ave))]
print("done")
"""

y1 = [70] * len(agent1_price_ave)
pyplot.plot(range(len(agent1_price_ave)), agent1_price_ave, color = "blue")
# pyplot.fill_between(range(len(agent1_price_ave)), agent1_price_ave-agent1_price_stdev, agent1_price_ave+agent1_price_stdev, color="blue", alpha = 0.1)
pyplot.plot(range(len(agent2_price_ave)), agent2_price_ave, color = "red")
# pyplot.fill_between(range(len(agent2_price_ave)), agent2_price_ave-agent2_price_stdev, agent2_price_ave+agent2_price_stdev, color="red", alpha = 0.1)
pyplot.plot(range(len(agent1_price_ave)), y1, color = "yellow")
pyplot.ylim(0, 101)
pyplot.grid(which = "both")
if args.fig_save == "save":
    pyplot.savefig("price{0}.png".format(datetime.datetime.now()))
pyplot.show()
#############################################


#############################################
# amount
"""
    # variance
agent1_amount_stdev = [stat.stdev(agent1_amount1[i:(i+ave_n)]) for i in range(len(agent1_amount_ave))]
print("done")
agent2_amount_stdev = [stat.stdev(agent2_amount1[i:(i+ave_n)]) for i in range(len(agent2_amount_ave))]
print("done")
"""

y2 = [8] * len(agent2_price_ave)
pyplot.plot(range(len(agent1_amount_ave)), agent1_amount_ave, color = "blue")
# pyplot.fill_between(range(len(agent1_amount_ave)), agent1_amount_ave-agent1_amount_stdev, agent1_amount_ave+agent1_amount_stdev, color="blue", alpha = 0.1)
pyplot.plot(range(len(agent2_amount_ave)), agent2_amount_ave, color = "red")
# pyplot.fill_between(range(len(agent2_amount_ave)), agent2_amount_ave-agent2_amount_stdev, agent2_amount_ave+agent2_amount_stdev, color="red", alpha = 0.1)
pyplot.plot(range(len(agent1_amount_ave)), y2, color = "yellow")
pyplot.ylim(0, 10.5)
pyplot.grid(which = "both")
if args.fig_save == "save":
    pyplot.savefig("amount{0}.png".format(datetime.datetime.now()))
pyplot.show()
#############################################


#############################################
# total_sell
total_sell_ave = np.convolve(total_sell,np.ones(ave_n)/ave_n, mode='valid')
y3 = [560] * len(total_sell_ave)
pyplot.plot(range(len(total_sell_ave)), total_sell_ave)
pyplot.plot(range(len(total_sell_ave)), y3)
pyplot.ylim(0, 1200)
pyplot.show()
#############################################


#############################################
# total_amount
total_amount_ave = np.convolve(total_amount,np.ones(ave_n)/ave_n, mode='valid')
y4 = [8] * len(total_amount_ave)
pyplot.plot(range(len(total_amount_ave)), total_amount_ave)
pyplot.plot(range(len(total_amount_ave)), y4)
pyplot.ylim(0, 20)
if args.fig_save == "save":
    pyplot.savefig("total_amount{0}.png".format(datetime.datetime.now()))
pyplot.show()
#############################################