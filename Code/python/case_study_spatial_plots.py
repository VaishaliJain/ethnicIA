import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Point
import geopandas as gpd


# Cities and Towns information fetched from
# https://public.opendatasoft.com/explore/dataset/cities-and-towns-of-the-united-states/information/
def get_processed_city_data(state):
    city_data = pd.read_csv('../../Data/CaseStudy/cities-and-towns-of-the-united-states.csv', delimiter=';')
    city_data = city_data[city_data.STATE == state]
    city_data = city_data[['STATE', 'NAME', 'LONGITUDE', 'LATITUDE']]
    city_data['NAME'] = city_data['NAME'].str.lower()
    geometry = [Point(xy) for xy in zip(city_data['LONGITUDE'], city_data['LATITUDE'])]
    city_data = gpd.GeoDataFrame(city_data, crs="EPSG:4326", geometry=geometry)
    return city_data


# State Boundaries fetched from
# https://www.census.gov/geographies/mapping-files/time-series/geo/carto-boundary-file.html
def get_usa_states_data(state):
    usa = gpd.read_file('../../Data/CaseStudy/cb_2018_us_state_5m/cb_2018_us_state_5m.shp')
    usa.to_crs(epsg=4326, inplace=True)
    state_data = usa[usa.STUSPS == state]
    return state_data


def get_fec_processed_data(state, presidential_race=1):
    if presidential_race:
        fec_data = pd.read_csv('../../Data/CaseStudy/FECdata_City.csv')
    else:
        fec_data = pd.read_csv('../../Data/CaseStudy/FECdata_GA_City.csv')
    fec_data['CITY'] = fec_data['CITY'].str.lower()
    fec_data = fec_data[fec_data.STATE == state]
    fec_data = fec_data[fec_data.presidential_race == presidential_race]
    return fec_data


def generate_merged_city_fec_data(city_data, fec_data, race, party, presidential_race=1):
    fec_data = fec_data[fec_data.predicted_race == race]
    fec_data = fec_data[fec_data.CAND_PID == party]
    if not presidential_race:
        fec_data = fec_data.groupby(['CITY'])['amount'].agg('sum').reset_index()
    city_fec_data = city_data.merge(fec_data, left_on='NAME', right_on='CITY')
    del city_fec_data['LONGITUDE']
    del city_fec_data['LATITUDE']
    return city_fec_data


def generate_spatial_plot_state(state, presidential_race=1):
    state_data = get_usa_states_data(state)
    city_data = get_processed_city_data(state)
    fec_data = get_fec_processed_data(state, presidential_race=presidential_race)
    races = ['Asian', 'Black', 'Hispanic', 'White']
    parties = ['DEM', 'REP']
    fig, axs = plt.subplots(4, 2, figsize=(20, 40))
    for race_idx in range(4):
        for party_idx in range(2):
            race = races[race_idx]
            party = parties[party_idx]
            dot_color = 'blue'
            if party == 'REP':
                dot_color = 'red'
            city_fec_data = generate_merged_city_fec_data(city_data, fec_data, race, party,
                                                          presidential_race=presidential_race)
            state_data.plot(ax=axs[race_idx, party_idx], color='white', edgecolor='black')
            city_fec_data.plot(ax=axs[race_idx, party_idx], markersize=city_fec_data['amount'] / 1000, color=dot_color,
                               marker='o', alpha=0.5)
            axs[race_idx, party_idx].set_title(race, fontsize=20)
            axs[race_idx, party_idx].axis('off')
    if presidential_race:
        plt.savefig('../../Visualizations/SpatialPlots/' + state + '.png')
    else:
        plt.savefig('../../Visualizations/SpatialPlots/Senate_' + state + '.png')
    plt.close(fig)


def generate_spatial_plots_for_each_state():
    states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
              "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
              "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
              "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
              "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
    for state in states:
        generate_spatial_plot_state(state)
    generate_spatial_plot_state('GA', presidential_race=0)
