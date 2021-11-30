from flask import Flask, render_template, request, url_for
import nltk
import nltk.tokenize
from werkzeug.utils import redirect

app = Flask(__name__)
app.debug = True


@app.route('/', methods=['POST', 'GET'])
def home():
    return render_template('home.html')


@app.route('/summary', methods=['POST', 'GET'])
def summary():
    if request.method == 'POST':
        return redirect(url_for('result'))
    return render_template('summary.html')


@app.route('/result', methods=['POST', 'GET'])
def result():
    text1 = request.form['text']
    words = nltk.word_tokenize(text1)
    stopwords = set(nltk.corpus.stopwords.words("english"))
    freqTable = dict()  # for storing the frequency of each word
    for word in words:
        word = word.lower()
        if word in stopwords:
            continue
        if word in freqTable:
            freqTable[word] += 1
        else:
            freqTable[word] = 1

    sentences = nltk.sent_tokenize(text1)
    sentenceValue = dict()
    for sentence in sentences:
        for word, freq in freqTable.items():
            if word in sentence.lower():
                if sentence in sentenceValue:
                    sentenceValue[sentence] += freq
                else:
                    sentenceValue[sentence] = freq
    sumValues = 0
    for sentence in sentenceValue:
        sumValues += sentenceValue[sentence]

    average = int(sumValues / len(sentenceValue))
    summary = ''
    summaryList = summary.split(".")

    for sentence in sentences:
        if (sentence in sentenceValue) and (sentenceValue[sentence] >= average):
            summary += sentence + " "
    return render_template('result.html', summary=summary, accuracy=((len(summaryList) / len(sentenceValue))*100))


if __name__ == '__main__':
    app.run()
