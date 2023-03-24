import requests
from urllib.parse import urlencode, quote_plus
import pandas as pd
import string
import glob
import numpy as np

def query_ads(year, journal,startmo=None, endmo=None):
    # https://github.com/adsabs/adsabs-dev-api
    # https://ui.adsabs.harvard.edu/help/search/search-syntax
    # curl -H "Authorization: Bearer copy-token-here" "https://api.adsabs.harvard.edu/v1/search/query?copy-encoded-query-here"

    token = '4rmPlv5aTa1HiAUoisYpN1SPzfg6xMspxLQa7L0X' # Suk Sien token

    if startmo is not None:
        encoded_query = urlencode({"q": "pubdate:[%s-%s TO %s-%s]" % (year,startmo,year,endmo),
                                   "fl": "title, first_author, author, aff, citation_count, read_count, date",
                                   "fq": "property:refereed",
                                   "fq": "doctype: article",
                                   "fq": "author_count: 16",
                                   "fq": "database:astronomy",
                                   "fq": "bibstem: %s" % journal,
                                   #"fq": "title:/.\:*/",  # "fq": "facility:/magell.*/"
                                   "rows": 2000,  # 2000 is the max
                                   "sort": "date desc"})

    else:
        encoded_query = urlencode({"q": "year:%s" % (year),
                                   "fl": "title, first_author, author, aff, citation_count, read_count, date",
                                   "fq": "property:refereed",
                                   "fq": "doctype: article",
                                   "fq": "author_count: 16",
                                   "fq": "database:astronomy",
                                   "fq": "bibstem: %s" % journal,
                                   # "fq": "title:/.\:*/",  # "fq": "facility:/magell.*/"
                                   "rows": 2000,  # 2000 is the max
                                   "sort": "date desc"})
    results = requests.get("https://api.adsabs.harvard.edu/v1/search/query?{}".format(encoded_query), headers={'Authorization': 'Bearer ' + token})
    results = results.json() # is a dictionary

    data = results['response']['docs']
    ntot = results['response']['numFound']
    print("ntot", ntot)

    return results, data, ntot

def run_query_year(year_want):

    data_all = []
    ntot_all = 0
    all_journals = ['ApJ', 'ApJS', 'MNRAS', 'AJ', 'A&A', 'A&ARv', 'JCos', 'JCAP'] # "ApL"
    print("====== year %d ======" % year_want)
    for journal in all_journals:
        print(journal)
        results, data, ntot = query_ads(year_want, journal)
        ntot_all += ntot

        if ntot > 2000:
            if ntot > 4000:
                start = [1, 5, 9]
                ds = 3
            else:
                start = [1, 7]
                ds = 5

            for s in start:
                results, data, _ = query_ads(year_want, journal, startmo=s, endmo=s+ds)
                data_all += data
        else:
            data_all += data

    print(ntot_all, len(data_all))
    return data_all

def filter_results(data):
    if type(data) != pd.core.frame.DataFrame:
        print("error: data needs to be in pandas dataframe format")
        return 0

    out_index = []
    out_nocolon_index = []

    #for i, elem in enumerate(data):
    #    title = elem['title'][0]
    for index, row in data.iterrows():
        title = row['title']
        if type(title) is str:
            if "Correction to" in title or "Erratum" in title:
                pass
            else:
                if ":" in title:
                    out_index.append(index)
                else:
                    out_nocolon_index.append(index)

    print("ncolon", len(out_index))
    return out_index, out_nocolon_index

def combine_outputs():
    all_files = glob.glob('*.xlsx')
    big_output = []

    for file in all_files:
        data = pd.read_excel(file)
        big_output.append(data)

    df = pd.concat(big_output)
    df.to_excel('master_output.xlsx')