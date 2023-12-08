from scipy.stats import pearsonr
import pandas as pd
from rtree import index
from scipy import stats

def cal_pearsonr(data1, data2):
    """
    Calculate the Pearson correlation coefficient and its associated p-value between two pandas Series.

    Parameters:
    - data1 (pd.Series): First pandas Series for correlation.
    - data2 (pd.Series): Second pandas Series for correlation.

    Raises:
    - AssertionError: If data1 or data2 is not a pandas Series.

    Returns:
    - Tuple: A tuple containing the Pearson correlation coefficient and its associated p-value.
    """
    assert isinstance(data1, pd.Series) and isinstance(data2, pd.Series)

    corr, p_value = pearsonr(data1, data2)
    return corr, p_value

def cal_corr_p(data, p_data):
    """
    Format correlation coefficients with p-values into a list of strings.

    Parameters:
    - data (list): List of correlation coefficients.
    - p_data (list): List of p-values corresponding to the correlation coefficients.

    Raises:
    - AssertionError: If data or p_data is not a list.

    Returns:
    - list: Formatted list of strings representing correlation coefficients with significance indicators.
    """
    assert isinstance(data, list) and isinstance(p_data, list)

    corr_p = []
    for i in range(len(data)):
        row = []
        for j in range(len(data[0])):
            if p_data[i][j] < 0.01:
                row.append(f"{round(data[i][j], 3)}***")
            elif p_data[i][j] < 0.05:
                row.append(f"{round(data[i][j], 3)}**")
            elif p_data[i][j] < 0.1:
                row.append(f"{round(data[i][j], 3)}*")
            else:
                row.append(f"{round(data[i][j], 3)}")
        corr_p.append(row)
    return corr_p

def get_nearest_county(heavily_affected_group, less_affected_group):
    """
    Assign nearest neighbors from less_affected_group to each row in heavily_affected_group based on spatial proximity.

    Parameters:
    - heavily_affected_group (pd.DataFrame): DataFrame containing heavily affected group data with a 'geometry' column.
    - less_affected_group (pd.DataFrame): DataFrame containing less affected group data with a 'geometry' column.

    Raises:
    - AssertionError: If heavily_affected_group or less_affected_group is not a DataFrame.

    Returns:
    - pd.DataFrame: The heavily_affected_group DataFrame with added columns 'neighbor_state', 'neighbor_county', and 'neighbor_distance'.
    """
    assert isinstance(heavily_affected_group, pd.DataFrame) and isinstance(less_affected_group, pd.DataFrame)

    # Create spatial index for less_affected_group
    spatial_index = index.Index()
    for i, geom in enumerate(less_affected_group['geometry']):
        spatial_index.insert(i, geom.bounds)

    # Iterate row in heavily_affected_group
    for idx, row in heavily_affected_group.iterrows():
        point = row['geometry']
        nearest_idx = list(spatial_index.nearest(point.bounds, 1))[0]
        nearest_neighbor = less_affected_group.loc[nearest_idx]
        heavily_affected_group.at[idx, 'neighbor_state'] = nearest_neighbor['State']
        heavily_affected_group.at[idx, 'neighbor_county'] = nearest_neighbor['County']
        heavily_affected_group.at[idx, 'neighbor_distance'] = nearest_neighbor['geometry'].distance(point)
    return heavily_affected_group

def cal_ttest(data, data1):
    """
    Calculate the paired t-test for two related samples.

    Parameters:
    - data (tuple): Tuple containing two column names for the samples in data1.
    - data1 (pd.DataFrame): DataFrame containing the data for the paired t-test.

    Raises:
    - AssertionError: If data is not a list or data1 is not a DataFrame.

    Returns:
    - tuple: A tuple containing the mean difference, t-statistic, and p-value.
    """
    assert isinstance(data, tuple) and isinstance(data1, pd.DataFrame)

    data1.dropna(subset=[data[0],data[1]], inplace=True)
    t,p = stats.ttest_rel(data1[data[0]], data1[data[1]])
    mean_diff = data1[data[0]].mean() - data1[data[1]].mean()
    return mean_diff,t,p

def cal_freq(data, data1):
    """
    Calculate the paired t-test for multiple related samples.

    Parameters:
    - data (list): List containing column names for the samples in data1.
    - data1 (pd.DataFrame): DataFrame containing the data for the paired t-tests.

    Raises:
    - AssertionError: If data is not a list or data1 is not a DataFrame.

    Returns:
    - tuple: A tuple containing lists of mean differences, t-statistics, and p-values for each specified column.
    """
    assert isinstance(data, list) and isinstance(data1, pd.DataFrame)

    mean_diff_freq = []
    t_freq = []
    p_freq = []
    for col in data:
        mean_diff,t,p = cal_ttest(col, data1)
        mean_diff_freq.append(mean_diff)
        t_freq.append(t)
        p_freq.append(p)

    return mean_diff_freq, t_freq, p_freq