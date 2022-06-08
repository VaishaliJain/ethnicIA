import pandas as pd


def proportions_FL_NC():
    dataFL = pd.read_csv("../../Data/FinalDataSet_Combos/FLtrain_NCtest_GAtest/FL_Train_s.csv",
                         usecols=['id', 'race', 'indis'])
    # P(indis|white train) = P(indis|white test)
    p_indis_white_train = dataFL[(dataFL.race == 'White') & (dataFL.indis == 1)].shape[0] / \
                          dataFL[dataFL.race == 'White'].shape[0]
    print("P(indis|white train) = P(indis|white test) = ", p_indis_white_train)
    # P(indis|black train) = P(indis|black test)
    p_indis_black_train = dataFL[(dataFL.race == 'Black') & (dataFL.indis == 1)].shape[0] / \
                          dataFL[dataFL.race == 'Black'].shape[0]
    print("P(indis|black train) = P(indis|black test) = ", p_indis_black_train)
    # P(indis|hispanic train) = P(indis|hispanic test)
    p_indis_hispanic_train = dataFL[(dataFL.race == 'Hispanic') & (dataFL.indis == 1)].shape[0] / \
                             dataFL[dataFL.race == 'Hispanic'].shape[0]
    print("P(indis|hispanic train) = P(indis|hispanic test) = ", p_indis_hispanic_train)
    # P(indis|asian train) = P(indis|asian test)
    p_indis_asian_train = dataFL[(dataFL.race == 'Asian') & (dataFL.indis == 1)].shape[0] / \
                          dataFL[dataFL.race == 'Asian'].shape[0]
    print("P(indis|asian train) = P(indis|asian test) = ", p_indis_asian_train)
    del dataFL

    dataNC = pd.read_csv("../../Results/predictions_NC_test_FL_train_with_indis_s.csv",
                         usecols=['id', 'predicted_race', 'race', 'indis'])
    # P(white | test) = P(white | dis test)
    p_white_dis_test = dataNC[(dataNC.predicted_race == 'White') & (dataNC.indis == 0)].shape[0] / \
                       dataNC[dataNC.indis == 0].shape[0]
    print("P(white | test) = P(white | dis test) = ", p_white_dis_test)
    # P(black | test) = P(black | dis test)
    p_black_dis_test = dataNC[(dataNC.predicted_race == 'Black') & (dataNC.indis == 0)].shape[0] / \
                       dataNC[dataNC.indis == 0].shape[0]
    print("P(black | test) = P(black | dis test) = ", p_black_dis_test)
    # P(hispanic | test) = P(hispanic | dis test)
    p_hispanic_dis_test = dataNC[(dataNC.predicted_race == 'Hispanic') & (dataNC.indis == 0)].shape[0] / \
                          dataNC[dataNC.indis == 0].shape[0]
    print("P(hispanic | test) = P(hispanic | dis test) = ", p_hispanic_dis_test)
    # P(asian | test) = P(asian | dis test)
    p_asian_dis_test = dataNC[(dataNC.predicted_race == 'Asian') & (dataNC.indis == 0)].shape[0] / \
                       dataNC[dataNC.indis == 0].shape[0]
    print("P(asian | test) = P(asian | dis test) = ", p_asian_dis_test)

    # P(indis | test) = P(indis|white test)P(white | test) + P(indis|black test)P(black | test) +
    #               P(indis|hispanic test)P(hispanic | test) + P(indis|asian test)P(asian | test)
    p_indis_test = (p_indis_white_train * p_white_dis_test) + (
            p_indis_black_train * p_black_dis_test) + (p_indis_hispanic_train * p_hispanic_dis_test) + (
                           p_indis_asian_train * p_asian_dis_test)
    print(
        "P(indis | test) = P(indis|white test)P(white | test) + P(indis|black test)P(black | test) + "
        "P(indis|hispanic test)P(hispanic | test) + P(indis|asian test)P(asian | test) = ",
        p_indis_test)

    # P(white|indis test) = P(indis|white test)P(white | test)/ P(indis | test)
    p_white_indis_test = (p_indis_white_train * p_white_dis_test) / p_indis_test
    print(
        "P(indis|white test)P(white | test)/ P(indis | test) = ",
        p_white_indis_test)

    # P(black|indis test) = P(indis|black test)P(black | test)/ P(indis | test))
    p_black_indis_test = (p_indis_black_train * p_black_dis_test) / p_indis_test
    print(
        "P(black|indis test) = P(indis|black test)P(black | test)/ P(indis | test) = ",
        p_black_indis_test)

    print("True Indistinguishable White number for test data: ",
          dataNC[(dataNC.race == 'White') & (dataNC.indis == 1)].shape[0])
    print("True Indistinguishable Black number for test data: ",
          dataNC[(dataNC.race == 'Black') & (dataNC.indis == 1)].shape[0])
    print("Predicted Indistinguishable White number for test data: ",
          dataNC[(dataNC.predicted_race == 'White') & (dataNC.indis == 1)].shape[0])
    print("Predicted Indistinguishable Black number for test data: ",
          dataNC[(dataNC.predicted_race == 'Black') & (dataNC.indis == 1)].shape[0])

    num_indis_test = dataNC[dataNC.indis == 1].shape[0]
    print("Number of Indistinguishables in test dataset: N(indis test) = ", num_indis_test)
    print("Based on proportions, Indistinguishable White number for test data: N(indis test) * P(white|indis test) = ",
          num_indis_test * p_white_indis_test)
    print("Based on proportions, Indistinguishable Black number for test data: N(indis test) * P(black|indis test) = ",
          num_indis_test * p_black_indis_test)


def proportions_FL_GA():
    dataGA = pd.read_csv("../../Data/FinalDataSet_Combos/GAtrain_NCtest_FLtest/GA_Train_s.csv",
                         usecols=['id', 'race', 'indis'])
    # P(indis|white train) = P(indis|white test)
    p_indis_white_train = dataGA[(dataGA.race == 'White') & (dataGA.indis == 1)].shape[0] / \
                          dataGA[dataGA.race == 'White'].shape[0]
    print("P(indis|white train) = P(indis|white test) = ", p_indis_white_train)
    # P(indis|black train) = P(indis|black test)
    p_indis_black_train = dataGA[(dataGA.race == 'Black') & (dataGA.indis == 1)].shape[0] / \
                          dataGA[dataGA.race == 'Black'].shape[0]
    print("P(indis|black train) = P(indis|black test) = ", p_indis_black_train)
    # P(indis|hispanic train) = P(indis|hispanic test)
    p_indis_hispanic_train = dataGA[(dataGA.race == 'Hispanic') & (dataGA.indis == 1)].shape[0] / \
                             dataGA[dataGA.race == 'Hispanic'].shape[0]
    print("P(indis|hispanic train) = P(indis|hispanic test) = ", p_indis_hispanic_train)
    # P(indis|asian train) = P(indis|asian test)
    p_indis_asian_train = dataGA[(dataGA.race == 'Asian') & (dataGA.indis == 1)].shape[0] / \
                          dataGA[dataGA.race == 'Asian'].shape[0]
    print("P(indis|asian train) = P(indis|asian test) = ", p_indis_asian_train)
    del dataGA

    dataNC = pd.read_csv("../../Results/predictions_NC_test_GA_train_with_indis_s.csv",
                         usecols=['id', 'predicted_race', 'race', 'indis'])
    # P(white | test) = P(white | dis test)
    p_white_dis_test = dataNC[(dataNC.predicted_race == 'White') & (dataNC.indis == 0)].shape[0] / \
                       dataNC[dataNC.indis == 0].shape[0]
    print("P(white | test) = P(white | dis test) = ", p_white_dis_test)
    # P(black | test) = P(black | dis test)
    p_black_dis_test = dataNC[(dataNC.predicted_race == 'Black') & (dataNC.indis == 0)].shape[0] / \
                       dataNC[dataNC.indis == 0].shape[0]
    print("P(black | test) = P(black | dis test) = ", p_black_dis_test)
    # P(hispanic | test) = P(hispanic | dis test)
    p_hispanic_dis_test = dataNC[(dataNC.predicted_race == 'Hispanic') & (dataNC.indis == 0)].shape[0] / \
                          dataNC[dataNC.indis == 0].shape[0]
    print("P(hispanic | test) = P(hispanic | dis test) = ", p_hispanic_dis_test)
    # P(asian | test) = P(asian | dis test)
    p_asian_dis_test = dataNC[(dataNC.predicted_race == 'Asian') & (dataNC.indis == 0)].shape[0] / \
                       dataNC[dataNC.indis == 0].shape[0]
    print("P(asian | test) = P(asian | dis test) = ", p_asian_dis_test)

    # P(indis | test) = P(indis|white test)P(white | test) + P(indis|black test)P(black | test) +
    #               P(indis|hispanic test)P(hispanic | test) + P(indis|asian test)P(asian | test)
    p_indis_test = (p_indis_white_train * p_white_dis_test) + (
            p_indis_black_train * p_black_dis_test) + (p_indis_hispanic_train * p_hispanic_dis_test) + (
                           p_indis_asian_train * p_asian_dis_test)
    print(
        "P(indis | test) = P(indis|white test)P(white | test) + P(indis|black test)P(black | test) + "
        "P(indis|hispanic test)P(hispanic | test) + P(indis|asian test)P(asian | test) = ",
        p_indis_test)

    # P(white|indis test) = P(indis|white test)P(white | test)/ P(indis | test)
    p_white_indis_test = (p_indis_white_train * p_white_dis_test) / p_indis_test
    print(
        "P(indis|white test)P(white | test)/ P(indis | test) = ",
        p_white_indis_test)

    # P(black|indis test) = P(indis|black test)P(black | test)/ P(indis | test))
    p_black_indis_test = (p_indis_black_train * p_black_dis_test) / p_indis_test
    print(
        "P(black|indis test) = P(indis|black test)P(black | test)/ P(indis | test) = ",
        p_black_indis_test)

    print("True Indistinguishable White number for test data: ",
          dataNC[(dataNC.race == 'White') & (dataNC.indis == 1)].shape[0])
    print("True Indistinguishable Black number for test data: ",
          dataNC[(dataNC.race == 'Black') & (dataNC.indis == 1)].shape[0])
    print("Predicted Indistinguishable White number for test data: ",
          dataNC[(dataNC.predicted_race == 'White') & (dataNC.indis == 1)].shape[0])
    print("Predicted Indistinguishable Black number for test data: ",
          dataNC[(dataNC.predicted_race == 'Black') & (dataNC.indis == 1)].shape[0])

    num_indis_test = dataNC[dataNC.indis == 1].shape[0]
    print("Number of Indistinguishables in test dataset: N(indis test) = ", num_indis_test)
    print("Based on proportions, Indistinguishable White number for test data: N(indis test) * P(white|indis test) = ",
          num_indis_test * p_white_indis_test)
    print("Based on proportions, Indistinguishable Black number for test data: N(indis test) * P(black|indis test) = ",
          num_indis_test * p_black_indis_test)
