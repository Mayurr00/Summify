from __future__ import unicode_literals
from flask import Flask,render_template,url_for,request

from spacy_summarization import text_summarizer
import time
import spacy
nlp = spacy.load("en_core_web_sm")
app = Flask(__name__)

from bs4 import BeautifulSoup
from urllib.request import urlopen

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

def sumy_summary(docx):
	parser = PlaintextParser.from_string(docx,Tokenizer("english"))
	lex_summarizer = LexRankSummarizer()
	summary = lex_summarizer(parser.document,3)
	summary_list = [str(sentence) for sentence in summary]
	result = ' '.join(summary_list)
	return result


def readingTime(mytext):
	total_words = len([ token.text for token in nlp(mytext)])
	estimatedTime = total_words/200.0
	return estimatedTime, total_words

def get_text(url):
	page = urlopen(url)
	soup = BeautifulSoup(page)
	fetched_text = ' '.join(map(lambda p:p.text,soup.find_all('p')))
	return fetched_text

@app.route('/')
def index():
	return render_template('index.html')


@app.route('/analyze',methods=['GET','POST'])
def analyze():
	start = time.time()
	if request.method == 'POST':
		rawtext = request.form['rawtext']
		final_reading = readingTime(rawtext)
		final_reading_time, final_total_words = final_reading[0], final_reading[1]
		final_summary = text_summarizer(rawtext)
		summary_reading = readingTime(final_summary)
		summary_reading_time, summary_total_words = summary_reading[0], summary_reading[1]
		end = time.time()
		final_time = end-start
	return render_template('index.html',ctext=rawtext,final_summary=final_summary,final_time=final_time,final_reading_time=final_reading_time,final_total_words=final_total_words,summary_reading_time=summary_reading_time,summary_total_words=summary_total_words)

@app.route('/analyze_url',methods=['GET','POST'])
def analyze_url():
	start = time.time()
	if request.method == 'POST':
		raw_url = request.form['raw_url']
		rawtext = get_text(raw_url)
		final_reading = readingTime(rawtext)
		final_reading_time, final_total_words = final_reading[0], final_reading[1]
		final_summary = text_summarizer(rawtext)
		summary_reading = readingTime(final_summary)
		summary_reading_time, summary_total_words = summary_reading[0], summary_reading[1]
		end = time.time()
		final_time = end-start
	return render_template('index.html',ctext=rawtext,final_summary=final_summary,final_time=final_time,final_reading_time=final_reading_time,final_total_words=final_total_words,summary_reading_time=summary_reading_time,summary_total_words=summary_total_words)

if __name__ == '__main__':
	app.run(debug=True)