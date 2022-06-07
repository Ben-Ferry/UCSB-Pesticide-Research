"""
This is the main file for processing data and visualizing it.
"""
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt


def load_in_data(
    shp_file_towns,
    chloro2014,
    chloro2015,
    chloro2016,
    chloro2017,
    chloro2018,
    data2013,
    data2010,
    data2009,
    data2008,
    data2012,
    data2011,
):
    """
    Loads in all the pesticide data for Santa Barbra County for the years
    2018-2008 and the shapefile and combines them into one geopandasDataFrame.
    """
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
    chloro_csv = [
        chloro2014,
        chloro2015,
        chloro2016,
        chloro2017,
        chloro2018,
        data2013,
        data2010,
        data2009,
        data2008,
        data2012,
        data2011,
    ]
    chloro_csv = pd.concat(chloro_csv)
    chemical_chloro = chloro_csv["CHEMICAL NAME"] == "CHLOROPICRIN"
    chemical_miner = chloro_csv["CHEMICAL NAME"] == "MINERAL OIL"
    chemical_dichlo = chloro_csv["CHEMICAL NAME"] == "1,3-DICHLOROPROPENE"
    chemical_sulf = chloro_csv["CHEMICAL NAME"] == "SULFUR DIOXIDE"
    chemical_potas = (
        chloro_csv["CHEMICAL NAME"] == "POTASSIUM N-METHYLDITHIOCARBAMATE"
    )
    county = chloro_csv["COUNTY NAME"] == "SANTA BARBARA"
    chloro_csv = chloro_csv.loc[
        county
        & (
            chemical_chloro
            | chemical_dichlo
            | chemical_potas
            | chemical_miner
            | chemical_sulf
        ),
        [
            "YEAR",
            "COUNTY NAME",
            "COMTRS",
            "CHEMICAL NAME",
            "POUNDS CHEMICAL APPLIED",
            "SITE NAME",
        ],
    ]
    chloro_data = sb_shape_towns.merge(
        chloro_csv, left_on="CO_MTRS", right_on="COMTRS", how="left"
    )
    return chloro_data


def plot_santa_barbara_sections(chloro_data):
    """
    This function take in the created geopandasDF and filters the data
    into four geoDFs. The function also plots each of these DFs as
    subplots.
    """
    chloro_mask = chloro_data["CHEMICAL NAME"] == "CHLOROPICRIN"
    chloro_plot = chloro_data.loc[
        chloro_mask, ["POUNDS CHEMICAL APPLIED", "geometry", "CHEMICAL NAME"]
    ]
    dichlo_mask = chloro_data["CHEMICAL NAME"] == "1,3-DICHLOROPROPENE"
    dichlo_plot = chloro_data.loc[
        dichlo_mask, ["POUNDS CHEMICAL APPLIED", "geometry", "CHEMICAL NAME"]
    ]
    mineral_mask = chloro_data["CHEMICAL NAME"] == "MINERAL OIL"
    mineral_plot = chloro_data.loc[
        mineral_mask, ["POUNDS CHEMICAL APPLIED", "geometry", "CHEMICAL NAME"]
    ]
    potas_mask = (
        chloro_data["CHEMICAL NAME"] == "POTASSIUM N-METHYLDITHIOCARBAMATE"
    )
    potas_plot = chloro_data.loc[
        potas_mask, ["POUNDS CHEMICAL APPLIED", "geometry", "CHEMICAL NAME"]
    ]
    fig, [[ax1, ax2], [ax3, ax4]] = plt.subplots(2, 2)
    chloro_data.plot(ax=ax1, color="#EEEEEE")
    chloro_data.plot(ax=ax2, color="#EEEEEE")
    chloro_data.plot(ax=ax3, color="#EEEEEE")
    chloro_data.plot(ax=ax4, color="#EEEEEE")
    chloro_plot.plot(
        ax=ax1, column="POUNDS CHEMICAL APPLIED", legend=True, cmap="plasma"
    )
    dichlo_plot.plot(ax=ax2, column="POUNDS CHEMICAL APPLIED", legend=True)
    mineral_plot.plot(
        ax=ax3, column="POUNDS CHEMICAL APPLIED", legend=True, cmap="magma"
    )
    potas_plot.plot(
        ax=ax4, column="POUNDS CHEMICAL APPLIED", legend=True, cmap="cividis"
    )
    ax1.set_title(
        "AMOUNT OF CHLOROPRICIN PER SECTION", loc="center", fontsize=6
    )
    ax2.set_title("AMOUNT OF 1,3-DICHLOROPROPENE PER SECTION", fontsize=6)
    ax3.set_title("AMOUNT OF MINERAL OIL PER SECTION", fontsize=6)
    ax4.set_title(
        "AMOUNT OF POTASSIUM N-METHYLDITHIOCARBAMATE PER SECTION", fontsize=6
    )
    plt.subplots_adjust(
        left=0.05, bottom=0.1, right=0.9, top=0.9, wspace=0.4, hspace=0.4
    )
    plt.savefig("Santa Barbara Chemicals by Section.png")


def plot_chemical_totals(chloro_data):
    """
    This function take in the created geopandasDF and filters the data
    into four geoDFs by chemical name and sums the pounds of chemcial
    applied. The function also plots each of these DFs as
    subplots.
    """
    chloro_mask = chloro_data["CHEMICAL NAME"] == "CHLOROPICRIN"
    chloro_plot = chloro_data.loc[
        chloro_mask, ["POUNDS CHEMICAL APPLIED", "geometry", "CHEMICAL NAME"]
    ]
    chloro_plot = chloro_plot.dissolve(by="CHEMICAL NAME", aggfunc="sum")
    dichlo_mask = chloro_data["CHEMICAL NAME"] == "1,3-DICHLOROPROPENE"
    dichlo_plot = chloro_data.loc[
        dichlo_mask, ["POUNDS CHEMICAL APPLIED", "geometry", "CHEMICAL NAME"]
    ]
    dichlo_plot = dichlo_plot.dissolve(by="CHEMICAL NAME", aggfunc="sum")
    mineral_mask = chloro_data["CHEMICAL NAME"] == "MINERAL OIL"
    mineral_plot = chloro_data.loc[
        mineral_mask, ["POUNDS CHEMICAL APPLIED", "geometry", "CHEMICAL NAME"]
    ]
    mineral_plot = mineral_plot.dissolve(by="CHEMICAL NAME", aggfunc="sum")
    potas_mask = (
        chloro_data["CHEMICAL NAME"] == "POTASSIUM N-METHYLDITHIOCARBAMATE"
    )
    potas_plot = chloro_data.loc[
        potas_mask, ["POUNDS CHEMICAL APPLIED", "geometry", "CHEMICAL NAME"]
    ]
    potas_plot = potas_plot.dissolve(by="CHEMICAL NAME", aggfunc="sum")
    fig, [[ax1, ax2], [ax3, ax4]] = plt.subplots(2, 2)
    chloro_data.plot(ax=ax1, color="#EEEEEE")
    chloro_data.plot(ax=ax2, color="#EEEEEE")
    chloro_data.plot(ax=ax3, color="#EEEEEE")
    chloro_data.plot(ax=ax4, color="#EEEEEE")
    chloro_plot.plot(
        ax=ax1, column="POUNDS CHEMICAL APPLIED", legend=True, cmap="plasma"
    )
    dichlo_plot.plot(ax=ax2, column="POUNDS CHEMICAL APPLIED", legend=True)
    mineral_plot.plot(
        ax=ax3, column="POUNDS CHEMICAL APPLIED", legend=True, cmap="magma"
    )
    potas_plot.plot(
        ax=ax4, column="POUNDS CHEMICAL APPLIED", legend=True, cmap="cividis"
    )
    ax1.set_title("TOTAL CHLOROPRICIN USAGE", loc="center", fontsize=6)
    ax2.set_title("TOTAL 1,3-DICHLOROPROPENE USAGE", fontsize=6)
    ax3.set_title("AMOUNT OF MINERAL OIL PER SECTION", fontsize=6)
    ax4.set_title("TOTAL POTASSIUM N-METHYLDITHIOCARBAMATE USAGE", fontsize=6)
    plt.subplots_adjust(
        left=0.05, bottom=0.1, right=0.9, top=0.9, wspace=0.4, hspace=0.4
    )
    plt.savefig("Santa Barbara Chemicals Total.png")


def main():
    """
    This is the main function.
    """
    chloro_data = load_in_data(
        "/Users/benferry/Desktop/GitHub/CSE-163-Final/Santa_Barbara_sections/"
        "pls_42_nad83.shp",
        "~/Desktop/GitHub/CSE-163-Final/" "Data_csv/2014_data.csv",
        "~/Desktop/GitHub/CSE-163-Final/" "Data_csv/2015_data.csv",
        "~/Desktop/GitHub/CSE-163-Final/" "Data_csv/2016_data.csv",
        "~/Desktop/GitHub/CSE-163-Final/" "Data_csv/2017_data.csv",
        "~/Desktop/GitHub/CSE-163-Final/" "Data_csv/2018_data.csv",
        "~/Desktop/GitHub/CSE-163-Final/" "Data_csv/2013_data.csv",
        "~/Desktop/GitHub/CSE-163-Final/" "Data_csv/2010_data.csv",
        "~/Desktop/GitHub/CSE-163-Final/" "Data_csv/2009_data.csv",
        "~/Desktop/GitHub/CSE-163-Final/" "Data_csv/2008_data.csv",
        "~/Desktop/GitHub/CSE-163-Final/" "Data_csv/2012_data.csv",
        "~/Desktop/GitHub/CSE-163-Final/" "Data_csv/2011_data.csv",
    )
    plot_santa_barbara_sections(chloro_data)
    plot_chemical_totals(chloro_data)


if __name__ == "__main__":
    main()
