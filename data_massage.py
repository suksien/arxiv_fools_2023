import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import utils
import scipy.stats as stats

df = pd.read_excel('final_output_ranked_6016.xlsx') #final w/ 6016 entries

jt_rank_init = df.iloc[:250, -1]
st_rank_init = df.iloc[:250, -2]

rank_bins = np.arange(1, 6)
plt.hist(jt_rank_init, bins=rank_bins, histtype='step', color='mediumvioletred', label="JT")
plt.hist(st_rank_init, bins=rank_bins, histtype='step', color='darkturquoise', label="ST")
plt.legend()
plt.show()

jt_hist_data = np.histogram(jt_rank_init, bins=np.arange(1, 7))
st_hist_data = np.histogram(st_rank_init, bins=np.arange(1, 7))

plt.plot(rank_bins, jt_hist_data[0], '.', color='mediumvioletred', label="JT")
plt.plot(rank_bins, st_hist_data[0], '.', color='darkturquoise', label="ST")
plt.legend()
plt.show()

# can look at mean/var(*_rank_init) and correlation between the two

jt_rank_init.describe()