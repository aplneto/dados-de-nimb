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
  rxp_rolagem = "(?:^\\b(?:(?:[\+\-]?\d+d\d+(?:(?:(?:kl?|th?)\d+)(?:c[sf]\d+)?)?)|(?:[\+\-]?[\d]+))+\\b$)"
  # Regex do formato da string de teste
  rxp_teste = "(?:[\+\-]?\d+d\d+[><]\d*)+"
  def __init__(self):
    pass

  @staticmethod
  def rolar(string_dados: str):
    '''
    Converte o formato da string para os dados e modificadores apropriados,

    Ex: decifrar_rolagem("1d6+4-2") retorna uma rolagem aleatória entre 1 e 6,
      soma 4 e subtrai 2 do resultado

    Retorna um dicionário contendo as chaves valor, rolagens, mods e crit
    '''
    dados = re.findall("\\b(?:[\+\-]?\d+d\d+(?:(?:(?:kl?|th?)\d+)(?:c[sf]\d+)?)?)\\b", string_dados)
    rolagens = []
    soma = 0
    criticos = []
    modificadores = re.findall("[\+\-]?\\b[\d]+\\b", string_dados)
    for dado in dados:
        resultado, rolagem, c = Dados.__decifrar_rolagem(dado)
        if len(criticos) == 0:
            criticos.append(c)
        rolagens.append(rolagem)
        soma += resultado
    for m in [int(x) for x in modificadores]:
        soma += m

    return {
      'valor': soma,
      'rolagens': rolagens,
      'mods': modificadores,
      'crit': criticos[0]
      }

  @staticmethod
  def __decifrar_rolagem(string_rolagem: str, **kwargs):
    '''
    Converte uma string de rolagem em um valor numérico
    '''
    opt = re.findall('(?:(?:kl?|th?)\d+)(?:c[sf]\d+)?', string_rolagem)
    opt = opt[0] if len(opt)>0 else ""
    resultados = []
    soma = critico = 0
    rolagens, dado = re.findall("\\b\d+d\d+", string_rolagem)[0].split('d')
    for x in range(int(rolagens)):
        resultados.append(random.randint(1, int(dado)))
    soma, critico = Dados.avaliar_soma(resultados, opt, dado)
    return soma, resultados, critico

  @staticmethod
  def avaliar_soma(dados: list, options: str, maximo: int):
    dados.sort(reverse=True)
    n = int(re.sub('(?:kl?|th?)', '', re.findall('(?:kl?|th?)\d+', options)[0])) if options else 0
    if 'k' in options:
        useful = dados[len(dados) - n:] if ('l' in options) else dados[:n]
    elif 't' in options:
        useful = dados[n:] if ('h' in options) else dados[:len(dados) - n]
    else:
        useful = dados
    total = sum(useful)

    # Determinando se o ataque foi acerto ou falha crítica
    critico = 0
    cs = int(maximo) if not 'cs' in options else int(re.sub('cs', '', re.findall('cs\d+', options)[0]))
    cf = 1 if not 'cf' in options else int(re.sub('cf', '', re.findall('cf\d+', options)[0]))
    if dados[0] >= cs:
         critico = 1
    elif dados[0] <= cf:
        critico = -1

    return total, critico
    

  @staticmethod
  def testar(string_rolagens):
    '''
    Retorna o número de sucessos e oo resultados de todos os testes
    '''
    dados = re.findall('(?:[\+\-]?\d+d\d+[><]\d*)', string_rolagens)
    sucessos = 0
    rolagens = []
    dificuldades = []
    for rolagem in dados:
        s, r, d = Dados.avaliar_teste(rolagem)
        sucessos += s
        rolagens.append(r)
        dificuldades.append(r)
    return sucessos, rolagens, dificuldades
  
  @staticmethod
  def avaliar_teste(string_rolagem):
    '''
    Retorna o número de sucessos e os resultados parciais do teste
    '''
    resultados = []
    sucessos = 0
    rolagens, dado = re.findall("\\b\d+d\d+", string_rolagem)[0].split('d')
    dificuldade = int(re.sub('[><]', '', re.findall('[><]\d*', string_rolagem)[0]))
    for n in range(int(rolagens)):
        r = random.randint(1, int(dado))
        if '>' in string_rolagem:
            sucessos += 1 if r >= dificuldade else 0
        elif '<' in string_rolagem:
            sucessos += 1 if r <= dificuldade else 0
        resultados.append(r)
    return sucessos, resultados, dificuldade

  @staticmethod
  def teste_alpha(dificuldade: int):
    '''
    Faz um teste rápido como o do 3d&t Alpha 1d6<=dificuldade
    '''
    d6 = random.randint(1, 6)
    critico = 0
    
    if d6 == 1:
        critico = 1
    elif d6 == 6:
        critico = -1
    
    sucessos = 1 if d6 <= dificuldade else 0
    return sucessos, [d6], critico