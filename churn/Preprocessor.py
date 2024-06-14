import os
# Load helper files
import errors as er
import config
# Load libraries dataframe
import pandas as pd
from sklearn.preprocessing import LabelEncoder


def clean_data(path):
    df = load_data(path)
    # create new features
    df = create_new_features(df)
    drop_columns(df, config.COLUMNS_TO_REMOVE)
    # save new dataframe
    store_cleaned_dataframe(df)
    print(f'Data Cleaning Successful. File Location: {config.CLEANED_CSV_PATH}')
    return df


def clean_predict_data(df):
    # create new features
    df = create_new_features(df)
    # drop unused columns
    drop_columns(df, config.COLUMNS_TO_REMOVE)
    return df


def create_new_features(df):
    encode_names(df)
    group_ages(df)
    create_binary_customer_balance(df)
    combine_geography_gender(df)
    combine_IsActiveMember_NumOfProducts(df)
    combine_Generation_NumOfProducts(df)
    combine_Generation_Geography(df)
    return df


def load_data(path):
    if not os.path.exists(path):
        raise FileNotFoundError(er.error_1)
    return pd.read_csv(path)


def drop_missing_values(df):
    df.dropna(axis=0, inplace=True)
    return df


def encode_names(df):
    # Encode Surnames
    encoder = LabelEncoder()
    df['Surname_encoded'] = encoder.fit_transform(df['Surname'])


def group_ages(df):
    # Group Ages into generations
    age = list(range(30, 81, 10))
    for i, ages in enumerate(age):
        if i == 0:
            condition = df['Age'] < ages
            df.loc[condition, 'Generation'] = i*10
        elif i == len(age)-1:
            condition = df['Age'] > ages
            df.loc[condition, 'Generation'] = i*10
        else:
            condition = (df['Age'] >= ages - 10) & (df['Age'] < ages)
            df.loc[condition, 'Generation'] = i*10


def create_binary_customer_balance(df):
    df['HasBalance'] = 'N'
    df.loc[df['Balance'] > 0, 'HasBalance'] = 'Y'


def combine_geography_gender(df):
    # combine geography and gender
    df["GeoGender"] = df['Geography'] + df['Gender']


def combine_IsActiveMember_NumOfProducts(df):
    # combine active members and number of products
    df['Active__Prod'] = df['NumOfProducts'] * df['IsActiveMember']


def combine_Generation_NumOfProducts(df):
    # Number of product by generation
    df['Gen_Prod'] = df['Generation'] * df['NumOfProducts']


def combine_Generation_Geography(df):
    # Generation combined with geography
    encoder = LabelEncoder()
    df['Gen_Geo'] = encoder.fit_transform(df['Geography'] + df['Generation'].astype(str))


def drop_columns(df, columns):
    df.drop(columns, axis=1, inplace=True)


def store_cleaned_dataframe(df):
    df.to_csv(config.CLEANED_CSV_PATH, index=False)
