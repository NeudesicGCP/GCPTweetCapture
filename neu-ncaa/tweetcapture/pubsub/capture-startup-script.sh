gcloud beta container --project "neu-ncaa" clusters create "ncaatweet-cluster" --zone "us-central1-a" --service-account "neu-ncaa-tweet-serviceaccount@neu-ncaa.iam.gserviceaccount.com"

kubectl config view

export KUBECONFIG=home/mike_sherrill/GCPTweetCapture/config

kubectl config view

gcloud container clusters get-credentials ncaatweet-cluster --zone us-central1-a --project neu-ncaa

kubectl config view

sudo kubectl create -f home/mike_sherrill/GCPTweetCapture/neu-ncaa/tweetcapture/pubsub/twitter-stream.yaml
sudo kubectl create -f home/mike_sherrill/GCPTweetCapture/neu-ncaa/tweetcapture/pubsub/bigquery-controller.yaml
