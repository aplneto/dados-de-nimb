'''
Esse script trata a invocação de dados
'''

import random
import re

def decifrar_rolagem(string_dados: str):
  '''
  Converte o formato da string para os dados e modificadores apropriados,

  Ex: decifrar_rolagem("1d6+4-2") retorna uma rolagem aleatória entre 1 e 6,
    soma 4 e subtrai 2 do resultado

  Retorna uma tupla contendo três elementos:
    [0] lista contendo as rolagens, que por si são listas de inteiros
    [1] lista contendo os modificadores
    [2] total da rolagem
  '''
  dados = re.findall("[\+\-]?\d+d\d+", string_dados)
  rolagens = []
  soma = 0
  modificadores = re.findall("[\+\-]?\\b[\d]+\\b", string_dados)
  for dado in dados:
    rolagem, resultado = rolar(dado)
    rolagens.append(rolagem)
    soma += resultado
  for m in [int(x) for x in modificadores]:
    soma += m
  return rolagens, modificadores, soma


  

def rolar(string_rolagem: str):
  '''
  Converte uma string de rolagem em um valor numérico
  '''
  resultados = []
  rolagens, dado = string_rolagem.replace("+","").replace("-","").split('d')
  soma = 0
  print(rolagens)
  for x in range(int(rolagens)):
    resultados.append(random.randint(1, int(dado)))
    soma += resultados[x]
  if string_rolagem.startswith('-'):
    resultados = -resultados
  return resultados, soma