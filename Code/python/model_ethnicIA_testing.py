from itertools import cycle

from sklearn import metrics
from torch.utils.data import SubsetRandomSampler

from model_definition import LogisticRegressionModel
from model_ethnicIA_utilities import get_test_dataset
from sklearn.preprocessing import label_binarize
import torch
import gc
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def test_ethnicIA_model(train_data_label, test_data_label, generate_csv=False, model_path='',
                        generate_performance_report=True, add_prediction_probabilities=False, num_rows=0,
                        add_pos_weights=True, draw_roc_curve=False, indis_remove=True, model_uid=0):
    suffix = "_s"
    if model_uid == 1:
        suffix = suffix + "_uid"
    if not add_pos_weights:
        suffix = suffix + "_no_pos_weights"
    # race_dict = {0: 'Asian', 1: 'Black', 2: 'Hispanic', 3: 'White'}
    X_test, y, test_data, y_test = get_test_dataset(train_data_label, test_data_label, num_rows=num_rows,
                                                    indis_remove=indis_remove, model_uid=model_uid)

    test_dataset = torch.utils.data.TensorDataset(torch.tensor(np.array(X_test), dtype=torch.float32),
                                                  torch.tensor(np.array(y_test), dtype=torch.long))
    test_loader = torch.utils.data.DataLoader(dataset=test_dataset, batch_size=X_test.shape[0], shuffle=False)

    if model_path == '':
        path = "../../Models/model_" + train_data_label + suffix + ".pt"
    else:
        path = model_path
    print(path)
    features_count = 30
    if model_uid == 1:
        features_count = 14
    model = LogisticRegressionModel(features_count, 4)

    model.load_state_dict(torch.load(path))
    model.eval()
    for test_features, labels in test_loader:
        outputs = model(test_features)
        _, predicted = torch.max(outputs.data, 1)

    del X_test
    del test_dataset
    del test_loader
    gc.collect()
    test_data.loc[:, 'predicted_race'] = predicted
    original = labels.detach().numpy()

    if draw_roc_curve:
        normalised_outputs = torch.nn.functional.softmax(outputs.data, dim=1)
        predicted_probs = pd.DataFrame(normalised_outputs).astype("float")
        original_binarized = label_binarize(original, classes=[0, 1, 2, 3])
        fpr = dict()
        tpr = dict()
        roc_auc = dict()
        for i in range(4):
            fpr[i], tpr[i], _ = metrics.roc_curve(original_binarized[:, i], predicted_probs.loc[:, i])
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
        plt.xticks(fontsize=12)
        plt.ylim([0.0, 1.05])
        plt.yticks(fontsize=12)
        plt.xlabel('False Positive Rate', fontsize=14)
        plt.ylabel('True Positive Rate', fontsize=14)
        plt.title('ROC curves and AUC values for ethnicIA', fontsize=16)
        plt.legend(loc="lower right", prop={"size": 12})
        plt.savefig("../../Visualizations/ROC_AUC_" + train_data_label + "_" + test_data_label + suffix + ".png")

    if generate_csv:
        mapping = {0: "Asian", 1: "Black", 2: "Hispanic", 3: "White"}
        test_data['predicted_race'] = test_data['predicted_race'].map(mapping)
        if add_prediction_probabilities:
            normalised_outputs = torch.nn.functional.softmax(outputs.data, dim=1)
            probs = pd.DataFrame(normalised_outputs).astype("float")
            probs.rename(columns={0: 'Asian', 1: 'Black', 2: 'Hispanic', 3: 'White'}, inplace=True)
            for col in probs.columns:
                test_data.loc[:, col] = probs.loc[:, col]
        if indis_remove:
            test_data.to_csv(
                "../../Results/predictions_" + test_data_label + "_test_" + train_data_label + "_train" + suffix + ".csv",
                index=False)
        else:
            test_data.to_csv(
                "../../Results/predictions_" + test_data_label + "_test_" + train_data_label + "_train_with_indis" + suffix + ".csv",
                index=False)

    if generate_performance_report:
        accuracy = metrics.accuracy_score(original, predicted)
        balanced_accuracy = metrics.balanced_accuracy_score(original, predicted)
        print("Train: " + train_data_label)
        print("Test: " + test_data_label)
        print("Accuracy: ", accuracy)
        print("Balanced Accuracy: ", balanced_accuracy)
        print("Confusion Matrix: ", metrics.confusion_matrix(original, predicted))
        print("Report", metrics.classification_report(original, predicted))
        return accuracy, balanced_accuracy
