import sys
import collections
import sklearn.naive_bayes
import sklearn.linear_model
from sklearn.naive_bayes import BernoulliNB, GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
import nltk
import random
from collections import Counter
random.seed(0)
from gensim.models.doc2vec import LabeledSentence, Doc2Vec, TaggedDocument
#nltk.download("stopwords")          # Download the stop words from nltk


# User input path to the train-pos.txt, train-neg.txt, test-pos.txt, and test-neg.txt datasets
if len(sys.argv) != 3:
    print "python sentiment.py <path_to_data> <0|1>"
    print "0 = NLP, 1 = Doc2Vec"
    exit(1)
path_to_data = sys.argv[1]
method = int(sys.argv[2])


def main():
    train_pos, train_neg, test_pos, test_neg = load_data(path_to_data)
    
    if method == 0:
        train_pos_vec, train_neg_vec, test_pos_vec, test_neg_vec = feature_vecs_NLP(train_pos, train_neg, test_pos, test_neg)
        nb_model, lr_model = build_models_NLP(train_pos_vec, train_neg_vec)
    if method == 1:
        train_pos_vec, train_neg_vec, test_pos_vec, test_neg_vec = feature_vecs_DOC(train_pos, train_neg, test_pos, test_neg)
        nb_model, lr_model = build_models_DOC(train_pos_vec, train_neg_vec)
    print "Naive Bayes"
    print "-----------"
    evaluate_model(nb_model, test_pos_vec, test_neg_vec, True)
    print ""
    print "Logistic Regression"
    print "-------------------"
    evaluate_model(lr_model, test_pos_vec, test_neg_vec, True)


def load_data(path_to_dir):
    """
    Loads the train and test set into four different lists.
    """
    train_pos = []
    train_neg = []
    test_pos = []
    test_neg = []
    with open(path_to_dir+"train-pos.txt", "r") as f:
        for i,line in enumerate(f):
            words = [w.lower() for w in line.strip().split() if len(w)>=3]
            train_pos.append(words)
    with open(path_to_dir+"train-neg.txt", "r") as f:
        for line in f:
            words = [w.lower() for w in line.strip().split() if len(w)>=3]
            train_neg.append(words)
    with open(path_to_dir+"test-pos.txt", "r") as f:
        for line in f:
            words = [w.lower() for w in line.strip().split() if len(w)>=3]
            test_pos.append(words)
    with open(path_to_dir+"test-neg.txt", "r") as f:
        for line in f:
            words = [w.lower() for w in line.strip().split() if len(w)>=3]
            test_neg.append(words)

    return train_pos, train_neg, test_pos, test_neg



def feature_vecs_NLP(train_pos, train_neg, test_pos, test_neg):
    """
    Returns the feature vectors for all text in the train and test datasets.
    """
    # English stopwords from nltk
    stopwords = set(nltk.corpus.stopwords.words('english'))
    stopwords=list(stopwords)
    # Determine a list of words that will be used as features. 
    # This list should have the following properties:
    #   (1) Contains no stop words
    #   (2) Is in at least 1% of the positive texts or 1% of the negative texts
    #   (3) Is in at least twice as many postive texts as negative texts, or vice-versa.
    # YOUR CODE HERE
    features=list()
    pos=dict()
    neg=dict()
    
    def getFlatWordList(train):
        temp_list=[]
        for words in train:
            temp=[]
            for word in words:
                if word not in temp:
                    temp.append(word)
                    temp_list.append(word)
        return temp_list

    pos=Counter(getFlatWordList(train_pos))
    neg=Counter(getFlatWordList(train_neg))

    for key, value in pos.iteritems():
        if(key not in features and key not in stopwords and (value>=len(train_pos)/100 or neg.get(key)>=len(train_neg)/100) and value>=2*neg.get(key)):
            features.append(key)
    
    for key, value in neg.iteritems():
        if(key not in features and key not in stopwords and (value>=len(train_neg)/100 or pos.get(key)>=len(train_pos)/100) and value>=2*pos.get(key)):
            features.append(key)

    count= len(features)
  
    # Using the above words as features, construct binary vectors for each text in the training and test set.
    # These should be python lists containing 0 and 1 integers.
    # YOUR CODE HERE

    train_pos_vec = map(lambda y: map(lambda x: 1 if x in y else 0, features), train_pos)
    train_neg_vec = map(lambda y: map(lambda x: 1 if x in y else 0, features), train_neg)
    test_pos_vec = map(lambda y: map(lambda x: 1 if x in y else 0, features), test_pos)
    test_neg_vec = map(lambda y: map(lambda x: 1 if x in y else 0, features), test_neg)	

    # Return the four feature vectors
    return train_pos_vec, train_neg_vec, test_pos_vec, test_neg_vec



def feature_vecs_DOC(train_pos, train_neg, test_pos, test_neg):
    """
    Returns the feature vectors for all text in the train and test datasets.
    """
    # Doc2Vec requires LabeledSentence objects as input.
    # Turn the datasets from lists of words to lists of LabeledSentence objects.
    # YOUR CODE HERE

    def labelizeReviews(reviews, label_type):
	    labelized = []
	    for i in range(len(reviews)):
	        label = label_type+str(i)
	        labelized.append(LabeledSentence(reviews[i], [label]))
	    return labelized

    labeled_train_pos = labelizeReviews(train_pos, 'train_pos')
    labeled_train_neg = labelizeReviews(train_neg, 'train_neg')
    labeled_test_pos = labelizeReviews(test_pos, 'test_pos')
    labeled_test_neg = labelizeReviews(test_neg, 'test_neg')

    # Initialize model
    model = Doc2Vec(min_count=1, window=10, size=100, sample=1e-4, negative=5, workers=4)
    sentences = labeled_train_pos + labeled_train_neg + labeled_test_pos + labeled_test_neg
    model.build_vocab(sentences)

    # Train the model
    # This may take a bit to run 
    for i in range(5):
        print "Training iteration %d" % (i)
        random.shuffle(sentences)
        model.train(sentences)

    # Use the docvecs function to extract the feature vectors for the training and test data
    # YOUR CODE HERE

    train_pos_vec=[]
    train_neg_vec=[]
    test_pos_vec=[]
    test_neg_vec=[]

    for i in range(len(train_pos)):
    	train_pos_vec.append(model.docvecs['train_pos'+str(i)])

    for i in range(len(train_neg)):
    	train_neg_vec.append(model.docvecs['train_neg'+str(i)])

    for i in range(len(test_pos)):
    	test_pos_vec.append(model.docvecs['test_pos'+str(i)])

    for i in range(len(test_neg)):
    	test_neg_vec.append(model.docvecs['test_neg'+str(i)])

    # Return the four feature vectors
    return train_pos_vec, train_neg_vec, test_pos_vec, test_neg_vec



def build_models_NLP(train_pos_vec, train_neg_vec):
    """
    Returns a BernoulliNB and LosticRegression Model that are fit to the training data.
    """
    Y = ["pos"]*len(train_pos_vec) + ["neg"]*len(train_neg_vec)

    # Use sklearn's BernoulliNB and LogisticRegression functions to fit two models to the training data.
    # For BernoulliNB, use alpha=1.0 and binarize=None
    # For LogisticRegression, pass no parameters
    # YOUR CODE HERE
    X = train_pos_vec + train_neg_vec

    nb_model = BernoulliNB(alpha=1.0, binarize=None).fit(X, Y)

    lr_model = LogisticRegression().fit(X, Y)

    return nb_model, lr_model



def build_models_DOC(train_pos_vec, train_neg_vec):
    """
    Returns a GaussianNB and LosticRegression Model that are fit to the training data.
    """
    Y = ["pos"]*len(train_pos_vec) + ["neg"]*len(train_neg_vec)

    # Use sklearn's GaussianNB and LogisticRegression functions to fit two models to the training data.
    # For LogisticRegression, pass no parameters
    # YOUR CODE HERE
    X = train_pos_vec + train_neg_vec

    nb_model = GaussianNB().fit(X, Y)

    lr_model = LogisticRegression().fit(X, Y)

    return nb_model, lr_model



def evaluate_model(model, test_pos_vec, test_neg_vec, print_confusion=False):
    """
    Prints the confusion matrix and accuracy of the model.
    """
    # Use the predict function and calculate the true/false positives and true/false negative.
    # YOUR CODE HERE

    #print test_neg_vec
    original = ["pos"]*len(test_pos_vec) + ["neg"]*len(test_neg_vec)

    print len(original)
    predicted = model.predict(test_pos_vec + test_neg_vec)

    tp = 0
    fp = 0
    tn = 0
    fn = 0
    correct = 0

    for i in range(len(original)): 
        if original[i]==predicted[i]:
        	correct += 1
        	if original[i]=='pos':
        		tp += 1
        	else:
        		tn += 1
        else:
        	if original[i]=='pos':
        		fn += 1
        	else:
        		fp += 1


   	accuracy = float((float)(correct)/(float)(len(original)))
    if print_confusion:
        print "predicted:\tpos\tneg"
        print "actual:"
        print "pos\t\t%d\t%d" % (tp, fn)
        print "neg\t\t%d\t%d" % (fp, tn)
    print "accuracy: %f" % (accuracy)



if __name__ == "__main__":
    main()
