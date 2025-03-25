# Database query and loading utilities
import mysql.connector

passwdFile="dbPassword.params"
dbDefs={
    "host":"localhost",
    "username":"",
    "password":"",
    "dbname":"chainletters"
}

global dbObj, dbCur # Global objects for Database object and connector
cc=0;    # Commit counter, see submit()

def dbConnect():
    global dbObj, dbCur
    # Connect to the database and set dbObj object
    print("Connecting to database")
    
    # Open password file
    print("  Opening password file")
    
    try:
        with open(passwdFile, "r") as f:
            data = f.read().split("\n")
    except Exception as e:
        print("ERROR: Unable to open database password file \"{}\". Make sure it exists and has the correct permissions".format(passwdFile))
        print(e)
        exit(1)

    for lines in data:
        #print("Line: ", lines)
        line = lines.split("=")
        if(len(line)==2):
            # Ignore anything that is not something=something format
            dbDefs[line[0]]=line[1]
            
    #print(dbDefs)
    
    # Connect to database
    try:
        dbObj = mysql.connector.connect(
            host=dbDefs["host"],
            user=dbDefs["username"],
            password=dbDefs["password"],
            database=dbDefs["dbname"]
        )
        dbCur=dbObj.cursor()
        
    except Exception as e:
        print("Error connecting to database: ", e)

def close():
    dbObj.close()
    
def submit(sql, commit=0):
    # Generic function for database submission where a response is not expected
    # e.g., INSERT
    # If commit is 0 (default) it will commit every line. If commit is greater
    # than 0 it will commit every n times this is called.
    global cc
    
    #print("Commit = {}, cc={}".format(commit, cc))
    #print(sql)
    try:
        dbCur.execute(sql)
        cc+=1
        if cc>=commit:
            dbObj.commit()      # Not every query needs this
            cc=0
    except Exception as e:
        print("Database query error: ", e)
        
def commit():
    # Called at the end of a batch session if the batch limit was not reached
    # with the last one
    dbObj.commit()