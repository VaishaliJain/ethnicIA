from itertools import cycle

import matplotlib.pyplot as plt
import pandas as pd
from ethnicolr import pred_fl_reg_name
from sklearn import metrics
from sklearn.preprocessing import label_binarize


def get_NC_data(indis_remove=True):
    data = pd.read_csv("../../Data/FinalDataSet_Combos/FLtrain_NCtest_GAtest/NCtest_FLtrain.csv",
                       usecols=['first_name', 'last_name', 'race', 'indis'])
    data = data.dropna(subset=['first_name'])
    data = data.dropna(subset=['last_name'])
    data = data.dropna(subset=['race'])
    if indis_remove:
        data = data[data.indis != 1]
    data.reset_index(drop=True, inplace=True)
    print("Shape: ", data.shape)
    print("Races: ", data.race.unique())
    return data


def ethnicolr_model_prediction(indis_remove=True, draw_roc_curve=False):
    test_data = get_NC_data(indis_remove=indis_remove)
    race_dict = {
        "asian": "Asian",
        "hispanic": "Hispanic",
        "nh_black": "Black",
        "nh_white": "White"
    }
    test_data['race_original'] = test_data['race']
    del test_data['race']
    result = pred_fl_reg_name(test_data, 'last_name', 'first_name')
    result['race'] = result['race'].map(race_dict, na_action='ignore').fillna(result['race'])

    if draw_roc_curve:
        race_list = ["asian", "nh_black", "hispanic", "nh_white"]
        original = result['race_original'].map({'Asian': 0, 'Black': 1, 'Hispanic': 2, 'White': 3},
                                               na_action='ignore').fillna(result['race_original'])
        original_binarized = label_binarize(original, classes=[0, 1, 2, 3])
        fpr = dict()
        tpr = dict()
        roc_auc = dict()
        for i in range(4):
            fpr[i], tpr[i], _ = metrics.roc_curve(original_binarized[:, i], result.loc[:, race_list[i]])
            roc_auc[i] = metrics.auc(fpr[i], tpr[i])

        plt.figure()
        lw = 2
        race_dict = {0: 'Asian', 1: 'Black', 2: 'Hispanic', 3: 'White'}
        colors = cycle(['aqua', 'darkorange', 'cornflowerblue', 'deeppink'])
        for i, color in zip(range(4), colors):
            plt.plot(fpr[i], tpr[i], color=color, lw=lw,
                     label='ROC curve of class {0} (area = {1:0.2f})'
                           ''.format(race_dict.get(i), roc_auc[i]))
        plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('ROC AUC curve for ethnicolr')
        plt.legend(loc="lower right")
        plt.savefig("../../Visualizations/ROC_AUC_ethnicolr.png")

    if indis_remove:
        print("After Indistinguishable Removal")
    else:
        print("Without Indistinguishable Removal")
    print("Accuracy: ", metrics.accuracy_score(result.race_original, result.race))
    print("Balanced Accuracy: ", metrics.balanced_accuracy_score(result.race_original, result.race))
    print("Confusion Matrix: ", metrics.confusion_matrix(result.race_original, result.race))
    print("Report", metrics.classification_report(result.race_original, result.race))
