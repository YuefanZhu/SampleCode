import pandas as pd
import nltk
from nltk import sent_tokenize,word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import sentiwordnet as swn



def sentianalysis_words(text):
    # This function takes a string and counts the sentiment score for each word,
    # divide the total scores by the number of words and return the word count and average score.
    try:
        if type(text) == str:
            text_lower = text.lower()
            words = nltk.Text(word_tokenize(text_lower))
            taggedlist=[]
            taggedlist.append(nltk.pos_tag(words))

            wnl = nltk.WordNetLemmatizer()

            senti_word_count = 0
            total_senti_score = 0
            for index1,taggedtoken in enumerate(taggedlist[0]):
                # Correct the tags to the form which sentiwordnet recognizes
                newtag=''
                lemmatized_token=wnl.lemmatize(taggedtoken[0])
                if taggedtoken[1].startswith('NN'):
                    newtag='n'
                elif taggedtoken[1].startswith('JJ'):
                    newtag='a'
                elif taggedtoken[1].startswith('V'):
                    newtag='v'
                elif taggedtoken[1].startswith('R'):
                    newtag='r'
                else:
                    newtag=''       
                if(newtag!=''):    
                    synsets = list(swn.senti_synsets(lemmatized_token, newtag))

                    #Getting average of all possible sentiments
                    score=0
                    if(len(synsets)>0):
                        senti_word_count += 1
                        for syn in synsets:
                            score+=syn.pos_score()-syn.neg_score()
                        total_senti_score += score/len(synsets)
                        
            return(senti_word_count, total_senti_score/senti_word_count)
        else:
            print("The input text is not a string, please check agian!")
            return(0,0)
    except:
        return(0,0)

text1 = """
The samgupsul was amazing !! My friend ordered it. Although t was quite pricey they give you a lot and the texture was so perfect I'm going to go back to get it. We also got tofu seafood soup (soondooboo) it was good but I was so full from the pancakes ( we got a small order around 7$) it was good service though they put the food on your plates for you ! And the rice soup was good. 
We went Tuesday around 5:30 pm there wasn't a line I know usually there is.
Everything came to be 50$ . Next time I won't get pancake Cus I was so full afterward until like 2am LOL.
Ktown is great tho esp when it's getting so cold !
"""    

print (sentianalysis_words(text1),text1)


def sentianalysis_sentences(text):
    # This function takes a string and counts the sentiment score for each word in sentence,
    # obtain the sentence sentiment score by dividing the sum of each word's sentiment score by 
    # number of words in that sentence, then averages the sentiment scores of each sentence, 
    # after that, return the sentence count and the average sentiment scores.
    try:
        if type(text) == str:
            text_lower = text.lower()
            words = nltk.Text(word_tokenize(text_lower))
            sentences = nltk.Text(sent_tokenize(text_lower))
            tokens_sentence = [nltk.word_tokenize(sentence) for sentence in sentences]
            taggedlist=[]
            for token in tokens_sentence:
                taggedlist.append(nltk.pos_tag(token))

            wnl = nltk.WordNetLemmatizer()
            score_list=[]

            for index1,taggedsentence in enumerate(taggedlist):
                score_list.append([])
                for index2,taggedtoken in enumerate(taggedsentence):
                    # Correct the tags to the form which sentiwordnet recognizes
                    newtag=''
                    lemmatized_token=wnl.lemmatize(taggedtoken[0])
                    if taggedtoken[1].startswith('NN'):
                        newtag='n'
                    elif taggedtoken[1].startswith('JJ'):
                        newtag='a'
                    elif taggedtoken[1].startswith('V'):
                        newtag='v'
                    elif taggedtoken[1].startswith('R'):
                        newtag='r'
                    else:
                        newtag=''       
                    if(newtag!=''):    
                        synsets = list(swn.senti_synsets(lemmatized_token, newtag))

                        #Getting average of all possible sentiments
                        score=0
                        if(len(synsets)>0):
                            for syn in synsets:
                                score+=syn.pos_score()-syn.neg_score()
                            score_list[index1].append(score/len(synsets))

            sentence_sentiment=[]
            for score_sentence in score_list:
                if len(score_sentence) != 0:
                    sentence_sentiment.append(sum([word_score for word_score in score_sentence])/len(score_sentence))
            
            return(len(sentence_sentiment), sum(score_sentence for score_sentence in sentence_sentiment)/len(sentence_sentiment))
        else:
            print("The input text is not a string, please check agian!")
            return(0,0)
    except:
        return(0,0)

text2 = """
The samgupsul was amazing !! My friend ordered it. Although t was quite pricey they give you a lot and the texture was so perfect I'm going to go back to get it. We also got tofu seafood soup (soondooboo) it was good but I was so full from the pancakes ( we got a small order around 7$) it was good service though they put the food on your plates for you ! And the rice soup was good. 
We went Tuesday around 5:30 pm there wasn't a line I know usually there is.
Everything came to be 50$ . Next time I won't get pancake Cus I was so full afterward until like 2am LOL.
Ktown is great tho esp when it's getting so cold !
"""

print (sentianalysis_sentences('he samgupsul was amazing !! My friend ordered it. Although t was quit'))

# data = pd.read_csv('C:/Users/yz283/Desktop/pxk.csv')
# r=list()
# for i in data.comments:
	# i=str(i)
	# r.append(sentianalysis_sentences(i))
# print (r)