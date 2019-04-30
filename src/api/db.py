# == Intention ==

"""
Helper functions for accessing a firebase database.
"""

""" 
**Pyrebase** is a fun little pythonic library for accessing firebase. <br>
We need to specify the [pyrebase4](https://github.com/nhorvath/Pyrebase4) fork though.
The main project is no longer maintained. Additionally, pyrebase doesn't have access
to the newer firebase Firestore database, only the older Realtime Database.
"""
import pyrebase

# **environs** gives us handy tools for handling environment variables
from environs import Env

"""
Create an Env instance, and with it, read the file with our
API keys. It defaults to searching for a file with the name *.env*, but we could 
point it elsewhere if necessary.
"""
env = Env()
env.read_env()

"""
Our firebase configuration settings. <br>
The strange one is the **serviceAccount** which points to a json file with additional creds
this gives the application admin access to the db so we can make changes w/o needing explicit permissions.
"""
config = {
  "apiKey": env("FIRE_APIKEY"),
  "authDomain": env("FIRE_AUTH_DOMAIN"),
  "databaseURL": env("FIRE_DB_URL"),
  "storageBucket": env("FIRE_STORAGE_BUCKET"),
  "serviceAccount": env("FIRE_SERVICE_ACCOUNT")
}

# The base connection to firebase.
firebase = pyrebase.initialize_app(config)

"""
The specific connection to our firebase Realtime Database. <br>
**All writes** to the database will pass through this connection on the server.
[ The [svelte](svelte.dev) application in the browser will only have read access to firebase ]
"""
db = firebase.database()

def get_all_documents(root_name):
  """
  Given a document root as stored in the db,
  this function will return an array of all child documents. <br>
  **Example:** <br>
  `get_all_documents('stories')` <br>
  \>> [{'id' : 'SR13', 'title': 'The Fifth Season'},
      {'id' : 'SR14', 'title' : 'Provenance'} ...]
      <br>

  * **root_name** : <string> The root of the document tree ('stories', 'chapters', etc.)
  """
  # Using our db connection, get all documents with the root, **root_name**
  documents = db.child(root_name).get()
  
  # The **doc_list** will eventually be a list of document objects
  # formatted in a more workable manner than the OrderedDicts that we get. \* <br> 
  doc_list = []

  for doc in documents.each():
    """
    **documents** are an OrderedDict containing the results of our query. 
    Each **doc** within it has a key and a val. The key is the document id, which
    we'll use to reference the document for db manipulation later, and the val
    contains the document object itself. That'll be things like the 'title', 
    'username', 'chapter_list'
    """
    doc_object = doc.val()
    doc_object['id'] = doc.key()
    doc_list.append(doc_object)

  return doc_list
 

# \* I hope that I don't end up missing out on something special here.