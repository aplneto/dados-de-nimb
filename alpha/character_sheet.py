import dados


class CharacterSheet:
  def __init__(self, F=0, H=0, R=0, A=0, PdF=0, **keywords):
    self.__F = F
    self.__H = H
    self.__R = R
    self.__A = A
    self.__PdF = PdF

def atacar(self):
  rolagem = dados.Dados.rolar(f"1d6+{self.__F}+{self.__H}")
  FA = rolagem['total']
  if rolagem['critico']:
    FA += self.__F