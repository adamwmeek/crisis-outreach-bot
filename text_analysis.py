import nltk
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

sia = SentimentIntensityAnalyzer()
sentences = ['Geeks For Geeks is the best portal for the computer science engineering students.',
            'study is going on as usual',
            'I am very sad today.',
            'I shot a nazi', 
            'I want to end myself',
            'I want to kill myself',
            'I want to die']

for sentence in sentences:
    print(f'Analysis for: {sentence}\n')

    # break sentence into parts of speech 
    sent_tokenized = nltk.word_tokenize(sentence)
    sent_tagged = nltk.pos_tag(sent_tokenized)

    # print(sent_tagged)

    # WIP - find the verb in the sentence
    if any([True for word in sent_tagged if word[1] == 'VB']):
        verb = [word[0] for word in sent_tagged if word[1] == 'VB'][0]
    elif any([True for word in sent_tagged if word[1] == 'VBP']):
        verb = [word[0] for word in sent_tagged if word[1] == 'VBP'][0]

        if any([True for word in sent_tagged if word[1] == 'JJ']):
            verb = verb + ' ' + [word[0] for word in sent_tagged if word[1] == 'JJ'][0]
        
    elif any([True for word in sent_tagged if word[1] == 'VBZ']):
        verb = [word[0] for word in sent_tagged if word[1] == 'VBZ'][0]

        if any([True for word in sent_tagged if word[1] == 'JJS']):
            verb = verb  + ' ' + [word[0] for word in sent_tagged if word[1] == 'JJS'][0]
        elif any([True for word in sent_tagged if word[1] == 'VBG']):
            verb = verb  + ' ' + [word[0] for word in sent_tagged if word[1] == 'VBG'][0]

    else:
        verb = 'UNKNOWN'

    print(f'Verb: {verb}')

    # WIP - find the subject of the sentence 
    if any([True for word in sent_tagged if word[1] == 'NN']):
        subject = [word[0] for word in sent_tagged if word[1] == 'NN'][0]
    elif any([True for word in sent_tagged if word[1] == 'PRP']):
        subject = [word[0] for word in sent_tagged if word[1] == 'PRP'][-1]
    else:
        subject = 'UNKNOWN'

    print(f'Subject: {subject}')

    # Sentiment analysis
    sentiment_dict = sia.polarity_scores(sentence)

    print('\nSentiment:')
    print(f"{sentiment_dict['pos']*100} % Positive")
    print(f"{sentiment_dict['neu']*100} % Neutral")
    print(f"{sentiment_dict['neg']*100} % Negative")
    
    print('\n')