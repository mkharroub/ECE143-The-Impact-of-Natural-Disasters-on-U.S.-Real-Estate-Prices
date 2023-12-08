import pandas as pd
import os
import glob
import geopandas as gpd

def read_csv_data(path):
    """
    Read data from a CSV file and return it as a pandas DataFrame.

    Parameters:
    - path (str): The file path of the CSV file to be read.

    Raises:
    - AssertionError: If the input path is not a string, or if its length is less than 5, or if it does not end with '.csv'.
    - FileNotFoundError: If the specified file path does not exist.

    Returns:
    - pd.DataFrame: The DataFrame containing the data from the CSV file.
    """
    assert isinstance(path, str) and len(path) > 4 and path[-4:] == ".csv"

    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        raise FileNotFoundError("File not found: {}".format(path))

    return df

def read_all_zipped_csv(path):
    """
    Read all compressed CSV files (*.csv.gz) in the specified directory and concatenate them into a single DataFrame.

    Parameters:
    - path (str): The directory path containing compressed CSV files.

    Raises:
    - AssertionError: If the input path is not a string, or if its length is less than 8, or if it does not end with '*.csv.gz'.

    Returns:
    - pd.DataFrame: A DataFrame containing the concatenated data from all compressed CSV files in the specified directory.
    """
    assert isinstance(path, str) and len(path) > 8 and path[-8:] == "*.csv.gz"

    dfs = []
    for file in glob.glob(os.getcwd()+path):
        df = pd.read_csv(file, compression='gzip')
        dfs.append(df)

    final_df = pd.concat(dfs, ignore_index=True)
    del dfs

    return final_df

def read_gpd_file(path):
    """
    Read a GeoPandas DataFrame from a GeoJSON or Shapefile.

    Parameters:
    - path (str): The file path of the GeoJSON or Shapefile to be read.

    Raises:
    - AssertionError: If the input path is not a string or if its length is less than or equal to 0.
    - FileNotFoundError: If the specified GeoJSON or Shapefile does not exist.

    Returns:
    - gpd.GeoDataFrame: The GeoPandas DataFrame containing the spatial data.
    """
    assert isinstance(path, str) and len(path) > 0

    try:
        return gpd.read_file(os.getcwd()+path)
    except FileNotFoundError:
        raise FileNotFoundError("File not found: {}".format(path))
    
def read_excel_file(path, skiprows):
    """
    Read data from an Excel file and return it as a pandas DataFrame.

    Parameters:
    - path (str): The file path of the Excel file to be read.
    - skiprows (int): Number of rows to skip from the beginning of the Excel file.

    Raises:
    - AssertionError: If the input path is not a string, or if its length is less than 5, or if it does not end with '.xlsx'.
                      Also, raises an AssertionError if skiprows is not a non-negative integer.
    - FileNotFoundError: If the specified file path does not exist.

    Returns:
    - pd.DataFrame: The DataFrame containing the data from the Excel file.
    """
    assert isinstance(path, str) and len(path) > 5 and path[-5:] == ".xlsx"
    assert isinstance(skiprows, int) and skiprows >= 0

    try:
        return pd.read_excel(os.getcwd() + path, skiprows=skiprows)
    except:
        raise FileNotFoundError("File not found: {}".format(path))