<head>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Didact+Gothic&family=Paytone+One&family=Play:wght@400;700&family=Reddit+Sans:ital,wght@0,200..900;1,200..900&display=swap" rel="stylesheet">
    <link href="style.css" rel="stylesheet">
</head>
<style>
    div.body {
        width: 100%;
        color: white;
        margin: 0;
        font-family: "Reddit Sans", sans-serif;
    }
    h2 {
        font-family: "Play", sans-serif;
        font-size: 30px;
    }
    h3 {
        font-size: 20px;
    }
    span {
        font-style: italic;
        color: aquamarine;
        font-weight: 200;
        word-spacing: 10px;
    }

</style>

<div class="body">
<div style="display:flex;">
    <div>
        <img src="./static/logomark.png" height="100px" width="100px" alt="Logo">
    </div>
    <h1> Machine Learning Web Application - Churn Prediction</h1>
</div>
created by: Dalton R. Burton<br>
<a href="https://www.youtube.com/watch?v=mqi83kE17mY">Youtube Demo Here</a>

<h2> What is a churn predictor?</h2>

<img src="./static/readme_images/journey.jpg" alt="Customer Churn Diagram"><br>

Churn Predictor is a web application that can accurately process a dataset of customers and output the probability of a customer exiting. It's main goal is to assist those whose duty it is to ensure customer retention to identify these members and carry out thorough investigation and implement strategies and solutions to prevent churn.

<h2>Application Architecture </h2>

The model is built on classification algorithms such as XGBoost, LightGBM and CatBoost, constructed using flask and Django as the framework and trained using a synthetic dataset of customers sourced from kaggle.com.

<h3>Built With</h3>

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![django](https://img.shields.io/badge/Django-20232A?style=for-the-badge&logo=django&logoColor=white)
![html](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![css](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![Numpy](https://img.shields.io/badge/Numpy-blue?style=for-the-badge&logo=numpy&logoColor=white)
![pandas](https://img.shields.io/badge/Pandas-green?style=for-the-badge&logo=pandas&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-blue?style=for-the-badge&logo=flask&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit%20learn-orange?style=for-the-badge&logo=scikit-learn&logoColor=blue)
![sqlite](https://img.shields.io/badge/SQLite-white?style=for-the-badge&logo=sqlite&logoColor=blue)


<h2>Project Files</h2>

<h3>Main file - <span>app.py</span></h3>



This file houses the core functionality of the web application. It uses flask to render the html files and pass processed data from the backend to the frontend and vice versa. It also calls the functions to create and update the database, train the machine learning model, clean datasets and predict churn probability. When run from main, an updated model is trained based on the provided dataset.

<h3>The Model - <span>Preprocessor.py, predict.py, TrainModel.py</span></h3>

The Modelling process follows that of the data science methodology.
* The data is sourced and then processed by <b>Preprocessor.py</b>, which removes missing data or features that are not necessary to train the model. It then stores the cleaned dataset for training the model.
* <b>TrainModel.py</b> loads the processed data set and then builds a predictive model by averaging the results of three machine learning algorithms, XGBoost, LightGBM and CatBoost classifier and stores the model.
* <b>predict.py</b> takes the input from the user, processes it by calling a function from the preprocessor, and finally uses the saved model to make a prediction on the input. It then returns the results in the form of a flash message for a single input, or an added column if a dataset was uploaded.

<h3>Helpers - <span>helpers.py, config.py, errors.py</span></h3>

* helpers.py
* config.py
* errors.py

Helpers contain paths, classes and security functions and error messages to help reduce the clutter in the main files.

<h3>Database - <span>database.db</span></h3>

Database.db is the database of users that access the web application. The database uses the user's username as the key values and stores a hashed value generated from the users password.


<h3>Templates</h3>
<h3><span>
layout.html
index.html
landing.html
register.html
login.html
about.html
apology.html
</span></h3>

These are the list of html files used to build the web app.<br> <b>- layout.html</b> contains the main structure of the web application such as the head, the main navigation and footer. These elements are displayed on all other web pages.<br>
<b>- landing.html</b> acts as the home page for visitors, where they can register or login for further usage.<br>
<b>- register and login.html</b> gives a user access to the core functionality of the churn preditor application.
<b>- index.html</b> is the homepage once a user has logged in. from here, the user has the ability to either upload a dataset in the form of a csv, or manually enter an individual users data for prediction.
<b>- about.html</b> provides a simple breakdown tutorial on how to use the application.
<b>- apology.html</b> renders various error messages based on user error or missing data.

<h3>Static - <span>Images styles.css</span></h3>

This is where images used in the web app are stored as well as the applications stylesheet.

<h3>Predictive Model - <span>model.pkl</span></h3>

The trained model is stored into a folder called model as a '.pkl' file. each time the application is run from main, the model is retrained. this allows the model to be updated if a new dataset is sourced.

<h3>Model Data</h3>

The model data is a synthetic dataset of bank customers and churn status. The original dataset called <b>'Churn_Modelling'</b> was uploaded and stored in the data folder.<br>
When the preprocessor is called, it loads this dataset and proceeds to clean it and stores the newly cleaned dataset in the data folder as <b>'cleaned.csv'</b>.<br>
Also, when a user uploads a dataset, said dataset is stored as <b>'uploaded.csv'</b> and then processed and the clean version stored as <b>'uploaded_results.csv'</b>.

<h3>Notes - <span>README.md requirements.txt</span></h3>

The <b>README.md</b> file contains important information about web application, it's usage and functionality. <b>requirements.txt</b> is a text file of the important files necessary for installing and successfuly running the web application.

<h2>Design Challenges</h2>
<div>
    <div>
    One of the key design challenge was the functionality  of the application. Initially, the application was designed to only take a single customer data as input. While this would have been good, it would not have been practical for institutions or business to utilize, hence the decision to offer multiple functions. users would be able to do single inquires as well as mass inquires on the entirety or subsets of customers.
    </div>
    <div>
        <h3>CSV upload</h3>
        <img src="./static/readme_images/Dataset.png">
        <h3 style="text-align:right;">Manual Customer Entry</h3>
        <img src="./static/readme_images/Individual data.png">
    </div>
</div>
<h2>Screenshots</h2>
    <h3>Landing Page</h3>
    <img src="./static/readme_images/landing.png">
    <h3 style="text-align:right;">Registration Page</h3>
    <img src="./static/readme_images/register.png">
    <h3>Login Page</h3>
    <img src="./static/readme_images/Login.png">
    <h3 style="text-align:right;">About Page</h3>
    <img src="./static/readme_images/about.png">
</div>

