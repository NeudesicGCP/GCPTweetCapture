gcloud beta container --project "neu-ncaa" clusters create "ncaatweet-cluster" --zone "us-central1-a" --service-account "neu-ncaa-tweet-serviceaccount@neu-ncaa.iam.gserviceaccount.com"

kubectl config view

export KUBECONFIG=GCPTweetCapture/config

kubectl config view

gcloud container clusters get-credentials ncaatweet-cluster --zone us-central1-a --project neu-ncaa

ls

cd GCPTweetCapture/neu-ncaa/tweetcapture/pubsub

ls

kubectl create -f twitter-stream.yaml
kubectl create -f bigquery-controller.yaml
