"""
model.py is responsible for training the model and making predictions
"""

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import numpy as np

from database import Database
from stats import statCEO

db = Database()
stats = statCEO()
stats.addPerformances(db.getGames(700, 1326))

df = pd.DataFrame(stats.getStats(), columns=stats.getStatNames())

X = df.drop("Win", axis=1)
y = df["Win"]

pca = PCA()
pca.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

forest = RandomForestClassifier(n_estimators=100)
forest.fit(X_train, y_train)
print(forest.score(X_test, y_test))

# logReg = LogisticRegression()
# logReg.fit(X_train, y_train)
# print(logReg.score(X_test, y_test))

forestAcc = []
logRegAcc = []
for i in range(100):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    forest = RandomForestClassifier(n_estimators=100)
    forest.fit(X_train, y_train)
    forestAcc.append(forest.score(X_test, y_test))
    print(forest.score(X_test, y_test))

    # logReg = LogisticRegression()
    # logReg.fit(X_train, y_train)
    # logRegAcc.append(logReg.score(X_test, y_test))

plt.hist(forestAcc)
plt.xticks(np.arange(.65, 1, .01))
plt.title("Random Forest Accuracy")
plt.show()

# plt.hist(logRegAcc)
# plt.xticks(np.arange(.65, 1, .01))
# plt.title("Logistic Regression Accuracy")
# plt.show()