gcloud beta container --project "neu-ncaa" clusters create "ncaatweet-cluster" --zone "us-central1-a" --service-account "neu-ncaa-tweet-serviceaccount@neu-ncaa.iam.gserviceaccount.com"
gcloud container clusters get-credentials ncaatweet-cluster --zone us-central1-a --project neu-ncaa

kubectl create -f /$HOME/GCPTweetCapture/neu-ncaa/tweetcapture/pubsub/twitter-stream.yaml
kubectl create -f /$HOME/GCPTweetCapture/neu-ncaa/tweetcapture/pubsub/bigquery-controller.yaml