# Dados e rolagens

Bot simples de rolagm de dados para discord

## Comandos

### !rolar *string_de_rolagem* *efeito*
Faz a rolagem descrita pela string, pode conter dados, modificadores e operações de soma e subtração entre números e dados, além de opções avançadas de rolagem (veja a tabela adiante), retornando a soma dos valores.
Pode também ser usada para testes, podendo conter comparações matemáticas como "<" e ">" e opções avançadas de rolagem e retorna a quantidade de sucessos resultante do teste

#### Rolagens
opção|descrição|exemplo
--|--|--
k|Essa opção permite manter apenas os n dados de maior valor para o resultado final. |`3d6k2` rola 3d6 e mantém apenas os dois maiores valores na soma final.
t|Ao contrário da opção `k`, essa opção permite descartar os n menores valores do resultado final.|`3d6t2` rola 3d6 e descarta os dois menores resultados.
kl|Funciona como a opção k, mas mantém apenas os menores resultados|`3d6k2` rola 3d6 e mantém apenas os dois menores resultados na soma final.
th|Funciona como a opção t, mas descarta os maiores valores|`3d6th2` rola 3d6 e mantém apenas o menor resultados.
cs|Define o valor  que é considerado para o cálculo do acerto crítico, considerando apenas o primeiro dado para definir se o acerto é ou não crítico|`3d6cs5` rola 3d6 e considera o teste como acerto crítico se o primeiro dado for 5 ou maior.
cf|Define o valor que é considerado para o cálculo de falha crítica, considerando apenas o primeiro dado para definir se o teste é ou não uma falha crítica|`3d6cf2` rola 3d6 e considera o teste como uma falha crítica se o primeiro dado for 2 ou menor.

#### Testes
opção|descrição|exemplo
--|--|--
k|Essa opção permite manter apenas os n dados de maior valor para o resultado final. |`3d6>2k2` rola 3d6 e mantém apenas os dois maiores valores para calcular a quantidade de sucessos.
t|Ao contrário da opção `k`, essa opção permite descartar os n menores valores do resultado final.|`3d6<5t2` rola 3d6 e descarta os dois menores resultados para calcular a quantidade de sucessos.

#### Efeitos

Os efeitos são bônus ou penalidades que o valor final do teste recebe condicionalmente. Podem ser os seguintes:

condicional|descrição|exemplo
--|--|--
c|Adiciona um modificador caso o resultado rolado seja um acerto crítico | `c+4` caso o teste seja  um acerto crítico, o valor final recebe +4
f|Adiciona um modificador caso o resultado rolado seja uma falha crítica | `f-3` caso o personagem um teste seja uma falha crítia, o valor final recebe -3

### !salvar *apelido* *string_de_rolagem*

Salva uma rolagem específica com um apelido que pode ser usado por qualquer jogador da mesa, mas apenas mestres podem usar esse comando. Caso uma rolagem já exista, seu valor é atualizado.

`!salvar bola_de_fogo 2d6+5`

### !rolagem *apelido*

Executa uma rolagem específica salva anteriormente pelo mestre.

`!rolagem bola_de_fogo`

### !listar_rolagens

Lista todas as rolagens da mesa  seus apelidos

### !apagar *apelido*

Apaga uma rolagem salva na mesa. Apenas mestres podem usar esse comando

`!apagar bola_de_fogo`

<!--
TODO:

[ ] Efeitos de rolagens
[ ] !salvar apelido string_de_rolagem
[ ] !rolagem *apelido*
[ ] !listar_rolagens
[ ] !apagar *apelido*
[ ] modificar o comando !help

-->