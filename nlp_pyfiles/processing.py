import spacy
from spacy import displacy
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
from nltk.corpus import stopwords
from googletrans import Translator
import en_core_web_sm
import re


class NLProcessing(object):
    def __init__(self, text):
        self.nlp = en_core_web_sm.load()
        self.text = self.nlp(text)

    def get_entities(self):
        return displacy.render(self.text, style='ent')

    def analyze_sentiment(self, threshold):
        overall_score = SentimentIntensityAnalyzer().polarity_scores(f"u'{self.text}'")
        neg_sentences, pos_sentences = [], []
        for sent in self.text.sents:
            score = SentimentIntensityAnalyzer().polarity_scores(f"u'{sent}'")
            neg = score["neg"]
            pos = score["pos"]
            if neg - pos > threshold:
                neg_sentences.append(sent)
            elif pos - neg > threshold:
                pos_sentences.append(sent)

        return [overall_score, neg_sentences, pos_sentences]

    def translate_most_freq_words(self, nb_top):
        translator = Translator()
        tokens = {}
        stop_words = stopwords.words('english')
        freq_words = []
        en_ja = {}
        removing_words = r"!.?:,"

        # get most frequent words
        for token in self.text:
            if token.text not in tokens:
                if token.text not in stop_words:
                    tokens[token.text] = 1
            else:
                tokens[token.text] += 1
        sorted_tokens = sorted(tokens.items(), key=lambda x: -x[1])

        # pick up top nb_top words
        for item in sorted_tokens:
            if len(freq_words) < nb_top:
                freq_words.append(item[0])
            else:
                break
        # translate them
        for word in freq_words:
            if word in removing_words:
                continue
            else:
                en_ja[word] = translator.translate(word, dest="ja").text

        return en_ja

    def get_nb_words(self):
        return len(self.text)



