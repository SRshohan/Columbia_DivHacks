from dotenv import load_dotenv
import os
import boto3

# Load environment variables from .env file
load_dotenv()

# Initialize Comprehend client
comprehend = boto3.client(
    'comprehend',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_DEFAULT_REGION')
)

def detect_sentiment(text):
    response = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    sentiment = response['Sentiment']
    return sentiment
