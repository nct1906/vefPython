#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#9.1 Prints only the words with more than 20 characters 
fhand=open('words.txt')
for line in fhand:
    word=line.rstrip()
    if(len(word)>20):
        print(word)


# In[ ]:


#9.2 Print only the words that have no e 
fhand=open('words.txt')
def has_no_e(word):
    if 'e' in word:
        return False
    return True
countAll=0
countE=0
for line in fhand:   
    countAll+=1
    word=line.rstrip()
    if has_no_e(word)==True:
        print(word)
        countE+=1
print(countE/countAll*100)


# In[ ]:


#9.3 Find letter(s) that excludes the least number of words
def avoids(word, string):
    for letter in string:
        if letter in word:
            return False
            break
    return True
def findCount(string):
    fhand=open('words.txt')
    count=0
    for line in fhand:        
        word=line.rstrip()      
        if avoids(word,string)==True:
            count=count+1
    return count
alphabet=list(map(chr, range(97, 123)))
from itertools import combinations
def makeString():
    t=list()
    numLetter=int(input('Enter the length of forbidden string: '))
    allString = list(combinations(alphabet, numLetter))
    for string in allString:
        count=findCount(''.join(string))        
        t.append((count,string))       
    print(max(t))
makeString()


# In[ ]:


#9.4 Takes a word and a string of letters, returns true if the word contains only letters in the list
fhand=open('words.txt')
def uses_only(word,string):
    check=True
    str=list(string)
    for letter in word:
        if letter not in str:
            check=False
            continue
    if check==True:
        print(word)
    return check
string=input('Enter string: ')
for line in fhand:
        word=line.rstrip()
        uses_only(word,string)


# In[13]:


#9.5 Returns true if the word uses all the required letters in string at least once
fhand=open('words.txt')
def uses_all(word,string):
    check=True
    w=list(word)
    string=list(string)
    for letter in string:
        if letter not in w:
            check=False
            continue
    if check==True:
        print(word)
    return check
string=input('Enter string: ')
count =0
for line in fhand:
    word=line.rstrip()
    check=uses_all(word,string)
    if check==True:
        count+=1
print(count)


# In[9]:


#9.6 Returns true if the letters in a word appear in alphabetical order 
fhand=open('words.txt')
def is_abecedarian(word):
    check=True
    w=list(word)
    prev='`'
    for letter in w:
        if letter>=prev:
            prev=letter
        else:
            check=False
            break
    if check==True:
        print(word)
    return check
count=0
for line in fhand:
    word=line.rstrip()
    check=is_abecedarian(word)
    if check==True:
        count+=1
print(count)


# In[ ]:




