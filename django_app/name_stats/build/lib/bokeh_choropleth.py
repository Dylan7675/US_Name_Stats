import pandas as pd
from collections import OrderedDict
from bokeh_helpers import query_popularity
from bokeh_helpers import build_state_name_df
from bokeh_helpers import build_matrix
import os
from connector import connect
from bokeh.server.server import Server
from bokeh.sampledata.us_states import data as us_states
from bokeh.models import Slider, CustomJS, ColumnDataSource, LogColorMapper, ColorBar, LogTicker, LabelSet, Label
from bokeh.layouts import row, column, widgetbox
from bokeh.palettes import Viridis9 as palette
from bokeh.plotting import figure, save, show, output_file
from bokeh.io import curdoc


def main():
    name = 'Dylan'
    sex = 'M'

    """Begin formatting data for popularity trend model.
       Once data is formatted, build the model and add labels"""

    pop_df, vals = query_popularity(name, sex)
    x = pop_df['Year']
    y = pop_df['Qty']

    circ_data=dict(
        year=[x[0]],
        qty=[y[0]]
    )

    label_data = dict(
        year=[x[0]],
        qty=[y[0]],
        value=[str(y[0])]
    )

    circ_source = ColumnDataSource(circ_data)
    label_source = ColumnDataSource(label_data)

    pop_plt = figure(title="Popularity Trend", x_axis_label='Year', y_axis_label="Quantity")
    pop_plt.line(x, y, legend="Qty", line_width=2)
    pop_plt.circle('year', 'qty', source=circ_source, size=14, color="navy", alpha=0.5)
    labels = LabelSet(x='year', y='qty', text='value',
                      level='glyph', x_offset=5, y_offset=5, source=label_source)
    pop_plt.add_layout(labels)

    """Begin formatting data for choropleth model.
       Once data is formatted, configure the plot and add
       the slider and color bar"""

    state_name_dfs = build_state_name_df(name, sex)

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

    choro_plt = figure(title="US Name Distribution", tools=TOOLS,
                       x_axis_location=None, plot_width=850,
                       y_axis_location=None, plot_height=565,
                       tooltips=[("State", "@state_names"), ("Quantity", "@rate")])

    choro_plt.grid.grid_line_color = None
    choro_plt.hover.point_policy = "follow_mouse"

    choro_plt.patches('x', 'y', source=plot_source,
                      fill_color={'field': 'rate', 'transform': color_mapper},
                      line_color="white",
                      fill_alpha=.8, line_width=0.5)

    year_slider = Slider(start=1910, end=2017,
                         value=1910, step=1,
                         title="Year")

    color_bar = ColorBar(color_mapper=color_mapper, ticker=LogTicker(),
                         label_standoff=12, border_line_color=None, location=(0, 0))
    choro_plt.add_layout(color_bar, 'right')

    def slider_callback(attr, old, new):
        """Called by year_slider to cause interactive changes
        on the popularity trend and choropleth models"""

        yr = str(year_slider.value)

        #x is a pandas series
        xlist = x.tolist()

        # x~year y~qty
        if year_slider.value in xlist:

            new_circ_data = dict(
                year=[x[xlist.index(year_slider.value)]],
                qty=[y[xlist.index(year_slider.value)]]
            )

            new_label_data = dict(
                year=new_circ_data['year'],
                qty=new_circ_data['qty'],
                value=new_circ_data['qty']
            )

            label_source.data = new_label_data
            circ_source.data = new_circ_data

        choro_data = dict(
            x=state_xs,
            y=state_ys,
            state_names=states,
            rate=year_state_matrix[str(yr)]
        )
        plot_source.data = choro_data

    def input_callback(attr, old, new):
        print("replace")


    year_slider.on_change('value', slider_callback)

    layout = row(pop_plt, column(choro_plt, widgetbox(year_slider)))

    curdoc().add_root(layout)


main()