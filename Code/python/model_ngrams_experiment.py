import pandas as pd
from model_ngrams_training import train_FL_ngram_model
from model_ngrams_testing import test_ngram_model
import seaborn as sns
import matplotlib.pyplot as plt
import math


# Replication of model from Name-Ethnicity Classification and Ethnicity-Sensitive Name Matching paper


def train_and_test_all_ngram_models(train_flag=False):
    df = pd.DataFrame(columns=['label', 'values', 'type'])
    labels = [-6, -5, -4, -3, -2, -1, 0, 1, 2, 3, 4]
    for label in labels:
        lambda_label = math.pow(10, label)
        print("Lambda: ", lambda_label)
        if train_flag:
            train_FL_ngram_model(lambda_label)
        print("Dataset: FL")
        train_acc, train_bal_acc = test_ngram_model('FL', lambda_label)
        print("Dataset: NC")
        test_acc, test_bal_acc = test_ngram_model('NC', lambda_label)
        dicts = [{"label": label, "values": train_acc, "type": 'Train Accuracy'},
                 {"label": label, "values": train_bal_acc, "type": 'Train Balanced Accuracy'},
                 {"label": label, "values": test_acc, "type": 'Test Accuracy'},
                 {"label": label, "values": test_bal_acc, "type": 'Test Balanced Accuracy'}]
        df = df.append(dicts, ignore_index=True, sort=False)
    df.to_csv('../../Results/computation_ngrams_performance.csv', index=False)


def plot_performance_ngrams():
    df = pd.read_csv('../../Results/computation_ngrams_performance.csv')
    sns.set(style='white')
    sns_plot = sns.lineplot(data=df, x="label", y="values", hue="type",
                            hue_order=["Train Accuracy", "Test Accuracy", "Train Balanced Accuracy",
                                       "Test Balanced Accuracy"],
                            palette={"Train Accuracy": "#13448E", "Train Balanced Accuracy": "#0D6C28",
                                     "Test Accuracy": "#199AD6", "Test Balanced Accuracy": "#10BA41"})
    plt.xlabel('Regularization Parameter (10e{x})', fontsize=12)
    plt.ylabel('')
    plt.setp(sns_plot.get_legend().get_texts(), fontsize='10')
    sns_plot.tick_params(labelsize=12)
    sns_plot.axhline(.8049, ls='--', color='#922B21')  # ethnicIA FLGA/NC Train Accuracy
    plt.plot([0.8049], label="ethnicIA Train Accuracy", linestyle='--', color='#922B21')
    sns_plot.axhline(.7482, ls='--', color='#DC7633')  # ethnicIA FLGA/NC Test Accuracy
    plt.plot([0.7482], label="ethnicIA Test Accuracy", linestyle='--', color='#DC7633')
    sns_plot.axhline(.8320, ls='--', color='#17202A')  # ethnicIA FLGA/NC Train Balanced Accuracy
    plt.plot([0.8320], label="ethnicIA Train Balanced Accuracy", linestyle='--', color='#17202A')
    sns_plot.axhline(.7739, ls='--', color='#808B96')  # ethnicIA FLGA/NC Test Balanced Accuracy
    plt.plot([0.7739], label="ethnicIA Test Balanced Accuracy", linestyle='--', color='#808B96')
    handles, labels = sns_plot.get_legend_handles_labels()
    sns_plot.legend(handles=handles[1:], labels=labels[1:], bbox_to_anchor=(1.04, 0.5), loc="center left",
                    borderaxespad=0)
    figure = sns_plot.get_figure()
    figure.savefig("../../Visualizations/computation_n_grams_model.png", bbox_inches="tight")
    figure.clear()
