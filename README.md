# tweetcapture
#NCAA Demo

#SETUP

#Set project

gcloud config set project neu-ncaa-demo

#Kubernetes cluster create (cloud shell)

gcloud beta container --project "neu-ncaa-demo" clusters create "ncaatweet-cluster" --zone "us-central1-a" --service-account "neu-ncaa-tweet-serviceaccount@neu-ncaa-demo.iam.gserviceaccount.com"

gcloud container clusters get-credentials ncaatweet-cluster --zone us-central1-a --project neu-ncaa-demo

#create the pods

#(from /neu-ncaa/tweetcapture/pubsub folder)

kubectl create -f twitter-stream.yaml
kubectl create -f bigquery-controller.yaml

#check the pods
kubectl get pods

#Create the docker image using cloud build - (if topics are changed)
(from /neu-ncaa/tweetcapture/pubsub/tweetcapture-docker-image folder)
gcloud builds submit --tag gcr.io/neu-ncaa-demo/tweetcapture-image .


#Sentiment Analysis using Google Natural Language API
#	(must be run from a virtual environment)

pip install virtualenv

virtualenv twitter

source twitter/bin/activate

twitter/bin/pip install google-cloud-language
pip install google-cloud-bigquery

#From the Sentiment directory in cloud shell:

python bigquery-sentiment-analysis-naturallanguage.py neu-ncaa-serviceaccount-key.json ncaa_tweets


#Clean-Up
#delete the deployments & pods (to stop the capture)
kubectl delete deployment -l "name in (twitter-stream, bigquery-controller)"

#Delete Kubernetes cluster
gcloud beta container --project "neu-ncaa-demo" clusters delete "ncaatweet-cluster" --zone "us-central1-a"
