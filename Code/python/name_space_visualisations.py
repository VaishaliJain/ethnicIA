import pandas as pd
import seaborn as sns
import pacmap
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import matplotlib as mpl  # noqa
from mpl_toolkits.mplot3d import Axes3D  # noqa

mpl.style.use('seaborn')


def get_data_probability():
    data = pd.read_csv("../../Results/predictions_NC_test_FLGA_train_s.csv")
    data = data.dropna(subset=['first_name'])
    data = data.dropna(subset=['last_name'])
    data = data.dropna(subset=['race'])
    data = data.sample(n=250000, random_state=2)
    data.reset_index(drop=True, inplace=True)
    X = data[['Asian', 'Black', 'Hispanic', 'White']]
    return data, X


def pacmap_reduction(X):
    embedding = pacmap.PaCMAP(n_dims=2, n_neighbors=100, MN_ratio=0.5, FP_ratio=2.0)
    X_transformed = embedding.fit_transform(X.to_numpy(), init="pca")
    return X_transformed


def plot_direct_3d_graph():
    data, X = get_data_probability()
    race_dict = {'Asian': 0, 'Black': 1, 'Hispanic': 2, 'White': 3}
    labels = ['Asian', 'Black', 'Hispanic', 'White']
    ax_label_categories = [['Asian', 'Black', 'Hispanic'], ['Asian', 'Black', 'White'], ['Asian', 'Hispanic', 'White'],
                           ['Black', 'Hispanic', 'White']]
    for ax_labels in ax_label_categories:
        label = '-'.join(ax_labels)
        sns.set(style='white')
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        colours = ListedColormap(['r', 'b', 'g', 'orange'])
        scatter = ax.scatter(data.loc[:, ax_labels[0]], data.loc[:, ax_labels[1]], data.loc[:, ax_labels[2]],
                             c=[race_dict[x] for x in data.race], cmap=colours, s=1)
        ax.set_xlabel(ax_labels[0], fontsize=13)
        ax.set_ylabel(ax_labels[1], fontsize=13)
        ax.set_zlabel(ax_labels[2], fontsize=13)
        plt.legend(handles=scatter.legend_elements()[0], labels=labels, loc='upper right')
        if label == 'Black-Hispanic-White':
            for angle in [-60, -30, 0, 30, 60, 90, 120, 180]:
                ax.view_init(30, angle)
                new_label = label + '-' + str(angle)
                plt.savefig("../../Visualizations/NameSpace/" + new_label + ".png")
            plt.clf()
        else:
            plt.savefig("../../Visualizations/NameSpace/" + label + ".png")
            plt.clf()


def generate_pacmap_coordinates():
    data, X = get_data_probability()
    X_transformed = pacmap_reduction(X)
    embedding_data = pd.DataFrame(data=X_transformed, columns=['x', 'y'])
    embedding_data['race'] = data['race']
    embedding_data['first_name'] = data['first_name']
    embedding_data['last_name'] = data['last_name']
    embedding_data.to_csv("../../Results/pacmap_coordinates.csv", index=False)


def plot_pacmap_2d_graph():
    embedding_data = pd.read_csv("../../Results/pacmap_coordinates.csv")
    sns.set(style='white', rc={'figure.figsize': (15, 12)})
    sns_plot = sns.scatterplot(data=embedding_data, x="x", y="y", hue="race", style="race")
    handles, labels = sns_plot.get_legend_handles_labels()
    sns_plot.legend(handles=handles[1:], labels=labels[1:], loc='lower right')
    plt.setp(sns_plot.get_legend().get_texts(), fontsize='20')
    plt.setp(sns_plot.get_legend().get_title(), fontsize='24')
    plt.tick_params(bottom=False, top=False, left=False, right=False, labelbottom=False, labeltop=False,
                    labelleft=False, labelright=False)
    plt.ylabel('')
    plt.xlabel('')
    plt.axis("off")
    add_group_annotations()
    figure = sns_plot.get_figure()
    figure.savefig("../../Visualizations/NameSpace/pacmap.png")


def add_group_annotations():
    bbox_props = dict(boxstyle="round,pad=0.5", fc="w", ec="k", lw=1)
    blue_tip = "Grzegorz Koscik \n Suzanne Olshefski \n Kathryn Higbee \n Susan Gigliotti \n " \
               "Scott Olaughlin \n Holly Radloff \n Jill Isenberg"
    plt.annotate(blue_tip, xy=(-40, 4),
                 xytext=(-40 - 12, 4 - 5),
                 arrowprops=dict(arrowstyle="simple", facecolor='tab:brown'),
                 horizontalalignment="left",
                 verticalalignment='top',
                 bbox=bbox_props,
                 fontsize=14)
    green_tip = "Quaneisha Boykins \n Khadijah Diop \n Mamadou Sanogo" \
                " \n Chioma Okoye \n Ebony Washington \n Olumide Adeniyi" \
                " \n Isatou Njie"
    plt.annotate(green_tip, xy=(17, -17.25),
                 xytext=(17 - 18, -17.25 - 0.5),
                 arrowprops=dict(arrowstyle="simple", facecolor='tab:brown'),
                 horizontalalignment="left",
                 verticalalignment='top',
                 bbox=bbox_props,
                 fontsize=14)
    red_tip = " Ushaben Patel " \
              "\n Wei Zhao \n Min Xu \n Yun Kim " \
              "\n Bhavna Mehta \n Ngoc Tran \n Phuong Nguyen "
    plt.annotate(red_tip, xy=(7, 22),
                 xytext=(7 + 5, 22 + 12),
                 arrowprops=dict(arrowstyle="simple", facecolor='tab:brown'),
                 horizontalalignment="left",
                 verticalalignment='top',
                 bbox=bbox_props,
                 fontsize=14)
    orange_tip = "Jose Rivera Velazquez \n Luis Gonzalez-Chavez \n Salvador Torres Lopez " \
                 "\n Silvia Marrero Ortiz \n Carlos Garcia-Ortiz \n Rafael Garcia-Ramos " \
                 "\n Hector Silva Rodriguez"
    plt.annotate(orange_tip, xy=(6, 26.5),
                 xytext=(6 - 24, 26.5 + 8),
                 arrowprops=dict(arrowstyle="simple", facecolor='tab:brown'),
                 horizontalalignment="left",
                 verticalalignment='top',
                 bbox=bbox_props,
                 fontsize=14)
    close_to_orange = "Ricardo Wallace \n Sergio Mitchell " \
                      "\n Karen Luciano \n Maria Phillips " \
                      "\n Carmen Smith \n Carlos Davis"
    plt.annotate(close_to_orange, xy=(0, 9.3),
                 xytext=(0 - 28, 9.3 + 10),
                 arrowprops=dict(arrowstyle="simple", facecolor='tab:brown'),
                 horizontalalignment="left",
                 verticalalignment='top',
                 bbox=bbox_props,
                 fontsize=14)
    close_to_red = " Mala Brewer \n Amisha Polk " \
                   "\n Nancy Farhad \n Sidra Owens " \
                   "\n Malavika William \n Cynthia Mohan"
    plt.annotate(close_to_red, xy=(2, 9.2),
                 xytext=(2 + 25, 9.2 + 15),
                 arrowprops=dict(arrowstyle="simple", facecolor='tab:brown'),
                 horizontalalignment="right",
                 verticalalignment='top',
                 bbox=bbox_props,
                 fontsize=14)


def add_annotation_through_csv():
    data_annotations = pd.read_csv("../../Results/pacmap_coordinates_annotation.csv")
    for index, row in data_annotations.iterrows():
        if row['selected'] == 1:
            plt.annotate(row['name'], xy=(row['x'], row['y']),
                         xytext=(row['x'] + row['shift_x'], row['y'] + row['shift_y']),
                         arrowprops=dict(arrowstyle="simple", facecolor='tab:brown'),
                         horizontalalignment="left",
                         verticalalignment='top',
                         fontsize=14)


def find_probabilities_for_a_name(fname, lname):
    file_name = "../../Data/FinalDataSet_Combos/FLGAtrain_NCtest/NCtest_FLGAtrain_s.csv"
    columns = ['first_name', 'last_name', 'indis',
               'white_black_indis_fn', 'white_hispa_indis_fn', 'white_asian_indis_fn',
               'white_black_indis_ln', 'white_hispa_indis_ln', 'white_asian_indis_ln',
               'black_asian_indis_ln', 'black_hispa_indis_ln', 'asian_hispa_indis_ln',
               'black_asian_indis_fn', 'black_hispa_indis_fn', 'asian_hispa_indis_fn',
               "pop_ln_asian", "pop_ln_hispa", "pop_ln_black", "pop_ln_white",
               "pop_fn_asian", "pop_fn_hispa", "pop_fn_black", "pop_fn_white",
               ]
    data = pd.read_csv(file_name, usecols=columns)
    data = data[data.first_name == fname]
    data = data[data.last_name == lname]
    for col in columns:
        print(col)
        print(data[col])
