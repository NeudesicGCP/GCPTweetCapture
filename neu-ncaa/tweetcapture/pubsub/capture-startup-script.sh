sudo snap install kubectl

gcloud beta container --project "neu-ncaa" clusters create "ncaatweet-cluster" --zone "us-central1-a" --service-account "neu-ncaa-tweet-serviceaccount@neu-ncaa.iam.gserviceaccount.com"

kubectl create -f GCPTweetCapture/neu-ncaa/tweetcapture/pubsub/twitter-stream.yaml
kubectl create -f GCPTweetCapture/neu-ncaa/tweetcapture/pubsub/bigquery-controller.yaml
