import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Importing the dataset

dataset = pd.read_csv('Crop_recommendation.csv')
X = dataset.iloc[:, :-1].values
y = dataset.iloc[:, -1].values

from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
y = le.fit_transform(y)

# Splitting the dataset into the Training set and Test set

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 0)

print(X_train)

print(y_train)

print(X_test)

print(y_test)

# Feature Scaling

from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

print(X_train)

print(X_test)

# Training the Naive Bayes Classification model on the Training set

from sklearn.naive_bayes import GaussianNB
classifier = GaussianNB()
classifier.fit(X_train, y_train)

# Predicting the Test set results

y_pred = classifier.predict(X_test)
print(np.concatenate((y_pred.reshape(len(y_pred),1), y_test.reshape(len(y_test),1)),1))

# Making the Confusion Matrix

from sklearn.metrics import confusion_matrix, accuracy_score,precision_score,recall_score
cm = confusion_matrix(y_test, y_pred)
pr=precision_score(y_test, y_pred,average='micro')
re=recall_score(y_test, y_pred,average='micro')
print(cm)
accuracy_score(y_test, y_pred)
print(pr)
print(re)

from sklearn.model_selection import GridSearchCV
param_grid = {
    'var_smoothing': [1e-9, 1e-8, 1e-7, 1e-6],
}

# Perform Grid Search
grid_search = GridSearchCV(classifier, param_grid, cv=5, scoring='accuracy', n_jobs=-1)
grid_search.fit(X_train, y_train)

# Best parameters and score
print("Best Parameters:", grid_search.best_params_)
print("Best Score:", grid_search.best_score_)



from sklearn.pipeline import Pipeline
pipeline = Pipeline([
    ('std',sc),
    ('classifier', classifier),
])

import joblib
joblib.dump(pipeline, 'model_nb.pkl')
joblib.dump(le, 'label_encoder.pkl')
