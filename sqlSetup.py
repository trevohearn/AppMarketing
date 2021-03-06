#Trevor O'Hearn
#4/20/20
#SQL setup
#testing file using sqlite3 for local database

import sqlite3

#sqlite cursor
conn = sqlite3.connect('apps.db')


#methods

#creates table
def createTable(conn, table):
    cursor = conn.cursor()
    try:
        cursor.execute(table)
        conn.commit()
    except:
        print(table)
        print('table already exists')

#given cursor to connection of sql database, table name, and list of values
#add values to given table
#values must be in accordance with table parameters
def AddRow(cursor, tableName, valuesList):
    #values set to NOT NULL in apple schema
    c = cursor
    if (type(c) != sqlite3.Cursor):
        print('cursor not of sqlite3 type')
        return
    if (type(c) == sqlite3.Connection):
        c = c.cursor()
    if (valuesList[1] == None or valuesList[2] == None or valuesList[5] == None or valuesList[9] == None):
        print('Not Null value found in row {}'.format(valuesList[0]))
        return None

    deliminator = "', '"
    results = deliminator.join([str(x) for x in valuesList])
    #results = "'" + resultas + "'"
    sqlstr = """INSERT INTO '{}' VALUES ('{}');""".format(tableName, results)
    try:
        c.execute(sqlstr)
        print('success')
    except sqlite3.Error as e:
        print(tableName)
        print(e)
        print('couldnt add row')

#given connection to database and name of table
#retrieve rows from table based on condition
def getRows(conn, tableName, condition):
    cursor = conn.cursor()
    sqlstr = 'SELECT {} FROM {}'.format(condition, tableName)
    try:
        cursor.execute(sqlstr)
        return cursor.fetchall()
    except:
        print('couldnt retrieve data from {}'.format(tableName))
        return None
#tables

##apple

# "id" : App ID
# "track_name": App Name
# "size_bytes": Size (in Bytes)
# "currency": Currency Type
# "price": Price amount
# "ratingcounttot": User Rating counts (for all version)
# "ratingcountver": User Rating counts (for current version)
# "user_rating" : Average User Rating value (for all version)
# "userratingver": Average User Rating value (for current version)
# "ver" : Latest version code
# "cont_rating": Content Rating
# "prime_genre": Primary Genre
# "sup_devices.num": Number of supporting devices
# "ipadSc_urls.num": Number of screenshots showed for display
# "lang.num": Number of supported languages
# "vpp_lic": Vpp Device Based Licensing Enabled


apple_table = """
Create TABLE apple
(
name varchar(255),
id int(255) NOT NULL UNIQUE,
size int(255) NOT NULL,
currency varchar(255),
price DOUBLE(255, 2),
totalRatingCount int(255) NOT NULL,
userRating DOUBLE(255, 2),
contentRating varchar(255),
primeGenre varchar(255),
languages int(255) NOT NULL,
appDescription varchar(255)

);
"""

appleTestStr = ['app1', 1, 150000, 'USD', 4.99, 150,
 4.2, 'E', 'Games', 1, 'this is a test']
apple_desc_table = """
CREATE TABLE appleDescription
(

);
"""
##google
# App - Application name
# Category - Category the app belongs to
# Rating - Overall user rating of the app (as when scraped)
# Reviews - Number of user reviews for the app (as when scraped)
# Size - Size of the app (as when scraped)
# Installs - Number of user downloads/installs for the app (as when scraped)
# Type - Paid or Free
# Price - Price of the app (as when scraped)
# Content Rating - Age group the app is targeted at - Children / Mature 21+ / Adult
# Genres - An app can belong to multiple genres (apart from its main category). For eg, a musical family game will belong to Music, Game, Family genres.
# Last Updated - Date when the app was last updated on Play Store (as when scraped)
# Current Ver - Current version of the app available on Play Store (as when scraped)
# Android Ver - Min required Android version (as when scraped)

google_table = """
CREATE TABLE google
(
id int(255) NOT NULL UNIQUE,
name varchar(255),
primeGenre varchar(255),
rating DOUBLE(255, 1),
reviews int(255) NOT NULL,
size int(255) NOT NULL,
installs int(555) NOT NULL,
type varchar(255),
price DOUBLE(255, 2),
contentRating varchar(255),
subgenres varchar(255),
lastUpdated varchar(255),
currentVer varchar(255),
androidVer varchar(255),

);
"""
#app description needs to be in a different table


createTable(conn, apple_table)
createTable(conn, google_table)
addRow(conn, 'apple', appleTestStr)
stuffs = getRows(conn, 'apple')
print('this returned {}'.format(stuffs))


# Open cleaded google data csv file
# read in lnes with while loop
f = open(file='googleDF.csv', mode='r')

last_line = False
#break while loop when list is length 0
while last_line == False:
    cur = f.readline()
    values = (cur.split(','))[:-1]
    if (len(values) < 14):
        last_line == True
        break;
    else:
        addRow(c, 'google', values)

conn.close()
f.close()
#deal with rows that don't properly get added to table
#test written methods in testing_databases.ipynb
