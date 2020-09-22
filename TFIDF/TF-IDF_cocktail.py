import pandas as pd
import csv
import re
from sklearn.feature_extraction.text import TfidfTransformer, TfidfVectorizer, CountVectorizer
#spacy------------------------------
import spacy
# print('spaCy Version: %s' % (spacy.__version__))  # spaCy Version: 2.3.2
import en_core_web_sm
import en_core_web_lg
from spacy.lang.en import English
from spacy.tokens import Doc
from spacy.symbols import PUNCT, NUM, AUX, X, CONJ, ADJ, VERB, PART, SPACE, CCONJ,INTJ,NOUN
from spacy.lang.en.stop_words import STOP_WORDS
#---------------------------------------
nlp = spacy.load('en_core_web_lg')
spacy_stopwords = spacy.lang.en.stop_words.STOP_WORDS
spacy_stopwords = spacy_stopwords.union({
    'easy', 'long', 'nice', 'tasty','white','dry','little','simple',
    'great', 'good','username','text','oz','sure'})
# print('Number of stop words: %d' % len(spacy_stopwords))
# print('First ten stop words: %s' % list(spacy_stopwords)[:])
#---------------------------------------
df = pd.read_csv(r'.\cocktail\cocktail_all_08924_class_combine.csv',encoding='utf-8-sig')  #cocktail_all_combine
df['mix'] = '['+ df['ins'].map(str)+']' +df['comment'].map(str)+'\r''\r'+ df['Vodka'].map(str)+'\r'+ df['Rum'].map(str)+'\r'+ df['Gin'].map(str)+'\r'+ df['Tequila'].map(str)+'\r'+'\r'+''+ df['Whiskey'].map(str)+'\r'+'\r'+ df['Brandy'].map(str)+'\r'+ df['liqueur'].map(str)+']'
# print(df['mix'])
# df['mix'] = '['+ df['ins'].map(str)+']' +df['comment'].map(str)+'\r'+'\r'+df['favor'].map(str)+'\r''\r'+ df['Vodka'].map(str)+'\r'+ df['Rum'].map(str)+'\r'+ df['Gin'].map(str)+'\r'+ df['Tequila'].map(str)+'\r'+'\r'+''+ df['Whiskey'].map(str)+'\r'+'\r'+ df['Brandy'].map(str)+'\r'+ df['liqueur'].map(str)+']'
#
dff = df[df['mix'] != '[nan]nannannannannannannannan']
data = list(dff['mix'])
# print(data)
data_i = [i.lower().replace('nan','').strip().strip('\r').strip('\\').strip('\t') for i in data if len(i) != 0]
# print(data_i)
remove_chars = '[0-9’!"#$%&()*+-./:;<=>?@，。?★、…【】\'\r《》？“”‘’！\\\\[\\]^_`{|}~]+' #移除數字及特殊符號
remove = [re.sub(remove_chars, '' , i) for i in data_i]
text = [re.compile('').sub('', i)for i in remove]
# # text = [re.compile('').sub('', i)for i in remove if len(i) != 0] #移除空格
# print(text)
#
# # print(index)
name = list(dff['name'])
print(name)
##-----------------------------查看資訊-------------------------
'''
# for token in nlp(str(text[0:10])):
#     # if  token.pos_ == 'ADJ' or  token.pos_ == 'NOUN':
#     #     print('token.text:',token.text,'token.lemma_:',token.lemma_,'token.pos_:',token.pos_,'token.tag_:',token.tag_)
#
#     print('token.text:',token.text,'token.lemma_:',token.lemma_,'token.pos_:',token.pos_,'token.tag_:',token.tag_,
#     'token.dep_:',token.dep_,'token.shape_:', token.shape_,'token.is_alpha:',token.is_alpha,'token.is_stop:',token.is_stop)
'''
# # #-----------------------用正則及CountVectorizer做詞性還原及分詞-及停用詞-------------------------------------------------
lemma_data = []
for idx, item in enumerate(text):
    doc = nlp(item)  # --> set the document vocab
    doc_spacy = Doc(doc.vocab, words=[t.text for t in doc]) #vocab：詞彙表
    token_lemma_data = [token.lemma_ for token in doc_spacy if not token.is_stop]

    # print(token_lemma_data)
    lemma_data.append(token_lemma_data)
corpus = [str(item).strip().replace('\\','').replace('\t','') for item in lemma_data if len(str(item)) > 1]
print('corpus',corpus)
# # # -----------------詞性還原 及 詞性標註(只留形容詞、感嘆詞、名詞)---------------------------------------
# # #
pos_data =[]
for n, item in enumerate(text):
    doc = nlp(item)
    # pos = [token.pos_ for token in doc]
    # doc_spacy = Doc(doc.vocab, words=[t.text for t in doc])
    no_VERB = [token.lemma_ for token in doc if token.pos_ == 'ADJ' ] #or token.pos_ == 'NOUN'or token.pos_ == 'PROPN'
    pos_data.append(no_VERB)
# print('pos_data',pos_data)
pos = [str(item).strip().replace('\\','').replace('\t','') for item in pos_data if len(str(item)) > 1]
print('pos',pos)

# # # ---------------------------------------------------------------
# # # # # 計算單字次數：
vect = CountVectorizer(token_pattern='(?u)\\b\\w\\w+\\b',stop_words=spacy_stopwords,min_df=0.008)#,max_df=0.99,min_df=0.01)
x_train = vect.fit_transform(pos)
feature = vect.get_feature_names()
print(feature)
# # # # # #------------dataframe貯存---------------------
count_feature = pd.DataFrame(x_train.toarray(), columns=feature, index=name)
print('dataframe:',count_feature)
# count_feature.to_csv(r'./cocktail/tfidf/mix_pos_feature_matrix_0824.csv', encoding='utf-8-sig')
# # # # # ---------------------------------------------------------------
# # # #計算tfidf權重--------------------------------------
transformer = TfidfTransformer()
tfidf_matrix = transformer.fit_transform(x_train)
weight = tfidf_matrix.toarray()
# # # #------------dataframe貯存---------------------
tfidf = pd.DataFrame(tfidf_matrix.toarray(),columns=feature,index=name)
print('tfidf_matrix:',tfidf)
# tfidf.to_csv(r'./cocktail/tfidf/tfidf_min0.005_pos_matrix_0824.csv', encoding='utf-8-sig')