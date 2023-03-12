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
with open('data/reddit_data_sentiment.csv', 'r', encoding='utf-8') as input_file:

    # Create a CSV reader object
    reader = csv.reader(input_file, delimiter=',')

    # Create an empty list to hold the words
    words_nature1 = []
    words_nature2 = []

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

          # Determine the nature of the row
        label = row[13]

        # Add the filtered tokens to the appropriate list based on the nature
        if label == 'POSITIVE':
            words_nature1.extend(filtered_tokens)
        elif label == 'NEGATIVE':
            words_nature2.extend(filtered_tokens)
      
        # Add the filtered tokens to the words list
        words_nature1.extend(filtered_tokens)
        words_nature2.extend(filtered_tokens)
# Create frequency distributions for each nature
freq_dist_nature1 = FreqDist(words_nature1)
freq_dist_nature2 = FreqDist(words_nature2)


# Get the 25 most frequent words and least frequent words for each nature
most_frequent_words_nature1 = freq_dist_nature1.most_common(25)
most_frequent_words_nature2 = freq_dist_nature2.most_common(25)


# Create a bar graph for the most frequent words for each nature
plt.figure(figsize=(10,5))
plt.bar([word[0] for word in most_frequent_words_nature1], [word[1] for word in most_frequent_words_nature1])
plt.xticks(rotation=90)
plt.title("Most frequent words for POSITIVE")
plt.xlabel("Words")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("bar_graph_most_frequent_POSITIVE.png")

plt.figure(figsize=(10,5))
plt.bar([word[0] for word in most_frequent_words_nature2], [word[1] for word in most_frequent_words_nature2])
plt.xticks(rotation=90)
plt.title("Most frequent words for NEGATIVE")
plt.xlabel("Words")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig("bar_graph_most_frequent_NEGATIVE.png")

# Generate a word cloud
wordcloud = WordCloud(width=800, height=800, background_color='white').generate_from_frequencies(freq_dist_nature1)
wordcloud2 = WordCloud(width=800, height=800, background_color='white').generate_from_frequencies(freq_dist_nature2) 
# Plot the word cloud
plt.figure(figsize=(8, 8), facecolor=None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad=0)

# Save the word cloud as a PNG file
plt.savefig("wordcloud2.png")
plt.figure(figsize=(8, 8), facecolor=None)
plt.imshow(wordcloud2)
plt.axis("off")
plt.tight_layout(pad=0)

# Save the word cloud as a PNG file
plt.savefig("wordcloud.png")

# Show the plots
plt.show()
## We notice that there are really close similarities between the most frequent words in positive and negative posts for starters
## chicken is the most frequently used words in both sets of data and most of the words that appear in the charts are the same 
## It is surprising that rice, soup and salad appear in the negative subset and fried to appear in the positive subset this shows
## that other than the nature of our analysis food terms are hard to assign to a category different types of food can be healthy 
## just as they can be unhealthy and positive and negative sentiment towards food is highly subjective as they're not chosen by 
## their value rather mostly by taste.