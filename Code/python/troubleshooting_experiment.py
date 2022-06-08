import seaborn as sns
from torch.utils.data import SubsetRandomSampler

from model_definition import LogisticRegressionModel
from model_ethnicIA_utilities import get_FLGA_duplicates
from sklearn import metrics
import torch
import numpy as np
import matplotlib.pyplot as plt


def test_duplicates_on_FLGA(count):
    # race_dict = {0: 'Asian', 1: 'Black', 2: 'Hispanic', 3: 'White'}
    X_test, y, test_data, y_test = get_FLGA_duplicates(count)
    test_dataset = torch.utils.data.TensorDataset(torch.tensor(np.array(X_test), dtype=torch.float32),
                                                  torch.tensor(np.array(y_test), dtype=torch.long))
    test_loader = torch.utils.data.DataLoader(dataset=test_dataset, batch_size=X_test.shape[0], shuffle=False)

    path = "../../Models/model_FLGA_s.pt"
    model = LogisticRegressionModel(30, 4)
    model.load_state_dict(torch.load(path))
    model.eval()
    for test_features, labels in test_loader:
        outputs = model(test_features)
        _, predicted = torch.max(outputs.data, 1)

    original = labels.detach().numpy()

    print("Accuracy: ", metrics.accuracy_score(original, predicted))
    print("Balanced Accuracy: ", metrics.balanced_accuracy_score(original, predicted))
    print("Confusion Matrix: ", metrics.confusion_matrix(original, predicted))
    print("Report", metrics.classification_report(original, predicted))
    return metrics.accuracy_score(original, predicted), metrics.balanced_accuracy_score(original, predicted)


def plot_duplicates_performance():
    count_list = [5, 10, 20, 30, 50, 100, 250, 500]
    accs = []
    bl_accs = []
    for count in count_list:
        accuracy, bl_acc = test_duplicates_on_FLGA(count)
        accs.append(accuracy)
        bl_accs.append(bl_acc)

    sns.set(style='white')
    plt.figure()
    plt.plot(count_list, accs)
    plt.xlabel('Number of Duplicates')
    plt.ylabel('Accuracy')
    plt.title('Performance based on duplicates for 300 names')
    plt.savefig("../../Visualizations/troubleshooting_experiment5.png")
    plt.show()
