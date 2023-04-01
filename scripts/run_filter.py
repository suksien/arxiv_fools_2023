import utils
import pandas as pd

filename = 'master_output.xlsx'
df = pd.read_excel(filename)

colon_idx, _ = utils.filter_results(df)
sub_df = df.iloc[colon_idx]
sub_df.to_excel('master_output_colon_noerratum.xlsx')

