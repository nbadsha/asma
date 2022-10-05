# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 13:56:31 2022

@author: DollaR
"""

import numpy as np
import pandas as pd
import nltk
import os
from gensim.models import Word2Vec
from gensim.similarities import WordEmbeddingSimilarityIndex, SoftCosineSimilarity, SparseTermSimilarityMatrix

from nltk.tokenize import word_tokenize, sent_tokenize
from sklearn.metrics.pairwise import cosine_similarity
import gensim


file_docs = []

os.chdir(r'C:\Users\DollaR\OneDrive\Documents\HR Analytics\Resume_Scoring_NLP')

with open('Data Anlyst.txt',encoding="utf8") as f:
    tokens = sent_tokenize(f.read())
    for line in tokens:
        file_docs.append(line)

print("Number of documents:",len(file_docs))


from nltk.stem import WordNetLemmatizer
wordnet_lemmatizer = WordNetLemmatizer()
def pre_pros1(file):    
    pre_pros1 = \
        [gensim.utils.simple_preprocess(wordnet_lemmatizer.lemmatize(text)) for text in file_docs if text not in nltk.corpus.stopwords.words('english')]
    return pre_pros1

pre_pros1 = pre_pros1(file_docs)

exp1 = ['Inventory',
   'Etl',
   'Expenses',
   'Nosql',
   'Billing',
   'Jira',
   'Mobile',
   'Html',
   'Js',
   'Analysis',
   'Training',
   'System',
   'Automation',
   'Pharmacy',
   'Design',
   'Technical',
   'Sql',
   'Finance',
   'Cloud',
   'Hadoop',
   'End user',
   'Oracle',
   'Analytics',
   'English',
   'Modeling',
   'Photography',
   'Improvement',
   'Presentation',
   'Sales',
   'Reports',
   'Communication',
   'Mysql',
   'Keras',
   'Engineering']


exp2 = ['Inventory',
    'Etl',
    'Expenses',
    'Nosql',
    'Billing',
    'Jira',
    'Mobile',
    'Html',
    'Js',
    'Analysis',
    'Training',
    'System',
    'Automation',
    'Architecture',
    'Opencv',
    'Python',
    'Javascript',
    'Programming',
    'Html',
    'C',
    'Video',
    'Website',
    'R',
    'Statistics',
    'Engineering',
    'Safety'
    'Photography',
    'Improvement',
    'Presentation',
    'Sales',
    'Reports',
    'Communication',
    'Mysql',
    'Keras',
    'Engineering']


# dictionary = gensim.corpora.Dictionary(pre_pros1)

# corpus = [dictionary.doc2bow(doc) for doc in pre_pros1]

model = Word2Vec(vector_size=20, window=4, min_count=2, workers=4)
 
model.build_vocab(pre_pros1)

model.train(pre_pros1, total_examples=model.corpus_count, epochs=model.epochs)

# model.wv.most_similar("analytics")

termsim_index = WordEmbeddingSimilarityIndex(model.wv)

mypath = r'Resumes'
#Path for the files
onlyfiles = [os.path.join(mypath, f) for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]


import collections
import PyPDF2
def pdfextract(file):
    pdf_file = open(file, 'rb')
    read_pdf = PyPDF2.PdfFileReader(pdf_file)
    number_of_pages = read_pdf.getNumPages()
    c = collections.Counter(range(number_of_pages))
    page_content = ""
    for i in c:
        #page
        page = read_pdf.getPage(i)
        page_content += page.extractText()
    return(str(page_content.encode('utf-8')).replace('\\n','').lower())

results = []

for file in onlyfiles:
    str1 = str(pdfextract(file))
    # rsm1 = nltk.tokenize.regexp_tokenize(str1, r"[a-zA-Z]\w+")
    rsm1 = [sent for sent in sent_tokenize(str1)]
    rsm2 = [word_tokenize(sent)  for sent in rsm1]    
    rsm2 = [[word for word in sent if word.isalpha()] for sent in rsm2]
    dictionary = gensim.corpora.Dictionary(rsm2)
    bow_corpus = [dictionary.doc2bow(document) for document in rsm2]
    similarity_matrix = SparseTermSimilarityMatrix(termsim_index, dictionary)
    docsim_index = SoftCosineSimilarity(bow_corpus, similarity_matrix, num_best=10)
    sims = docsim_index[dictionary.doc2bow([word for word in dictionary.itervalues()])]
    print([dictionary.id2token[v[0]] for v in sims])
    print(len(sims))
    cand = file.split('\\')[-1].split('.')[0]
    results.append({'Cand':cand, 'Score':list(sims[0])[1]})
    
import pandas as pd
result_df = pd.DataFrame(results)



str1 = str(pdfextract(file))
# rsm1 = nltk.tokenize.regexp_tokenize(str1, r"[a-zA-Z]\w+")
rsm1 = [sent for sent in sent_tokenize()]
rsm2 = [word_tokenize(sent)  for sent in rsm1]    
rsm2 = [[word for word in sent if word.isalpha()] for sent in rsm2]
dictionary = gensim.corpora.Dictionary([exp2])
bow_corpus = [dictionary.doc2bow(document) for document in [exp2]]
similarity_matrix = SparseTermSimilarityMatrix(termsim_index, dictionary)
docsim_index = SoftCosineSimilarity(bow_corpus, similarity_matrix, num_best=10)
sims = docsim_index[dictionary.doc2bow([word for word in dictionary.itervalues()])]
print(sims)
print(len(sims))
cand = file.split('\\')[-1].split('.')[0]
results.append({'Cand':cand, 'Score':list(sims[0])[1]})
