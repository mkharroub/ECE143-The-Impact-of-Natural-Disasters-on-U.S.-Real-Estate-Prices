import pandas as pd
import numpy as np
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt

def convert_to_numeric(value):
    """
    Convert a value to a numeric representation.

    Parameters:
    - value (int, float, or str): The value to be converted.

    Raises:
    - AssertionError: If the input value is not an instance of int, float, or str.

    Returns:
    - numeric value: The numeric representation of the input value. If the input is already numeric, it returns the same value.
                     If the input is a string with 'K' or 'M' suffix, it converts it to numeric (e.g., '1K' becomes 1000).
                     If the conversion fails, it returns the original value.
    """
    assert isinstance(value, (int, float, str))

    if pd.isnull(value):
        return np.nan
    elif isinstance(value, (int, float)):
        return value
    else:
        try:
            value = value.replace('K', 'e3').replace('M', 'e6')
            return pd.to_numeric(value, errors='coerce')
        except:
            return value
        
def makeColorColumn(gdf,variable,vmin,vmax):
    """
    Add a new column to a GeoDataFrame containing color values based on a specified variable.

    Parameters:
    - gdf (pd.DataFrame): The GeoDataFrame to which the color column will be added.
    - variable (str): The variable used to determine the color values.
    - vmin (float or int): The minimum value for color normalization.
    - vmax (float or int): The maximum value for color normalization.

    Raises:
    - AssertionError: If the input arguments do not have the expected types.

    Returns:
    - pd.DataFrame: The GeoDataFrame with the added 'value_determined_color' column.
    """
    assert isinstance(gdf, pd.DataFrame) and isinstance(variable, str) and isinstance(vmin, (int, float)) and isinstance(vmax, (int, float))
    
    norm = mcolors.Normalize(vmin=vmin, vmax=vmax, clip=True)
    mapper = plt.cm.ScalarMappable(norm=norm, cmap=plt.cm.YlOrBr)
    gdf['value_determined_color'] = gdf[variable].apply(lambda x: mcolors.to_hex(mapper.to_rgba(x)))
    return gdf