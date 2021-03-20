import alpha.personagens

pasta_dos_personagens = "personagens/"

import json

template = pasta_dos_personagens + "template.json"
with open(template) as tmp:
  modelo = json.load(tmp)

print(modelo)