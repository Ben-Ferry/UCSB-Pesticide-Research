"""
This is the main file for processing data and visualizing it.
"""
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import plotly.express as px
import json


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
                                 "POUNDS CHEMICAL APPLIED",
                                 "SITE NAME"]]
    chloro_data = sb_shape_towns.merge(chloro_csv, left_on="CO_MTRS",
                                       right_on="COMTRS", how="left")
    print(chloro_data["CHEMICAL NAME"].unique())
    return chloro_data


def plot_santa_barbara_sections(chloro_data):
    chloro_mask = chloro_data["CHEMICAL NAME"] == "CHLOROPICRIN"
    chloro_plot = chloro_data.loc[chloro_mask, ["POUNDS CHEMICAL APPLIED",
                                                "geometry", "CHEMICAL NAME"]]
    chloro_plot = chloro_plot.dissolve(by="CHEMICAL NAME", aggfunc="sum")
    print(chloro_plot)
    dichlo_mask = chloro_data["CHEMICAL NAME"] == "1,3-DICHLOROPROPENE"
    dichlo_plot = chloro_data.loc[dichlo_mask, ["POUNDS CHEMICAL APPLIED",
                                                "geometry", "CHEMICAL NAME"]]

    dichlo_plot = dichlo_plot.dissolve(by="CHEMICAL NAME", aggfunc="sum")
    print(dichlo_plot)
    mineral_mask = chloro_data["CHEMICAL NAME"] == "MINERAL OIL"
    mineral_plot = chloro_data.loc[mineral_mask, ["POUNDS CHEMICAL APPLIED",
                                                  "geometry", "CHEMICAL NAME"]]
    mineral_plot = mineral_plot.dissolve(by="CHEMICAL NAME", aggfunc="sum")
    potas_mask = chloro_data["CHEMICAL NAME"] == "POTASSIUM N-METHYLDITHIOCARBAMATE"
    potas_plot = chloro_data.loc[potas_mask, ["POUNDS CHEMICAL APPLIED",
                                              "geometry", "CHEMICAL NAME"]]
    potas_plot = potas_plot.dissolve(by="CHEMICAL NAME", aggfunc="sum")
    fig, [[ax1, ax2], [ax3, ax4]] = plt.subplots(2, 2)
    chloro_data.plot(ax=ax1, color="#EEEEEE")
    chloro_data.plot(ax=ax2, color="#EEEEEE")
    chloro_data.plot(ax=ax3, color="#EEEEEE")
    chloro_data.plot(ax=ax4, color="#EEEEEE")
    chloro_plot.plot(ax=ax1, column="POUNDS CHEMICAL APPLIED", legend=True,
                     cmap="plasma")
    dichlo_plot.plot(ax=ax2, column="POUNDS CHEMICAL APPLIED", legend=True)
    mineral_plot.plot(ax=ax3, column="POUNDS CHEMICAL APPLIED", legend=True,
                      cmap="magma")
    potas_plot.plot(ax=ax4, column="POUNDS CHEMICAL APPLIED", legend=True,
                    cmap="cividis")
    ax1.set_title("AMOUNT OF CHLOROPRICIN", loc="center", fontsize=6)
    ax2.set_title
    plt.subplots_adjust(left=0.05,
                        bottom=0.1,
                        right=0.9,
                        top=0.9,
                        wspace=0.4,
                        hspace=0.4)
    plt.show()
    # plt.savefig("map.png")


def plot_pest_plotly(chloro_data, shape_path):
    shape_path_gdf = gpd.read_file(shape_path)
    shape_path_gdf.to_file("/Users/benferry/Desktop/GitHub/CSE-163-Final/"
                           "Santa_Barbara_sections\\"
                           "Santa_Barbara_sections_gpd.json",
                           driver='GeoJSON')


# def plot_chem_produce(Chloro_data):
#     fig, ax = plt.subplots(1)
#     plot_by_produce = Chloro_data[["POUNDS CHEMICAL APPLIED", "geometry",
#                                   "SITE NAME"]]
#     plot_by_produce = plot_by_produce.dissolve(by="SITE NAME",
#                                                aggfunc="sum")
#     Chloro_data.plot(ax=ax, color="#EEEEEE")
#     Chloro_data.plot(ax=ax, column="POUNDS CHEMICAL APPLIED", legend=True,)
#     plt.savefig("Produce map")


# def alt_plot_chloro(chloro_data):
#     # selection = alt.selection_multi(fields=[year])
#     # color = alt.condition(selection,
#     #                 alt.Color(color_column, type='nominal',
#     #                         scale=alt.Scale(scheme=color_scheme)),
#     #                 alt.value('lightgray'))
#     # chloro_json = json.loads(chloro_data.to_json())
#     # chloro_alt_data = alt.Data(values=chloro_json['features'])
#     chem_dropdown = alt.binding_select(options=chloro_data["CHEMICAL NAME"].unique())
#     selection = alt.selection_single(fields=["CHEMICAL NAME"],
#                                      bind=chem_dropdown, name="Chemical",
#                                      init={"CHEMICAL NAME": "CHLOROPRICIN"})
#     base = alt.Chart(chloro_data, title="CHEMICALS").mark_geoshape(
#         fill="lightgray",
#         stroke="black",
#         strokeWidth=1
#         ).properties(width=800, height=800)
#     choro = alt.Chart(chloro_data).mark_geoshape(
#         ).encode(color=alt.Color("POUNDS CHEMICAL APPLIED:Q")
#         ).add_selection(selection
#         ).transform_filter(
#             selection
#         )

#     (base + choro).save("Chemical_map.html")


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
    # plot_chem_produce(chloro_data)

    


if __name__ == '__main__':
    main()
