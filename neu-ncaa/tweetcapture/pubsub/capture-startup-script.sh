gcloud container clusters get-credentials ncaatweet-cluster --zone us-central1-a --project neu-ncaa

kubectl create -f GCPTweetCapture/neu-ncaa/tweetcapture/pubsub/twitter-stream.yaml
kubectl create -f GCPTweetCapture/neu-ncaa/tweetcapture/pubsub/bigquery-controller.yaml
