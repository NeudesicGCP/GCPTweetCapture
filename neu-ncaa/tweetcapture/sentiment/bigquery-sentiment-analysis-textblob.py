import argparse
import csv
import os
import time

from google.cloud import bigquery
from google.cloud.bigquery import SchemaField
from google.cloud.exceptions import NotFound
from textblob import TextBlob


def main(dataset):
    # Auth stuff setup
    # -----------------

    # Instantiates a client
    bigquery_service = bigquery.Client()

    # Fetch tweet text from BigQuery dataset
    # -------------------------------------------------

    QUERY = ('SELECT id as id_str, text FROM `neu-ncaa.ncaa_tweets.TweetTopicAndSentiment` '
             'WHERE score is null '
             'limit 1000000')
    query_job = bigquery_service.query(QUERY,location='US')
#    for row in query_job: 
#        print(row.id_str, row.text)

    # Prepare a file writer to write a CSV and load to BigQuery
    # ---------------------------------------------------------

    csv_file = open('sentimenttextblob.csv', 'wt')
    writer = csv.writer(csv_file)
    writer.writerow(('id', 'polarity', 'subjectivity', 'sentiment'))

    # Create the dataset & table
    # --------------------------
    dataset_id = 'ncaa_tweets'

    dataset_ref = bigquery_service.dataset(dataset_id) 

    try:
        bigquery_service.get_dataset(dataset_ref)
    except NotFound:
        dataset.create()

#    if not dataset.exists: - depricated

    table_ref = dataset_ref.table('tweetsentiment_textblob')

    try:
        table = bigquery_service.get_table(table_ref)  
#        table.delete  # truncate - depricated
    except NotFound:
        SCHEMA = [
        SchemaField('id', 'STRING', mode='required'),
        SchemaField('polarity', 'FLOAT', mode='required'),
        SchemaField('subjectivity', 'FLOAT', mode='required'),
        SchemaField('sentiment', 'STRING', mode='required')
        ]
        table = bigquery.Table(table_ref, schema=SCHEMA)
        table = bigquery_service.create_table(table)

    # Run each tweet text through the natural language API to get the sentiment of the text (sleep or else it will exceed quota)
    # -------------------------------------------------------------------------------------

    records_processed = 0
    for row in query_job:
        # time.sleep(0.1000)
        id_str, text = row[0], row[1]
        records_processed += 1
#        print('Processing record %d with tweet: "%s"' % (records_processed, row.text))
        try:
            # The text to analyze
            
            analysis = TextBlob(row.text)
            # print(analysis.sentiment)
            if analysis.sentiment[0]>0:
              sentiment='Positive'
            elif analysis.sentiment[0]<0:
              sentiment='Negative'
            else:
              sentiment='Neutral'

            # Write the results
            writer.writerow((row.id_str, analysis.sentiment.polarity, analysis.sentiment.subjectivity, sentiment))

            # Write the results to BigQuery
            row_to_insert = [(row.id_str,analysis.sentiment.polarity, analysis.sentiment.subjectivity, sentiment)]

            errors = bigquery_service.insert_rows(table, row_to_insert)  # API request
            assert errors == []

        except Exception as e:
            print(e)

'''
    # Upload the sentiment file to BigQuery as a table
    # ------------------------------------------------
    csv_file.flush()
    csv_file.close()
    with open(csv_file.name, 'rb') as readable:
        errors = bigquery_service.insert_rows(table, readable)  # API request
    assert errors == []
    #    table.upload_from_file(readable, source_format='CSV', skip_leading_rows=1)
'''

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('dataset', help='The dataset where the sentiment results should be uploaded to as a BQ table')
    args = parser.parse_args()
    main(dataset=args.dataset)