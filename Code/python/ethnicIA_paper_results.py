from case_study import case_study_train_test, generate_spatial_plots, general_stats
from case_study_spatial_plots import generate_spatial_plot_state
from computation_experiment import train_FLGA_ethnicIA_models, test_FLGA_ethnicIA_models, plot_ethnicIA_performance
from dataset_basic_stats import dataset_counts_and_distribution, average_of_top_two_most_likely_classes
from feature_importance import get_model_coefficients, generate_feature_importance_tornado_plot
from model_ethnicIA_testing import test_ethnicIA_model
from model_ethnicIA_training import train_ethnicIA_model
from model_ethnicolr_testing import ethnicolr_model_prediction
from model_ngrams_experiment import train_and_test_all_ngram_models, plot_performance_ngrams
from name_space_visualisations import plot_direct_3d_graph, generate_pacmap_coordinates, plot_pacmap_2d_graph
from proportions_experiment import proportions_FL_NC, proportions_FL_GA
from troubleshooting_experiment import plot_duplicates_performance


# Remove main functions from other files before running this!

# Steps for experiments, case study, and appendices
# Step 1: Run 01_Create_Train_Features_Master_sparse.R  and 01_Create_Train_Features_Master_UID.R
# to generate all training datasets
# Step 2: Run 02_Create_Test_Features_Master_sparse.R and 02_Create_Test_Features_Master_UID.R
# to generate all test datasets
# Step 3: Run function ethnicIA_model_training() in this file to train all the required models
# Step 4: Run function corresponding to the respective experiment from this file to replicate the results.
# Follow any instruction provided in the functions for the header.


def ethnicIA_model_training():
    train_ethnicIA_model('FL')
    train_ethnicIA_model('FL', add_pos_weights=False)
    train_ethnicIA_model('GA')
    train_ethnicIA_model('NC')
    train_ethnicIA_model('FLGA')
    train_ethnicIA_model('FLGA', add_pos_weights=False)
    train_ethnicIA_model('NC_rest')
    train_ethnicIA_model('NC_rest', add_pos_weights=False)


def general_statistics():
    dataset_counts_and_distribution('FL')
    dataset_counts_and_distribution('GA')
    dataset_counts_and_distribution('NC')
    average_of_top_two_most_likely_classes(indis_included=True)
    average_of_top_two_most_likely_classes(indis_included=False)
    average_of_top_two_most_likely_classes(indis_only=True)


def experiment1():
    test_ethnicIA_model('FL', 'NC', draw_roc_curve=True)
    ethnicolr_model_prediction(indis_remove=True)


def experiment2():
    get_model_coefficients()
    generate_feature_importance_tornado_plot()


def experiment3():
    # test_ethnicIA_model('FL', 'NC', generate_csv=True, add_prediction_probabilities=True, indis_remove=False)
    proportions_FL_NC()
    proportions_FL_GA()


def experiment4():
    train_FLGA_ethnicIA_models()
    test_FLGA_ethnicIA_models()
    plot_ethnicIA_performance()
    train_and_test_all_ngram_models(train_flag=False)
    plot_performance_ngrams()


def experiment5():
    print("With Balancing Weights")
    test_ethnicIA_model('NC_rest', 'NC_white')
    print("Without Balancing Weights")
    test_ethnicIA_model('NC_rest', 'NC_white', add_pos_weights=False)
    print("With Balancing Weights")
    test_ethnicIA_model('FLGA', 'NC_white')
    print("Without Balancing Weights")
    test_ethnicIA_model('FLGA', 'NC_white', add_pos_weights=False)


def experiment6():
    # test_ethnicIA_model('FLGA', 'FLGA', generate_csv=True, add_prediction_probabilities=True)
    # Run 05_Create_FLGA_Train_Duplicates_Master.R before running this function.
    plot_duplicates_performance()


def experiment8():
    test_ethnicIA_model('FLGA', 'NC', generate_csv=True, add_prediction_probabilities=True)
    plot_direct_3d_graph()
    generate_pacmap_coordinates()
    plot_pacmap_2d_graph()


def case_study():
    # Run 08_Overlap.R for statistics on Training dataset and FEC dataset overlap.
    dataset_counts_and_distribution('FLGANC', '../../Data/FinalDataSet_Combos/FLGANCtrain_ContrPred/FLGANC_Train_s.csv')
    case_study_train_test()
    # Need to regenerate the data sets for plots through R at this point
    # Run 06_FEC_Names_Subset.R and 06_FEC_GA_Names_Subset.R at this point
    general_stats()
    # Run 07_Plot_Donations.R to generate GASenate plots
    # Run 06_FEC_Small.R for Small Donors experiment
    generate_spatial_plots()


def appendix1():
    ethnicolr_model_prediction(indis_remove=False)


def appendix2():
    test_ethnicIA_model('FL', 'NC', add_pos_weights=False)


def appendix3():
    test_ethnicIA_model('FLGA', 'NC')
    test_ethnicIA_model('FL', 'GA')
    test_ethnicIA_model('GA', 'NC')
    test_ethnicIA_model('GA', 'FL')
    test_ethnicIA_model('NC', 'FL')
    test_ethnicIA_model('NC', 'GA')


# Run 15_PlotBracketed.R for Appendix 6

def appendix7():
    train_ethnicIA_model('FL', model_uid=1)
    test_ethnicIA_model('FL', 'NC', model_uid=1)


def appendix8():
    states = ["GA", "NC"]
    for state in states:
        generate_spatial_plot_state(state)

# Run 07_Plot_Donations.R, 07_Plot_Donations_Overlap.R and 07_Donations_Stats.R for Appendix 9


def main():
    print("Main Start!")


if __name__ == "__main__":
    main()
