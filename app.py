# PyShiny Imports
from shiny import reactive, render
from shiny.express import ui
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

# Icons import
from faicons import icon_svg

# ----------------------------------------------------------------------------------
 # Seaborn Datafile: https://github.com/mwaskom/seaborn-data/blob/master/geyser.csv
# ----------------------------------------------------------------------------------

theme.cerulean

# Reactive calc to be called by UI output components
# @reactive.calc()
# def reactive_calc():

# UI Page Layout
ui.page_opts(title="Geyser Activity", fillable=True)

# UI Page Inputs


# UI Sidebar
with ui.sidebar(open="open"):

    ui.input_select(
    "select",
    "Select Duration Type",
    {"Long":"Long","Short":"Short"}
    )

    ui.hr()
    
    ui.input_slider(
        "slider",
        "Select Wait Time Range",
        0,100,50
    )

# UI Main Panel

  
# UI Main Panel

