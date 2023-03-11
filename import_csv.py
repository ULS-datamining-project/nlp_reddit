import csv
import re
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Download stopwords if not already downloaded
import nltk
nltk.download('stopwords')

# Open the CSV file for reading
with open('data/subreddit_health.csv', 'r', encoding='utf-8') as ids_file:
    # Create a CSV reader object
    ids_reader = csv.reader(ids_file)
    # Create three empty lists to hold the IDs for each subset
    healthy_ids = []
    neutral_ids = []
    unhealthy_ids = []
    # Iterate through each row of the CSV file
    for row in ids_reader:
        # Check the label in the second column and add the ID to the appropriate list
        if row[0] == 'healthy':
            healthy_ids.append(row[0])
        elif row[0] == 'neutral':
            neutral_ids.append(row[0])
        elif row[0] == 'unhealthy':
            unhealthy_ids.append(row[0])

# Define a function to preprocess the text by removing punctuation, stop words, links, and demonstrative words
def preprocess_text(text):
    # Remove links
    text = re.sub(r'http\S+', '', text)
    # Tokenize the text using NLTK's word_tokenize function
    tokens = word_tokenize(text)
    # Remove punctuation marks and lowercase the words
    words = [word.lower() for word in tokens if word.isalpha()]
    # Remove stop words
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]
    # Remove demonstrative words
    words = [word for word in words if word not in ['this', 'that', 'these', 'those']]
    return words

# Define a function to generate a word cloud and a bar chart for a given subset
def generate_visualizations(subset_name, ids):
    # Open the CSV file for reading
    with open('data/raw_reddit_data.csv', 'r', encoding='utf-8') as input_file:
        # Create a CSV reader object
        reader = csv.reader(input_file)
        # Create an empty list to hold the words
        words = []
        # Iterate through each row of the CSV file
        for row in reader:
            # Check if the ID is in the current subset
            if row[1] in ids:
                # Preprocess the text
                tokens = preprocess_text(row[0])
                print(row)
                # Add the tokens to the words list
                words.extend(tokens)
    # Create a frequency distribution of the words
    freq_dist = FreqDist(words)
    # Get the 25 most frequent words and least frequent words
    most_frequent_words = freq_dist.most_common(25)
    least_frequent_words = freq_dist.most_common()[-25:]
    # Print the most frequent and least frequent words
    print(f"Most frequent words in {subset_name}:")
    for word in most_frequent_words:
        print(word[0], "-", word[1])
    print(f"\nLeast frequent words in {subset_name}:")
    for word in least_frequent_words:
        print(word[0], "-", word[1])
    # Generate a word cloud
    print('aaa')
    wordcloud = WordCloud(width=800)
