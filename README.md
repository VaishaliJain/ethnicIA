# ethnicIA

![](/Images/ethnicIA_logo.png?raw=true)

"The Importance of being Ernest, Ekundayo, or Eswari: An Interpretable Machine Learning Approach to Name-based Ethnicity Classification"
Authors: Vaishali Jain, Ted Enamorado, and Cynthia Rudin

Citation: Jain, V., Enamorado, T., & Rudin, C. (2022). The Importance of Being Ernest, Ekundayo, or Eswari: An Interpretable Machine Learning Approach to Name-Based Ethnicity Classification. Harvard Data Science Review, 4(3). https://doi.org/10.1162/99608f92.db1aba8b

# Data

You can download the datasets from NC and FL from here: https://users.cs.duke.edu/~cynthia/ethnicIA/Data/. The GA data is not publicly available, so we have created 3 processed training and test datasets using only NC and FL that can be useful for testing algorithms.

# Steps to replicate experiments, case study, and appendices

Step 1: Run Code/R/01_Create_Train_Features_Master_sparse.R and Code/R/01_Create_Train_Features_Master_UID.R to generate all training datasets
Step 2: Run Code/R/02_Create_Test_Features_Master_sparse.R and Code/R/02_Create_Test_Features_Master_UID.R to generate all test datasets
Step 3: Run function ethnicIA_model_training() in Code/python/ethnicIA_paper_results.py file to train all the required models
Step 4: Run functions corresponding to the respective experiment from Code/python/ethnicIA_paper_results.py file to replicate the results.

Follow any instruction provided in the functions in the python file. 
(Open up Code/python/ethnicIA_paper_results.py for clarification on this step.)

# Replication for Section 3: Sensitivity of parameters for Indistinguishibility

Run Code/R/03_Create_Features_FLGA_multCuts.R and Code/R/03_Plot_multCuts.R to generate the contour plot shown in Figure 1.

![Namespace](/Images/Namespace.png?raw=true "Namespace")
