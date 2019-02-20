import argparse
import csv
import os
import time

from google.cloud import bigquery
from google.cloud import language
from google.cloud.bigquery import SchemaField
from google.cloud.exceptions import NotFound
from google.cloud.language import enums 
from google.cloud.language import types 


def main(dataset):
    # Auth stuff setup
    # -----------------

    # Instantiates a client
    language_service = language.LanguageServiceClient()
    bigquery_service = bigquery.Client()

    # Fetch tweet text from BigQuery dataset
    # -------------------------------------------------

#    QUERY = ('SELECT id as id_str, text FROM `neu-ncaa.ncaa_tweets.tweets` '     -- use this query to initially to create the tweetsentiment table in BigQuery

    QUERY = ('SELECT id as id_str, text FROM `neu-ncaa.ncaa_tweets.TweetTopicAndSentiment` '
             'WHERE score is null '
             'limit 1000000')
    query_job = bigquery_service.query(QUERY,location='US')
#    for row in query_job: 
#        print(row.id_str, row.text)

    # Prepare a file writer to write a CSV and load to BigQuery
    # ---------------------------------------------------------

    csv_file = open('sentiment.csv', 'wt')
    writer = csv.writer(csv_file)
    writer.writerow(('id', 'score', 'magnitude'))

    # Create the dataset & table
    # --------------------------
    dataset_id = 'ncaa_tweets'

    dataset_ref = bigquery_service.dataset(dataset_id) 

    try:
        bigquery_service.get_dataset(dataset_ref)
    except NotFound:
        dataset.create()

#    if not dataset.exists: - depricated

    table_ref = dataset_ref.table('tweetsentiment')

    try:
        table = bigquery_service.get_table(table_ref)  
#        table.delete  # truncate - depricated
    except NotFound:
        SCHEMA = [
        SchemaField('id', 'STRING', mode='required'),
        SchemaField('score', 'FLOAT', mode='required'),
        SchemaField('magnitude', 'FLOAT', mode='required')
        ]
        table = bigquery.Table(table_ref, schema=SCHEMA)
        table = bigquery_service.create_table(table)

    # Run each tweet text through the natural language API to get the sentiment of the text (sleep or else it will exceed quota)
    # -------------------------------------------------------------------------------------

    records_processed = 0
    for row in query_job:
        time.sleep(0.1000)
        id_str, text = row[0], row[1]
        records_processed += 1
        
#        print('Processing record %d with tweet: "%s"' % (records_processed, row.text))
        try:
            # The text to analyze
            document = types.Document(
            content=row.text,
            type=enums.Document.Type.PLAIN_TEXT)

#            document = language_service.document_from_text(row.text)  --depricated

            # Detects the sentiment of the text
            sentiment = language_service.analyze_sentiment(document=document).document_sentiment

            # Write the results to .csv
            writer.writerow((row.id_str, sentiment.score, sentiment.magnitude))


            # Write the results to BigQuery
            row_to_insert = [(row.id_str,sentiment.score,sentiment.magnitude)]

            errors = bigquery_service.insert_rows(table, row_to_insert)  # API request
            assert errors == []

        except Exception as e:
            print(e)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('credential_file', help='Path to your service account key (JSON file)')
    parser.add_argument('dataset', help='The dataset where the sentiment results should be uploaded to as a BQ table')
    args = parser.parse_args()
    main(credential_file=args.credential_file, dataset=args.dataset)
