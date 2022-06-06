"""
Second and Third questions reasearch questions 
"""
from os import O_TEMPORARY
import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.stats.proportion import proportions_ztest

path = "https://github.com/Ben-Ferry/CSE-163-Final/tree/main/Data_csv"
sbchloro2018 = pd.read_csv(path + "name of file here " )

"""
2
"""
pounds_chloro_sd = chlorodata[chlorodata['PRODUCT_NAME'] == "CHLOROPICRIN"]
total_applied = pounds_chloro_sd['POUNDS_CHEMICAL_APPLIED']
mean_usage = total_applied.mean()
print(mean_ussage)

# ztest 
counts = np.array([sum(pounds_chloro_sd['POUNDS_CHEMICAL_APPLIED']), sum(Guadalpue["POUNDS_CHEMICAL_APPLIED"])])
num_occur = np.array([len(pounds_chloro_sd['POUNDS_CHEMICAL_APPLIED']), len(Guadalpue["POUNDS_CHEMICAL_APPLIED"])])

proportions_ztest(counts, num_occur )
