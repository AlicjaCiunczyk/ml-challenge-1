## installing libraries
import numpy as np
import os
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# fix random seed for reproducibility
seed = 7
np.random.seed(seed)

## loading the data
written_tr = np.load("written_train.npy", allow_pickle=True)
written_te = np.load("written_test.npy", allow_pickle=True)
spoken_tr = np.load("spoken_train.npy", allow_pickle=True)
spoken_te = np.load("spoken_test.npy", allow_pickle=True)
match_tr = np.load("match_train.npy", allow_pickle=True)


# subsetting the data to get some test set
written_test = written_tr[:4000,:]
written_train = written_tr[4000:,:]
spoken_test = spoken_tr[:4000]
spoken_train = spoken_tr[4000:]
match_test = match_tr[:4000] 
match_train = match_tr[4000:]


# fucntion to determine how many true/false values are in target
def true_false(y):
    unique,counts=np.unique(y,return_counts=True)
    return dict(zip(unique,counts))

## Feature engineering ##

def spoken_features(data,functions):
    features=[]
    for example in data:
        feat=np.concatenate([fun(example,axis=0) for fun in functions])
        features.append(feat)
    return np.array(features)

#feature engineering on spoken
def feat_eng_spoken(spoken,summaries):
    X_s=spoken_features(spoken,summaries)
    #lengths of spoken
    lens=np.array([example.shape[0] for example in spoken])
    lens=lens.reshape(lens.shape[0],1)
    #concatenate all the parts
    X=np.concatenate((X_s,lens),axis=1)
    #standardise
    from sklearn.preprocessing import StandardScaler
    X_scaled = StandardScaler().fit_transform(X)
    return X_scaled

#define functions to be applied to spoken data
summaries=[np.mean, np.max, np.min, np.std, np.median, np.sum, np.argmin, np.argmax]


# Preparing training data
written_train=written_train.astype('float32')
#normalise written
written_train/=255

#apply functions on sproken
spoken_train_m=feat_eng_spoken(spoken_train,summaries)


# Perparing the data for the prediction
#written
written_test=written_test.astype('float32')
#normalise written
written_test/=255

#apply functions on sproken
spoken_test_m=feat_eng_spoken(spoken_test,summaries)

all_train = np.concatenate((written_train, spoken_train_m), axis = 1)
all_test = np.concatenate((written_test, spoken_test_m), axis = 1)

clf = LogisticRegression(random_state=0, solver='lbfgs')
clf.fit(all_train, match_train)
y_pred = clf.predict(all_test)

accuracy_score(y_pred, match_test)
