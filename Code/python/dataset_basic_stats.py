import pandas as pd


def dataset_counts_and_distribution(data_label, input_file=None):
    file_name = "../../Data/NameRaceData/" + data_label + ".csv"
    if input_file:
        file_name = input_file
    data = pd.read_csv(file_name, usecols=['first_name', 'last_name', 'race'])
    data = data.dropna(subset=['first_name'])
    data = data.dropna(subset=['last_name'])
    data = data.dropna(subset=['race'])
    print(data_label)
    print(len(data))
    print(data['race'].value_counts(dropna=False, normalize=True))


def indistinguishable_in_NC():
    file_name = "../../Data/FinalDataSet_Combos/FLGAtrain_NCtest/NCtest_FLGAtrain.csv"
    data = pd.read_csv(file_name, usecols=['first_name', 'last_name', 'race', 'indis'])
    print(len(data))
    print(data['indis'].value_counts())
    print(data['indis'].value_counts(normalize=True))


def indistinguishable_in_FLGA():
    file_name = "../../Data/FinalDataSet_Combos/FLGAtrain_NCtest/FLGA_Train.csv"
    data = pd.read_csv(file_name, usecols=['first_name', 'last_name', 'race', 'indis'])
    print(len(data))
    print(data['indis'].value_counts())
    print(data['indis'].value_counts(normalize=True))


def find_name_distribution(name, last_name_flag=False):
    file_name = "../../Data/FinalDataSet_Combos/FLGAtrain_NCtest/FLGA_Train.csv"
    data = pd.read_csv(file_name, usecols=['first_name', 'last_name', 'race', 'indis'])
    if last_name_flag:
        data = data[data.last_name == name]
    else:
        data = data[data.first_name == name]
    print(name)
    print(len(data))
    print(data['indis'].value_counts())
    print(data['race'].value_counts(normalize=True))


def pure_hispanic_last_names():
    file_name = "../../Data/FinalDataSet_Combos/FLGAtrain_NCtest/FLGA_Train.csv"
    data = pd.read_csv(file_name, usecols=['last_name', 'race', 'indis', "pop_ln_asian",
                                           "pop_ln_hispa",
                                           "pop_ln_black",
                                           "pop_ln_white"])
    data = data[data.pop_ln_asian == 0]
    data = data[data.pop_ln_black == 0]
    data = data[data.pop_ln_white == 0]
    data = data['last_name'].value_counts().rename_axis('Unique Hispanic Last Names').reset_index(name='Frequency')
    data.to_csv("../../Results/hispanic_last_names.csv", index=False)


def average_of_top_two_most_likely_classes(indis_included=False, indis_only=False):
    file_name = "../../Results/predictions_NC_test_FLGA_train_s.csv"
    if indis_included or indis_only:
        print("Indistinguishable included")
        file_name = "../../Results/predictions_NC_test_FLGA_train_with_indis_s.csv"
    df = pd.read_csv(file_name, usecols=['Asian', 'Black', 'Hispanic', 'White', 'indis'])
    if indis_only:
        print("Indistinguishable Only")
        df = df[df.indis == 1]
    del df['indis']
    df['first'] = df.max(axis=1)
    average_first = df["first"].mean()
    print("Average First: ", average_first)
    del df['first']
    df['second'] = df.apply(lambda row: row.nlargest(2).values[-1], axis=1)
    average_second = df["second"].mean()
    print("Average Second: ", average_second)
    print("Diff in average: ", average_first - average_second)
