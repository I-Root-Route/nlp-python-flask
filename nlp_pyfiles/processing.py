# import spacy
from spacy import displacy
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from googletrans import Translator
import en_core_web_sm


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
        stop_words = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll",
                      "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's",
                      'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs',
                      'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am',
                      'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does',
                      'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while',
                      'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during',
                      'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over',
                      'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how',
                      'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not',
                      'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don',
                      "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren',
                      "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn',
                      "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't",
                      'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren',
                      "weren't", 'won', "won't", 'wouldn', "wouldn't"]
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
