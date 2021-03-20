'''
Esse script trata a invocação de dados

As rolagens devem ser feitas a partir de strings de rolagem padrão, usando o formato [x]d[n], onde o x representa o número de dados a ser rolados e o [n] representa o número de faces do dado.
É possível adicionar modificadores com dados ou números inteiros, por exemplo:

A rolagem 1d6+3, rola um dado de seis lados e soma 3 ao resultado;
A rolagem 2d6-1d6, rola dois dados de seis lados e subtrai do resultado o valor de um outro dado de seis lados

Desde que as regras sejam mantidas, é possível rolar qualquer combinação de dados e modificadores

A string de opções contem configurações da rolagem. Por exemplo:

Options:
  cs = critical success
  cf = critical failure
  k = keep highest
  t = throw lowest
  kl = keep lowest
  th = throw highest

'''

import random
import re

class Dados:
  # Regex do formato da string de rolagem
  rxp_rolagem = "(?:^\\b(?:(?:[\+\-]?\d+d\d+(?:(?:(?:kl?|th?)\d+)(?:c[sf]\d+)?)?)|(?:[\+\-]?[\d]+)){1,}\\b$)"
  # Regex do formato da string de teste
  rxp_teste = "(?:[\+\-]?\d+d\d+[><]\d*)+"
  def __init__(self, string_rolagem=""):
    self.__string_rolagem = string_rolagem
    self.__rolagem = False
    self.__dados = []
    self.__modificadores = []
    self.__valor = 0
  
  @property
  def rolagem(self):
    return self.__rolagem

  @property
  def dados(self):
    return self.__dados
  
  @property
  def valor(self):
    return self.__valor
  
  @property
  def modificadores(self):
    return self.__modificadores
  
  def rolar_inplace(self, string_rolagem=""):
    if not bool(re.match(Dados.rxp_rolagem, string_rolagem)):
      raise ValueError
    '''
    Realiza todos os procedimentos de rolagem, modificando os valores apropriados
    '''
    self.__rolagem = True
    string_rolagem = self.__string_rolagem if not string_rolagem else string_rolagem
    self.__string_rolagem = string_rolagem
    valor, rolagens, modificadores = Dados.decifrar_rolagem(string_rolagem)
    self.__dados = rolagens
    self.__modificadores = modificadores
    self.__valor = valor

  def __repr__(self):
    return f"Dados({self.__string_rolagem})"

  @staticmethod
  def rolar(string_dados: str):
    '''
    Converte o formato da string para os dados e modificadores apropriados,

    Ex: decifrar_rolagem("1d6+4-2") retorna uma rolagem aleatória entre 1 e 6,
      soma 4 e subtrai 2 do resultado

    Retorna uma tupla contendo três elementos:
      [0] total da rolagem
      [1] lista contendo as rolagens, que por si são listas de inteiros
      [2] lista contendo os modificadores
    '''
    dados = re.findall("\\b(?:[\+\-]?\d+d\d+(?:(?:(?:kl?|th?)\d+)(?:c[sf]\d+)?)?)\\b", string_dados)
    rolagens = []
    soma = 0
    modificadores = re.findall("[\+\-]?\\b[\d]+\\b", string_dados)
    for dado in dados:
      resultado, rolagem = Dados.__decifrar_rolagem(dado)
      rolagens.append(rolagem)
      soma += resultado
    for m in [int(x) for x in modificadores]:
      soma += m
    return soma, rolagens, modificadores

  @staticmethod
  def __decifrar_rolagem(string_rolagem: str, **kwargs):
    '''
    Converte uma string de rolagem em um valor numérico
    '''
    opt = re.findall('(?:(?:kl?|th?)\d+)(?:c[sf]\d+)?', string_rolagem)
    opt = opt[0] if len(opt)>0 else ""
    resultados = []
    soma = 0
    rolagens, dado = re.findall("\\b\d+d\d+", string_rolagem)[0].split('d')
    for x in range(int(rolagens)):
      resultados.append(random.randint(1, int(dado)))
    if (opt):
      m = re.findall('(?:kl?|th?)\d+', string_rolagem)[0]
      m = re.sub('(?:(?:kl?)|(?:th?))', '', m)
      m = int(m)
      if 'k' in opt:
        rv = not('l' in opt)
        l = resultados.copy()
        l.sort(reverse=rv)
        l = l[:m]
      else:
        rv = 'h' in opt
        l = resultados.copy()
        l.sort(reverse=False)
        l = l[m:]
    else:
      l = resultados
    for num in l:
      soma += num
    if string_rolagem.startswith('-'):
      soma = -soma
    return soma, resultados

  @staticmethod
  def testar(string_rolagem):
    pass