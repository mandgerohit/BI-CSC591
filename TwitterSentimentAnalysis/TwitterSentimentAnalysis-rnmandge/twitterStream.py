from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import operator
import numpy as np
import matplotlib.pyplot as plt


def main():
    conf = SparkConf().setMaster("local[2]").setAppName("Streamer")
    sc = SparkContext(conf=conf)
    ssc = StreamingContext(sc, 10)   # Create a streaming context with batch interval of 10 sec
    ssc.checkpoint("checkpoint")

    pwords = load_wordlist("positive.txt")
    nwords = load_wordlist("negative.txt")

    counts = stream(ssc, pwords, nwords, 100)
    make_plot(counts)


def make_plot(counts):
    """
    Plot the counts for the positive and negative words for each timestep.
    Use plt.show() so that the plot will popup.
    """
    # YOUR CODE HERE
    #print counts
    fig = plt.figure()
    ax = fig.add_subplot(111)
    pos = list()
    neg = list()

    #First element of the list is empty, hence popping it out
    counts.pop(0)
    time = list()
    i = 0
    for plot in counts:
        pos.append(plot[0][1])
        neg.append(plot[1][1])
        time.append(i)
        i = i+1
    plt.xlabel("Time Step")
    plt.ylabel("Word Count")
    plt.plot(time, pos, 'bo-', time, neg, 'go-')
    ax.legend(('positive', 'negative'), loc='upper left')
    axis = plt.subplot()
    axis.set_ylim(ymin=0, ymax=max(pos)+50)
    axis.set_xlim(xmin=-1, xmax=i+1)
    axis.set_autoscale_on(True)
    plt.show()


def load_wordlist(filename):
    """ 
    This function should return a list or set of words from the given filename.
    """
    fin = open(filename)
    wordlist=list()
    for line in fin.read():
        wordlist.append(line)
    return wordlist

    # YOUR CODE HERE



def stream(ssc, pwords, nwords, duration):
    kstream = KafkaUtils.createDirectStream(
        ssc, topics = ['twitterstream'], kafkaParams = {"metadata.broker.list": 'localhost:9092'})
    tweets = kstream.map(lambda x: x[1].encode("ascii","ignore"))

    # Each element of tweets will be the text of a tweet.
    # You need to find the count of all the positive and negative words in these tweets.
    # Keep track of a running total counts and print this at every time step (use the pprint function).
    # YOUR CODE HERE
    words = tweets.flatMap(lambda line: line.split(' ')) \
            .map(lambda word: ('positive', 1) if word in pwords else ('negative', 1) if word in nwords else ('none', 1)) \
            .filter(lambda x: x[0]=='positive' or x[0]=='negative') \
            .reduceByKey(lambda x, y: x + y)
    # Print the first ten elements of each RDD generated in this DStream to the console
    def updateValues(values, count):
        if count is None:
            count = 0
        return sum(values, count)

    updatedWords = words.updateStateByKey(updateValues)
    updatedWords.pprint()
    
    # Let the counts variable hold the word counts for all time steps
    # You will need to use the foreachRDD function.
    # For our implementation, counts looked like:
    #   [[("positive", 100), ("negative", 50)], [("positive", 80), ("negative", 60)], ...]
    counts = []
    # YOURDSTREAMOBJECT.foreachRDD(lambda t,rdd: counts.append(rdd.collect()))
    words.foreachRDD(lambda t,rdd: counts.append(rdd.collect()))

    ssc.start()                         # Start the computation
    ssc.awaitTerminationOrTimeout(duration)
    ssc.stop(stopGraceFully=True)

    return counts


if __name__=="__main__":
    main()
