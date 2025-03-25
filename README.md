# chainletters
Scripts and utils for a popular word game. Add, remove or change a single character in a word to make another one.

For example:
*Add some examples here*
  
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

## Prerequisites
Python 3
Python 3 MySQL connector
```
python -m pip install mysql-connector-python
or
sudo apt install python3-mysql.connector
```

## Database set up and word loading

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

Change dbPasswords.params to contain your username and password. Optionally you can add add parameters to change the database name and the server, e.g:
```
username=clet_rw
password=badPassword
host=192.168.1.10
dbname=mychain
```

Testing:
```
mysql -h localhost -u clet_rw -p chainletters
show tables;
```
This should allow a connection and not show any tables.
