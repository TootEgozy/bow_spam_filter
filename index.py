import csv
import os

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB


# TODO: split the huge twitter sentiment dataset and add to the data
def answer_templates(category):
    if (category == 'spam'):
        return {
            "spam": "We are {}% certain that your input is spam"
        }


def process_learning_files(class_type, label_index, text_index):
    filenames = os.listdir(f'learning_data/{class_type}')
    texts = list()
    labels = list()
    for filename in filenames:
        with open(f'learning_data/{class_type}/{filename}', 'r', encoding='latin1') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)
            for row in csv_reader:
                labels.append(row[label_index].strip('"'))
                texts.append(row[text_index].strip('"'))
    vectorizer = CountVectorizer()
    matrix = vectorizer.fit_transform(texts)
    return {
        "matrix": matrix,
        "labels": labels,
        "vectorizer": vectorizer
    }


def process_learning_data():
    spam_data = process_learning_files('spam', 0, 1)
    sentiment_data = process_learning_files('sentiment', 0, 5)
    return {
        'spam': spam_data,
        'sentiment': sentiment_data
    }

def label_to_text(cls_type, predicted_label):
    if(cls_type == 'sentiment'):
        match predicted_label:
            case '0':
                return 'negative'
            case '2':
                return 'neutral'
            case '4':
                return 'positive'

def classify_input(input, cls_type, cls_data):
    input_vec = cls_data['vectorizer'].transform([input])
    X_train, X_test, y_train, y_test = train_test_split(cls_data['matrix'], cls_data['labels'], test_size=0.2, random_state=42)
    classifier = MultinomialNB()
    classifier.fit(X_train, y_train)
    predicted_label = classifier.predict(input_vec)[0]
    return label_to_text(cls_type, predicted_label)
