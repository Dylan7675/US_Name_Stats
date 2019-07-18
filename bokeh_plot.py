from bokeh.plotting import figure, output_file, show
import pandas as pd
from query_to_df import query
import os


def main():

    df, vals = query()

    os.chdir('bokeh')

    output_file("{0}-{1}.html".format(vals['name'], vals['sex']))
    x = df['Year']
    y = df['Qty']

    plt = figure(title="Popularity Trend", x_axis_label='Year', y_axis_label="Quantity")
    plt.line(x,y, legend="Qty", line_width=2)
    show(plt)


if __name__ == "__main__":
    main()
