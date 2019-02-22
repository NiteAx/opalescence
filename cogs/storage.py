from tinydb import TinyDB, Query 
from pathlib import Path

parentdir = Path('../')
dbdir = str(parentdir / 'db.json')
db  = TinyDB(dbdir) 

"""
Proposed data structure
{'cog': 'parser', 'name': 'whitelist1', 'category': 'template', 'value': 'discord.gg\/[a-zA-Z]+'}
{'cog': 'parser', 'name': 'whitelist1', 'category': 'exception', 'value': 'discord.gg/AbC'}
{'cog': 'parser', 'name': 'whitelist1', 'category': 'exception', 'value': 'discord.gg/xYz'}
{'cog': 'parser', 'name': 'whitelist2', 'category': 'template', 'value': 'otherfilter'}
{'cog': 'parser', 'name': 'whitelist2', 'category': 'exception', 'value': 'othervalue'}
{'cog': 'cog_name', 'name': 'whateverThey'reStoring', 'category': 'blah', 'value': 'something'}
.
.
.
"""

def Insert(data): #Correct formatting is the duty of the cog calling this function.
  try:
    db.insert(data)
    return True
  except Exception as e:
    print(f'Failed to Insert into database.\n Exception: {e}\n Data: {data}\n')
    return False

def Update(olddata, newdata): #Correct formatting is the duty of the cog calling this function.
  try:
    q = Query()
    # Update(what to update with, condition of where to update)
    db.update(newdata, (q.cog == olddata.cog) & (q.category == olddata.category) & (olddata.value == olddata.value))
    return True
  except Exception as e:
    print(f'Failed to Update database.\n Exception: {e}\n Old data: {olddata}\n New data: {newdata}\n')
    traceback.print_exc()
    return False

#I don't think we need a function where you can delete everything by one cog.

def RemoveCN(cog, name): #Remove all values by exact name
  try:
    q = Query()
    db.remove((q.cog == cog) & (q.name == name))
    return True
  except Exception as e:
    print(f'Failed to Remove from database.\n Exception: {e}\n')
    traceback.print_exc()
    return False

def RemoveCNC(cog, name, category): #Remove all values by exact name and category
  try:
    q = Query()
    db.remove((q.cog == cog) & (q.name == name) & (q.category == category))
    return True
  except Exception as e:
    print(f'Failed to Remove from database.\n Exception: {e}\n')
    traceback.print_exc()
    return False

def RemoveCCV(cog, category, value): #Remove all values by exact category and value
  try:
    q = Query()
    db.remove((q.cog == cog) & (q.category == category) & (q.value == value))
    return True
  except Exception as e:
    print(f'Failed to Remove from database.\n Exception: {e}\n')
    #traceback.print_exc()
    return False

def RemoveCNCV(cog, name, category, value): #Remove all values by exact name, category and value
  try:
      q = Query()
      db.remove((q.cog == cog) & (q.name == name) & (q.category == category) & (q.value == value))
      return True
  except Exception as e:
      print(f'Failed to Remove from database.\n Exception: {e}\n')
      traceback.print_exc()
      return False

def QueryC(cog):
  q = Query()
  result = db.search(q.cog == cog)
  if result == []:
    return False
  return result

def QueryCN(cog, name):
  q = Query()
  result = db.search((q.cog == cog) & (q.name == name))
  if result == []:
    return False
  return result

def QueryCC(cog, category):
  q = Query()
  result = db.search((q.cog == cog) & (q.category == category))
  if result == []:
    return False
  return result

def QueryCNC(cog, name, category):
  q = Query()
  result = db.search((q.cog == cog) & (q.name == name) & (q.category == category))
  if result == []:
    return False
  return result

def QueryCNCV(cog, name, category, value):
  q = Query()
  result = db.search((q.cog == cog) & (q.name == name) & (q.category == category) & (q.value == value))
  if result == []:
    return False
  return result