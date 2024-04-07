# PyShiny Imports
from shiny import reactive, render
from shiny.express import ui, input
from shinyswatch import theme

# Python Standard Library Imports
import random
from datetime import datetime
from collections import deque
import plotly.express as px
from shinywidgets import render_plotly
from scipy import stats

# Pandas import for data
import pandas as pd
import seaborn as sns

# Icons import
from faicons import icon_svg

from urllib.request import urlopen
from PIL import Image

# ----------------------------------------------------------------------------------
 # Seaborn Datafile: https://github.com/mwaskom/seaborn-data/blob/master/geyser.csv
# ----------------------------------------------------------------------------------

df = sns.load_dataset("geyser")

theme.sandstone

# Reactive calc to be called by UI output components
# @reactive.calc()
# def reactive_calc():

# UI Page Layout
ui.page_opts(title="Geyser Activity", fillable=True)

# UI Page Inputs


# UI Sidebar
with ui.sidebar(open="open"):

    # https://shiny.posit.co/py/components/inputs/select-single/
    ui.input_select(
    "select",
    "Select Duration Type",
    {"Long":"Long","Short":"Short"}
    )

    ui.hr()

    # https://shiny.posit.co/py/components/inputs/slider/
    ui.input_slider(
        "slider",
        "Select Wait Time Range",
        0,100,50
    )

    ui.h2()
    
    @render.image
    def image():
        img = Image.open(urlopen("https://static.vecteezy.com/system/resources/previews/000/304/383/original/water-comping-out-of-the-ground-vector.jpg"))

# UI Main Panel
with ui.card(full_screen=True, min_height="60%"):
    ui.card_header("Geyser Duration Chart")

    @render_plotly
    def display_plot():
    # Fetch from the reactive calc function
        #deque_snapshot, df, latest_dictionary_entry = reactive_calc_combined()

        # Ensure the DataFrame is not empty before plotting
        #if not df.empty:
            # Convert Time Stamp to datetime for better plotting
            #df["Time Stamp"] = pd.to_datetime(df["Time Stamp"])

        # Create scatter plot for readings
        fig = px.scatter(df,
            x="duration",
            y="waiting",
            title="Duration and Waiting",
            labels={"duration": " seconds", "waiting": " minutes"},
            color_discrete_sequence=["black"] )    
            
        # https://shiny.posit.co/py/components/outputs/plot-plotly/

# https://shiny.posit.co/py/components/outputs/data-grid/
with ui.card(full_screen=True, min_height="40%"):
    ui.card_header("Geyser Activity Data Table")
