"""
Contiene las funciones de machine learning
"""
import json
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectKBest
from sklearn import SVC
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import os
import sys
import numpy as np
dir = os.path.dirname
src_path = dir(dir(os.path.abspath(__file__)))
sys.path.append(src_path)


fullpath = dir(dir(dir(os.path.abspath(__file__)))) + os.sep + 'config' + os.sep + "bd_info.json"
with open(fullpath, "r") as json_file_readed:
    json_readed = json.load(json_file_readed)

def machine_functions(df):
    
    X = np.array(df.iloc[:, :-1])
    y = np.array(df.iloc[:, -1])
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    pipe = Pipeline(steps=[
        ('preproceso', PCA())
    ])

    random_forest_params = {
        'classifier': [RandomForestClassifier()],
        'classifier__n_estimators': [10, 100,],
        'classifier__max_features': [1,2]
    }

    svc_params = {
    'classifier': [SVC()],
    'classifier__kernel':('linear'), 
    'classifier__C':[0.2, 0.3], 
    'classifier__coef0': [-10.,-1.],
    'classifier__gamma': ('auto')
    }
 
    logistic_params = {
    'classifier': [LogisticRegression()],
    
    }

    search_space = [
        random_forest_params,
        svc_params,
        logistic_params
        
    ]

    clf = GridSearchCV(estimator = pipe,
                    param_grid = search_space,
                    cv = 5,
                    verbose=1,
                    n_jobs=-1)

    clf.fit(X_train, y_train)
    return clf.best_estimator_.predict(X)

