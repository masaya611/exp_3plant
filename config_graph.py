import numpy as np
from matplotlib import pyplot as plt


SolarPV = [25, 25, 25, 25, 50, 50,
            100, 100, 300, 300, 400, 400,
            400, 400, 300, 300, 100, 100,
            50, 50, 25, 25, 25, 25]
# Gauss = np.random.normal(loc=0, scale=1, size =100000)
plt.plot(range(len(SolarPV)), SolarPV)
# plt.plot(range(len(v_max_pv)), demand)
# pyplot.plot(range(len(reward_log3_ave)), reward_log3_ave)
plt.ylim(0, 630)
#pyplot.plot(range(len(reward_list)), reward_list)
plt.xticks([0, 5, 11, 17, 23])
# plt.xlim(0, 23)
plt.grid(which = "both")
plt.minorticks_on()
plt.show()