from dataclasses import dataclass,field
from typing import List, Optional
from pprint import pprint
import json

test_case = """Attacker (Rotom-Frost) @ Life Orb  
Ability: Surge Surfer  
EVs: 248 HP / 252 SpA / 8 Spe  
Modest Nature  
IVs: 0 Atk  
- Rising Voltage  
- Blizzard  
- Nasty Plot  
- Pain Split  
"""

@dataclass
class Pokemon: 
   set_name: str = ""
   species: str = ""
   level: int = 100
   ability: str = ""
   item: str = ""
   nature: str = ""
   evs: dict = field(default_factory=dict)
   ivs: Optional[dict] = field(default_factory=dict)
   moves: List[str] = field(default_factory=list)
   def to_json(self):
      new_dict = self.__dict__
      species = new_dict['species']
      set_name = new_dict['set_name']
      del new_dict['species']
      del new_dict['set_name']
      double_quotes = json.dumps(new_dict)
      return '{{\"{0}\":{{\"{1}\":{2}}}}}'.format(species, set_name, double_quotes)



def paste_to_json(paste):
   mon = Pokemon()
   if len(paste) <= 0: raise Exception
   for line in paste.split("\n"):
      if "@" in line:
         mon.item = line.split("@")[-1].strip()
      if "(" in line:
         mon.species = line[line.index("(")+1:line.index(")")].strip()
         mon.set_name = line[0:line.index("(")-1].strip()
         print(f"FOUND POKEMON {mon.species} WITH THE SET {mon.set_name}")
      if "Ability" in line:
         mon.ability = line.split(":")[-1][1:].strip()
      if "EVs" in line:
         line = line.replace("Atk","at").replace("Def","df").replace("SpA","sa").replace("SpD","sd").replace("Spe","sp")
         _,evs_line = line.split(":")
         evs = [ev.strip() for ev in evs_line.split("/")]
         mon.evs = {stat.lower():value for value,stat in [ev.split(" ") for ev in evs]}
      if "Nature" in line:
         mon.nature = line.split("Nature")[0].strip()
      if "IVs" in line:
         line = line.replace("Atk","at").replace("Def","df").replace("SpA","sa").replace("SpD","sd").replace("Spe","sp")
         _,ivs_line = line.split(":")
         ivs = [iv.strip() for iv in ivs_line.split("/")]
         mon.ivs = {stat.lower():value for value,stat in [iv.split(" ") for iv in ivs]}
      if "- " in line:
         mon.moves.append(line[2:].strip())
   return mon.to_json()

#print(paste_to_json(test_case))