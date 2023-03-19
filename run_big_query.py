import utils
import json
import pandas as pd

all_years = range(2020, 2024)
#big_output = []

for year in all_years:
    data = utils.run_query_year(year)
    df = pd.DataFrame.from_dict(data)
    df.to_excel('output_%d.xlsx' % year) # query kept getting interrupted for no reason, so saving year by year

    #big_output += data

#df = pd.DataFrame.from_dict(big_output)
#df.to_excel('output.xlsx')
# pd.read_excel(filename)

# saving as json takes up 5x more storage than excel
#json_obj = json.dumps(big_output)
#outfile = open('output.json', 'w')
#outfile.write(json_obj)

# how to read in json file
#infile = open('output.json')
#data = json.load(infile)



