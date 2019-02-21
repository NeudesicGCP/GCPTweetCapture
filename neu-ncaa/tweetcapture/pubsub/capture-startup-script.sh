#!/bin/bash

gcloud beta container --project "neu-ncaa" clusters create "ncaatweet-cluster" --zone "us-central1-a" --service-account "neu-ncaa-tweet-serviceaccount@neu-ncaa.iam.gserviceaccount.com"
cd /$HOME/GCPTweetCapture/neu-ncaa/tweetcapture/pubsub/
kubectl create -f twitter-stream.yaml
kubectl create -f bigquery-controller.yaml
