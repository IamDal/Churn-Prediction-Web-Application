import os
import pandas as pd
from helpers import apology, ChurnCustomer, Customer
import config
import TrainModel as TrainModel
import Preprocessor as Preprocessor


def Predict(current_customer):
    model = TrainModel.load_model()
    churn_customer = predict_churn(current_customer)
    predictions = model.predict_proba(churn_customer)[:, 1]
    return predictions


def predict_churn(current_customer):
    df = Customer(current_customer)
    df = df.CustomerDataFrame()
    df = Preprocessor.clean_predict_data(df)
    return df


def predict_csv(path_of_upload):
    if os.path.getsize(path_of_upload) == 0:
        return apology("error", 403)
    model = TrainModel.load_model()
    csv_file = Preprocessor.clean_data(path_of_upload)
    original_file = pd.read_csv(path_of_upload)
    original_file['churn'] = model.predict_proba(csv_file)[:, 1]
    original_file.to_csv(config.RESULTS, index=False)


print(os.getcwd())

# Test Scenario below. Uncomment to Run


def test():
    customer0 = [15647311, 'Hill', 608, 'Spain', 'Female', 41, 1, 83807.86, 1, 0, 1, 112542.58, 0]
    customer1 = [15619304, 'Onio', 502, 'France', 'Female', 42, 8, 159660.8, 3, 1, 0, 113931.57, 1]
    customer3 = [15701354, 'Boni', 699, 'France', 'Female', 39, 1, 0, 2, 0, 0, 93826.63, 0]
    customer4 = [15574012, 'Chu', 645, 'Spain', 'Male', 44, 8, 113755.78, 2, 1, 0, 149756.71, 1]
    customer5 = [15656148, 'Obinna', 376, 'Germany', 'Female', 29, 4, 115046.74, 4, 1, 0, 119346.88, 1]

    customer = ChurnCustomer(
        CustomerId=customer1[0],
        Surname=customer1[1],
        CreditScore=customer1[2],
        Geography=customer1[3],
        Gender=customer1[4],
        Age=customer1[5],
        Tenure=customer1[6],
        Balance=customer1[7],
        NumOfProducts=customer1[8],
        HasCrCard=customer1[9],
        IsActiveMember=customer1[10],
        EstimatedSalary=customer1[11])

    pred = Predict(customer)
    print(f'customer {customer.Surname} is {pred}% likely to churn!')

# test()
