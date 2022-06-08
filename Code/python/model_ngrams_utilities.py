import pandas as pd
import numpy as np
import fuzzy
import unicodedata
from pyphonetics import Soundex
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import MultiLabelBinarizer


def create_term_document_matrix_df_full(docs, dmp=False):
    vectorizer = CountVectorizer(analyzer='char', ngram_range=(2, 4))
    x = vectorizer.fit_transform(docs)
    df = pd.DataFrame(x.toarray(), columns=vectorizer.get_feature_names())
    if dmp:
        df = df.add_suffix('_dmp')
    print("Created n-grams Vector")
    return df


def get_FL_names_list():
    file_name = "../../Data/NameRaceData/FL.csv"
    data = pd.read_csv(file_name, usecols=['first_name', 'last_name', 'race'])
    data = data.dropna(subset=['first_name'])
    data = data.dropna(subset=['last_name'])
    data = data.dropna(subset=['race'])
    data = data.sample(n=200000, random_state=2)
    data.reset_index(drop=True, inplace=True)
    return data


def get_NC_names_list():
    file_name = "../../Data/NameRaceData/NC.csv"
    data = pd.read_csv(file_name, usecols=['first_name', 'last_name', 'race'])
    data = data.dropna(subset=['first_name'])
    data = data.dropna(subset=['last_name'])
    data = data.dropna(subset=['race'])
    data = data.sample(n=200000, random_state=2)
    data.reset_index(drop=True, inplace=True)
    return data


def create_feature_space(data, lambda_label, train=True):
    print("Starting to create feature space ...")
    feature_space = create_feature_space_util(data, lambda_label, train=train)
    X = feature_space
    print("Feature Space Shape: ", X.shape)
    y = data['race'].astype('category')
    print("Races: ", dict(enumerate(y.cat.categories)))
    y = y.cat.codes
    y.reset_index(drop=True, inplace=True)
    y_onehot = pd.get_dummies(y)
    print("y_onehot shape = ", y_onehot.shape)
    print("y_onehot columns = ", y_onehot.columns)
    return X, y_onehot, data, y


def create_feature_space_util(data, lambda_label, train=True):
    feature_space = create_non_ascii_features(data)
    data['n_first_name'] = data['first_name'].apply(normalise_names)
    data['n_last_name'] = data['last_name'].apply(normalise_names)
    data = data.assign(combined_name='$' + data.n_first_name + '$ +' + data.n_last_name + '+')
    docs_1 = np.array(data['combined_name'].values.tolist())
    print("Starting to create Document Term Matrix ...")
    document_term_matrix_1 = create_term_document_matrix_df_full(docs_1)
    feature_space = feature_space.join(document_term_matrix_1)
    del [document_term_matrix_1]
    print("Created Document Term Matrix")
    data['dmp_first_name'] = data['n_first_name'].apply(double_metaphone)
    data['dmp_last_name'] = data['n_last_name'].apply(double_metaphone)
    data = data.assign(dmp_combined_name='$' + data.dmp_first_name + '$ +' + data.dmp_last_name + '+')
    docs_2 = np.array(data['dmp_combined_name'].values.tolist())
    print("Starting to create Document Term Matrix ...")
    document_term_matrix_2 = create_term_document_matrix_df_full(docs_2, dmp=True)
    print("Created Document Term Matrix")
    feature_space = feature_space.join(document_term_matrix_2)
    del [document_term_matrix_2]
    print("Starting to create Soundex Features ...")
    soundex_features = create_soundex_features(data)
    print("Created Soundex Features")
    feature_space = feature_space.join(soundex_features)
    del [soundex_features]
    if train:
        with open('../../Results/train_features_' + str(lambda_label) + '.txt', 'w') as f:
            for item in feature_space.columns:
                f.write("%s\n" % item)
    else:
        with open('../../Results/train_features_' + str(lambda_label) + '.txt', 'r') as fp:
            train_features = fp.readlines()
        train_features = [e.rstrip('\n') for e in train_features]
        print("Start deleting extra features")
        to_delete = set(feature_space.columns) - set(train_features)
        print(len(to_delete))
        feature_space.drop(columns=list(to_delete), axis=1, inplace=True)
        print("Extra features deleted")
        print("Start adding extra features")
        to_add = set(train_features) - set(feature_space.columns)
        print(len(to_add))
        feature_space = pd.concat(
            [feature_space, pd.DataFrame([[0] * len(to_add)], index=feature_space.index, columns=list(to_add))], axis=1
        )
        print("Extra features added")
    return feature_space


def normalise_names(name):
    return str(unicodedata.normalize('NFKD', name).encode("ascii", "ignore"), 'utf-8')


def create_soundex_features(data):
    data['soundex_first_name'] = data['n_first_name'].apply(soundex_feature)
    data['soundex_last_name'] = data['n_last_name'].apply(soundex_feature)
    soundex_features = data[['soundex_first_name', 'soundex_last_name']]
    soundex_features = pd.get_dummies(soundex_features.stack()).max(level=0)
    soundex_features = soundex_features.add_suffix('_soundex')
    return soundex_features


def create_non_ascii_features(data):
    data = data.assign(full_name=data.first_name + data.last_name)
    data['non_ascii_chars'] = data['full_name'].apply(get_nonascii_chars)
    mlb = MultiLabelBinarizer()
    non_ascii_features = pd.DataFrame(mlb.fit_transform(data['non_ascii_chars']), columns=mlb.classes_,
                                      index=data.index)
    return non_ascii_features


def soundex_feature(name):
    soundex = Soundex()
    name = ''.join([i if ord(i) < 128 else '' for i in name])
    if name == '' or name.startswith('*'):
        return ''
    return soundex.phonetics(name)


def double_metaphone(name):
    dmeta = fuzzy.DMetaphone()
    dmp = dmeta(name)[0]
    if isinstance(dmp, (bytes, bytearray)):
        return str(dmp, 'utf-8')
    return ""


def get_nonascii_chars(name):
    return [c for c in str(name) if ord(c) >= 128]


########################################################################################################

def find_pos_weights(y_train):
    pos_weights = []
    for race_class in range(4):
        label = y_train.iloc[:, race_class]
        negative_label_count = label.count() - label.sum()  # count - sum
        print("Negative count: ", negative_label_count)
        positive_label_count = label.sum()  # sum
        print("Positive count: ", positive_label_count)
        pos_weight = negative_label_count / positive_label_count
        pos_weights.append(pos_weight)
    return pos_weights

########################################################################################################
