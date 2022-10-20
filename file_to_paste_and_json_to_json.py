import pastestojson
import json
import sys
from pprint import pprint
import collections.abc

def update(d, u):
    for k, v in u.items():
           if isinstance(v, collections.abc.Mapping):
                  d[k] = update(d.get(k, {}), v)
           else:
                  d[k] = v
    return d




if len(sys.argv) <= 1:
   print("Usage: ftpajtj.py <path to a file with pastes>")
   sys.exit()

with open(sys.argv[1],"rt") as file:
   sets = file.read().split("\n\n")
with open("db.json","r") as file:
   current_sets = json.load(file)

for pkmn_set in sets:
   jsoned = pastestojson.paste_to_json(pkmn_set)
   set_as_dict = json.loads(jsoned)
   pprint(set_as_dict)
   # Check if a relative duplicate already exists
   species = list(set_as_dict.keys())[0]
   set_name = list(set_as_dict[species].keys())[0]
   break_inner = False
   for added_setname in current_sets[species]:
      iterated_set = current_sets[species][added_setname]
      # If at least 2 moves and the ability are the same call it a dupe 
      moves = set(set_as_dict[species][set_name]['moves'])
      if len(set(iterated_set['moves']) & moves) >= 2 and iterated_set['ability'] == set_as_dict[species][set_name]['ability']:
         print("FOUND A DUPE!")
         print(added_setname,species,end="")
         print(" is possibly in the database already.")
         break_inner = True
         break
   if break_inner: break
   update(current_sets, set_as_dict)

with open("db.json","w+") as file:
   file.write(json.dumps(current_sets))