# Various file locations are stored here

# Existing csv file
CSV_PATH = './data/Churn_Modelling.csv'

# End user csv upload
UPLOAD_PATH = './data/uploaded.csv'

# End user csv download
RESULTS = './data/uploaded_results.csv'

# Training dataset postprocessed
CLEANED_CSV_PATH = './data/cleaned.csv'

# Unused columns
COLUMNS_TO_REMOVE = ['CustomerId', 'Surname']

FEATURES = ['CustomerId', 'Surname', 'CreditScore', 'Geography', 'Gender', 'Age', 'Tenure',
            'Balance', 'NumOfProducts', 'HasCrCard', 'IsActiveMember', 'EstimatedSalary']
# Continuous Features used to train model
NUMERICAL_COLUMNS = ['Gen_Prod', 'CreditScore', 'Balance', 'NumOfProducts', 'HasCrCard',
                     'Tenure', 'IsActiveMember', 'Active__Prod', 'Age', 'EstimatedSalary',
                     'Generation', 'Gen_Geo', 'Surname_encoded']

# Categorical Features used to train model
CATEGORICAL_COLUMNS = ['GeoGender', 'Geography', 'Gender', 'HasBalance']

# Saved model file path
SAVE_MODEL = './models/model.pkl'

# Saved database file path
DATABASE_PATH = "sqlite:///database.db"

# Secret Key
SECRET_KEY = '\xfc\xaf\x85=\x97\xc2-\xb5\xaa5\xca"\xd13<;'
