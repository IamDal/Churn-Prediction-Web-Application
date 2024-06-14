import config
import os
import pickle
import errors as er
import pandas as pd
import Preprocessor as Preprocessor
# Load Classifiers
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.model_selection import train_test_split

# Load Preprocessing Libraries
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder

# Import accuracy metrics
from sklearn.metrics import accuracy_score
from sklearn.metrics import roc_auc_score

# Import pipeline and preprocessing imputers and encoders
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer

# run the training process


def train():
    df = read_df()
    print(f'Model training initiated.\n\n')
    Xtrain, Xtest, Ytrain, Ytest = split_data(df)
    print(f'Data split @80% train & 20% validate.\n\n')
    preprocessor = create_pipeline(df)
    print(f'Pipeline created.\n\n')
    results = train_model(Xtrain, Xtest, Ytrain, Ytest, preprocessor)
    voting_model, score, accuracy = train_voting_classifier(Xtrain, Xtest, Ytrain, Ytest, results).values()
    print(f'*** Model Successfully trained. Training score: {score}.***\n\n ')
    print(f'*** Accuracy : {accuracy}. ***\n\n')
    print(f'Saving model, please wait...\n\n')
    save_model(voting_model)
    print(f'Model successfully saved at: {config.SAVE_MODEL}\n')

# Loads the cleaned csv file


def read_df():
    try:
        if not os.path.exists(config.CLEANED_CSV_PATH):
            raise FileExistsError(er.error_1)
    except Exception as e:
        print(e)
        Preprocessor.clean_data(config.CSV_PATH)
    return pd.read_csv(config.CLEANED_CSV_PATH)

# Splits the dataframe


def split_data(df):
    X = df.drop('Exited', axis=1)
    y = df['Exited']
    return train_test_split(X, y, test_size=.2, random_state=42)

# Creates Pipeline to clean and train models


def create_pipeline(df):
    X = df.drop('Exited', axis=1)
    num = X.select_dtypes(include=['int64', 'float64']).columns
    col = X.select_dtypes(include=['object']).columns

    # Preprocessing for numerical data: imputation and scaling
    numerical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', MinMaxScaler())])

    # Preprocessing for categorical data: imputation and one-hot encoding
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numerical_transformer, num),
            ('cat', categorical_transformer, col)])
    return preprocessor


def fit(Xtrain, Xtest, Ytrain, Ytest, model):
    name = type(model.named_steps['model']).__name__
    print(f'Fitting to {name} to data.\n\n')
    model.fit(Xtrain, Ytrain)
    predictions = model.predict_proba(Xtest)[:, 1]
    auc_roc = roc_auc_score(Ytest, predictions)
    return {'model_name': name, 'score': auc_roc, 'model': model}


# Train the model
def train_model(Xtrain, Xtest, Ytrain, Ytest, preprocessor):
    # Set hyperparameters for XGBClassifier
    XGB = XGBClassifier(**{'n_estimators': 810, 'learning_rate': 0.07921079869615913, 'max_depth': 5,
                           'min_child_weight': 8, 'gamma': 0.27423983829634263, 'random_state': 42, 'objective': 'binary:logistic',
                           'eval_metric': 'auc', 'n_jobs': -1})

    # Set hyperparameters for CatBoostClassifier
    CATB = CatBoostClassifier(**{'iterations': 830, 'learning_rate': 0.08238714339235984, 'depth': 5,
                                 'l2_leaf_reg': 0.8106903985997884, 'random_state': 42, 'verbose': 0})

    # Set hyperparameters for LGBMClassifier
    LGBM = LGBMClassifier(**{'n_estimators': 960, 'learning_rate': 0.031725771326186744, 'max_depth': 8, 'min_child_samples': 8, 'force_row_wise': True,
                             'subsample': 0.7458307885861184, 'num_leaves': 10, 'colsample_bytree': 0.5111460378911089, 'random_state': 42})

    # Create pipelines
    XGB_best = Pipeline(steps=[('preprocessor', preprocessor), ('model', XGB)])
    CAT_best = Pipeline(steps=[('preprocessor', preprocessor), ('model', CATB)])
    LGBM_best = Pipeline(steps=[('preprocessor', preprocessor), ('model', LGBM)])

    XGB_results = fit(Xtrain, Xtest, Ytrain, Ytest, XGB_best)
    LGBM_results = fit(Xtrain, Xtest, Ytrain, Ytest, LGBM_best)
    CAT_results = fit(Xtrain, Xtest, Ytrain, Ytest, CAT_best)

    return [LGBM_results, XGB_results, CAT_results]


def train_voting_classifier(Xtrain, Xtest, Ytrain, Ytest, models):
    # Create a VotingClassifier with the three XGBoost models
    voting = VotingClassifier(estimators=[
        ('Model1', models[0]['model']),
        ('Model2', models[1]['model']),
        ('Model3', models[2]['model'])
    ], voting='soft', weights=[0.5, 0.3, 0.2], flatten_transform=True)

    voting.fit(Xtrain, Ytrain)
    predictions = voting.predict_proba(Xtest)[:, 1]
    predict = voting.predict(Xtest)

    auc_roc = roc_auc_score(Ytest, predictions)
    acuu = accuracy_score(Ytest, predict)
    return {'model': voting, 'auc_roc_score': auc_roc, 'accuracy': acuu}

# Save final Model


def save_model(voting):
    with open(config.SAVE_MODEL, 'wb') as f:
        pickle.dump(voting, f)
    print('Model saved successfully!')


def load_model():
    with open(config.SAVE_MODEL, 'rb') as f:
        return pickle.load(f)
