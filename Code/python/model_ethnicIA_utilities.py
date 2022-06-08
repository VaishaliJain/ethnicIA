import pandas as pd
import numpy as np


def get_train_dataset(train_data_label, num_rows=500000, model_uid=0):
    if train_data_label == 'FLGA':
        file_name = "../../Data/FinalDataSet_Combos/FLGAtrain_NCtest/FLGA_Train"
    elif train_data_label == 'FLGANC':
        file_name = "../../Data/FinalDataSet_Combos/FLGANCtrain_ContrPred/FLGANC_Train"
    else:
        folder = ''
        if train_data_label == 'FL':
            folder = 'FLtrain_NCtest_GAtest'
        elif train_data_label == 'NC':
            folder = 'NCtrain_FLtest_GAtest'
        elif train_data_label == 'GA':
            folder = 'GAtrain_NCtest_FLtest'
        elif train_data_label == 'NC_rest':
            folder = 'NCtrain_NCtest_white'
        file_name = "../../Data/FinalDataSet_Combos/" + folder + "/" + train_data_label + "_Train"
    if model_uid == 1:
        file_name = file_name + "_UID.csv"
    else:
        file_name = file_name + "_s.csv"

    X, y_onehot, main_data, y = process_data_set(file_name, indis_remove=False, num_rows=num_rows,
                                                 model_uid=model_uid)
    return X, y_onehot, main_data, y


def get_test_dataset(train_data_label, test_data_label, num_rows=0, indis_remove=True, model_uid=0):
    drop_null_first_or_last = True
    if train_data_label == 'FLGA':
        if test_data_label == 'NC':
            file_name = "../../Data/FinalDataSet_Combos/FLGAtrain_NCtest/NCtest_FLGAtrain"
        elif test_data_label == 'NC_white':
            file_name = "../../Data/FinalDataSet_Combos/NCtrain_NCtest_white/NCwtest_FLGAtrain"
        else:
            file_name = "../../Data/FinalDataSet_Combos/FLGAtrain_NCtest/FLGA_Train"
    elif train_data_label == 'FLGANC':
        if test_data_label == 'CaseStudy':
            file_name = "../../Data/FinalDataSet_Combos/FLGANCtrain_ContrPred/ContTest_FLGANCtrain"
        else:
            file_name = "../../Data/FinalDataSet_Combos/FLGANCtrain_ContrPred/ContTest_GA_FLGANCtrain"
        drop_null_first_or_last = False
    elif train_data_label == 'NC_rest':
        file_name = "../../Data/FinalDataSet_Combos/NCtrain_NCtest_white/NCwtest_NCtrain"
    else:
        folder = ''
        if train_data_label == 'FL':
            folder = 'FLtrain_NCtest_GAtest'
        elif train_data_label == 'NC':
            folder = 'NCtrain_FLtest_GAtest'
        elif train_data_label == 'GA':
            folder = 'GAtrain_NCtest_FLtest'
        file_name = "../../Data/FinalDataSet_Combos/" + folder + "/" + test_data_label + "test_" + \
                    train_data_label + "train"
    if model_uid == 1:
        file_name = file_name + "_UID.csv"
    else:
        file_name = file_name + "_s.csv"
    if num_rows == 0:
        X, y_onehot, main_data, y = process_data_set(file_name, indis_remove=indis_remove, full_data=True,
                                                     drop_null_first_or_last=drop_null_first_or_last,
                                                     model_uid=model_uid)
    else:
        X, y_onehot, main_data, y = process_data_set(file_name, indis_remove=indis_remove, num_rows=num_rows,
                                                     drop_null_first_or_last=drop_null_first_or_last,
                                                     model_uid=model_uid)
    return X, y_onehot, main_data, y


def process_data_set(file_name, indis_remove=True, drop_duplicates=False, full_data=False, num_rows=500000,
                     drop_null_first_or_last=True, model_uid=0):
    data = pd.read_csv(file_name)  # Can select a smaller set for train, if the full data set cannot loaded into memory
    if drop_null_first_or_last:
        data = data.dropna(subset=['first_name'])
        data = data.dropna(subset=['last_name'])
    if 'race' not in data.columns:  # Used in Case Study
        data.loc[:, 'race'] = 'unavailable'
    data = data.dropna(subset=['race'])
    if drop_duplicates:  # Used in Troubleshooting experiment 5
        data.drop(columns=['dup', 'id'], inplace=True)
        data = data.drop_duplicates()
    data = data.assign(combined_name=data.first_name + " " + data.last_name)
    data.fillna(0, inplace=True)
    if indis_remove:
        data_shape = data.shape
        data = data[data.indis != 1]
        data_shape_after_indis = data.shape
        print("Indistinguishable count = ", data_shape[0] - data_shape_after_indis[0])
    if not full_data:
        data = data.sample(n=num_rows, random_state=1)
    data.reset_index(drop=True, inplace=True)
    data['n_sub_names'] = np.minimum(4, data['n_sub_names'])

    if 'id' in data.columns:
        main_data = data[['first_name', 'last_name', 'race', 'indis', 'id']]
    else:
        main_data = data[['first_name', 'last_name', 'race', 'indis']]

    y = main_data['race'].astype('category')
    print("Races: ", dict(enumerate(y.cat.categories)))
    y = y.cat.codes
    y.reset_index(drop=True, inplace=True)
    y_onehot = pd.get_dummies(y)
    print("y_onehot shape = ", y_onehot.shape)
    print("y_onehot columns = ", y_onehot.columns)

    feature_space_cols = get_feature_space_cols(model_uid=model_uid)
    X = data.loc[:, feature_space_cols]
    print("X shape = ", X.shape)

    return X, y_onehot, main_data, y


def find_pos_weights(y_train):
    pos_weights = []
    for race_class in range(4):
        label = y_train.iloc[:, race_class]
        negative_label_count = label.count() - label.sum()  # count - sum
        print("Negative count: ", negative_label_count)
        positive_label_count = label.sum()  # sum
        print("Positive count: ", positive_label_count)
        pos_weight = negative_label_count / positive_label_count
        pos_weights.append(pos_weight)
    return pos_weights


def get_feature_space_cols(model_uid=0):
    uid_feature_space_cols = ['pop_ln_asian', 'pop_ln_hispa', 'pop_ln_black', 'pop_ln_white',
                                   'pop_fn_asian', 'pop_fn_hispa', 'pop_fn_black', 'pop_fn_white',
                                   "best_evidence_asian", "best_evidence_black",
                                   "best_evidence_hispanic", "best_evidence_white",
                                   'dash_indicator', 'n_sub_names']
    feature_space_cols = ['pop_ln_asian', 'pop_ln_hispa', 'pop_ln_black', 'pop_ln_white',
                                   'pop_fn_asian', 'pop_fn_hispa', 'pop_fn_black', 'pop_fn_white',
                                   "best_evidence_asian", "best_evidence_black",
                                   "best_evidence_hispanic", "best_evidence_white",
                                   "pop_ln_asian_f4", "pop_ln_hispa_f4",
                                   "pop_ln_black_f4", "pop_ln_white_f4",
                                   "pop_fn_asian_f4", "pop_fn_hispa_f4",
                                   "pop_fn_black_f4", "pop_fn_white_f4",
                                   "pop_ln_asian_l4", "pop_ln_hispa_l4",
                                   "pop_ln_black_l4", "pop_ln_white_l4",
                                   "pop_fn_asian_l4", "pop_fn_hispa_l4",
                                   "pop_fn_black_l4", "pop_fn_white_l4",
                                   'dash_indicator', 'n_sub_names']
    if model_uid == 1:
        return uid_feature_space_cols
    return feature_space_cols


def find_max_value_of_feature_FLGA_train(feature):
    file_name = "../../Data/FinalDataSet_Combos/FLGAtrain_NCtest/FLGA_Train_s.csv"
    data = pd.read_csv(file_name, usecols=[feature])
    max_val = data[feature].max()
    print(max_val)
    return max_val


def get_FLGA_duplicates(count):
    file_name = "../../Data/Duplicates/FLGA_dups" + str(count) + ".csv"
    X, y_onehot, main_data, y = process_data_set(file_name, indis_remove=False, drop_duplicates=True, full_data=True)
    return X, y_onehot, main_data, y
