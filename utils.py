import requests
from urllib.parse import urlencode, quote_plus
import pandas as pd

def query_ads():
    # https://github.com/adsabs/adsabs-dev-api
    # https://ui.adsabs.harvard.edu/help/search/search-syntax
    # curl -H "Authorization: Bearer copy-token-here" "https://api.adsabs.harvard.edu/v1/search/query?copy-encoded-query-here"

    token = '4rmPlv5aTa1HiAUoisYpN1SPzfg6xMspxLQa7L0X' # Suk Sien token
    encoded_query = urlencode({"q": "year:[2000 TO 2023]",
                           "fl": "title, first_author, author, aff, citation_count, date",
                           "fq": "property:refereed",
                           "fq": "doctype: article",
                           #"fq": "author_count: 20",
                           "fq": "database:astronomy",
                           "rows": 2000, # 2000 is the max
                           "sort": "date desc"})

    results = requests.get("https://api.adsabs.harvard.edu/v1/search/query?{}".format(encoded_query), headers={'Authorization': 'Bearer ' + token})
    results = results.json()
    print(results['response']['numFound'])

    return results

def massage_results(results):
    data = results['response']['docs']
    df = pd.DataFrame.from_dict(data)
    cols = df.columns
    print(df['title'])
