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

    if clip_max is not None:
        dc = np.clip(df_colon[colname], 0, clip_max)
        dnc = np.clip(df_nocolon[colname], 0, clip_max)
    else:
        dc = df_colon[colname]
        dnc = df_nocolon[colname]

    plt.hist(dc, bins=np.arange(0, 200, 2), histtype='step', density=True, color='r', zorder=20)
    plt.hist(dnc, bins=np.arange(0, 200, 2), histtype = 'step', density = True, color='k')
    plt.xlim([-2, 100])

    plt.axvline(np.median(dc), ls='--', c='r', label='median=%0.1f' % np.median(dc), zorder=1)
    plt.axvline(np.median(dnc), ls='--', c='k', label='median=%0.1f' % np.median(dnc), zorder=1)

    plt.axvline(np.mean(dc), ls=':', c='r', label='mean=%0.1f' % np.mean(dc))
    plt.axvline(np.mean(dnc), ls=':', c='k', label='mean=%0.1f' % np.mean(dnc))

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

def medtest(df_colon, df_nocolon, colname):

    dc = df_colon[colname]
    dnc = df_nocolon[colname]

    res = stats.median_test(dc, dnc)
    return res