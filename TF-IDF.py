#!/usr/bin/env python
# coding: utf-8

# # Importing Skills document.

# In[9]:


import os
import time
import numpy as np
import pandas as pd


# In[1]:


import nltk
import gensim
from nltk.tokenize import word_tokenize, sent_tokenize

file_docs = []

with open ('Resume_Scoring_NLP/Data Anlyst.txt',encoding="utf8") as f:
#     print(f.read())
    tokens = sent_tokenize(f.read())
    for line in tokens:
        file_docs.append(line)

print("Number of documents:",len(file_docs))


# In[17]:


file_docs


# # Preprcessing the document
# ### It will convert the document into a list of lowercase tokens, ignoring tokens that are too short or too long. Also removed stop words. using `nltk.corpus.stopwords.words('english')`
# 
# # Lemmatization
# ### It stems the word but makes sure that it does not lose its meaning.  Lemmatization has a pre-defined dictionary that stores the context of words and checks the word in the dictionary while diminishing.

# In[2]:


get_ipython().run_cell_magic('time', '', "from nltk.stem import WordNetLemmatizer\nwordnet_lemmatizer = WordNetLemmatizer()\ndef pre_pros1(file):    \n    pre_pros1 = [gensim.utils.simple_preprocess(wordnet_lemmatizer.lemmatize(text)) for text in file_docs if text not in nltk.corpus.stopwords.words('english')]\n    return pre_pros1")


# In[27]:



import nltk
nltk.download('wordnet')

from nltk.stem import WordNetLemmatizer
 
# Create WordNetLemmatizer object
wnl = WordNetLemmatizer()
 
# single word lemmatization examples
list1 = ['kites', 'babies', 'dogs', 'flying', 'smiling', 'driving', 'died', 'tried', 'feet']
for words in list1:
    print(words + " ---> " + wnl.lemmatize(words))


# In[3]:


pre_pros1 = pre_pros1(file_docs)


# In[55]:


pre_pros1[1]


# # Dictionary maps each word to a unique id

# In[32]:


dictionary = gensim.corpora.Dictionary(pre_pros1)


# In[56]:


for i in dictionary:
    print('id ',i, dictionary[i])


# # Creating a bag of words
# ### It contains the word id and its frequency in each document

# In[5]:


get_ipython().run_cell_magic('time', '', 'corpus = [dictionary.doc2bow(doc) for doc in pre_pros1]')


# In[60]:


for i in corpus:
    for j in i:
        print('word ',dictionary[j[0]], 'id ',j[0], 'freq ',j[1])


# In[54]:


for i in corpus:
    for j in i:
        print(dictionary[j[0]], j[1])
    print('---')


# In[6]:


list(dictionary.keys())[-1]


# # TF-IDF (term frequency-inverse document frequency) 
# ### It is a statistical measure that evaluates how relevant a word is to a document in a collection of documents. 

# In[7]:


get_ipython().run_cell_magic('time', '', 'tf_idf = gensim.models.TfidfModel(corpus)')


# In[10]:


for doc in tf_idf[corpus]:
    for id_, freq in doc:
        print(dictionary[id_], np.around(freq, decimals=2))


# In[11]:


get_ipython().run_cell_magic('time', '', "sims = gensim.similarities.Similarity('xx',tf_idf[corpus], num_features=len(dictionary))")


# In[12]:


mypath=r'C:\Users\DollaR\OneDrive\Documents\HR Analytics\Resume_Scoring_NLP\Resumes'
#Path for the files
onlyfiles = [os.path.join(mypath, f) for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]


# In[61]:


import collections
import PyPDF2
def pdfextract(file):
    pdf_file = open(file, 'rb')
    read_pdf = PyPDF2.PdfFileReader(pdf_file)
    number_of_pages = read_pdf.getNumPages()
    c = collections.Counter(range(number_of_pages))
    for i in c:
        #page
        page = read_pdf.getPage(i)
        page_content = page.extractText()
    return(page_content.encode('utf-8'))


# In[73]:


cand_name = []
cand_score = []
for file_path in onlyfiles:
    str1 = str(pdfextract(file_path))
    str1 = str1.replace('\\n','').lower()
    rsm1 = nltk.tokenize.regexp_tokenize(str1, r"[a-zA-Z]\w+")
    new_rsm1 = []
    for word in rsm1:
        if word not in nltk.corpus.stopwords.words('english'):
            new_rsm1.append(wordnet_lemmatizer.lemmatize(word).lower())
    query_doc_bow = dictionary.doc2bow(new_rsm1)
    query_doc_tf_idf = tf_idf[query_doc_bow]
#     print(sims[query_doc_tf_idf])
    score = np.round(np.average(sims[query_doc_tf_idf])*100,2)
    cand = file_path.split('\\')[-1].split('.')[0]   
    cand_name.append(cand)
    cand_score.append(score)


# In[74]:


final_result = pd.DataFrame({'cand_name':cand_name, 'cand_score':cand_score})


# In[15]:


final_result


# In[75]:


final_result


# In[67]:


final_result


# In[ ]:




