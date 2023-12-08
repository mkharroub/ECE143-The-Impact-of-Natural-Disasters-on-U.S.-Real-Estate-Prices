import pandas as pd
import matplotlib.pyplot as plt
from scripts.clean import makeColorColumn
from matplotlib.ticker import FuncFormatter
from shapely.geometry import Polygon
import os

def plot_time_series(x_values, y_values, x_label="", y_label="", title="", path=""):
    """
    Plot a time series graph for given values of x and y.

    Parameters:
    - x_values (pd.Series): Time values for the x-axis.
    - y_values (pd.Series): Corresponding values for the y-axis.
    - x_label (str, optional): Label for the x-axis. Default is an empty string.
    - y_label (str, optional): Label for the y-axis. Default is an empty string.
    - title (str, optional): Title for the plot. Default is an empty string.

    Raises:
    - AssertionError: If the input x_values and y_values are not instances of pd.Series,
                      or if their shapes do not match.

    Returns:
    None
    """
    assert isinstance(x_values, pd.Series) and isinstance(y_values, pd.Series)
    assert x_values.shape == y_values.shape
    assert isinstance(x_label, str) and isinstance(y_label, str) and isinstance(title, str)
    assert isinstance(path, str)

    _, ax = plt.subplots(figsize=(8, 5))
    ax.plot(x_values.to_numpy(), y_values.to_numpy())
    ax.set_title(title, fontsize=20)
    ax.set_xlabel(x_label, fontsize=15)
    ax.set_ylabel(y_label, fontsize=15)
    ax.tick_params(axis='x', labelrotation=45, labelsize=15)

    if path:
        plt.savefig(path)

    plt.show()

def plot_two_time_series(x_values1, x_values2, y_values1, y_values2, x_label="", y_label="", title="", path=""):
    """
    Plot two time series graphs for given values of x1, x2, and y.

    Parameters:
    - x_values1 (pd.Series): Time values for the first x-axis.
    - x_values2 (pd.Series): Time values for the second x-axis.
    - y_values1 (pd.Series): Corresponding values for the first y-axis.
    - y_values2 (pd.Series): Corresponding values for the second y-axis.
    - x_label (str, optional): Label for the x-axis. Default is an empty string.
    - y_label (str, optional): Label for the y-axis. Default is an empty string.
    - title (str, optional): Title for the plot. Default is an empty string.

    Raises:
    - AssertionError: If the input x_values1, x_values2, y_values1, or y_values2 are not instances of pd.Series,
                      or if their shapes do not match.

    Returns:
    None
    """
    assert isinstance(x_values1, pd.Series) and isinstance(x_values2, pd.Series) and isinstance(y_values1, pd.Series) and isinstance(y_values2, pd.Series)
    assert x_values1.shape == y_values1.shape and x_values2.shape == y_values2.shape
    assert isinstance(x_label, str) and isinstance(y_label, str) and isinstance(title, str)
    assert isinstance(path, str)

    _, ax = plt.subplots(figsize=(8, 5))
    ax.plot(x_values1.to_numpy(), y_values1.to_numpy())
    ax.plot(x_values2.to_numpy(), y_values2.to_numpy())
    ax.set_title(title, fontsize=20)
    ax.set_xlabel(x_label, fontsize=15)
    ax.set_ylabel(y_label, fontsize=15)
    ax.tick_params(axis='x', labelrotation=45, labelsize=15)
    ax.legend()

    if path:
        plt.savefig(path)

    plt.show()

def plot_scatter(x_values, y_values, x_label="", y_label="", title="", path=""):
    """
    Plot a scatter plot for given x and y values.

    Parameters:
    - x_values (pd.Series): Values for the x-axis.
    - y_values (pd.Series): Values for the y-axis.
    - x_label (str, optional): Label for the x-axis. Default is an empty string.
    - y_label (str, optional): Label for the y-axis. Default is an empty string.
    - title (str, optional): Title for the plot. Default is an empty string.
    - path (str, optional): File path to save the plot as an image. Default is an empty string.

    Raises:
    - AssertionError: If x_values and y_values are not instances of pd.Series,
                      if their shapes do not match, or if x_label, y_label, title, or path are not strings.

    Returns:
    None
    """
    assert isinstance(x_values, pd.Series) and isinstance(y_values, pd.Series)
    assert x_values.shape == y_values.shape
    assert isinstance(x_label, str) and isinstance(y_label, str) and isinstance(title, str)
    assert isinstance(path, str)

    _, ax = plt.subplots(figsize=(6, 6))
    ax.set_title(title, fontsize=20)
    ax.set_xlabel(x_label, fontsize=15)
    ax.set_ylabel(y_label, fontsize=15)
    plt.scatter(x_values.to_numpy(), y_values.to_numpy())
    
    if path:
        plt.savefig(path)
        
    plt.show()

def plot_disasters_map(gdf, variable, label, save_name, title1="", anno=""):
    """
    Create and save a choropleth map of a GeoDataFrame based on a specified variable.

    Parameters:
    - gdf (pd.DataFrame): The GeoDataFrame containing geographic data.
    - variable (str): The variable used to determine choropleth colors.
    - label (str): The label for the colorbar.
    - save_name (str): File name to save the map as a PNG file.
    - title1 (str, optional): Title for the map. Default is an empty string.
    - anno (str, optional): Additional annotation for the map. Default is an empty string.

    Raises:
    - AssertionError: If any input argument is not of the expected type or if the filename format is invalid.

    Returns:
    None
    """
    assert isinstance(gdf, pd.DataFrame) and isinstance(variable, str) and isinstance(label, str)
    assert isinstance(save_name, str) and len(save_name) > 4 and save_name[-4:] == ".png"
    assert isinstance(title1, str) and isinstance(anno, str)

    # make a column for value_determined_color in gdf
    # set the range for the choropleth values with the upper bound the rounded up maximum value
    vmin, vmax = gdf[variable].min(), gdf[variable].max()
    colormap = "YlOrBr"
    gdf = makeColorColumn(gdf, variable, vmin, vmax)

    # create "visframe" as a re-projected gdf using EPSG 2163
    visframe = gdf.to_crs({'init': 'epsg:2163'})

    # create figure and axes for Matplotlib
    fig, ax = plt.subplots(1, figsize=(20, 14))
    # remove the axis box around the vis
    ax.axis('off')
    #visframe[~visframe.STUSPS.isin(['HI','AK'])].plot(linewidth=0.8, ax=ax, edgecolor='0.8')

    # set the font for the visualization to Helvetica
    hfont = {'fontname': 'Helvetica'}

    # add a title and annotation
    ax.set_title(title1, **hfont,
                 fontdict={'fontsize': '42', 'fontweight': '1'}, y=0.93)

    # Create colorbar legend
    fig = ax.get_figure()
    # add colorbar axes to the figure
    # l:left, b:bottom, w:width, h:height; in normalized unit (0-1)
    cbax = fig.add_axes([0.75, 0.18, 0.02, 0.30])
    cbax.set_title(
        label, **hfont, fontdict={'fontsize': '26', 'fontweight': '0'}, pad=25)

    # add color scale
    sm = plt.cm.ScalarMappable(cmap=colormap,
                               norm=plt.Normalize(vmin=vmin, vmax=vmax))
    # reformat tick labels on legend
    sm._A = []
    comma_fmt = FuncFormatter(lambda x, p: format(int(x), ','))
    fig.colorbar(sm, cax=cbax, format=comma_fmt)
    tick_font_size = 24
    cbax.tick_params(labelsize=tick_font_size)

    ax.annotate(anno, xy=(0.22, .085), xycoords='figure fraction', fontsize=16, color='#555555')

    # create map
    for row in visframe.itertuples():
        if row.STUSPS not in ['AK', 'HI']:
            vf = visframe[visframe.STUSPS == row.STUSPS]
            c = gdf[gdf.STUSPS == row.STUSPS][0:1].value_determined_color.item()
            vf.plot(color=c, linewidth=0.8, ax=ax, edgecolor='0.8')

    # add Alaska
    akax = fig.add_axes([0.1, 0.17, 0.17, 0.16])
    akax.axis('off')
    # polygon to clip western islands
    polygon = Polygon([(-170, 50), (-170, 72), (-140, 72), (-140, 50)])
    alaska_gdf = gdf[gdf.STUSPS == 'AK']
    alaska_gdf.clip(polygon).plot(
        color=gdf[gdf.STUSPS == 'AK'].value_determined_color, linewidth=0.8, ax=akax, edgecolor='0.8')

    # add Hawaii
    hiax = fig.add_axes([.28, 0.20, 0.1, 0.1])
    hiax.axis('off')
    # polygon to clip western islands
    hipolygon = Polygon([(-160, 0), (-160, 90), (-120, 90), (-120, 0)])
    hawaii_gdf = gdf[gdf.STUSPS == 'HI']
    hawaii_gdf.clip(hipolygon).plot(
        column=variable, color=hawaii_gdf['value_determined_color'], linewidth=0.8, ax=hiax, edgecolor='0.8')

    fig.savefig(os.getcwd()+save_name, dpi=400, bbox_inches="tight")

def plot_disasters_map1(gdf, save_name, title="", label1="", label2=""):
    """
    Create and save a choropleth map of disaster levels using Matplotlib and GeoPandas.

    Parameters:
    - gdf (pd.DataFrame): The DataFrame containing geographical and disaster level data.
    - save_name (str): File name to save the plot as a PNG file.
    - title (str): Title for the map.
    - label1 (str): Label for the first legend item.
    - label2 (str): Label for the second legend item.

    Raises:
    - AssertionError: If any input argument is not of the expected type or if the filename format is invalid.

    Returns:
    None
    """
    assert isinstance(gdf, pd.DataFrame) and isinstance(label1, str) and isinstance(label2, str)
    assert isinstance(save_name, str) and len(save_name) > 4 and save_name[-4:] == ".png"
    assert isinstance(title, str)

    visframe = gdf.to_crs({'init': 'epsg:2163'})
    visframe = visframe[~visframe.STUSPS.isin(['HI','AK'])]

    # create figure and axes for Matplotlib
    fig, ax = plt.subplots(1, figsize=(24, 16))
    ax.axis('off')

    # set the font for the visualization to Helvetica
    hfont = {'fontname': 'Helvetica'}

    # add a title and annotation
    ax.set_title(title, **hfont,
                 fontdict={'fontsize': '30', 'fontweight': '1'}, y=0.93)

    # Create colorbar legend
    fig = ax.get_figure()

    # create map
    for row in visframe.itertuples():
        if row.STUSPS not in ['AK', 'HI']:
            vf = visframe[(visframe.STUSPS == row.STUSPS) & (visframe.NAME == row.NAME)]
            affected_level = gdf[(gdf.STUSPS == row.STUSPS) & (gdf.NAME == row.NAME)]['affected_level'].item()
            if affected_level == 'high':
                color = 'red'
            elif affected_level == 'low':
                color = 'orange'
            else:
                color = 'skyblue'
            
            vf.plot(color=color, linewidth=0.8, ax=ax, edgecolor='0.8',legend=True)
    
    red_patch = plt.Line2D([0], [0], marker='s', color='w', markerfacecolor='red', markersize=18, label=label1)
    blue_patch = plt.Line2D([0], [0], marker='s', color='w', markerfacecolor='orange', markersize=18, label=label2)

    legend = ax.legend(handles=[red_patch, blue_patch], loc='lower left')
    for label in legend.get_texts():
        label.set_fontsize(20) 

    fig.savefig(os.getcwd()+save_name, dpi=400, bbox_inches="tight")