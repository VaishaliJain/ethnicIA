import numpy as np
import pandas as pd

from case_study_spatial_plots import generate_spatial_plot_state
from model_ethnicIA_testing import test_ethnicIA_model
from model_ethnicIA_training import train_ethnicIA_model


def case_study_train_test():
    train_ethnicIA_model('FLGANC')
    test_ethnicIA_model('FLGANC', 'CaseStudy', generate_csv=True, generate_performance_report=False)
    test_ethnicIA_model('FLGANC', 'CaseStudy_GA', generate_csv=True, generate_performance_report=False)


def generate_spatial_plots():
    states = ["TX", "GA", "NC", "FL"]
    for state in states:
        generate_spatial_plot_state(state)


def fec_data_stats():
    fec_data = pd.read_csv('../../Data/CaseStudy/FECdata.csv', usecols=['CAND_NAME', 'TRANSACTION_AMT'])
    print("Number of Donations: ", fec_data.shape[0])
    print(fec_data.CAND_NAME.value_counts())
    fec_data_trump = fec_data[fec_data.CAND_NAME == "TRUMP"]
    print("Total amount of donations to Trump: ", sum(fec_data_trump.TRANSACTION_AMT))
    fec_data_biden = fec_data[fec_data.CAND_NAME == "BIDEN"]
    print("Total amount of donations to Biden: ", sum(fec_data_biden.TRANSACTION_AMT))


def check_name_ethnicity_distribution(name, last_name=True):
    data = pd.read_csv('../../Data/FinalDataSet_Combos/FLGANCtrain_ContrPred/FLGANC_Train_s.csv',
                       usecols=['first_name', 'last_name', 'race', 'indis_fn', 'indis_ln'])
    if last_name:
        print("Last name: ", name)
        data = data[data.last_name == name]
        if data.shape[0] > 0:
            print("Indistinguishable: ", data.indis_ln.iloc[0])
            print(dict(data.race.value_counts()))
        else:
            print("Name does not exist in the database")
    else:
        print("First name: ", name)
        data = data[data.first_name == name]
        if data.shape[0] > 0:
            print("Indistinguishable: ", data.indis_fn.iloc[0])
            print(dict(data.race.value_counts()))
        else:
            print("Name does not exist in the database")


def check_full_name_ethnicity_distribution(fname, lname):
    data = pd.read_csv('../../Data/FinalDataSet_Combos/FLGANCtrain_ContrPred/FLGANC_Train_s.csv',
                       usecols=['first_name', 'last_name', 'race', 'indis'])
    print(fname + ' ' + lname)
    data = data[data.first_name == fname]
    data = data[data.last_name == lname]
    if data.shape[0] > 0:
        print("Indistinguishable: ", data.indis.iloc[0])
        print(dict(data.race.value_counts()))
    else:
        print("Name does not exist in the database")


def general_stats():
    fec_data_stats()
    check_name_ethnicity_distribution("vaughn", last_name=False)
    check_name_ethnicity_distribution("vennerberg")
    check_name_ethnicity_distribution("annette", last_name=False)
    check_name_ethnicity_distribution("simmons")
    check_full_name_ethnicity_distribution("annette", "simmons")
    check_name_ethnicity_distribution("kelcy", last_name=False)
    check_name_ethnicity_distribution("warren")
    check_full_name_ethnicity_distribution("kelcy", "warren")


def generate_fec_data_state(state):
    fec_data = pd.read_csv('../../Data/CaseStudy/FECdata.csv')
    fec_data = fec_data[fec_data.STATE == state]
    fec_data = fec_data[(fec_data.CAND_NAME == 'TRUMP') | (fec_data.CAND_NAME == 'BIDEN')]
    fec_data.to_csv('../../Data/CaseStudy/FECdata_state/FECdata_' + state + '.csv', index=False)


def generate_fec_data_state_race(state, race):
    fec_data = pd.read_csv('../../Data/CaseStudy/FECdata.csv')
    fec_data = fec_data[fec_data.STATE == state]
    fec_data = fec_data[fec_data.predicted_race == race]
    fec_data.to_csv('../../Data/CaseStudy/FECdata_state/FECdata_' + state + '_' + race + '.csv', index=False)


def create_presidential_race_variable():
    fec_data = pd.read_csv('../../Data/CaseStudy/FECdataRaw_UP.csv')
    print(fec_data.columns)
    fec_data['presidential_race'] = np.where((fec_data['CAND_NAME'] == 'TRUMP') | (fec_data['CAND_NAME'] == 'BIDEN'), 1,
                                             0)
    fec_data.to_csv('../../Data/CaseStudy/FECdataRaw_UP.csv', index=False)


def case_study_stats_by_state(state):
    fec_data = pd.read_csv('../../Data/CaseStudy/FECdata.csv')
    fec_data = fec_data[fec_data.STATE == state]
    fec_data = fec_data[(fec_data.CAND_NAME == 'TRUMP') | (fec_data.CAND_NAME == 'BIDEN')]
    print(fec_data.groupby(["CAND_NAME", "predicted_race"]).TRANSACTION_AMT.sum())
    print(fec_data.groupby(["CAND_NAME", "predicted_race"]).TRANSACTION_AMT.count())
