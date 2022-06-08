import torch
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from model_definition import LogisticRegressionModel
from model_ethnicIA_utilities import get_feature_space_cols, find_max_value_of_feature_FLGA_train

plt.rcParams.update({'font.size': 12})
mapping = {
    'pop_ln_asian': 'probability_asian_last_name',
    'pop_ln_hispa': 'probability_hispanic_last_name',
    'pop_ln_black': 'probability_black_last_name',
    'pop_ln_white': 'probability_white_last_name',
    'pop_fn_asian': 'probability_asian_first_name',
    'pop_fn_hispa': 'probability_hispanic_first_name',
    'pop_fn_black': 'probability_black_first_name',
    'pop_fn_white': 'probability_white_first_name',
    "best_evidence_asian": 'best_evidence_asian',
    "best_evidence_black": 'best_evidence_black',
    "best_evidence_hispanic": 'best_evidence_hispanic',
    "best_evidence_white": 'best_evidence_white',
    "pop_ln_asian_f4": 'probability_asian_last_name_f4',
    "pop_ln_hispa_f4": 'probability_hispanic_last_name_f4',
    "pop_ln_black_f4": 'probability_black_last_name_f4',
    "pop_ln_white_f4": 'probability_white_last_name_f4',
    "pop_fn_asian_f4": 'probability_asian_first_name_f4',
    "pop_fn_hispa_f4": 'probability_hispanic_first_name_f4',
    "pop_fn_black_f4": 'probability_black_first_name_f4',
    "pop_fn_white_f4": 'probability_white_first_name_f4',
    "pop_ln_asian_l4": 'probability_asian_last_name_l4',
    "pop_ln_hispa_l4": 'probability_hispanic_last_name_l4',
    "pop_ln_black_l4": 'probability_black_last_name_l4',
    "pop_ln_white_l4": 'probability_white_last_name_l4',
    "pop_fn_asian_l4": 'probability_asian_first_name_l4',
    "pop_fn_hispa_l4": 'probability_hispanic_first_name_l4',
    "pop_fn_black_l4": 'probability_black_first_name_l4',
    "pop_fn_white_l4": 'probability_white_first_name_l4',
    'dash_indicator': 'dash_indicator',
    'n_sub_names': 'n_sub_names'
}


def get_model_coefficients(feature_scaling=False):
    features = get_feature_space_cols()
    model_coeff = pd.DataFrame(columns=['feature', 'Asian', 'Black', 'Hispanic', 'White', 'max_value'])
    race_dict = {0: 'Asian', 1: 'Black', 2: 'Hispanic', 3: 'White'}
    model_coeff['feature'] = features
    for race_class in range(4):
        path = "../../Models/model_FLGA_s.pt"
        model = LogisticRegressionModel(30, 4)
        model.load_state_dict(torch.load(path))
        model_coeff[race_dict[race_class]] = model.linear.weight.detach().numpy()[race_class].T
    if feature_scaling:
        for feature in features:
            max_val = find_max_value_of_feature_FLGA_train(feature)
            model_coeff.loc[model_coeff['feature'] == feature, 'max_value'] = max_val
            model_coeff.loc[model_coeff['feature'] == feature, 'Asian'] = \
                model_coeff.loc[model_coeff['feature'] == feature, 'Asian'] / max_val
            model_coeff.loc[model_coeff['feature'] == feature, 'Black'] = \
                model_coeff.loc[model_coeff['feature'] == feature, 'Black'] / max_val
            model_coeff.loc[model_coeff['feature'] == feature, 'Hispanic'] = \
                model_coeff.loc[model_coeff['feature'] == feature, 'Hispanic'] / max_val
            model_coeff.loc[model_coeff['feature'] == feature, 'White'] = \
                model_coeff.loc[model_coeff['feature'] == feature, 'White'] / max_val
    model_coeff.to_csv('../../Results/model_parameters_FLGA_s.csv', index=False)
    return model_coeff


def generate_feature_importance_tornado_plot():
    input_file = '../../Results/model_parameters_FLGA_s.csv'
    model_coeff = pd.read_csv(input_file)
    model_coeff.replace({"feature": mapping}, inplace=True)
    f, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, figsize=(14, 10), sharey='all')

    sns.barplot(x=model_coeff.Asian, y=model_coeff.feature, color='r', ax=ax1)
    ax1.axvline(0, color="k", clip_on=False)
    ax1.set_xlabel("Asian")
    ax1.set_ylabel("")

    sns.barplot(x=model_coeff.Black, y=model_coeff.feature, color='b', ax=ax2)
    ax2.axvline(0, color="k", clip_on=False)
    ax2.set_xlabel("Black")
    ax2.tick_params(axis='y', which='both', left=False)

    sns.barplot(x=model_coeff.Hispanic, y=model_coeff.feature, color='orange', ax=ax3)
    ax3.axvline(0, color="k", clip_on=False)
    ax3.set_xlabel("Hispanic")
    ax3.tick_params(axis='y', which='both', left=False)

    sns.barplot(x=model_coeff.White, y=model_coeff.feature, color='g', ax=ax4)
    ax4.axvline(0, color="k", clip_on=False)
    ax4.set_xlabel("White")
    ax4.tick_params(axis='y', which='both', left=False)

    ax1.label_outer()
    ax2.label_outer()
    ax3.label_outer()
    ax4.label_outer()

    sns.despine(left=True)
    plt.tight_layout()
    f.savefig('../../Visualizations/feature_importance_tornado_FLGA_s.png')
