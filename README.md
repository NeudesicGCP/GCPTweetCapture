# tweetcapture
# GCP tweet capture and sentiment analysis

This demo uses the following components of GCP:
  kubernetes, docker, pubsub, Natural Language (sentiment analysis), BigQuery, and Data Studio

# Setup

### Clone the example repo

If you haven't already, clone the Github repository for this demo:

```sh
git clone https://github.com/NeudesicGCP/GCPTweetCapture.git
```

### Set project

```sh
gcloud config set project neu-ncaa
```

## Changing topics
The topics that are being captured are found in the file neu-ncaa/tweetcapture/pubsub/tweet-capture-docker-image/twitter-to-pubsub.py   
### Edit the list of topics using your favorite editor
```sh
nano twitter-to-pubsub.py
```

### Create the docker image using cloud build - (if topics are changed)
(from /neu/tweetcapture/pubsub/tweetcapture-docker-image folder)

```sh
gcloud builds submit --tag gcr.io/neu-ncaa/tweetcapture-image .
```

## Capturing tweets
### Kubernetes cluster create (cloud shell)

```sh
gcloud beta container --project "neu-ncaa" clusters create "ncaatweet-cluster" --zone "us-central1-a" --service-account "neu-ncaa-tweet-serviceaccount@neu-ncaa.iam.gserviceaccount.com"
```
```sh
gcloud container clusters get-credentials ncaatweet-cluster --zone us-central1-a --project neu-ncaa
```

### Create the pods
#### (from /neu-ncaa/tweetcapture/pubsub folder)

```sh
kubectl create -f twitter-stream.yaml
```
```sh
kubectl create -f bigquery-controller.yaml
```

### Check the pods

```sh
kubectl get pods
```

## Stoping the tweet capture
```sh
kubectl delete deployment -l "name in (twitter-stream, bigquery-controller)"
```

###################################################################################
# Sentiment Analysis using Google Natural Language API 
## (must be run from a virtual environment using CloudShell)

```sh
pip install virtualenv
```
```sh
virtualenv twitter
```
```sh
source twitter/bin/activate
```
```sh
twitter/bin/pip install google-cloud-language
```
```sh
pip install google-cloud-bigquery
```

## Process tweet sentiment 
### (from /neu-ncaa/tweetcapture/sentiment folder)
### run during and after the tweet capture
```sh
python bigquery-sentiment-analysis-naturallanguage.py ncaa_tweets
```

###################################################################################
# Visualization - Data Studio
This visualization in Google Data Studio uses several views in BigQuery that pull from the tweet and tweetsentiment tables

```sh
https://datastudio.google.com/open/1m4S2Hqn1BCi7ql_2sfCEzz6H7x0oiAEY
```

###################################################################################
# Cleanup

## Delete kubernetes cluster
```sh
gcloud beta container --project "neu-ncaa" clusters delete "ncaatweet-cluster" --zone "us-central1-a"
```
