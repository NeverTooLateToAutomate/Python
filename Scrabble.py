#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# step 1 sorting words


# In[100]:


import pandas as pd


# In[133]:


from zipfile import ZipFile
from io import BytesIO
from urllib.request import urlopen

url = urlopen('https://sjp.pl/slownik/growy/sjp-20190731.zip')
file = ZipFile(BytesIO(url.read()))
words_csv = file.open('slowa.txt')
df = pd.read_csv(words_csv, header=None, names = ['words'])


# In[102]:


df.shape


# In[103]:


word_list = df['words'].tolist()


# In[104]:


print(len(word_list))


# In[105]:


x = 0

for i in word_list:
    word_list[x] = ''.join(sorted(i))
    x += 1


# In[106]:


df_sort = pd.DataFrame(word_list)
df_sort.columns = ['sorted']


# In[107]:


df_sort.tail(15)


# In[108]:


file_name = (r'C:\Users\PJanus\Documents\Python excercises\slowa_sort.txt')
df_sort.to_csv(file_name, index=False)


# In[109]:


# step 2 creating dictionary


# In[131]:


df_sort = pd.read_csv(r'C:\Users\PJanus\Documents\Python excercises\slowa_sort.txt')


# In[134]:


merged = pd.merge(df_sort, df, left_index=True, right_index=True)


# In[137]:


merged


# In[138]:


grouped = merged.groupby('sorted').agg(list)


# In[139]:


grouped = grouped.reset_index()


# In[172]:


grouped


# In[118]:


word_dict = grouped.set_index('sorted')['words'].to_dict()


# In[120]:


word_dict


# In[125]:


# save as pickle
import pickle

with open(r'C:\Users\PJanus\Documents\Python excercises\slowa_dict.pickle', 'wb') as f:
    pickle.dump(word_dict, f, protocol=pickle.HIGHEST_PROTOCOL)


# In[ ]:


# step 3 letter value


# In[173]:


letter_dict = {'a':1, 'e':1, 'i':1, 'n':1, 'o':1, 'r':1, 's':1, 'w':1, 'z':1,
'c':2, 'd':2, 'k':2, 'l':2, 'm':2, 'p':2, 't':2, 'y':2,
'b':3, 'g':3, 'h':3, 'j':3, 'ł':3, 'u':3,
'ą':5, 'ę':5, 'f':5, 'ó':5, 'ś':5, 'ż':5,
'ć':6, 'ń':7, 'ź':9}


# In[182]:


grouped


# In[183]:


grouped.shape


# In[184]:


letter_value_list  = []

for i in grouped['sorted']: 
    word_value = 0
    for j in list(i):
        if j in letter_dict:
            letter_value = letter_dict[j]
            word_value += letter_value
    letter_value_list.append(word_value)


# In[185]:


print(len(letter_value_list))


# In[192]:


df_letter = pd.DataFrame(letter_value_list)
df_letter.columns = ['value']


# In[193]:


merged2 = pd.merge(grouped, df_letter, left_index=True, right_index=True)


# In[200]:


merged2 = merged2.drop(['words'], axis=1)


# In[201]:


merged2


# In[202]:


letter_dict = merged2.set_index('sorted')['value'].to_dict()


# In[203]:


letter_dict


# In[211]:


# save as pickle
import pickle

with open(r'C:\Users\PJanus\Documents\Python excercises\slowa_value_dict.pickle', 'wb') as f:
    pickle.dump(letter_dict, f, protocol=pickle.HIGHEST_PROTOCOL)


# In[ ]:


# step 4 search for words


# In[213]:


from datetime import datetime
import pickle


# In[314]:


# load pickle
start_time = datetime.now()

with open(r'C:\Users\PJanus\Documents\Python excercises\slowa_dict.pickle', 'rb') as f:
    word_dict = pickle.load(f)

time_elapsed = datetime.now() - start_time 
print('Time elapsed (hh:mm:ss.ms) {}'.format(time_elapsed))


# In[313]:


# load pickle
start_time = datetime.now()
   
with open(r'C:\Users\PJanus\Documents\Python excercises\slowa_value_dict.pickle', 'rb') as f:
    word_dict_value = pickle.load(f)

time_elapsed = datetime.now() - start_time 
print('Time elapsed (hh:mm:ss.ms) {}'.format(time_elapsed))


# In[494]:


from datetime import datetime
start_time = datetime.now()

from itertools import combinations

input_txt = 'aa'
# input_sort = ''.join(sorted(input_txt))

import string
alphabet = list('aąbcćdeęfghijklłmnńoóprsśtuwyzźż')
blank = True
word_min = 1
word_max = 4

perm_list = set()

if blank:
    pass
    for char_len in range(word_min, word_max + 1): # len(input_txt) + 2
        for x in alphabet:
            char_list = list(input_txt + x)
            perm = combinations(char_list, char_len)
            for i in list(perm): 
                join_char = ''.join(i)
                join_sort = ''.join(sorted(join_char))
                perm_list.add(join_sort)  
    
else:
    for char_len in range(word_min, word_max + 1): # len(input_txt) + 1
        char_list = list(input_txt)
        perm = combinations(char_list, char_len)
        for i in list(perm): 
            join_char = ''.join(i)
            join_sort = ''.join(sorted(join_char))
            perm_list.add(join_sort)

results = []

for i in perm_list:
    if i in word_dict_value:
        value = word_dict_value[i]
        results.append(value)
    if i in word_dict:
        word = word_dict[i]
        results.append(word)
        
print(results)
       
time_elapsed = datetime.now() - start_time
print('Time elapsed (hh:mm:ss.ms) {}'.format(time_elapsed))

