'''
Estrutura de dados de personagens
'''

class Personagem:
  def __init__(self, **kwargs):
    resgatar_attr = lambda attr: kwargs.get(attr, default=0)
    self.forca = resgatar_attr("f")
    self.habilidade = resgatar_attr("h")
    self.resistencia = resgatar_attr("r")
    self.armadura = resgatar_attr("a")
    self.poder_de_fogo = resgatar_attr("pdf")