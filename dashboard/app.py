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

# Set Theme
theme.sandstone

# ---------------------------------------------------------------------------------
# Seaborn Datafile: https://github.com/mwaskom/seaborn-data/blob/master/geyser.csv
# ---------------------------------------------------------------------------------

geyser_df = sns.load_dataset("geyser")

# UI Page Layout
ui.page_opts(title="Geyser Activity", fillable=True)

# Reactive calc to filter by user selection on duration type

# UI Sidebar
# UI Page Inputs
with ui.sidebar(open="open"):

    # https://shiny.posit.co/py/components/inputs/select-single/
    ui.input_radio_buttons(
    "duration",
    "Select Duration Type",
    {"long":"Long","short":"Short","both": "Both"},
    selected="both",
    )
    
    ui.hr()

    # https://shiny.posit.co/py/components/inputs/slider/
    ui.input_slider(
        "slider",
        "Select Wait Time Range",
        min=0,max=geyser_df['waiting'].max(),value=[geyser_df['waiting'].max()/6, geyser_df['waiting'].max()/1.5]
    )

    ui.hr()

#    @render.image
#    def image():
#        img = Image.open(urlopen("https://static.vecteezy.com/system/resources/previews/000/304/383/original/water-comping-out-of-the-ground-vector.jpg"))




# UI Main Panel
# Add value boxes to show average wait and duration times for each geyser activity type
with ui.layout_column_wrap(fill=False):
    with ui.value_box(showcase=icon_svg("hourglass-end"),
        theme="bg-gradient-blue-red",
        ):
        "Average Duration"

        @render.text
        def avg_dur():
            if input.duration() == "long":
                return f"{geyser_df.loc[geyser_df['kind'] == 'long','duration'].mean():.2f} seconds"
            elif input.duration() == "short":
                return f"{geyser_df.loc[geyser_df['kind'] == 'short','duration'].mean():.2f} seconds"
            elif input.duration() == "both":
                return f"{geyser_df['duration'].mean():.2f} seconds"   
        
    with ui.value_box(showcase=icon_svg("spinner"),
        theme="bg-gradient-blue-red",
        ):
        "Average Wait Time"

        @render.text
        def avg_wait():
            if input.duration() == "long":
                return f"{geyser_df.loc[geyser_df['kind'] == 'long','waiting'].mean():.1f} minutes"
            elif input.duration() == "short":
                return f"{geyser_df.loc[geyser_df['kind'] == 'short','waiting'].mean():.1f} minutes"
            elif input.duration() == "both":
                return f"{geyser_df['waiting'].mean():.1f} minutes"

with ui.card(full_screen=True, min_height="50%"):    
    ui.card_header("Geyser Duration Chart")
    @render_plotly
    def display_plot(height="100%"):
        # Fetch from the reactive calc function

            # Ensure the DataFrame is not empty before plotting
            #if not geyser_df.empty:
                # Convert Time Stamp to datetime for better plotting
                #df["Time Stamp"] = pd.to_datetime(df["Time Stamp"])
            
            # https://shiny.posit.co/py/components/outputs/plot-plotly/
            # Create scatter plot for readings
            fig = px.scatter(
                data_frame=filtered_duration_df(),
                x="duration",
                y="waiting",
                color="kind",
                title="Duration and Waiting",
                labels={"duration": "Duration (seconds)", "waiting": "Wait Time (minutes)"},
                trendline="ols",
                            )
            return fig
        
# https://shiny.posit.co/py/components/outputs/data-grid/
with ui.layout_columns(col_widths=(8, 4)):
    with ui.card(full_screen=True, min_height="50%"):
        ui.card_header("Geyser Activity Data Table")
        
        @render.data_frame
        def display_data():
            return render.DataGrid(filtered_duration_df(), width="100%")
    
    # Placeholder to simulate obtaining the latest geyser activity recordings
    with ui.card(full_screen=True, min_height="50%"):
        ui.card_header("Latest Recordings")
        
        @render.data_frame
        def display_latest():
            return render.DataGrid(geyser_df.iloc[5:])


# Reactive calc to filter the data based upon the inputs
@reactive.calc
def filtered_duration_df():
    if input.duration() == "both":
        filtered_data = geyser_df
        return filtered_data 
    else:    
        filtered_data = geyser_df[geyser_df["kind"] == input.duration()]
        return filtered_data

