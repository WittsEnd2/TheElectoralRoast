"""
@package sentiment
Twitter sentiment analysis.

This code performs sentiment analysis on Tweets.

A custom feature extractor looks for key words and emoticons.  These are fed in
to a naive Bayes classifier to assign a label of 'positive', 'negative', or
'neutral'.  Optionally, a principle components transform (PCT) is used to lessen
the influence of covariant features.

"""
from firebase import firebase
import csv, random
import nltk
import tweet_features, tweet_pca
import time
from urllib.parse import quote
import json

# read all tweets and labels
fp = open( 'TrainingSet.txt', 'rt' )
reader = csv.reader( fp, delimiter='\t', quotechar='"', escapechar='\\' )
tweets = []
print(reader)
for row in reader:
    tweets.append( [row[1], row[0]] );
    print(row[1])
print(tweets[0:50])

# treat neutral and irrelevant the same
for t in tweets:
    print(t[0])
    if t[0] == 'irrelevant':
        t[0] = 'neutral'


# split in to training and test sets
random.shuffle( tweets );

fvecs = [(tweet_features.make_tweet_dict(s),t) for (t,s) in tweets]
v_train = fvecs[:375]
v_test  = fvecs[375:]
#print(str(v_train))
#print(str(v_test))
for i in range(0, 20):
    print(fvecs[i])

# dump tweets which our feature selector found nothing
tot = 0;
for i in range(0,len(tweets)):
    if tweet_features.is_zero_dict( fvecs[i][0] ):
        #print(tweets[i][1] + ': ' + tweets[i][0])
        tot = tot + 1
print(tot)

# apply PCA reduction
#(v_train, v_test) = \
#        tweet_pca.tweet_pca_reduce( v_train, v_test, output_dim=1.0 )


# train classifier
classifier = nltk.NaiveBayesClassifier.train(v_train);
#classifier = nltk.classify.maxent.train_maxent_classifier_with_gis(v_train);


# classify and dump results for interpretation
print("\nAccuracy " + str(nltk.classify.accuracy(classifier, v_test)) +"\n" )#% nltk.classify.accuracy(classifier, v_test)
#print classifier.show_most_informative_features(200)


# build confusion matrix over test set
test_truth   = [s for (t,s) in v_test]
test_predict = [classifier.classify(t) for (t,s) in v_test]

cruz = open("cruz.txt", "r")
bernie = open("bernie.txt", "r")
clinton = open("clinton.txt", "r")
trump = open("trump.txt", "r")
rubio = open("rubio.txt", "r")

db = firebase.FirebaseApplication("https://glowing-inferno-6337.firebaseio.com/Tweets")

while 1:
    whereCruz = cruz.tell()
    whereBernie = bernie.tell()
    whereClinton = clinton.tell()
    whereTrump = trump.tell()
    whereRubio = rubio.tell()
    lineCruz = cruz.readline()
    lineBernie = bernie.readline()
    lineClinton = clinton.readline()
    lineTrump = trump.readline()
    lineRubio = rubio.readline()
    if lineCruz != None and len(lineCruz) != 0:
        print(lineCruz)
        decoded = json.loads(str(lineCruz))
        data = {}
        cruzTest = tweet_features.make_tweet_dict(decoded["tweet"])
        data["attitude"] = str(classifier.classify(cruzTest))
        data["lat"] = decoded["coordinates"][0]
        data["long"] = decoded["coordinates"][1]
        data["tweet"] = decoded["tweet"]
        data["who"] = "cruz"
        print("Hei, man please I tried")
        db.post('/Cruz', data)
        #db.put('/Tweets', quote(str(data)), None)  
    elif lineBernie != None and len(lineBernie) != 0:
        print(lineBernie)
        decoded = json.loads(str(lineBernie))
        data = {}
        bernieTest = tweet_features.make_tweet_dict(decoded["tweet"])
        data["attitude"] = str(classifier.classify(bernieTest))
        data["lat"] = decoded["coordinates"][0]
        data["long"] = decoded["coordinates"][1]
        data["tweet"] = decoded["tweet"]
        data["who"] = "bernie"
        print("Hei, man please I tried")
        db.post('/Bernie', data)#, None)
        #db.put('/Tweets', quote(str(data)), None)  
    elif lineClinton != None and len(lineClinton) != 0:
        print(lineClinton)
        decoded = json.loads(str(lineClinton))
        data = {}
        clintonTest = tweet_features.make_tweet_dict(decoded["tweet"])
        data["attitude"] = str(classifier.classify(clintonTest))
        data["lat"] = decoded["coordinates"][0]
        data["long"] = decoded["coordinates"][1]
        data["tweet"] = decoded["tweet"]
        data["who"] = "clinton"
        print("Hei, man please I tried")
        db.post('/Clinton', data)#, None)
        #db.put('/Tweets', quote(str(data)), None)  
    elif lineTrump != None and len(lineTrump) != 0:
        print(lineTrump)
        decoded = json.loads(str(lineTrump))
        data = {}
        trumpTest = tweet_features.make_tweet_dict(decoded["tweet"])
        data["attitude"] = str(classifier.classify(trumpTest))
        data["lat"] = decoded["coordinates"][0]
        data["long"] = decoded["coordinates"][1]
        data["tweet"] = decoded["tweet"]
        data["who"] = "trump"
        print("Hei, man please I tried")
        db.post('/Trump', data)#), None)
        #db.put('/Tweets', quote(str(data)), None)
    elif lineRubio != None and len(lineRubio) != 0:
        print(lineRubio)
        decoded = json.loads(str(lineRubio))
        data = {}
        rubioTest = tweet_features.make_tweet_dict(decoded["tweet"])
        data["attitude"] = str(classifier.classify(rubioTest))
        data["lat"] = decoded["coordinates"][0]
        data["long"] = decoded["coordinates"][1]
        data["tweet"] = decoded["tweet"]
        data["who"] = "rubio"
        print("Hei, man please I tried")
        db.post('/Rubio', data)#, None)
    else:
        time.sleep(1)
        cruz.seek(whereCruz)
        bernie.seek(whereBernie)
        clinton.seek(whereClinton)
        trump.seek(whereTrump)
        rubio.seek(whereRubio)
#print('Confusion Matrix')
#print (str(nltk.ConfusionMatrix( test_truth, test_predict )))

