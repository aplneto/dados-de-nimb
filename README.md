# Dados e rolagens

[Discord Invite link](https://discord.com/api/oauth2/authorize?client_id=822648071867465748&permissions=2147743808&scope=bot)

[Repl.it repository](https://replit.com/@paulinolimakl/Dados-de-Nimb)

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

Os efeitos são bônus ou penalidades que o valor final do teste recebe condicionalmente. Podem ser os seguintes:

condicional|descrição|exemplo
--|--|--
c|Adiciona um modificador caso o resultado rolado seja um acerto crítico | `c+4` caso o teste seja  um acerto crítico, o valor final recebe +4
f|Adiciona um modificador caso o resultado rolado seja uma falha crítica | `f-3` caso o personagem um teste seja uma falha crítia, o valor final recebe -3

#### Testes
opção|descrição|exemplo
--|--|--
k|Essa opção permite manter apenas os n dados de maior valor para o resultado final. |`3d6>2k2` rola 3d6 e mantém apenas os dois maiores valores para calcular a quantidade de sucessos.
t|Ao contrário da opção `k`, essa opção permite descartar os n menores valores do resultado final.|`3d6<5t2` rola 3d6 e descarta os dois menores resultados para calcular a quantidade de sucessos.

### !salvar *apelido* *string_de_rolagem*

Salva uma rolagem específica com um apelido que pode ser usado por qualquer jogador da mesa, mas apenas mestres podem usar esse comando. Caso uma rolagem já exista, seu valor é atualizado.
As rolagens usadas com esse comando são associadas ao canal em que foram usadas.

`!salvar bola_de_fogo 2d6+5`

### !rolar *apelido*

Executa uma rolagem específica salva anteriormente pelo mestre ou uma rolagem favorita do jogador, tendo prioridade a rolagm da mesa.

`!rolar bola_de_fogo`

### !rolagens

Lista todas as rolagens da mesa

### !consultar *apelido*

Checa se a rolagem específica existe

`!consultar bola_de_fogo`

### !apagar *apelido*

Apaga uma rolagem salva na mesa. Apenas mestres podem usar esse comando

`!apagar bola_de_fogo`

### !lembrar *apelido* *string_de_rolagem*

Salva uma rolagem específica com um apelido que pode ser usado por você, pode ser usado por qualquer membro jogador. Caso uma rolagem já exista, seu valor é atualizado.

`!lembrar "Ataque Especial" 1d12+5 c+6`

### !favoritas

Lista todas as suas rolagens

### !esquecer *apelido*

Apaga uma rolagem salva por você
