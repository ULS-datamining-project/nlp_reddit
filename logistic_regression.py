# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 13:51:36 2023

@author: Sebastian
"""

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

from statsmodels.formula.api import logit

sentiment_data = pd.read_csv("data/reddit_data_sentiment.csv")

with pd.option_context('display.max_rows', 20,
                       'display.max_columns', None,
                       'display.precision', 3,
                       ):
    print(sentiment_data)

def sentiment2int(sentiment):
    if sentiment == "NEGATIVE":
        return(False)
    if sentiment == "POSITIVE":
        return(True)


def nature2int(nature):
    if nature == "Unhealthy":
        return(False)
    if nature == "Neutral":
        return(False)
    if nature == "Healthy":
        return(True)

X = sentiment_data.loc[:, ("upvote_ratio", "is_self", "label")]
#Change sentiments to logical
X["title_is_positive"] = [sentiment2int(sentiment) for sentiment in X["label"]]
X.drop("label", axis = 1, inplace = True)

Y = pd.Series([nature2int(nature) for nature in sentiment_data.loc[:, "nature"]], name = "nature")

# Split into training and validation sets
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=2023)


base_lr = LogisticRegression(solver='liblinear') #liblinear dumps everything in one category

model = base_lr.fit(X_train, Y_train)

#Oh, all positive
confusion_matrix(Y_train, model.predict(X_train))

# Let's double check
any(model.predict(X_train))

#Oh, well that's kind of disappointing. If you declare everything as unhealthy then the model works well. Some model, huh?

model.predict(X_test)
any(model.predict(X_test))


#I'd really like a p-value to demonstrate the lack of relationship, but scikit learn isn't statistical software
# So I guess we're going to have to use something more statistical:
        

logit_data = pd.concat([Y_train, X_train], axis = 1)

# Convert bools to int so statsmodels can process it
logit_data["nature"] = logit_data.nature.apply(int)
logit_data["is_self"] = logit_data.is_self.apply(int)
logit_data["title_is_positive"] = logit_data.title_is_positive.apply(int)

logit_model = logit("nature ~ upvote_ratio + is_self + title_is_positive", logit_data)
#logit_model = sm.Logit(np.array(Y_train),X_train)

result = logit_model.fit()
result.pred_table()
print(result.summary())

# This is perplexing. We clearly have a model where everything plays a role - 
# but they all cancel each other out to result in always predicting False
# Bizarre