import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import utils
import scipy.stats as stats

def init_citation_colon_vs_nocolon():
    df = pd.read_excel('master_output.xlsx')
    colon_idx, nocolon_idx = utils.filter_results(df)

    df_colon = df.iloc[colon_idx]
    df_nocolon = df.iloc[nocolon_idx]

    return df_colon, df_nocolon

def citation_colon_vs_nocolon(df_colon, df_nocolon, colname, clip_max=None):
    # Figure 1 in paper
    if clip_max is not None:
        dc = np.clip(df_colon[colname], 0, clip_max)
        dnc = np.clip(df_nocolon[colname], 0, clip_max)
    else:
        dc = df_colon[colname]
        dnc = df_nocolon[colname]

    plt.hist(dc, bins=np.arange(0, 200, 2), histtype='step', density=True, color='r', zorder=20, label='colon')
    plt.hist(dnc, bins=np.arange(0, 200, 2), histtype = 'step', density = True, color='k', label='No colon')
    plt.xlim([-2, 100])

    plt.axvline(np.median(dc), ls='--', c='r', zorder=1) #label='median=%0.1f' % np.median(dc), zorder=1)
    plt.text(np.median(dc)+1, 0.022, 'median=%0.1f' % np.median(dc), c='r', rotation=90)
    plt.axvline(np.median(dnc), ls='--', c='k', zorder=1) #label='median=%0.1f' % np.median(dnc), zorder=1)
    plt.text(np.median(dnc)-3.5, 0.022, 'median=%0.1f' % np.median(dnc), c='k', rotation=90)

    plt.axvline(np.mean(dc), ls=':', c='r')#, label='mean=%0.1f' % np.mean(dc))
    plt.text(np.mean(dc) + 0.5, 0.022, 'mean=%0.1f' % np.mean(dc), c='r', rotation=90)
    plt.axvline(np.mean(dnc), ls=':', c='k')#, label='mean=%0.1f' % np.mean(dnc))
    plt.text(np.mean(dnc) + 0.5, 0.022, 'mean=%0.1f' % np.mean(dnc), c='k', rotation=90)

    plt.legend()
    xlabel = colname.replace("_", " ").capitalize()
    plt.xlabel(xlabel)
    plt.ylabel('Normalized histogram')
    plt.show()

def ttest(df_colon, df_nocolon, colname, clip_max=None):
    # performs a t-test to test if the means of the samples are drawn from the same population or not
    if clip_max is not None:
        dc = np.clip(df_colon[colname], 0, clip_max)
        dnc = np.clip(df_nocolon[colname], 0, clip_max)
    else:
        dc = df_colon[colname]
        dnc = df_nocolon[colname]

    tstats, pval = stats.ttest_ind(dc, dnc, equal_var=False)
    print(tstats, pval)

    if pval > 0.05: print("the two samples are the same")
    else: print("the two samples are different")

def kstest(df_colon, df_nocolon, colname, clip_max=None):
    # non-parametric so distribution agnostic

    if clip_max is not None:
        dc = np.clip(df_colon[colname], 0, clip_max)
        dnc = np.clip(df_nocolon[colname], 0, clip_max)
    else:
        dc = df_colon[colname]
        dnc = df_nocolon[colname]

    ks_stats, pval = stats.ks_2samp(dc, dnc, mode='asymp')
    print(ks_stats, pval)

    if pval > 0.05: print("the two samples are the same")
    else: print("the two samples are different")

    n1 = len(dc)
    n2 = len(dnc)
    crit_val = 1.36 * np.sqrt((n1 + n2)/(n1 * n2)) #https://oak.ucc.nau.edu//rh83/Statistics/ks2/

    print(ks_stats, crit_val)

    if ks_stats < crit_val: print("the two samples are the same")
    else: print("the two samples are different")

############################
def extract_cheekyrank_all(df):

    crank = np.array(df['cheeky_rank'])
    ntot = np.sum(crank >= 1)
    all_rank = [1, 2, 3, 4, 5, 6]

    out_df = []
    for rank in all_rank:
        i = np.argwhere(crank == rank).flatten()
        print(rank, len(i), len(i)/ntot)
        out_df.append(df.iloc[i])
        if rank < 6:
            cit = df['citation_count'].iloc[i]

    return out_df

def plot_cheeky_cit(out_df):

    all_rank = [1, 2, 3, 4, 5, 6]
    for i, subdf in enumerate(out_df):
        cit = subdf['citation_count']
        print(all_rank[i], np.mean(cit))
        cts, bins = np.histogram(cit, bins=np.arange(0, 50, 2), density=True)
        bins_mid = (bins[0:-1] + bins[1:]) / 2
        if all_rank[i] < 6:
            plt.plot(bins_mid, cts, 'o-', label=all_rank[i])
    plt.legend()
    plt.show()


############################
from collections import Counter
def ncheeky_vs_time(df, cutoff):
    # Figure 3 of paper

    crank = np.array(df['cheeky_rank'])
    iwant_boring = np.argwhere(crank <= cutoff).flatten()
    iwant_cheeky = np.argwhere(crank > cutoff).flatten()

    date_boring = []
    date_cheeky = []
    for i in iwant_boring:
        date_boring.append(df.iloc[i]['date'][0:7])
    for i in iwant_cheeky:
        date_cheeky.append(df.iloc[i]['date'][0:7])

    all_dates = [date_cheeky, date_boring]
    alpha = [1.0, 1.0]
    label = ['rank > %d' % cutoff, 'rank <= %d' % cutoff]
    plt.figure(figsize=(8, 6))

    for i, d in enumerate(all_dates):
        cobj = Counter(d)
        cobj_date = list(cobj.keys())
        cobj_n = list(cobj.values())
        mean_count = np.mean(cobj_n)
        print(mean_count)

        N = np.array(cobj_n[::-1])
        sigma = 1.0
        upper = N + sigma * np.sqrt(N + 1) + (sigma**2 + 2)/3
        lower = N * (1. - 1. / (9. * N) - sigma / (3. * np.sqrt(N))) ** 3.

        # plt.plot(cobj_date[::-1], cobj_n[::-1]/mean_count, '.-', alpha=alpha[i], label=label[i])
        plt.errorbar(cobj_date[::-1], N / mean_count, yerr=(upper - lower) / mean_count, alpha=alpha[i], \
                     label=label[i], fmt='.-', capsize=3, capthick=1)

    plt.xticks(rotation=60)
    plt.xlabel('Date')
    plt.ylabel(r'$N_{\rm{papers}}/<N_{\rm{papers}}>$', fontsize=15)
    plt.legend(loc=2)
    plt.tight_layout()
    plt.show()

    #return cobj_date, cobj_n

############################ OBSOLETE
def medtest(df_colon, df_nocolon, colname):

    dc = df_colon[colname]
    dnc = df_nocolon[colname]

    res = stats.median_test(dc, dnc)
    return res

def ncit_year(df, year_str):

    # obsolete
    ncit = 0
    npaper = 0
    for i in range(len(df)):
        if df['date'][i].startswith(year_str):
            npaper += 1
            ncit += df['citation_count'][i]

    return ncit, npaper

def hist_cheeky(df):
    crank = df['cheeky_rank']
    i = ~np.isnan(crank)
    crank = crank[i]
    plt.hist(crank, bins=5)

# d = datetime.datetime.strptime(df['date'][100], '%Y-%m-%dT%H:%M:%SZ')