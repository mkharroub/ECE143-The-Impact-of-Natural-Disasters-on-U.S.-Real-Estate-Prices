import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd

def plot_bar_and_line(x, y_bar, y_line, name_bar="", name_line="", title="", x_title="", y_bar_title="", y_line_title="", filename="plot_bar_line.html"):
    """
    Create and display a combined bar and line plot using Plotly.

    Parameters:
    - x (list): The x-axis values.
    - y_bar (list): The y-axis values for the bar plot.
    - y_line (list): The y-axis values for the line plot.
    - name_bar (str, optional): Name for the bar plot. Default is an empty string.
    - name_line (str, optional): Name for the line plot. Default is an empty string.
    - title (str, optional): Title for the plot. Default is an empty string.
    - x_title (str, optional): Label for the x-axis. Default is an empty string.
    - y_bar_title (str, optional): Label for the y-axis (bar plot). Default is an empty string.
    - y_line_title (str, optional): Label for the y-axis (line plot). Default is an empty string.
    - filename (str, optional): File name to save the plot as an HTML file. Default is an empty string.

    Raises:
    - AssertionError: If any input argument is not of the expected type or if the filename format is invalid.

    Returns:
    None
    """
    assert isinstance(x, list) and isinstance(y_bar, list) and isinstance(y_line, list)
    assert isinstance(name_bar, str) and isinstance(name_line, str) and isinstance(title, str)
    assert isinstance(x_title, str) and isinstance(y_bar_title, str) and isinstance(y_line_title, str)
    assert isinstance(filename, str) and len(filename) > 5 and filename[-5:] == ".html"

    fig = go.Figure()

    fig.add_trace(go.Bar(x=x, y=y_bar, name=name_bar, marker_color='orange'))
    fig.add_trace(go.Scatter(x=x, y=y_line, mode='lines', name=name_line, yaxis='y2',marker_color='blue'))

    fig.update_layout(
        title=title,
        title_font_size =30,
        title_x=0.5,
        xaxis=dict(title=x_title,titlefont_size=20,tickfont=dict(size=16)),
        yaxis=dict(title=y_bar_title, titlefont=dict(color='orange'),titlefont_size=20,tickfont=dict(size=16)),
        yaxis2=dict(title=y_line_title, titlefont=dict(color='blue'), titlefont_size=20,overlaying='y', side='right',tickfont=dict(size=16)),
        height=500,
        width=1000,
        legend=dict(x=0.02, y=1.0, font=dict(size=16))
    )

    fig.write_html("./plots/"+filename)
    fig.show()

def plot_bar_chart(name, val,title="", title_yaxis="",filename="plot_bar.html"):
    """
    Create and display a bar chart using Plotly Express.

    Parameters:
    - name (list): Labels for the bars on the x-axis.
    - val (list): Values for the bars on the y-axis.
    - title (str): Title for the plot.
    - title_yaxis (str): Label for the y-axis.
    - filename (str): File name to save the plot as an HTML file.

    Raises:
    - AssertionError: If any input argument is not of the expected type or if the filename format is invalid.

    Returns:
    None
    """
    assert isinstance(name, (list, np.ndarray)) and isinstance(val, (list, np.ndarray)) and isinstance(title, str) and isinstance(title_yaxis, str)
    assert isinstance(filename, str) and len(filename) > 5 and filename[-5:] == ".html"

    x_labels=[]
    for label in name:
        x_labels.append(label.replace(' ','<br>'))
    formatted_val = [f'{v:,}' for v in val]
    fig = px.bar(x=x_labels, y=val, labels={'x':'', 'y':''}, title=title)
    fig.update_traces(marker_color='orange',text=formatted_val, textposition='outside', textfont = dict(size=15), hovertemplate='%{x}: %{text}')
    fig.update_layout(
        title_font_size =30,
        title_x=0.5,
        xaxis=dict(
           tickfont=dict(size=16)),
        yaxis=dict(title=title_yaxis, titlefont_size=20, tickfont_size = 16, side='top'),
        height=570,
        width=700,
        barmode='group',
        bargap=0.5,
        bargroupgap=0.1,
    )
    fig.write_html("./plots/"+filename)
    fig.show()

def plot_scatter_line(x, y, name="", title="", x_title="", y_title="", filename="plot_scatter.html"):
    """
    Create and display a scatter plot with a line using Plotly.

    Parameters:
    - x (list or np.ndarray): Values for the x-axis.
    - y (list or np.ndarray): Values for the y-axis.
    - name (str): Name for the plot.
    - title (str): Title for the plot.
    - x_title (str): Label for the x-axis.
    - y_title (str): Label for the y-axis.
    - filename (str): File name to save the plot as an HTML file.

    Raises:
    - AssertionError: If any input argument is not of the expected type or if the filename format is invalid.

    Returns:
    None
    """
    assert isinstance(x, (list, np.ndarray)) and isinstance(y, (list, np.ndarray)) and isinstance(name, str)
    assert isinstance(title, str) and isinstance(x_title, str) and isinstance(y_title, str)
    assert isinstance(filename, str) and len(filename) > 5 and filename[-5:] == ".html"
    
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=x, y=y, mode='lines+markers',name=name, marker_color='Blue'))

    # update layout
    fig.update_layout(
        title=title,
        title_font_size =30,
        title_x=0.5,
        xaxis=dict(title=x_title,titlefont_size=20,tickfont=dict(size=18)),
        yaxis=dict(title=y_title,titlefont_size=20,tickfont=dict(size=18)),
        height=500,
        width=1000,
        legend=dict(x=0.02, y=1.0, font=dict(size=16))
    )

    fig.write_html("./plots/"+filename)
    fig.show()

def plot_heatmap(heatmap, title="", x_title="", y_title="", filename="plot_heatmap.html"):
    """
    Create and display a heatmap using Plotly based on a pandas DataFrame.

    Parameters:
    - heatmap (pd.DataFrame): The DataFrame containing the heatmap data.
    - title (str): Title for the heatmap.
    - x_title (str): Label for the x-axis.
    - y_title (str): Label for the y-axis.
    - filename (str): File name to save the plot as an HTML file.

    Raises:
    - AssertionError: If the input heatmap is not a pandas DataFrame or if any other input argument is not of the expected type.
                      Also, raises an AssertionError if the filename format is invalid.

    Returns:
    None
    """
    assert isinstance(heatmap, pd.DataFrame)
    assert isinstance(title, str) and isinstance(x_title, str) and isinstance(y_title, str)
    assert isinstance(filename, str) and len(filename) > 5 and filename[-5:] == ".html"

    fig = go.Figure(data=go.Heatmap(
                   z=heatmap.values,
                   x=heatmap.columns, 
                   y=heatmap.index,
                   colorscale='Viridis',
                   hoverongaps=False))

    fig.update_layout(
        title=title,
        title_font_size =30,
        title_x=0.5,
        xaxis=dict(title=x_title,tickfont_size = 16, titlefont_size = 20, zeroline=False),
        yaxis=dict(title=y_title,showticklabels=False,showgrid=False,zeroline=False),
        width=1000,
        height=600,
        margin=dict(l=50, r=50, b=100, t=100),
        xaxis_range=[heatmap.columns[0], heatmap.columns[-1]],
    )

    fig.write_html("./plots/"+filename)
    fig.show()

def plot_two_scatter_lines(x, y1, y2, name1="", name2="", title="", x_title="", y_title1="", y_title2="", filename="plot_two_scatter.html"):
    """
    Create and display a plot with two scatter lines using Plotly.

    Parameters:
    - x (list or np.ndarray): Values for the x-axis.
    - y1 (list or np.ndarray): Values for the first y-axis.
    - y2 (list or np.ndarray): Values for the second y-axis.
    - name1 (str): Name for the first scatter line.
    - name2 (str): Name for the second scatter line.
    - title (str): Title for the plot.
    - x_title (str): Label for the x-axis.
    - y_title1 (str): Label for the first y-axis.
    - y_title2 (str): Label for the second y-axis.
    - filename (str): File name to save the plot as an HTML file.

    Raises:
    - AssertionError: If any input argument is not of the expected type or if the filename format is invalid.

    Returns:
    None
    """
    assert isinstance(x, (list, np.ndarray)) and isinstance(y1, (list, np.ndarray)) and isinstance(y2, (list, np.ndarray)) and isinstance(name1, str) and isinstance(name2, str)
    assert isinstance(title, str) and isinstance(x_title, str) and isinstance(y_title1, str) and isinstance(y_title2, str)
    assert isinstance(filename, str) and len(filename) > 5 and filename[-5:] == ".html"

    fig = go.Figure()

    # add scatter chart
    fig.add_trace(go.Scatter(x=x,y=y1, mode='lines+markers', name=name1,marker_color='Orange'))
    fig.add_trace(go.Scatter(x=x, y=y2, mode='lines+markers',name=name2, yaxis='y2', marker_color='Blue'))

    # update layout
    fig.update_layout(
        title=title,
        title_font_size =30,
        title_x=0.5,
        xaxis=dict(title=x_title,titlefont_size=20,tickfont=dict(size=16)),
        yaxis=dict(title=y_title1, titlefont=dict(color='orange'),titlefont_size=20,tickfont=dict(size=16)),
        yaxis2=dict(title=y_title2, titlefont=dict(color='blue'),titlefont_size=20, overlaying='y', side='right',tickfont=dict(size=16)),
        height=500,
        width=1000,
        legend=dict(x=0.02, y=1.0, font=dict(size=16))
    )

    fig.write_html("./plots/"+filename)
    fig.show()

def plot_correlation(corr_data, corr_p, x, y, title="", filename="plot_corr.html"):
    """
    Create and display a heatmap of correlation coefficients with significance indicators using Plotly Express.

    Parameters:
    - corr_data (list): List of correlation coefficients.
    - corr_p (list): List of p-values corresponding to the correlation coefficients.
    - x (list): Labels for the x-axis.
    - y (list): Labels for the y-axis.
    - title (str): Title for the plot.
    - filename (str): File name to save the plot as an HTML file.

    Raises:
    - AssertionError: If any input argument is not of the expected type or if the filename format is invalid.

    Returns:
    None
    """
    assert isinstance(corr_data, list) and isinstance(corr_p, list) and isinstance(x, list) and isinstance(y, list)
    assert isinstance(title, str) and isinstance(filename, str) and len(filename) > 5 and filename[-5:] == ".html"

    fig = px.imshow(corr_data, x=x, y=y, color_continuous_scale='Viridis', aspect="auto")
    fig.update_traces(text=corr_p, texttemplate="%{text}", textfont_size = 16)
    fig.update_xaxes()
    fig.update_layout(
        title = title,
        title_font_size =28,
        title_x=0.5,
        title_y = 0.96,
        xaxis=dict(
            tickfont=dict(size=18)),
        yaxis=dict(tickfont_size = 18),
        height=400,
        width=900,
        barmode='group',
        bargap=0.5,
        bargroupgap=0.1,
    )
    
    fig.write_html("./plots/"+filename)
    fig.show()

def plot_two_lines(x1,x2, y1, y2, name1="", name2="", title="", x_title="", y_title="",legend={},filename="plot_two_lines.html"):
    """
    Create and display a plot with two lines using Plotly.

    Parameters:
    - x1 (list or np.ndarray): X-axis values for the first line.
    - x2 (list or np.ndarray): X-axis values for the second line.
    - y1 (list or np.ndarray): Y-axis values for the first line.
    - y2 (list or np.ndarray): Y-axis values for the second line.
    - name1 (str): Legend label for the first line.
    - name2 (str): Legend label for the second line.
    - title (str): Title for the plot.
    - x_title (str): Label for the x-axis.
    - y_title (str): Label for the y-axis.
    - legend (dict): Dictionary of legend settings.
    - filename (str): File name to save the plot as an HTML file.

    Raises:
    - AssertionError: If any input argument is not of the expected type or if the filename format is invalid.

    Returns:
    None
    """
    assert isinstance(x1, (list, np.ndarray)) and isinstance(x2, (list, np.ndarray))
    assert isinstance(y1, (list, np.ndarray)) and isinstance(y2, (list, np.ndarray))
    assert isinstance(name1, str) and isinstance(name2, str) and isinstance(title, str)
    assert isinstance(legend, dict) and isinstance(x_title, str) and isinstance(y_title, str)
    assert isinstance(filename, str) and len(filename) > 5 and filename[-5:] == ".html"

    fig = go.Figure()

    # add scatter chart
    fig.add_trace(go.Scatter(x=x1, y=y1, mode='lines+markers',name=name1, marker_color='Blue'))
    fig.add_trace(go.Scatter(x=x2, y=y2, mode='lines+markers', name=name2,marker_color='Orange'))


    # update layout
    fig.update_layout(
        title=title,
        title_font_size =30,
        title_x=0.5,
        xaxis=dict(title=x_title,titlefont_size=20,tickfont=dict(size=16)),
        yaxis=dict(title=y_title,titlefont=dict(color='orange'),titlefont_size=20,tickfont=dict(size=16)),
        #yaxis2=dict(titlefont=dict(color='blue'), overlaying='y', side='right',tickfont=dict(size=16)),
        height=500,
        width=1000,
        legend=legend
    )

    fig.write_html("./plots/"+filename)
    fig.show()

def plot_reverse_bars(x, y, text, name="", title="", x_title="", y_title="", filename="plot_reverse_bars.html"):
    """
    Create and display a bar plot with reversed y-axis values using Plotly.

    Parameters:
    - x (list or np.ndarray): X-axis values.
    - y (list or np.ndarray): Y-axis values.
    - text (str): Text to display on the bars.
    - title (str): Title for the plot.
    - x_title (str): Label for the x-axis.
    - y_title (str): Label for the y-axis.
    - filename (str): File name to save the plot as an HTML file.

    Raises:
    - AssertionError: If any input argument is not of the expected type or if the filename format is invalid.

    Returns:
    None
    """
    assert isinstance(x, (list, np.ndarray)) and isinstance(y, (list, np.ndarray)) and isinstance(text, list)
    assert isinstance(name, str) and isinstance(title, str) and isinstance(x_title, str) and isinstance(y_title, str)
    assert isinstance(filename, str) and len(filename) > 5 and filename[-5:] == ".html"

    fig = go.Figure()

    fig.add_trace(go.Bar(x=x,y=y, name=name,marker_color='blue',text=text, textposition='outside', textfont = dict(size=16)))

    # update layout
    fig.update_layout(
        title=title,
        title_font_size =24,
        title_x=0.5,
        xaxis=dict(title=x_title,titlefont_size=20,tickfont=dict(size=16)),
        yaxis=dict(title=y_title, titlefont_size=20,tickfont=dict(size=16),range=(-4,0)),
        height=500,
        width=1000,
        legend=dict(x=0.02, y=0.2),
        bargap=0.5,
        bargroupgap=0.1
    )

    fig.write_html("./plots/"+filename)
    fig.show()