import pandas as pd


def generate_indistinguishable_file(data_label):
    if data_label == 'FLGA':
        file_name = "../../Data/FinalDataSet_Combos/FLGAtrain_NCtest/FLGA_Train_s.csv"
    else:
        file_name = "../../Data/FinalDataSet_Combos/FLGAtrain_NCtest/NCtest_FLGAtrain_s.csv"
    data = pd.read_csv(file_name, usecols=['first_name', 'last_name', 'race', 'indis',
                                           'white_black_indis_fn', 'white_hispa_indis_fn', 'white_asian_indis_fn',
                                           'white_black_indis_ln', 'white_hispa_indis_ln', 'white_asian_indis_ln',
                                           'black_asian_indis_ln', 'black_hispa_indis_ln', 'asian_hispa_indis_ln',
                                           'black_asian_indis_fn', 'black_hispa_indis_fn', 'asian_hispa_indis_fn',
                                           "pop_ln_asian",
                                           "pop_ln_hispa",
                                           "pop_ln_black",
                                           "pop_ln_white",
                                           "pop_fn_asian",
                                           "pop_fn_hispa",
                                           "pop_fn_black",
                                           "pop_fn_white",
                                           ])
    data = data[data.indis == 1]
    if data_label == 'FLGA':
        data.to_csv("../../Data/Indistinguishable/FLGA_indistinguishable.csv", index=False)
    else:
        data.to_csv("../../Data/Indistinguishable/NC_FLGA_indistinguishable.csv", index=False)


def main():
    generate_indistinguishable_file('FLGA')
    generate_indistinguishable_file('NC')


if __name__ == "__main__":
    main()
