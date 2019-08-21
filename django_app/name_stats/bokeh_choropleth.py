import pandas as pd
from query_to_df import query
from collections import OrderedDict
import os
from connector import connect
from bokeh.server.server import Server
from bokeh.sampledata.us_states import data as us_states
from bokeh.models import Slider, CustomJS, ColumnDataSource, \
    LogColorMapper, ColorBar, LogTicker
from bokeh.layouts import row, column, widgetbox
from bokeh.palettes import Viridis9 as palette
from bokeh.plotting import figure, save, show, output_file
from bokeh.io import curdoc

#def heatmap_plot(name, sex):
def main():
    name = 'Dylan'
    sex = 'M'

    state_name_dfs = build_df(name, sex)

    years = [i for i in range(1910, 2018)]

    del us_states["HI"]
    del us_states["AK"]

    state_xs = [us_states[code]["lons"] for code in us_states]
    state_ys = [us_states[code]["lats"] for code in us_states]
    states = [state for state in us_states.keys()]

    palette.reverse()

    color_mapper = LogColorMapper(palette=palette)

    #Pass states list to keep the order the same as the xs/ys
    year_state_matrix = build_matrix(years, states, state_name_dfs)

    data=dict(
        x=state_xs,
        y=state_ys,
        state_names=states,
        rate=year_state_matrix['1910']
        )

    plot_source = ColumnDataSource(data)

    TOOLS = "pan,wheel_zoom,reset,hover,save"

    p = figure(title="US Name Distribution", tools=TOOLS,
               x_axis_location=None, plot_width=550,
               y_axis_location=None, plot_height=450,
               tooltips=[("State", "@state_names"), ("Quantity", "@rate")])

    p.grid.grid_line_color = None
    p.hover.point_policy = "follow_mouse"

    p.patches('x', 'y', source=plot_source,
              fill_color={'field': 'rate', 'transform': color_mapper}, line_color="white",
              fill_alpha=.8, line_width=0.5)

    year_slider = Slider(start=1910, end=2017,
                         value=1910, step=1,
                         title="Year")

    color_bar = ColorBar(color_mapper=color_mapper, ticker=LogTicker(),
                         label_standoff=12, border_line_color=None, location=(0, 0))
    p.add_layout(color_bar, 'right')

    def callback(attr, old, new):

        yr = str(year_slider.value)
        new_data = dict(
            x=state_xs,
            y=state_ys,
            state_names=states,
            rate=year_state_matrix[str(yr)]
        )
        plot_source.data = new_data

    year_slider.on_change('value', callback)

    layout = column(p,widgetbox(year_slider))

    curdoc().add_root(layout)


def build_matrix(years, states, state_name_dfs):
    """Input: Year List, State List, DF from build_df
       Output: Returns an OrderedDict of qty's per state by year"""

    qty_by_state = []
    matrix = OrderedDict()
    for year in years:

        if year not in matrix.keys():
            matrix[str(year)] = []
        for state in states:
            if year in state_name_dfs[state]['Year'].tolist():
                tempdf = state_name_dfs[state].query('Year == {0}'.format(year))
                qty_by_state.append(tempdf['Qty'].tolist()[0])
            else:
                qty_by_state.append(0)

        matrix[str(year)] = qty_by_state
        qty_by_state = []

    return matrix


def build_df(name, sex):
    """Input: Name and Sex to be queried
       Output: returns an Ordered dict of dataframes arranged by state
       This function Queries the database and builds state dataframes with
       data regarding the Name and Sex input"""

    connection, metadata, engine = connect()
    states = [file.split('.')[0] for file in os.listdir('./Names_By_State')]
    name_by_state = OrderedDict()

    for state in states:
        # check if state exist in db
        if not engine.dialect.has_table(engine, state):
            raise ValueError("{} not found in DB".format(state))
        else:
            query_db = "Select * from `{0}` where " \
                       "Name in ('{1}') AND " \
                       "Sex in ('{2}') " \
                       "Order by Year".format(state, name, sex)
            temp_df = pd.read_sql(query_db, connection)

        if state not in name_by_state.keys():
            name_by_state[state] = temp_df

    return (name_by_state)

#if __name__ == "__main__":
main()