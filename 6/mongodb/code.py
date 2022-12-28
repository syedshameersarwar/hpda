#!/usr/bin/python3
import re
import pymongo
from pymongo import MongoClient

client = MongoClient('localhost', 27017)

db = client['wikipedia']

# Creating articles collection
articles = db['articles']

# Creating indices
articles.create_index([('title', pymongo.ASCENDING)])
articles.create_index([('text', 'text')])

articles.insert_one({
    'title': 'Databases',
    'text': 'In computing, a database is an organized collection of data stored and accessed electronically. Small databases can be stored on a file system, while large databases are hosted on computer clusters or cloud storage',
    'categories': ['Database', 'Computer Science'],
    'links': ['NoSQL']
})


articles.insert_one({
    'title': 'NoSQL',
    'text': 'A NoSQL (originally referring to "non-SQL" or "non-relational")[1] database provides a mechanism for storage and retrieval of data that is modeled in means other than the tabular relations used in relational databases',
    'categories': ['Database', 'Computer Science'],
    'links': ['Databases', 'MongoDB']
})

articles.insert_one({
    'title': 'MongoDB',
    'text': 'MongoDB is a popular NoSQL database...',
    'categories': ['Database', 'Computer Science', 'Document Storage'],
    'links': ['Databases', 'NoSQL']
})


# Find all documents in the articles collection
print("\nFinding all documents in the articles collection")
cursor = articles.find()
for document in cursor:
    print(document)

# Find all documents with the title "MongoDB"
print("\nFinding all documents with the title \"MongoDB\"")
cursor = articles.find({'title': 'MongoDB'})
for document in cursor:
    print(document)

# Find all documents with the title containing "NoSQL"
cursor = articles.find({"title": re.compile('NoSQL')})
print("\nFinding all documents with the title containing \"NoSQL\"")
for document in cursor:
    print(document)

# Find all documents with the text containing "NoSQL"
print("\nFinding all documents with the text containing \"NoSQL\"")
cursor = articles.find({"$text": {"$search": "NoSQL"}})
for document in cursor:
    print(document)


# Find all documents with the category "Databases"
print("\nFinding all documents with the category \"Databases\"")
cursor = articles.find({'categories': 'Database'})
for document in cursor:
    print(document)
