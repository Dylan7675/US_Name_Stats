import pandas as pd
from collections import OrderedDict
from bokeh_helpers import query_popularity, build_matrix, build_state_name_df, check_tables
import os
from validators import name_validation
from connector import connect
from bokeh.server.server import Server
from bokeh.sampledata.us_states import data as us_states
from bokeh.models import Slider, CustomJS, ColumnDataSource, LogColorMapper, ColorBar, LogTicker, LabelSet, Label
from bokeh.models.widgets import Button, RadioGroup, TextInput, Paragraph
from bokeh.events import ButtonClick
from bokeh.layouts import row, column, widgetbox
from bokeh.palettes import Viridis9 as palette
from bokeh.plotting import figure, save, show, output_file
from bokeh.io import curdoc


def main():
    name = 'Dylan'
    sex = 'M'

    years = [i for i in range(1910, 2018)]

    if "HI" in us_states.keys():
        del us_states["HI"]

    if "AK" in us_states.keys():
        del us_states["AK"]

    state_xs = [us_states[code]["lons"] for code in us_states]
    state_ys = [us_states[code]["lats"] for code in us_states]
    states = [state for state in us_states.keys()]

    """Begin formatting data for popularity trend model.
       Once data is formatted, build the model and add labels"""

    data_sources = create_dataset(name, sex, years, states, state_xs, state_ys)

    #adding layout tools and color pallete
    name_field = TextInput(value="", title="Name")
    sex_selection = RadioGroup(
        labels=["Male", "Female"], active=0)
    sub_button = Button(label="Submit", button_type="success", disabled=False)
    directions = Paragraph(text="""Type in any name and select the sex you would like to query.
        Then press Submit to display your results.""",
              width=250, height=60)

    palette.reverse()
    color_mapper = LogColorMapper(palette=palette)

    #create popularity trend model
    pop_plt = figure(title="Popularity Trend", x_axis_label='Year', y_axis_label="Quantity")
    pop_plt.line('x', 'y', source=data_sources['line_source'], legend="Qty", line_width=2)
    pop_plt.circle('year', 'qty', source=data_sources['circ_source'], size=14, color="navy", alpha=0.5)
    labels = LabelSet(x='year', y='qty', text='value',
                      level='glyph', x_offset=5, y_offset=5, source=data_sources['label_source'])
    pop_plt.add_layout(labels)

    #create the choropleth model
    TOOLS = "pan,wheel_zoom,reset,hover,save"

    choro_plt = figure(title="US Name Distribution", tools=TOOLS,
                       x_axis_location=None, plot_width=850,
                       y_axis_location=None, plot_height=565,
                       tooltips=[("State", "@state_names"), ("Quantity", "@rate")])

    choro_plt.grid.grid_line_color = None
    choro_plt.hover.point_policy = "follow_mouse"

    choro_plt.patches('x', 'y', source=data_sources['choropleth_source'],
                      fill_color={'field': 'rate', 'transform': color_mapper},
                      line_color="white",
                      fill_alpha=.8, line_width=0.5)

    year_slider = Slider(start=1910, end=2017,
                         value=1910, step=1,
                         title="Year")

    color_bar = ColorBar(color_mapper=color_mapper, ticker=LogTicker(),
                         label_standoff=12, border_line_color=None, location=(0, 0))
    choro_plt.add_layout(color_bar, 'right')

    #handlers and callbacks
    def slider_callback(attr, old, new):
        """Called by year_slider to cause interactive changes
        on the popularity trend and choropleth models"""

        yr = str(year_slider.value)

        #x is a pandas series
        xlist = data_sources['line_source'].data['x'].tolist()

        # x~year y~qty
        if year_slider.value in xlist:

            new_circ_data = dict(
                year=[data_sources['line_source'].data['x'][xlist.index(year_slider.value)]],
                qty=[data_sources['line_source'].data['y'][xlist.index(year_slider.value)]]
            )

            new_label_data = dict(
                year=new_circ_data['year'],
                qty=new_circ_data['qty'],
                value=new_circ_data['qty']
            )

            data_sources['label_source'].data = new_label_data
            data_sources['circ_source'].data = new_circ_data

        choro_data = dict(
            x=state_xs,
            y=state_ys,
            state_names=states,
            rate=data_sources['matrix'][str(yr)]
        )
        data_sources['choropleth_source'].data = choro_data

    def text_input_handler(attr, old, new):

        new_name = new

        try:
            name_validation(new_name)

            try:
                new_name = new_name.capitalize()
                check_tables(new_name)

                new_query_data = dict(
                    name=[new_name],
                    sex=[data_sources["query_source"].data["sex"][0]]
                )
                query_data = ColumnDataSource(new_query_data)
                data_sources['query_source'] = query_data

            except ValueError:
                name_field.value = f"Sorry, {new_name} doesn't exist in the database"

        except ValueError:
            name_field.value = "Enter a name with valid letters only."

    def radio_handler(new):
        #value based on radio button index: 0-Male 1-Female
        if new == 0:
            sex = 'M'
        else:
            sex = 'F'

        new_query_data = dict(
            name=[data_sources["query_source"].data["name"][0]],
            sex=[sex]
        )

        query_data = ColumnDataSource(new_query_data)
        data_sources['query_source'] = query_data

    def input_handler():

        new_name = str(name_field.value).capitalize()

        if sex_selection.active == 0:
            new_sex = 'M'
        else:
            new_sex = 'F'

        data_dict = get_data(new_name, new_sex, years, states)

        new_query_data = dict(
            name=[new_name],
            sex=[new_sex]
        )
        data_sources['query_source'].data = new_query_data

        new_line_data = dict(
            x=data_dict['pop_df']['Year'],
            y=data_dict['pop_df']['Qty']
        )
        data_sources['line_source'].data = new_line_data
        xlist = data_sources['line_source'].data['x'].tolist()

        if year_slider.value not in xlist:

            new_circ_data = dict(
                year=[data_sources['line_source'].data['x'][0]],
                qty=[data_sources['line_source'].data['y'][0]]
            )
        else:
            new_circ_data = dict(
                year=[data_sources['line_source'].data['x'][xlist.index(year_slider.value)]],
                qty=[data_sources['line_source'].data['y'][xlist.index(year_slider.value)]]
            )

        new_label_data = dict(
            year=new_circ_data['year'],
            qty=new_circ_data['qty'],
            value=new_circ_data['qty']
        )

        new_choropleth_data = dict(
            x=state_xs,
            y=state_ys,
            state_names=states,
            rate=data_dict['matrix'][str(year_slider.value)]
        )

        data_sources['circ_source'].data = new_circ_data
        data_sources['label_source'].data = new_label_data
        data_sources['choropleth_source'].data = new_choropleth_data
        data_sources['matrix'] = data_dict['matrix']

    year_slider.on_change('value', slider_callback)
    sex_selection.on_click(radio_handler)
    name_field.on_change('value', text_input_handler)
    sub_button.on_click(input_handler)

    layout = row(column(directions, name_field, sex_selection, sub_button),
                 row(pop_plt, column(choro_plt, widgetbox(year_slider))))

    curdoc().add_root(layout)


def get_data(name, sex, years, states):

    pop_df = query_popularity(name, sex)

    state_name_dfs = build_state_name_df(name, sex)

    #Pass states list to keep the order the same as the xs/ys
    year_state_matrix = build_matrix(years, states, state_name_dfs)

    data_dict = dict(
        pop_df=pop_df,
        matrix=year_state_matrix
    )

    return data_dict

def create_dataset(name, sex, years, states, state_xs, state_ys):

    data_dict = get_data(name, sex, years, states)

    query_data = dict(
        name=[name],
        sex=[sex]
    )

    line_data = dict(
        x=data_dict['pop_df']['Year'],
        y=data_dict['pop_df']['Qty']
    )

    circ_data = dict(
        year=[line_data['x'][0]],
        qty=[line_data['y'][0]]
    )

    label_data = dict(
        year=circ_data['year'],
        qty=circ_data['qty'],
        value=[str(circ_data['qty'][0])]
    )

    choropleth_data=dict(
        x=state_xs,
        y=state_ys,
        state_names=states,
        rate=data_dict['matrix']['1910']
        )

    query_source = ColumnDataSource(query_data)
    choropleth_source = ColumnDataSource(choropleth_data)
    line_source = ColumnDataSource(line_data)
    circ_source = ColumnDataSource(circ_data)
    label_source = ColumnDataSource(label_data)

    data_source = dict(
        line_source=line_source,
        circ_source=circ_source,
        label_source=label_source,
        choropleth_source=choropleth_source,
        matrix=data_dict['matrix'],
        query_source=query_source
    )

    return data_source


main()