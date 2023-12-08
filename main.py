import pandas as pd
from scripts.extract import *
from scripts.clean import *
from scripts.plotly_plots import *
from scripts.mpl_plots import *
from scripts.stats import *
import warnings

warnings.filterwarnings("ignore")

storm_database = read_all_zipped_csv("/dataset/*.csv.gz")
storm_database.head()

storm_database.shape

storm_database.iloc[0:8,7:18]

storm_database['DAMAGE_P'] = storm_database['DAMAGE_PROPERTY'].apply(convert_to_numeric)
storm_database['DAMAGE_C'] = storm_database['DAMAGE_CROPS'].apply(convert_to_numeric)
storm_database.dropna(subset=['DAMAGE_P','DAMAGE_C'], inplace=True)
storm_database['DAMAGE_P'] =  storm_database['DAMAGE_P'] / 1000000
storm_database['DAMAGE_C'] =  storm_database['DAMAGE_C'] / 1000000
storm_database['DAMAGE'] = storm_database['DAMAGE_P'] + storm_database['DAMAGE_C']
storm = storm_database.copy()

storm['STATE'] = storm['STATE'].str.title()
state_freq = storm.groupby('STATE')['EVENT_ID'].count()

gdf = read_gpd_file("/dataset/cb_2022_us_state_500k")
gdf.head()

state_gdf = list(gdf.NAME.unique())
state_storm = state_freq.index.to_list()
state_same = []
for s in state_storm:
    if s in state_gdf:
        state_same.append(s)
state_gdf_l = set(state_gdf) - set(state_same)
state_storm_l = set(state_storm) - set(state_same)
print(state_gdf_l)
print(state_storm_l)

storm = storm[ ~ storm['STATE'].isin(state_storm_l)]
storm = storm[ ~ storm['STATE'].isin(['American Samoa','Guam'])]
storm.shape

gdf_state = gdf[['STUSPS','NAME']]
storm = pd.merge(storm, gdf_state, left_on='STATE', right_on='NAME', how='left')
storm['STUSPS'].isnull().sum()

year_freq = storm.groupby('YEAR')['EVENT_ID'].count()
year_list = year_freq.index.to_list()
year_freq = list(year_freq)
year_damage = storm.groupby('YEAR')['DAMAGE'].sum()
year_damage = list(year_damage)
year_damage = [ damage / 1000 for damage in year_damage]

plot_bar_and_line(year_list, year_damage, year_freq, 'Damage($Billions)', 'Frequency', 'Frequency and Damage of Natural Disasters 1980-2023', 'Year', 'Damage($Billions)', 'Frequency', "Frequency_and_Damage_of_Natural_Disasters_1980-2023.html")

event_type_freq = storm.groupby(['EVENT_TYPE'])['EVENT_ID'].count()
event_type_freq.sort_values(ascending = False, inplace=True)
event_type_top = event_type_freq[:5]

plot_bar_chart(event_type_top.index.to_list(), event_type_top.values, 'Top 5 Most Common Climate Disasters','Frequency','Top 5 Most Common Climate Disasters.html')

event_type_damage = storm.groupby(['EVENT_TYPE'])['DAMAGE'].sum()
event_type_damage.sort_values(ascending = False, inplace=True)
event_type_damage = event_type_damage[:5]
event_type_damage_label = event_type_damage.index
event_type_damage = [round(damage / 1000,1) for damage in event_type_damage]
plot_bar_chart(event_type_damage_label, event_type_damage, 'Top 5 Damage-causing Climate Disasters','Damage ($Billions)','Top 5 Damage-causing Climate Disasters.png')

state_freq = storm.groupby('STATE')['EVENT_ID'].count()
state_damage = storm.groupby('STATE')['DAMAGE'].sum()
state_disaster = pd.merge(state_freq, state_damage, left_index=True, right_index=True)
state_disaster.reset_index(inplace=True)
state_disaster.rename(columns={'EVENT_ID':'EVENT', 'STATE':'state'}, inplace=True)
state_disaster['DAMAGE'] = state_disaster['DAMAGE']/1000

gdf = gdf.merge(state_disaster,left_on='NAME',right_on='state')

variable = 'EVENT'
label = 'Frequency'
save_name = '/disasters_frequency_by_state_1980_2023.png'
plot_disasters_map(gdf, variable, label, save_name, 'Climate Disasters in US 1980-2023', "Data: NOAA's Storm Events Database\nhttps://www.ncdc.noaa.gov/stormevents/ftp.jsp")

variable = 'DAMAGE'
label = 'Damage ($Billions)'
save_name = '/disasters_damage_by_state_1980_2023.png'
plot_disasters_map(gdf, variable, label, save_name, 'Climate Disasters in US 1980-2023', "Data: NOAA's Storm Events Database\nhttps://www.ncdc.noaa.gov/stormevents/ftp.jsp")

hpi_county = read_excel_file("/dataset/HPI_AT_BDL_county.xlsx", 6)
hpi_county.head()

hpi_county['Year'] = hpi_county['Year'].astype(int)
hpi_county.sort_values(by=['State','County', 'Year'], inplace=True)
hpi_county['Annual Change (%)'] = pd.to_numeric(hpi_county['Annual Change (%)'], errors='coerce')
hpi_county['HPI'] = pd.to_numeric(hpi_county['HPI'], errors='coerce')
hpi_county['lag1_hpi_change'] = (hpi_county.groupby(['State','County'])['HPI'].shift(periods=-1) / hpi_county.groupby(['State','County'])['HPI'].shift(periods=1) - 1) * 100
hpi_county['lag3_hpi_change'] = (hpi_county.groupby(['State','County'])['HPI'].shift(periods=-3) / hpi_county.groupby(['State','County'])['HPI'].shift(periods=1) - 1) * 100
hpi_county['lag5_hpi_change'] = (hpi_county.groupby(['State','County'])['HPI'].shift(periods=-5) / hpi_county.groupby(['State','County'])['HPI'].shift(periods=1) - 1) * 100
hpi_county['lag10_hpi_change'] = (hpi_county.groupby(['State','County'])['HPI'].shift(periods=-10) / hpi_county.groupby(['State','County'])['HPI'].shift(periods=1) - 1) * 100
hpi_county = hpi_county[hpi_county['Year'] >= 1980]

hpi_county.groupby(['State', 'County']).size()

hpi_county.reset_index(inplace=True)
hpi_county.drop_duplicates(subset=['State', 'County', 'Year'], keep='first', inplace=True)

avg_hpi_year = hpi_county.groupby(['Year'])['HPI'].mean()
avg_hpi_year = avg_hpi_year / avg_hpi_year[1980] * 100

plot_scatter_line(avg_hpi_year.index, avg_hpi_year.values, name='Average HPI', title='Average House Price Index of US Counties 1980-2023', x_title='Year', y_title="Average HPI", filename='Average House Price Index of US Counties 1980-2023.html')

heatmap_hpi = hpi_county.pivot_table(values='HPI', index=['State', 'County'], columns='Year')

plot_heatmap(heatmap_hpi, title='House Price Index of US Counties 1980-2023', x_title='Year', y_title='County', filename='House Price Index of US Counties 1980-2023.html')

plot_two_scatter_lines(year_list, year_freq, avg_hpi_year.values, name1='Frequency', name2="House Price", title='Disasters Frequency & House Price Index of US 1980-2023', x_title='Year', y_title1="Frequency", y_title2='House Price', filename='Disasters Frequency & House Price Index of US 1980-2023.html')

county_freq = storm.groupby(['STUSPS','CZ_NAME','YEAR'])['EVENT_ID'].count()
county_damage = storm.groupby(['STUSPS','CZ_NAME','YEAR'])['DAMAGE'].sum()
county_year = pd.merge(county_freq, county_damage, left_index=True, right_index=True)
county_year.reset_index(inplace=True)
county_year['CZ_NAME'] = county_year['CZ_NAME'].str.title()
county_year.rename(columns={'EVENT_ID':'FREQ'}, inplace=True)

county_storm_hpi = pd.merge(county_year, hpi_county, left_on=['STUSPS','CZ_NAME','YEAR'], right_on=['State','County','Year'], how = 'right')
print(county_storm_hpi.duplicated(subset=['State', 'County', 'Year'], keep=False).sum())
county_storm_hpi.drop_duplicates(subset=['State', 'County', 'Year'], keep='first', inplace=True)

storm_hpi = county_storm_hpi[ ~ (county_storm_hpi['Year'] < 1980)]
storm_hpi['DAMAGE'] = storm_hpi['DAMAGE'].fillna(0)# If a county of a year has nan value, means this county didn't have disasters this year.
storm_hpi['FREQ'] = storm_hpi['FREQ'].fillna(0)
storm_hpi.sort_values(by=['State','County', 'Year'], inplace=True)
storm_hpi['lag_damage'] = storm_hpi.groupby(['State','County'])['DAMAGE'].shift(periods=1)
storm_hpi['lag_freq'] = storm_hpi.groupby(['State','County'])['FREQ'].shift(periods=1)
storm_hpi['damage_change'] = storm_hpi['DAMAGE'] - storm_hpi['lag_damage']
storm_hpi['freq_change'] = storm_hpi['FREQ'] - storm_hpi['lag_freq']
storm_hpi.head()

gdf = read_gpd_file("/dataset/cb_2022_us_county_500k")
gdf_polygon = gdf[['STUSPS','NAME','geometry']]
storm_hpi = pd.merge(storm_hpi, gdf_polygon, left_on=['State','County'], right_on=['STUSPS','NAME'], how = 'left')
storm_hpi.drop_duplicates(subset=['State', 'County', 'Year'], keep='first', inplace=True)
storm_hpi.dropna(subset=['geometry'], inplace=True)
data = storm_hpi.copy()

damage_hpi_corr = []
damage_hpi_p = []
freq_hpi_corr = []
freq_hpi_p = []
damage_c_hpi_corr = []
damage_c_hpi_p = []
freq_c_hpi_corr = []
freq_c_hpi_p = []
col = ['Annual Change (%)','lag1_hpi_change','lag3_hpi_change','lag5_hpi_change','lag10_hpi_change']
storm_hpi = data.copy()
for i in col:
    storm_hpi.dropna(subset=[i], inplace=True)
    corr, p_value = cal_pearsonr(storm_hpi['DAMAGE'], storm_hpi[i])
    damage_hpi_corr.append(corr)
    damage_hpi_p.append(p_value)
    corr, p_value = cal_pearsonr(storm_hpi['FREQ'], storm_hpi[i])
    freq_hpi_corr.append(corr)
    freq_hpi_p.append(p_value)
storm_hpi = data.copy()
for i in col:
    storm_hpi.dropna(subset=[i,'damage_change', 'freq_change'], inplace=True)
    corr, p_value = cal_pearsonr(storm_hpi['damage_change'], storm_hpi[i])
    damage_c_hpi_corr.append(corr)
    damage_c_hpi_p.append(p_value)
    corr, p_value = cal_pearsonr(storm_hpi['freq_change'], storm_hpi[i])
    freq_c_hpi_corr.append(corr)
    freq_c_hpi_p.append(p_value)

corr_data = [freq_hpi_corr, damage_hpi_corr]
p_data = [freq_hpi_p, damage_hpi_p]
corr_p = cal_corr_p(corr_data, p_data)

x = ['Disaster Year','1-Year Lag','3-Year Lag','5-Year Lag','10-Year Lag']
y = ['Frequency','Damage']
plot_correlation(corr_data, corr_p, x, y, title='Correlation Coefficient of Disasters & House Price Change', filename='Correlation Coefficient of Disasters & House Price Change.html')

storm_hpi = data.copy()
county_freq = storm_hpi.groupby(['State', 'County'])['FREQ'].sum()
county_freq = pd.DataFrame(county_freq)
county_freq.reset_index(inplace=True)
print(county_freq.shape)
county_freq = pd.merge(county_freq, gdf_polygon, left_on=['State','County'], right_on=['STUSPS','NAME'], how = 'left')
county_freq.drop_duplicates(subset=['State','County'], keep='first', inplace=True)
county_freq.drop(columns=['STUSPS','NAME'], inplace=True)
print(county_freq.shape)

quantile_25 = county_freq['FREQ'].quantile(0.25)
quantile_75 = county_freq['FREQ'].quantile(0.75)
county_freq_l = county_freq[county_freq['FREQ'] < quantile_25]
county_freq_h = county_freq[county_freq['FREQ'] > quantile_75]
print(county_freq_h.shape)
print(county_freq_l.shape)
county_freq_l.drop(columns=['FREQ'], inplace=True)
county_freq_h.drop(columns=['FREQ'], inplace=True)
county_freq_l = county_freq_l.reset_index(drop=True)

county_h = county_freq_h.copy()
county_h['affected_level'] = 'high'
county_l = county_freq_l.copy()
county_l['affected_level'] = 'low'
county_map = pd.concat([county_h, county_l], axis=0)
county_map.drop(columns='geometry', inplace=True)
gdf = read_gpd_file("/dataset/cb_2022_us_county_500k")
gdf = pd.merge(gdf, county_map,left_on=['STUSPS','NAME'],right_on=['State','County'],how='left')
gdf.head()

gdf.drop_duplicates(subset=['STUSPS','NAME'], keep='first', inplace=True)
gdf = gdf[~ gdf['STATE_NAME'].isin(['Commonwealth of the Northern Mariana Islands', 'District of Columbia', 'United States Virgin Islands','American Samoa','Guam','Hawaii','Alaska'])]
gdf.shape

save_name = '/disasters_affected_level_by_county_1980_2023.png'
plot_disasters_map1(gdf, save_name, 'Disasters Distriution: \nHeavily-affected Counties VS Less-affected Counties in US', 'Heavily-affected', 'Less-affected')

county_h = get_nearest_county(county_freq_h, county_freq_l)
county_h.drop(columns='geometry', inplace=True)
storm_hpi_h = pd.merge(storm_hpi, county_h, on=['State','County'], how='inner')
print(storm_hpi_h.shape)
keep_cols = ['FREQ', 'DAMAGE', 'State', 'County','Year', 'Annual Change (%)', 'HPI','lag1_hpi_change', 'lag3_hpi_change','lag5_hpi_change', 'lag10_hpi_change','lag_damage', 'lag_freq', 'damage_change', 'freq_change','geometry', 'neighbor_state', 'neighbor_county',
       'neighbor_distance']
storm_hpi_h = storm_hpi_h[keep_cols]
storm_hpi_h.shape
storm_hpi_l =storm_hpi[['FREQ', 'DAMAGE', 'State', 'County','Year', 'Annual Change (%)', 'HPI','lag1_hpi_change', 'lag3_hpi_change','lag5_hpi_change', 'lag10_hpi_change','lag_damage', 'lag_freq', 'damage_change', 'freq_change']]
storm_hpi_h = pd.merge(storm_hpi_h, storm_hpi_l, left_on=['neighbor_state', 'neighbor_county', 'Year'], right_on=['State', 'County','Year'], suffixes=('_h', '_l'))
storm_hpi_ttest_h= storm_hpi_h.copy()
storm_hpi_h.head()

h_year = storm_hpi_h.groupby('Year')['Annual Change (%)_h'].mean()
l_year = storm_hpi_h.groupby('Year')['Annual Change (%)_l'].mean()

name1 = 'Heavily-affected Counties'
name2 = 'Neighboring Less-affected Counties'
title = "Average House Price Change (%) <br>of Disasters' Happened Year"
filename = "Average House Price Change for Disasters Happened Year"
legend = dict(x=0.02, y=1.0, font=dict(size=16))
plot_two_lines(h_year.index,h_year.index, h_year.values, l_year.values, name1, name2, title, "Year","Percentage", legend, filename+'.html')

h_year_10 = storm_hpi_h.groupby('Year')['lag10_hpi_change_h'].mean()
l_year_10 = storm_hpi_h.groupby('Year')['lag10_hpi_change_l'].mean()
h_year_10.dropna(inplace=True)
l_year_10.dropna(inplace=True)
name1 = 'Heavily-affected Counties'
name2 = 'Neighboring Less-affected Counties'
title = "Average House Price Change (%) <br>of 10-Year Lag after Disasters' Happened"
filename = "Average House Price Change for 10-Year Lag after Disasters Happened"
legend = dict(x=0.02, y=0.02, font=dict(size=16))
year_list = [i for i in range(1990, 2023)]
plot_two_lines(year_list,year_list, h_year_10.values, l_year_10.values, name1, name2, title, "Year","Percentage", legend, title+'.html')

cols = [('Annual Change (%)_h','Annual Change (%)_l'),('lag1_hpi_change_h','lag1_hpi_change_l'),('lag3_hpi_change_h','lag3_hpi_change_l'),('lag5_hpi_change_h','lag5_hpi_change_l'),('lag10_hpi_change_h','lag10_hpi_change_l')]
storm_hpi_h = storm_hpi_ttest_h.copy()
mean_diff_freq,t_freq,p_freq = cal_freq(cols, storm_hpi)

year_list = ['Disaster Year','1-Year Lag','3-Year Lag','5-Year Lag','10-Year Lag']
mean_diff_freq = [round(f,2) for f in mean_diff_freq]
freq_labels = [f"{diff} {'***' if p < 0.01 else '**' if p < 0.05 else '*' if p < 0.1 else ''}" for diff, p in zip(mean_diff_freq, p_freq)]

plot_reverse_bars(year_list, mean_diff_freq, freq_labels, "Frequency", 'Difference of House Price Change (%):<br> Heavily-affected Counties minus Neighboring Less-affected Counties', 'Year', 'Difference(%)', 'Difference of House Price Change Heavily-affected Counties minus Neighboring Less-affected Counties.html')