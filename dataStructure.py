#!/usr/bin/env python
# coding: utf-8

# In[10]:


#1 reads a file, breaks each line into words, strips whitespace and punctuation from the words, and converts them to lowercase
fhand=open('emma.txt', encoding="utf8")
import string
char=list(string.punctuation)
char.append('”')
char.append('“')
def convertLine(line):
    line=line.replace('--',' ')
    
    
    for letter in line:
        if letter in char:
            line=line.replace(letter,'')
    line=line.rstrip().lower()     
    return line.split(' ')


# In[11]:


#2 Then modify the program to count the total number of words in the book, and the number of times each word is used
def skipHeader():
    for num,line in enumerate(fhand):
        line=line.rstrip()
        if line.startswith('***'):
            return num
count=dict()
def countWord(line):
    for word in line:
        if word not in count:
            count[word]=1
        else:
            count[word]+=1
    return count
with fhand as f:
    for _ in range(skipHeader()+1):
        next(f)
    for line in f:
        if(line.rstrip()and not (line.startswith('***') or line.startswith('CHAPTER'))):     
            word=convertLine(line)
            count=countWord(word)
        elif(line.startswith('***')):
            break
    print(sum(count.values()),len(count))   
    print(count)


# In[7]:


#3 Modify the program from the previous exercise to print the 20 most frequently used words in the book
reverse=list()
for key,val in list(count.items()):
    reverse.append((val,key))
reverse.sort(reverse=True)
for key,val in reverse[:20]:
    print((key,val))


# In[8]:


#4 Modify the previous program to read a word list (from previous exercises‘words.txt’) 
#and then print all the words in the book that are not in the word list
fhand2=open('words.txt')
wordList=list()
total=0
for line in fhand2:
    word=line.rstrip()
    wordList.append(word)
for key in count.keys():
    if (key not in wordList):
        total=total+count[key] 
        print(key,count[key])


# In[ ]:


#5 Write a function named choose_from_hist that takes a histogram and returns a
#random value from the histogram, chosen with probability in proportion to frequency

