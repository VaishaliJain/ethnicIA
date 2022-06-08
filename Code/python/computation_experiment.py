import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from model_ethnicIA_testing import test_ethnicIA_model
from computation_ethnicIA_training import computation_train_ethnicIA_model


def train_FLGA_ethnicIA_models():
    model_labels = [5, 10, 20, 40, 60, 80, 100]
    for model_label in model_labels:
        print('Model: ', model_label)
        computation_train_ethnicIA_model('FLGA', training_size=model_label * 1000)


def test_FLGA_ethnicIA_models():
    df = pd.DataFrame(columns=['label', 'values', 'type'])
    model_labels = [5, 10, 20, 40, 60, 80, 100]
    for model_label in model_labels:
        print("Model Label: ", model_label)
        path = "../../Models/model_FLGA_" + str(model_label) + "k.pt"
        test_acc, test_bal_acc = test_ethnicIA_model('FLGA', 'NC', model_path=path)
        train_acc, train_bal_acc = test_ethnicIA_model('FLGA', 'FLGA', model_path=path, num_rows=model_label * 1000)
        dicts = [{"label": model_label, "values": test_acc, "type": 'Test Accuracy'},
                 {"label": model_label, "values": test_bal_acc, "type": 'Test Balanced Accuracy'},
                 {"label": model_label, "values": train_acc, "type": 'Train Accuracy'},
                 {"label": model_label, "values": train_bal_acc, "type": 'Train Balanced Accuracy'}
                 ]
        df = df.append(dicts, ignore_index=True, sort=False)
    df.to_csv('../../Results/computation_ethnicIA_model.csv', index=False)


def plot_ethnicIA_performance():
    df = pd.read_csv('../../Results/computation_ethnicIA_model.csv')
    sns.set(style='white')
    sns_plot = sns.lineplot(data=df, x="label", y="values", hue="type",
                            hue_order=["Train Accuracy", "Test Accuracy", "Train Balanced Accuracy",
                                       "Test Balanced Accuracy"],
                            palette={"Train Accuracy": "#922B21", "Train Balanced Accuracy": "#17202A",
                                     "Test Accuracy": "#DC7633", "Test Balanced Accuracy": "#808B96"})
    sns_plot.set_yticks(list(np.arange(0.30, 1.00, 0.05)))
    plt.xlabel('Training Data Size (in thousands)', fontsize=12)
    plt.ylabel('')
    handles, labels = sns_plot.get_legend_handles_labels()
    sns_plot.legend(handles=handles[1:], labels=labels[1:])
    plt.setp(sns_plot.get_legend().get_texts(), fontsize='12')
    sns_plot.tick_params(labelsize=12)
    figure = sns_plot.get_figure()
    figure.savefig("../../Visualizations/computation_our_model.png")
    figure.clear()
