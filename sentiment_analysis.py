from textblob import TextBlob

pos_count = 0
pos_correct = 0

with open("/Users/Jared/Documents/Programming/Datasets/movie_review_positive.txt", "r", encoding="windows-1252") as file:
    for line in file.read().split("\n"):
        analysis = TextBlob(line)

        if analysis.sentiment.subjectivity > 0.9:
            if analysis.sentiment.polarity > 0.2:
                pos_correct += 1
        pos_count += 1


neg_count = 0
neg_correct = 0

with open("/Users/Jared/Documents/Programming/Datasets/movie_review_negative.txt", "r", encoding="windows-1252") as file:
    for line in file.read().split("\n"):
        analysis = TextBlob(line)

        if analysis.sentiment.subjectivity > 0.9:
            if analysis.sentiment.polarity <= 0.2:
                neg_correct += 1
        neg_count += 1

print(f"Positive accuracy = {pos_correct/pos_count * 100.00}%  via {pos_count} samples")
print(f"Negative accuracy = {neg_correct/neg_count * 100.00}%  via {neg_count} samples")


from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

vs = analyzer.polarity_scores("VADER Sentiment seems to be quite apalling actually. Not a fan!")
print(vs)
