import sklearn
from sklearn.neural_network import MLPClassifier
from sklearn.neural_network import MLPRegressor
from sklearn import datasets, linear_model

import cPickle
import sys


"""Stock Analysis Group
Jack Kraszewski
Christopher Hittner
Steph Oro
"""

"""
This is the start of a script to recieive the data 
from the data gathering group on the server and to
process the data and return whatever values the user 
is looking for.
"""
# The set of strings used to predict emotions
tokenStrings = []

def checkSentimentData(data):
    """
    Used inside the getSentimentData function to ensure that the 
    data has been provided in the correct format -> to be determined
    returns a boolean type to tell if its valid

    data - The data that needs to be verified.

    return - A boolean stating whether or not the data was verified.
    """
    if "overall_sentiment" not in data.keys():
        return False
    elif "noun_phrases" not in data.keys():
        return False
    elif not isinstance(data['overall_sentiment'], (int, float, long)):
        return False
    else:
        return not isinstance(data['noun_phrases'], basestring)


def checkStockData(data):
    """
    Used inside the getStockData function to ensure that the 
    data has been provided in the correct format -> to be determined
    returns a boolean type to tell if its valid

    data - The data that needs to be verified.

    return - A boolean stating whether or not the data was verified.
    """
    
    for x in range (0, len(data)):
        checks = 'Volume' in data[x]
        checks &= 'High' in data[x]
        checks &= 'Low' in data[x]
        checks &= 'Date' in data[x]
        checks &= 'Close' in data[x]
        checks &= 'Symbol' in data[x]
        checks &= 'Open' in data[x]
        checks &= 'Adj_Close' in data[x]
        if not checks:
            break
    if checks:
        return True
    else:
        return False

def getSentimentData():
    """
    Receives the sentiment data from the Twitter data analysis group through the server.

    return - The received sentiment data.
    """
    sentData = json.loads(flask.request.data)
    if not checkSentimentData(sentData):
        print("getSentimentData(): Provided sentiment data was invalid!");
        return None

    return sentData
        
    

def getStockData():
    """
    Receives the stock data from the stock data gathering group through the server.

    return - The received stock data.
    """
    stkData = json.loads(flask.request.data)
    if not checkStockData(stkData):
        print("getStockData(): Provided stock data was invalid!");
        return None
    
    return sentData

def computeStkCorrelation(sentData):
    """
    Based on the user request from the server, computes the correlation in data.

    precondition - checkSentimentData(sentData) returns True

    return - A classifier that predicts stock change given sentiment data.
    """

    # Load the classifier
    clf = loadClassifier("stockclassifier.pkl")

    # Build the input vector 
    vec = []
    for i in range(len(tokenStrings)):
        # If the string is found, make a vector from the sentiment level
        if tokenStrings[i] in sentData['noun_phrases']:
            vec.append(sentData['overall_sentiment'])
        else
            vec.append(0)

    return makePrediction(clf, vec)


def formatData(data):
    """
    Formats the data to be sent to the server.

    data - The data that will be sent to the server.
    """
    retData = { "Stock":"DJI", "Change":data}
    return JSON.stringify(retData)

def trainOn(X, Y):
    """Creates a classifier based on the desired type and data
    X - The input data
    Y - The output data
    precondition - len(X) == len(Y)
    """
    # Make the classifier
    clf = MLPRegressor(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(15,), random_state=1)

    # Fit the classifier to the data
    clf.fit(X, Y)

    return clf


def makePrediction(clf, vec):
    """Makes a prediction about a vector given a classifier.
    clf - The classifier to test the vector against.
    vec - The vector to test with.
    """
    return clf.predict([vec])[0]


def saveClassifier(filename, clf):
    """Saves a classifier to a file.
    filename - The file to store the classifier in
    clf      - The classifier to store
    """
    with open(filename, 'wb') as fid:
        cPickle.dump(clf, fid)

def loadClassifier(filename):
    """Loads a classifier from a file
    filename - The file to read
    """
    with open(filename, 'rb') as fid:
        return cPickle.load(fid)

if __name__ == "__main__":
    stkData = getStockData();
    sentData = getSentimentData();
    clf = computeStkCorrelation(sentData, stkData);
    info = formatData(clf);
    #sendData(info);
    
