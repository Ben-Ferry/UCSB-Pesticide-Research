"""
This is the main file for processing data and visualizing it.
"""
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import altair as alt


def load_in_data(shp_file_towns, chloro2014, chloro2015, chloro2016,
                 chloro2017, chloro2018, data2013, data2010, data2009,
                 data2008, data2012, data2011):
    sb_shape_towns = gpd.read_file(shp_file_towns)
    sb_shape_towns = sb_shape_towns[["CO_MTRS", "geometry"]]
    chloro2014 = pd.read_csv(chloro2014)
    chloro2015 = pd.read_csv(chloro2015)
    chloro2016 = pd.read_csv(chloro2016)
    chloro2017 = pd.read_csv(chloro2017)
    chloro2018 = pd.read_csv(chloro2018)
    data2013 = pd.read_csv(data2013)
    data2010 = pd.read_csv(data2010)
    data2009 = pd.read_csv(data2009)
    data2008 = pd.read_csv(data2008)
    data2012 = pd.read_csv(data2012)
    data2011 = pd.read_csv(data2011)
    chloro_csv = [chloro2014, chloro2015, chloro2016, chloro2017, chloro2018,
                  data2013, data2010, data2009, data2008, data2012, data2011]
    chloro_csv = pd.concat(chloro_csv)
    chemical_chloro = chloro_csv["CHEMICAL NAME"] == "CHLOROPICRIN"
    county = chloro_csv["COUNTY NAME"] == "SANTA BARBARA"
    chloro_csv = chloro_csv.loc[chemical_chloro & county,
                                ["YEAR", "COUNTY NAME",
                                 "COMTRS", "CHEMICAL NAME",
                                 "POUNDS CHEMICAL APPLIED"]]
    chloro_data = sb_shape_towns.merge(chloro_csv, left_on="CO_MTRS",
                                       right_on="COMTRS", how="left")
    return chloro_data


def plot_santa_barbara_sections(chloro_data):
    fig, ax = plt.subplots(1)
    chloro_data.plot(ax=ax, color="#EEEEEE")
    chloro_data.plot(ax=ax, column="POUNDS CHEMICAL APPLIED", legend=True)
    plt.savefig("map.png")


def main():
    """
    This is the main function.
    """
    chloro_data = load_in_data(
        "/Users/benferry/Desktop/GitHub/CSE-163-Final/Santa_Barbara_sections/"
        "pls_42_nad83.shp", "~/Desktop/GitHub/CSE-163-Final/"
                            "Data_csv/2014_Chloro.csv",
                            "~/Desktop/GitHub/CSE-163-Final/"
                            "Data_csv/2015_Chloro.csv",
                            "~/Desktop/GitHub/CSE-163-Final/"
                            "Data_csv/2016_Chloro.csv",
                            "~/Desktop/GitHub/CSE-163-Final/"
                            "Data_csv/2017_Chloro.csv",
                            "~/Desktop/GitHub/CSE-163-Final/"
                            "Data_csv/2018_Chloro.csv",
                            "~/Desktop/GitHub/CSE-163-Final/"
                            "Data_csv/2013_data.csv",
                            "~/Desktop/GitHub/CSE-163-Final/"
                            "Data_csv/2010_data.csv",
                            "~/Desktop/GitHub/CSE-163-Final/"
                            "Data_csv/2009_data.csv",
                            "~/Desktop/GitHub/CSE-163-Final/"
                            "Data_csv/2008_data.csv",
                            "~/Desktop/GitHub/CSE-163-Final/"
                            "Data_csv/2012_data.csv",
                            "~/Desktop/GitHub/CSE-163-Final/"
                            "Data_csv/2011_data.csv")
    plot_santa_barbara_sections(chloro_data)


if __name__ == '__main__':
    main()
