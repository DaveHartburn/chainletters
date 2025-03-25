#!/usr/bin/python

# Creates the database tables and loads word list for chain letter processing
# Usage: python createLoad.py [-y] [word file]
# Where -y overrides the "are you sure" prompt and "word file" is a path to an alternate list of words with one word
# on each line. If not specified, the default file "wordlist" in the local directory is used


import sys


import dbUtils as db

# Global variables
noConfirm=False
wordlist="wordlist"


tableDefs = [
 ["words", """CREATE TABLE IF NOT EXISTS words (
    word CHAR(60) NOT NULL,
    length INT,
    processed BOOL DEFAULT false,       # Have we found all links?
    visited BOOL DEFAULT false,         # Have we visited this node in current search?
    family INT,                         # All words with a link are part of the same family
    PRIMARY KEY (word)
    )
 """
 ],
 ["families", """CREATE TABLE IF NOT EXISTS families (
    family INT NOT NULL AUTO_INCREMENT,
    PRIMARY KEY (family)
    )
 
 """]
]

for i in sys.argv[1:] :
    if i=="-y":
        # Override check
        noConfirm=True
    else:
        # Assume anything else is the word file
        wordlist=i

if not noConfirm:
    print("Creating database tables. This will erase all data and reload from scratch.")
    print("Are you sure you want to continue? (yes/no)")
    i = input().lower()

    if(i != "yes"):
        print("Aborting")
        exit(1)
        
print("Confirmed, going ahead")

# Connect to database
db.dbConnect()

for t in tableDefs:
    tabName=t[0]
    print("Deleting table", tabName)
    sql="DROP TABLE IF EXISTS {}".format(tabName)
    #print(sql)
    db.submit(sql)
    db.submit(t[1])

print("Loading words from", wordlist)
try:
    with open(wordlist, "r") as f:
        for l in f:
            w=l.rstrip()
            #print(w)
            
            # Assume one word per line and content is sane
            sql="INSERT INTO words (word, length) VALUES (\"{}\",length(word))".format(w)
            #print(sql)
            db.submit(sql, commit=100)
 
    db.commit()
    
    f.close()
except (RuntimeError, TypeError, NameError):
    print("ERROR", NameError)
    exit(1)

# Close database connection 
db.close()