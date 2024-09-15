import os
import sys
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator



# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pipelines.aws_s3_pipeline import upload_s3_pipeline
from pipelines.reddit_pipeline import reddit_pipeline

default_args = {
    'owner': 'Seif Yasser',
    'start_date': datetime(2024, 8, 1)
}

file_postfix = datetime.now().strftime("%Y%m%d")

# def connect_reddit(client_id, client_secret, user_agent) -> Reddit:
#     try:
#         reddit = praw.Reddit(client_id=client_id,
#                              client_secret=client_secret,
#                              user_agent=user_agent)
#         print("connected to reddit!")
#         return reddit
#     except Exception as e:
#         print(e)
#         sys.exit(1)
#
#
# def extract_posts(reddit_instance: Reddit, subreddit: str, time_filter: str, limit=None):
#     subreddit = reddit_instance.subreddit(subreddit)
#     posts = subreddit.top(time_filter=time_filter, limit=limit)
#
#     post_lists = []
#     for post in posts:
#         post_dicts = vars(post)
#         print(post_dicts)
#
#
# def reddit_pipeline(file_name: str, subreddit: str, time_filter='day', limit=None):
#     # connecting to reddit instance
#     instance = connect_reddit('eW_RCzUS9WtEG26KlKM1PA', 'Ohl3MUfGKef6IfTpDt_lb9ccDCYhCA', 'Airscholar Agent')
#     # extraction
#     extract_posts(instance, subreddit, time_filter, limit)


dag = DAG(
    dag_id='etl_reddit_pipeline',
    default_args=default_args,
    schedule_interval='@daily'
)

# extraction from reddit
extract = PythonOperator(
    task_id='reddit_extraction',
    python_callable=reddit_pipeline,
    op_kwargs={
        'file_name': f'reddit_{file_postfix}',
        'subreddit': 'dataengineering',
        'time_filter': 'day',
        'limit': 100
    },

    dag=dag
)

upload_s3 = PythonOperator(
    task_id='s3_upload',
    python_callable=upload_s3_pipeline,
    dag=dag
)

extract >> upload_s3
