from torch.utils.data import SubsetRandomSampler
from sklearn import metrics
import torch
import numpy as np
from model_definition import LogisticRegressionModel
from model_ngrams_utilities import get_FL_names_list, create_feature_space, get_NC_names_list
from datetime import datetime


# Replication of model from Name-Ethnicity Classification and Ethnicity-Sensitive Name Matching paper


def test_ngram_model(data_label, lambda_label, generate_csv=False):
    dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print("date and time =", dt_string)
    # race_dict = {0: 'Asian', 1: 'Black', 2: 'Hispanic', 3: 'White'}
    if data_label == 'NC':
        X_test, y, test_data, y_test = create_feature_space(get_NC_names_list(), lambda_label, train=False)
    else:
        X_test, y, test_data, y_test = create_feature_space(get_FL_names_list(), lambda_label, train=False)
    test_dataset = torch.utils.data.TensorDataset(torch.tensor(np.array(X_test), dtype=torch.float32),
                                                  torch.tensor(np.array(y_test), dtype=torch.long))
    test_loader = torch.utils.data.DataLoader(dataset=test_dataset, batch_size=X_test.shape[0], shuffle=False)

    path = "../../Models/model_FL_ngram_" + str(lambda_label) + ".pt"
    model = LogisticRegressionModel(X_test.shape[1], 4)
    model.load_state_dict(torch.load(path))
    model.eval()
    for test_features, labels in test_loader:
        outputs = model(test_features)
        _, predicted = torch.max(outputs.data, 1)

    test_data['predicted_race'] = predicted
    original = labels.detach().numpy()

    accuracy = metrics.accuracy_score(original, predicted)
    balanced_accuracy = metrics.balanced_accuracy_score(original, predicted)
    print("Accuracy: ", accuracy)
    print("Balanced Accuracy: ", balanced_accuracy)
    print("Confusion Matrix: ", metrics.confusion_matrix(original, predicted))
    print("Report", metrics.classification_report(original, predicted))

    if generate_csv:
        test_data.to_csv(
            "../../Results/predictions_" + data_label + "_test_FL_train_ngram_" + str(lambda_label) + ".csv",
            index=False)

    dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    print("date and time =", dt_string)
    return accuracy, balanced_accuracy
