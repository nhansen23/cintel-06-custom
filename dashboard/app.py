# PyShiny Imports
from shiny import reactive, render
from shiny.express import ui, input
from shinyswatch import theme
# from shiny.types import ImgData

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

# Set Theme
theme.sandstone

# ---------------------------------------------------------------------------------
# Seaborn Datafile: https://github.com/mwaskom/seaborn-data/blob/master/geyser.csv
# ---------------------------------------------------------------------------------

geyser_df = sns.load_dataset("geyser")
short_wait = geyser_df["waiting"].min()
long_wait = geyser_df["waiting"].max()
short_dur = geyser_df["duration"].min()
long_dur = geyser_df["duration"].max()

UPDATE_INTERVAL_SECS: int = 2

DEQUE_SIZE: int = 5
reactive_value_wrapper = reactive.value(deque(maxlen=DEQUE_SIZE))

@reactive.calc()
def reactive_recordings():
    reactive.invalidate_later(UPDATE_INTERVAL_SECS)

    # Data grid data generation
#    latest_dur = round(random.uniform(input.dur_min(),input.dur_max()),3)
#    latest_wait = random.randint(input.wait_min(),input.wait_max())
    latest_kind = random.choice(["short","long"])
    new_recording_entry = {"duration":latest_dur, "waiting":latest_wait, "kind":latest_kind}

    reactive_value_wrapper.get().append(new_recording_entry)

    deque_snapshot = reactive_value_wrapper.get()

    latest_df = pd.DataFrame(deque_snapshot)

    latest_recording_entry = new_recording_entry

    return deque_snapshot, latest_df, latest_recording_entry

# UI Page Layout
ui.page_opts(title="Geyser Activity", fillable=True)

# UI Sidebar
with ui.sidebar(open="open"):
        
#    @render.image 
#    def image():
#        img: ImgData = {"src": "https://cdn.britannica.com/38/94438-050-1A943B1D/Old-Faithful-geyser-Yellowstone-National-Park-Wyoming.jpg", "width": "100px"}
#        return img
        
# UI Page Input
    # https://shiny.posit.co/py/components/inputs/select-single/
    ui.input_radio_buttons(
    "duration",
    "Select Duration Type",
    {"long":"Long","short":"Short","both": "Both"},
    selected="both",
    )

    ui.hr()

# Display duration and wait times
    with ui.layout_column_wrap(width=1 / 2): 
        with ui.card():
            ui.card_header("Shortest Wait", class_= "text-info")
            @render.text
            def wait_min_text():
                return short_wait

# Display duration and wait times
        with ui.card():
            ui.card_header("Longest Wait", class_="text-danger")
        
            @render.text
            def wait_max_text():
                return long_wait

# Display duration and wait times
        with ui.card():
            ui.card_header("Shortest Duration", class_= "text-info")
            @render.text
            def dur_min_text():
                return short_dur

# Display duration and wait times
        with ui.card():
            ui.card_header("Longest Duration", class_="text-danger")
            @render.text
            def dur_max_text():
                return long_dur

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
    ui.card_header("Geyser Duration Chart", class_="text-bg-secondary p-3")
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
        ui.card_header("Geyser Activity Data Table", class_="text-bg-secondary p-3")
        
        @render.data_frame
        def display_data():
            return render.DataGrid(filtered_duration_df(), width="100%")
    
    # Placeholder to simulate obtaining the latest geyser activity recordings
    with ui.card(full_screen=True, min_height="50%"):
        ui.card_header("Latest Recordings", class_="text-bg-secondary p-3")
            
        @render.data_frame
        def display_latest_df():
             return render.DataGrid(geyser_df.sample(5)) 
#            I tried to create a table that simulated live data but it doesn't work
#            deque_snapshot, latest_df, latest_recording_entry = reactive_recordings()
#            return render.DataGrid(latest_df,width="100%")

# Reactive calc to filter the data based upon the inputs
@reactive.calc
def filtered_duration_df():
    if input.duration() == "both":
        filtered_data = geyser_df
        return filtered_data 
    else:    
        filtered_data = geyser_df[geyser_df["kind"] == input.duration()]
        return filtered_data

#@reactive.calc()
#def wait_max():
#    return geyser_df[geyser_df["waiting"].max()]

#@reactive.calc()
#def wait_min():
#    return geyser_df[geyser_df["waiting"].min()]

#@reactive.calc()
#def dur_max():
#    return geyser_df[geyser_df["duration"].max()]

#@reactive.calc()
#def dur_min():
#    return geyser_df[geyser_df["duration"].min()]