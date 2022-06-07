"""
This is the main file for processing data and visualizing it.
"""
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sn
import statsmodels.api as sm
import altair as alt


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
    guadalpue,
    santmar,
):
    """
    Loads in all the data for Santa Barbra County for the years 2018-2008 and
    combines thenm into 1 big CSV
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
    guadalpue = pd.read_csv(guadalpue)
    santmar = pd.read_csv(santmar)

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
    print(len(chloro_data["SITE NAME"].unique()))

    return chloro_data


def find_fit_guad(chloro_data, guadalpue):
    """
    Calculates the mean and Standard deviation for the use of
    CHLOROPICRIN for Santa Barbra and compares it to the most
    recent data by Guadalupe
    """
    pounds_chloro_sd = chloro_data[
        chloro_data["CHEMICAL NAME"] == "CHLOROPICRIN"
    ]
    total_applied = pounds_chloro_sd["POUNDS CHEMICAL APPLIED"]
    mean_usage = total_applied.mean()
    print("All County Mean:", mean_usage)
    standard_dev = total_applied.std()
    print("All County Standard Deviation:", standard_dev)

    numbers_guad = []
    for line in guadalpue["POUNDS_CHEMICAL_APPLIED"]:
        new_num = line - mean_usage
        numbers_guad.append(new_num)

    teststat, pvalue = sm.stats.ztest(numbers_guad, value=0)
    sn.distplot(numbers_guad)
    plt.title("Guadalupe CHLOROPICRIN Usage Distribution Plot")
    plt.show()
    print("Test Statistic for Guadalupe:", teststat)
    print("p-value for Guadalupe:", pvalue)


def find_fit_santa(chloro_data, santmar):
    """
    Calculates the mean and Standard deviation for the use of CHLOROPICRIN for
    Santa Barbra and compares it to the most recent data by Santa Maria
    """
    pounds_chloro_sd = chloro_data[
        chloro_data["CHEMICAL NAME"] == "CHLOROPICRIN"
    ]
    total_applied = pounds_chloro_sd["POUNDS CHEMICAL APPLIED"]
    mean_usage = total_applied.mean()

    numbers_sant = []
    for line in santmar["POUNDS_CHEMICAL_APPLIED"]:
        new_num1 = line - mean_usage
        numbers_sant.append(new_num1)
    teststat, pvalue = sm.stats.ztest(numbers_sant, value=0)
    sn.distplot(numbers_sant)
    plt.title("Santa Maria CHLOROPICRIN Usage Distribution Plot")
    plt.show()
    print("Test Statistic for Santa Maria:", teststat)
    print("p-value for Santa Maria:", pvalue)


def plot_products(chloro_data):
    """
    Plots the top 5 crops by the ussage of
    pestisides on them as a bar graph utilizing altair and spearates
    those bars by the kind of toxic pestiside used on them.
    """
    strawberry = chloro_data["SITE NAME"] == "STRAWBERRY (ALL OR UNSPEC)"
    carrots = chloro_data["SITE NAME"] == "CARROTS, GENERAL"
    grapes = chloro_data["SITE NAME"] == "GRAPES, WINE"
    lemons = chloro_data["SITE NAME"] == "LEMON"
    avacados = chloro_data["SITE NAME"] == "AVOCADO (ALL OR UNSPEC)"
    top_5 = chloro_data.loc[
        strawberry | carrots | grapes | lemons | avacados,
        ["POUNDS CHEMICAL APPLIED", "SITE NAME", "CHEMICAL NAME"],
    ]
    bars = (
        alt.Chart(top_5)
        .mark_bar()
        .encode(
            x=alt.X("sum(POUNDS CHEMICAL APPLIED):Q", stack="zero"),
            y=alt.Y("SITE NAME:N"),
            color=alt.Color("CHEMICAL NAME"),
        )
        .properties(title="Top 5 Foods by Pounds of Petisides Applied")
    )

    text = (
        alt.Chart(top_5)
        .mark_text(dx=-15, dy=3, color="white")
        .encode(
            x=alt.X("sum(POUNDS CHEMICAL APPLIED):Q", stack="zero"),
            y=alt.Y("SITE NAME:N"),
            detail="CHEMICAL NAME:N",
        )
    )

    (bars + text).resolve_scale()
    (bars + text).save("Produce_map.html")


def main():
    """
    This is the main function.
    """
    chloro_data = load_in_data(
        "/Users/thomaskanenaga/Documents/GitHub/CSE-163-Final/"
        "Santa_Barbara_sections/pls_42_nad83.shp",
        "~/Documents/GitHub/CSE-163-Final/" "Data_csv/2014_data.csv",
        "~/Documents/GitHub/CSE-163-Final/" "Data_csv/2015_data.csv",
        "~/Documents/GitHub/CSE-163-Final/" "Data_csv/2016_data.csv",
        "~/Documents/GitHub/CSE-163-Final/" "Data_csv/2017_data.csv",
        "~/Documents/GitHub/CSE-163-Final/" "Data_csv/2018_data.csv",
        "~/Documents/GitHub/CSE-163-Final/" "Data_csv/2013_data.csv",
        "~/Documents/GitHub/CSE-163-Final/" "Data_csv/2010_data.csv",
        "~/Documents/GitHub/CSE-163-Final/" "Data_csv/2009_data.csv",
        "~/Documents/GitHub/CSE-163-Final/" "Data_csv/2008_data.csv",
        "~/Documents/GitHub/CSE-163-Final/" "Data_csv/2012_data.csv",
        "~/Documents/GitHub/CSE-163-Final/" "Data_csv/2011_data.csv",
        "~/Documents/GitHub/CSE-163-Final/" "Data_csv/GuadalupeCloro2018.csv",
        "~/Documents/GitHub/CSE-163-Final/"
        "Data_csv/SantaMariaChloro2018.csv",
    )
    guadalpue = pd.read_csv(
        "~/Documents/GitHub/CSE-163-Final/" "Data_csv/GuadalupeCloro2018.csv"
    )
    santmar = pd.read_csv(
        "~/Documents/GitHub/CSE-163-Final/" "Data_csv/SantaMariaChloro2018.csv"
    )
    find_fit_guad(chloro_data, guadalpue)
    find_fit_santa(chloro_data, santmar)
    plot_products(chloro_data)


if __name__ == "__main__":
    main()
