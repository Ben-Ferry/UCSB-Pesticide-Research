"""
This is the main file for processing data and visualizing it.
"""
import json
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
    chemical_miner = chloro_csv["CHEMICAL NAME"] == 'MINERAL OIL'
    chemical_dichlo = chloro_csv["CHEMICAL NAME"] == '1,3-DICHLOROPROPENE'
    chemical_sulf = chloro_csv["CHEMICAL NAME"] == 'SULFUR DIOXIDE'
    chemical_potas = chloro_csv["CHEMICAL NAME"] == 'POTASSIUM N-METHYLDITHIOCARBAMATE'
    county = chloro_csv["COUNTY NAME"] == "SANTA BARBARA"
    chloro_csv = chloro_csv.loc[county & (chemical_chloro |
                                chemical_dichlo | chemical_potas |
                                chemical_miner | chemical_sulf),
                                ["YEAR", "COUNTY NAME",
                                 "COMTRS", "CHEMICAL NAME",
                                 "POUNDS CHEMICAL APPLIED"]]
    chloro_data = sb_shape_towns.merge(chloro_csv, left_on="CO_MTRS",
                                       right_on="COMTRS", how="left")
    print(chloro_data["CHEMICAL NAME"].unique())
    return chloro_data


def plot_santa_barbara_sections(chloro_data):
    fig, ax = plt.subplots(1)
    plot_by_chem = chloro_data[["POUNDS CHEMICAL APPLIED", "CHEMICAL NAME",
                                "geometry"]]
    plot_by_chem = plot_by_chem.dissolve(by="CHEMICAL NAME", aggfunc="sum")
    chloro_data.plot(ax=ax, color="#EEEEEE")
    chloro_data.plot(ax=ax, column="POUNDS CHEMICAL APPLIED", legend=True)
    plt.savefig("map.png")


# def alt_plot_chloro(chloro_data, color_column, title, year,
#                     color_scheme="bluegreen"):
# selection = alt.selection_multi(fields=[year])
# color = alt.condition(selection,
#                     alt.Color(color_column, type='nominal',
#                             scale=alt.Scale(scheme=color_scheme)),
#                     alt.value('lightgray'))
#     chloro_json = json.loads(chloro_data.to_json())
#     chloro_alt_data = alt.Data(values=chloro_json['features'])
#     base = alt.Chart(chloro_alt_data, title=title).mark_geoshape(
#     stroke="black",
#     strokeWidth=1
#     ).encode().properties(width=800, height=800)
#     choro = alt.Chart(chloro_alt_data).mark_geoshape(
#     fill='lightgray',
#     stroke='black'
#     ).encode(color=color).add_selection(selection)

#     return base + choro


def main():
    """
    This is the main function.
    """
    chloro_data = load_in_data(
        "/Users/benferry/Desktop/GitHub/CSE-163-Final/Santa_Barbara_sections/"
        "pls_42_nad83.shp", "~/Desktop/GitHub/CSE-163-Final/"
                            "Data_csv/2014_data.csv",
                            "~/Desktop/GitHub/CSE-163-Final/"
                            "Data_csv/2015_data.csv",
                            "~/Desktop/GitHub/CSE-163-Final/"
                            "Data_csv/2016_data.csv",
                            "~/Desktop/GitHub/CSE-163-Final/"
                            "Data_csv/2017_data.csv",
                            "~/Desktop/GitHub/CSE-163-Final/"
                            "Data_csv/2018_data.csv",
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
    # alt_plot_chloro(chloro_data=chloro_data,
    #                 color_column='properties.POUNDS CHEMICAL APPLIED',
    #                 title="Amount of Chloropicrin used",
    #                 year="properties.YEAR", color_scheme='bluegreen')


if __name__ == '__main__':
    main()