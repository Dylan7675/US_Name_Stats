from bokeh.plotting import figure, output_file, save
import pandas as pd
from query_to_df import query
import os


def plot(name, sex):

    df, vals = query(name, sex)

    x = df['Year']
    y = df['Qty']

    plt = figure(title="Popularity Trend", x_axis_label='Year', y_axis_label="Quantity")
    plt.line(x,y, legend="Qty", line_width=2)
    save(plt)

    return(plt)


if __name__ == "__main__":
    main()