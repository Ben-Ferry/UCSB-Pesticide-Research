"""
Second and Third questions reasearch questions 
"""
import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
import altair as alt
from statsmodels.stats.proportion import proportions_ztest

path = "https://github.com/Ben-Ferry/CSE-163-Final/tree/main/Data_csv"
sbchloro2018 = pd.read_csv(path + "name of file here " )

"""
2
"""
pounds_chloro_sd = chlorodata[chlorodata['CHEMICAL_NAME'] == "CHLOROPICRIN"]
total_applied = pounds_chloro_sd['POUNDS_CHEMICAL_APPLIED']
mean_usage = total_applied.mean()
print(mean_ussage)

# ztest for guadalupe 
counts = np.array([sum(pounds_chloro_sd['POUNDS_CHEMICAL_APPLIED']), sum(Guadalpue["POUNDS_CHEMICAL_APPLIED"])])
num_occur = np.array([len(pounds_chloro_sd['POUNDS_CHEMICAL_APPLIED']), len(Guadalpue["POUNDS_CHEMICAL_APPLIED"])])

proportions_ztest(counts, num_occur )

#ztest for santa maria
counts = np.array([sum(pounds_chloro_sd['POUNDS_CHEMICAL_APPLIED']), sum(santmar["POUNDS_CHEMICAL_APPLIED"])])
num_occur = np.array([len(pounds_chloro_sd['POUNDS_CHEMICAL_APPLIED']), len(santmar["POUNDS_CHEMICAL_APPLIED"])])

proportions_ztest(counts, num_occur )


"""
3
"""


bars = alt.Chart(chlorodata).mark_bar().encode(
    x=alt.X('sum(POUNDS_CHEMICAL_APPLIED):Q', stack='zero'),
    y=alt.Y('SITE_NAME:N'),
    color=alt.Color('CHEMICAL_NAME')
)

text = alt.Chart(chlorodata).mark_text(dx=-15, dy=3, color='white').encode(
    x=alt.X('sum(POUNDS_CHEMICAL_APPLIED):Q', stack='zero'),
    y=alt.Y('SITE_NAME:N'),
    detail='CHEMICAL_NAME:N',
    text=alt.Text('sum(POUNDS_CHEMICAL_APPLIED):Q', format='.1f')
)

bars + text