# Data Mining

Practical works for university course "Data Mining"

## Stages

1. Map-Reduce
    - maximum
    - average
    - unique
    - number of unique 
2. Apriori algorithm
3. Classification
    - decision tree
    - k-means ([wat?](#k-means-approach-in-classification))
    - k-nearest neighbors algorithm
4. Clusterization
 - k-means
 - k-nearest neighbors algorithm ([wat?](#k-nearest-neighbours-approach-in-clusterisation))
5. Text Mining
    - Naive Bayes Classifier for sms spam
6. [Project](https://github.com/vaniakosmos/gender-recognition-by-voice)

## k-means approach in classification

- grouping dataset by classes
- for each test instance calculate how far moved center of class after adding this instance into it
- choose class with fewer changes

## k-nearest neighbours approach in clusterisation

1. initialize each cluster with one vector from data set
2. delete vectors that was added to clusters from data set
3. find nearest vectors to each cluster in data set 
4. add them to corresponding clusters
5. repeat steps 2-4 while data set isn't empty