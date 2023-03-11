import csv
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Download the stopwords corpus
import nltk
nltk.download('stopwords')

# Open the CSV file for reading
with open('data/raw_reddit_data.csv', 'r', encoding='utf-8') as input_file:

    # Create a CSV reader object
    reader = csv.reader(input_file, delimiter=',')

    # Create an empty list to hold the words
    words = []

    # Define stopwords to remove
    stop_words = set(stopwords.words('english'))

    # Iterate through each row of the CSV file
    for row in reader:

        # Remove links and punctuation marks
        text = re.sub(r'http\S+', '', row[1])
        text = re.sub(r'[^\w\s]', '', text)

        # Tokenize the text using word_tokenize
        tokens = word_tokenize(text)

        # Remove stopwords and demonstrative words
        filtered_tokens = [token.lower() for token in tokens if token.lower() not in stop_words and token.lower() not in ['this', 'that', 'these', 'those']]

        # Add the filtered tokens to the words list
        words.extend(filtered_tokens)

# Create a frequency distribution of the words
freq_dist = FreqDist(words)

# Get the 25 most frequent words and least frequent words
most_frequent_words = freq_dist.most_common(25)
least_frequent_words = freq_dist.most_common()[-25:]

# Create a bar graph for the most frequent words
plt.figure(figsize=(10,5))
plt.bar([word[0] for word in most_frequent_words], [word[1] for word in most_frequent_words])
plt.xticks(rotation=90)
plt.title("Most frequent words")
plt.xlabel("Words")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("bar_graph_most_frequent.png")

# Create a bar graph for the least frequent words
plt.figure(figsize=(10,5))
plt.bar([word[0] for word in least_frequent_words], [word[1] for word in least_frequent_words])
plt.xticks(rotation=90)
plt.title("Least frequent words")
plt.xlabel("Words")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("bar_graph_least_frequent.png")

# Generate a word cloud
wordcloud = WordCloud(width=800, height=800, background_color='white').generate_from_frequencies(freq_dist)

# Plot the word cloud
plt.figure(figsize=(8, 8), facecolor=None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad=0)

# Save the word cloud as a PNG file
plt.savefig("wordcloud.png")

# Show the plots
plt.show()
