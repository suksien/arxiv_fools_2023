import numpy as np
import matplotlib.pyplot as plt
import matplotlib.axis as ax
import matplotlib.pylab as pylab
import pandas as pd
import utils
import scipy.stats as stats

df = pd.read_excel('final_output_ranked_6016.xlsx') #final w/ 6016 entries

jt_rank_init = df.iloc[:250, -1]
st_rank_init = df.iloc[:250, -2]
ranks = df.iloc[:, -2]

rank_bins = np.arange(1, 6)
plt.hist(jt_rank_init, bins=rank_bins, histtype='step', color='mediumvioletred', label="JT")
plt.hist(st_rank_init, bins=rank_bins, histtype='step', color='darkturquoise', label="ST")
plt.legend()
plt.show()

params = {'legend.fontsize': 12,
          'figure.figsize': (10, 7),
         'axes.labelsize': 18,
         'axes.titlesize': 20,
         'xtick.labelsize': 16,
         'ytick.labelsize': 16,
         'lines.linewidth' : 1,
         'figure.dpi' : 72}
pylab.rcParams.update(params)

jt_hist_data = np.histogram(jt_rank_init, bins=np.arange(1, 7))
st_hist_data = np.histogram(st_rank_init, bins=np.arange(1, 7))
plt.figure(figsize=(7,5))
xtick = np.arange(1, 6, 1)
plt.plot(rank_bins, jt_hist_data[0], '*', ms = 15, color='mediumvioletred', label="JT")
plt.plot(rank_bins, st_hist_data[0], '.', ms = 15, color='darkturquoise', label="PD")
plt.xlabel("Rank")
plt.ylabel("Count")
plt.xticks(xtick)
plt.xlim(0.75, 5.25)
plt.ylim(-2, 210)
plt.tick_params(axis="x", direction='in')
plt.tick_params(axis="y", direction='in')
#plt.grid(color = 'silver', ls = '--')
plt.legend()
plt.savefig("rank_counts.pdf", bbox_inches='tight')
plt.savefig("rank_counts.png", bbox_inches='tight')
plt.show()



# can look at mean/var(*_rank_init) and correlation between the two

jt_rank_init.describe()

mean_jt = np.mean(jt_rank_init)
mean_st = np.mean(st_rank_init)
delta_mean = mean_st - mean_jt
stdv_jt = np.std(jt_rank_init)
stdv_st = np.std(st_rank_init)
stdv_br = 0.5*(stdv_jt + stdv_st)
corr = jt_rank_init.corr(st_rank_init)

rank_hist_data = np.histogram(ranks, bins=np.arange(1, 8))

df = df[df.cheeky_rank >=1]

num_aut = []
for aut_list in df.author.values:
	try:
		aut_names = aut_list.split("',")
		num_aut.append(len(aut_names))
	except:
		num_aut.append("NONE")

df['num_authors'] = num_aut
df = df[df.num_authors != 'NONE']

#df.shape = (6000, 14)

plt.plot(df.cheeky_rank, df.num_authors, '.')
plt.show()

## [tot_citations, avg_citations, avg_num_author]
data_arr = np.zeros([6, 3])
for i in range(1, 7):
	data_arr[i-1, 0] = np.sum(df['citation_count'][df['cheeky_rank'].values == i])
	data_arr[i-1, 1] = np.mean(df['citation_count'][df['cheeky_rank'].values == i])
	data_arr[i-1, 2] = np.mean(df['num_authors'][df['cheeky_rank'].values == i])


plt.plot(np.arange(1, 7, 1), data_arr[:, 0], '.', ms = 12, color='mediumvioletred')
plt.xlabel("Rank")
plt.ylabel("Total citations")
plt.xticks(xtick)
plt.xlim(0.75, 5.25)
#plt.ylim(-1, 205)
plt.tick_params(axis="x", direction='in')
plt.tick_params(axis="y", direction='in')
#plt.grid(color = 'silver', ls = '--')
plt.savefig("tot_citations_rank.pdf", bbox_inches='tight')
plt.savefig("tot_citations_rank.png", bbox_inches='tight')
plt.show()

plt.plot(np.arange(1, 7, 1), data_arr[:, 1], '.', ms = 12, color='mediumvioletred')
plt.xlabel("Rank")
plt.ylabel("Average citation counts")
plt.xticks(xtick)
plt.xlim(0.75, 5.25)
#plt.ylim(-1, 205)
plt.tick_params(axis="x", direction='in')
plt.tick_params(axis="y", direction='in')
#plt.grid(color = 'silver', ls = '--')
plt.savefig("avg_citations_rank.pdf", bbox_inches='tight')
plt.savefig("avg_citations_rank.png", bbox_inches='tight')
plt.show()

plt.plot(np.arange(1, 7, 1), data_arr[:, 2], '.', ms = 12, color='mediumvioletred')
plt.xlabel("Rank")
plt.ylabel("Average number of authors")
plt.xticks(xtick)
plt.xlim(0.75, 5.25)
#plt.ylim(-1, 205)
plt.tick_params(axis="x", direction='in')
plt.tick_params(axis="y", direction='in')
#plt.grid(color = 'silver', ls = '--')
plt.savefig("avg_authors_rank.pdf", bbox_inches='tight')
plt.savefig("avg_authors_rank.png", bbox_inches='tight')
plt.show()


fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
ax1.plot(np.arange(1, 7, 1), data_arr[:, 1], '.', ms = 24, color='darkturquoise')
ax2.plot(np.arange(1, 7, 1), data_arr[:, 2], '*', ms = 24, color='darkmagenta')
ax1.set_xlabel("Rank")
ax1.set_ylabel('Average citation counts', color='darkturquoise')
ax2.set_ylabel('Average number of authors', color='darkmagenta')#, rotation=270)
plt.xticks(xtick)
plt.xlim(0.75, 5.25)
plt.tick_params(axis="x", direction='in')
plt.tick_params(axis="y", direction='in')
plt.savefig("avg_citation_authors_rank.pdf", bbox_inches='tight')
plt.savefig("avg_citation_authors_rank.png", bbox_inches='tight')
plt.show()