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
long_avg_wait = geyser_df.loc[geyser_df['kind'] == 'long','waiting'].mean()
long_avg_dur = geyser_df.loc[geyser_df['kind'] == 'long','duration'].mean()
short_avg_wait = geyser_df.loc[geyser_df['kind'] == 'short','waiting'].mean()
short_avg_dur = geyser_df.loc[geyser_df['kind'] == 'short','duration'].mean()

# UI Page Layout
ui.page_opts(title="Geyser Activity", fillable=True)

# UI Sidebar
# UI Page Inputs
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

    ui.hr()



#    @render.image
#    def image():
#        img = Image.open(urlopen("https://static.vecteezy.com/system/resources/previews/000/304/383/original/water-comping-out-of-the-ground-vector.jpg"))

# UI Main Panel
with ui.card(full_screen=True, min_height="60%"):
    ui.card_header("Geyser Duration Chart")

    with ui.layout_columns(col_widths=(4, 8)):
        with ui.value_box(
            theme="bg-gradient-blue-red",
        ):
            "Geyser Type - Long"

            ui.hr()
            @render.ui
            def long_wait():
                return f"Avg Wait Time: {round(long_avg_wait,1)} minutes"
        
            @render.ui
            def long_dur():
                return f"Avg Duration: {round(long_avg_dur,1)} seconds"
     
        @render_plotly
        def display_plot():
        # Fetch from the reactive calc function
            #deque_snapshot, df, latest_dictionary_entry = reactive_calc_combined()
            #geyser_df

            # Ensure the DataFrame is not empty before plotting
            #if not geyser_df.empty:
                # Convert Time Stamp to datetime for better plotting
                #df["Time Stamp"] = pd.to_datetime(df["Time Stamp"])
            
            # https://shiny.posit.co/py/components/outputs/plot-plotly/
            # Create scatter plot for readings
            fig = px.scatter(geyser_df,
                x="duration",
                y="waiting",
                color="kind",
                title="Duration and Waiting",
                labels={"duration": "Duration (seconds)", "waiting": "Wait Time (minutes)"},
                trendline="ols",
                            )

            return fig
        
        with ui.value_box(
            theme="bg-gradient-red-blue",
        ):
            "Geyser Type - Short"

            ui.hr()
            @render.ui
            def short_wait():
                return f"Avg Wait Time: {round(short_avg_wait,1)} minutes"
        
            @render.ui
            def short_dur():
                return f"Avg Duration: {round(short_avg_dur,1)} seconds"
    
   

# https://shiny.posit.co/py/components/outputs/data-grid/
with ui.card(full_screen=True, min_height="40%"):
    ui.card_header("Geyser Activity Data Table")

    @render.data_frame
    def display_data():
        geyser_df
        return render.DataGrid(geyser_df, width="100%")


# Reactive calc to filter by user selection on duration type
@reactive.calc
def filtered_select_data():
    filtered_data = geyser_df["kind"].isin(input.input_select())
    return geyser_df[filtered_data]