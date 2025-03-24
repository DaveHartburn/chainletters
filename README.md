# chainletters
Scripts and utils for a popular word game. Add, remove or change a single character in a word to make another one.

For example:
*Add some examples here*

*See section on Database create and word loading for how to change the word list*

This leads to a number of questions such as:
 - How many unique words are there which can not be changed to any other word?
 - What is the longest chain of words which can be made, without repeats?
 - What is the shortest to longest word which can be made into a chain?
 - How many individual "families" of words exist, where a family is two or more words which can be chained.

This project uses a MySQL database to perform the processing side.

There are three stages to this project:
 1. Database set up and loading of the word list
 2. Processing of the word list to find links between words
 3. Data production. Answering all the interesting questions such as those above

## Database install and set up

Install MySQL server as appropriate for your operating system. See https://dev.mysql.com/doc/mysql-installation-excerpt/5.7/en/

Connect to your database with an appropriate client.

On Ubuntu/Debian systems install with `apt install mysql-server` then connect with `mysql -h localhost`

Create the database and user with the following, changing *yourPassword* for something secure.

```
CREATE DATABASE chainletters;
CREATE USER 'clet_rw'@'localhost' IDENTIFIED WITH mysql_native_password BY '*yourpassword*';
GRANT CREATE, ALTER, DROP, INSERT, UPDATE, DELETE, SELECT on chainletters.* TO 'clet_rw'@'localhost' WITH GRANT OPTION;
exit
```

Change dbPasswords.params to contain your username and password.

Testing:
```
mysql -h localhost -u clet_rw -p chainletters
show tables;
```
This should allow a connection and not show any tables.

## Database create and word loading

The word list used is located in dbCreate/wordlist, edit this as you see fit. It contains 147,789 British English words generated from the GitHub project https://github.com/cybrkyd/british-english-language-tools/tree/main/british-english-words

If you wish to regenerate this list, the following was performed on an Ubuntu system. It filters out all the words with 's on the end, and converts all words to lower case.
```
wget https://raw.githubusercontent.com/cybrkyd/british-english-language-tools/refs/heads/main/british-english-words/british-english-words/en-GB-words
grep -r '^[a-zA-Z]*$' en-GB-words | tr [A-Z] [a-z] | sort -u > wordlist
```
The latter part filters out words with various types of punctuation or numbers, e.g. 'AK47' or 'walkie-talkie' as these do not fit the rules of the game.


Create the database by running the python script:
```
python createDB.py
```
