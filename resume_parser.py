!pip install nltk
!pip install spacy==2.3.5
!pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.3.1/en_core_web_sm-2.3.1.tar.gz
!pip install pyresparser

import nltk
nltk.download('stopwords')
from pyresparser import ResumeParser

import os
my_dir = r'PATH_TO_RESUME'
os.listdir(my_dir)


my_list = []
for fileName in os.listdir(my_dir):
  print(fileName)
  filePath = my_dir + '/'+ fileName
  data = ResumeParser(filePath).get_extracted_data()
  my_list.append(data)

import pandas as pd
cand_df = pd.DataFrame(my_list)
