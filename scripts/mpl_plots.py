import pandas as pd
import matplotlib.pyplot as plt

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