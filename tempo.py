#
# tempo.py : Olimpíada Brasileira de Informática – OBI2021 – Prog. Nível 2 – Fase Fase 1
#            Uma solução para o problema 'Tempo de resposta', páginas 5-6
# Github   : 
# data     : 02/07/2021
# autor    : Professor Flávio Augusto de Freitas,
#            IFSEMG/DACC/Ciência da Computação
# linguagem: Python 3.9.1 64-bit
# hardware : MacBook Pro (Retina, 13-inch, Mid 2014)
#            mac OS Big Sur 11.4
#            2,6 GHz Intel Core i5 Dual-Core
#            8 GB 1600 MHz DDR3
#
#
from typing import Final

_ttresp : Final = 0 # constante que indica a posição do tempo total de resposta
_tmsgsnr: Final = 1 # constante que indica a posição do total de mensagens não respondidas
#
# criar os arquivos de entrada e saída
#
# arqNprova.[in | sol] = arquivos do pdf da prova, N = número
# arqNobi.[in | sol]   = arquivos do solver da OBI, N = número
#
fin  = open('arq2prova.in' , 'r') # arquivo de entrada
fout = open('arq2prova.sol', 'w') # arquivo de saída

#
# dicionário temporário que armazenará os tempos de cada evento
# {
#   amigo: [tempo de resposta, msgs sem resposta], # número do amigo
#   amigo: [tempo de resposta, msgs sem resposta], # tempo total em segundos
#   amigo: [tempo de resposta, msgs sem resposta]  # total de mensagens não respondidas
# }
#
temp_saida = {} # dicionário temporário {amigo: [tempo de resposta, msgs sem resposta]}
temp_eventos = [] # eventos temporário R x, E x, T x

n = int(fin.readline()) # número de registros de eventos está na primeira linha

#
# primeira restrição: o número de registros deve estar entre 1 e 20
#
if n >= 1 and n <= 20:
  temp_eventos = fin.readlines() # lê os eventos
  eventos = [] # lista com os eventos [['R', 3], ['T', 5]]

  # criar uma lista com os eventos formatados
  for i in range(n):
    r_e_t  = (temp_eventos[i].split(' ')[0]).rstrip() # R, E, T
    x = int((temp_eventos[i].split(' ')[1]).rstrip()) # amigo ou tempo
    eventos.append([r_e_t, x])
  # print(eventos)

  # criar um dicionário com todos os amigos únicos (não repetidos)
  for i in range(n):
    r_e_t  = eventos[i][0] # R, E, T
    x = eventos[i][1] # amigo ou tempo

    # segunda restrição: o número do amigo deve estar entre 1 e 100
    if (r_e_t == 'R' or r_e_t == 'E') and x >= 1 and x <= 100:
      try:
        _ = temp_saida[x]
      except:
        temp_saida[x] = [0, 0] # {amigo: [tempo de resposta, msgs sem resposta]}

    # segunda restrição: o número do amigo deve estar entre 1 e 100
    elif (r_e_t == 'R' or r_e_t == 'E') and (x < 1 or x > 100):
      print("ERRO: Número do amigo deve estar entre 1 e 100...")
      exit

  # como o dicionário temp_saida é desordenado, criamos outro dicionário ordenado
  saida = dict(sorted(temp_saida.items())) # dicionário de saída ordenado

  # selecionar um amigo por vez no dicionário
  # saida = {12: [0,1], 23: [0,0], 34: [0,0], 45: [0,0]}
  for amigo in saida:
    i = 0 # para cada amigo no dicionário, percorrer todos os eventos desde o início
    r_e_t = eventos[i][0] # R, E, T
    x = eventos[i][1] # amigo ou tempo

    # encontrar a primeira mensagem recebida do amigo atual no dicionário
    # marcar sua posição na variável i
    while True:
      if not(r_e_t == 'R' and x == amigo):
        i = i + 1
        r_e_t = eventos[i][0] # R, E, T
        x = eventos[i][1] # amigo ou tempo
      else:
        break
    
    saida[amigo][_tmsgsnr] += 1 # mais uma mensagem não respondida

    # percorrer o restante dos eventos calculando o tempo total
    # e o balanço entre mensagens recebidas e enviadas
    ## print(amigo, ":")
    # saida = {12: [5,1], 23: [0,0], 34: [0,0], 45: [0,0]}
    j = i + 1
    while j < n:
      r_e_t = eventos[j][0] # R, E, T
      x = eventos[j][1] # amigo ou tempo
      if saida[amigo][_tmsgsnr] != 0 and (r_e_t == 'E' or r_e_t == 'R') and eventos[j - 1][0] != 'T' and x != amigo:
        ## print("\t1 >>> ", j, r_e_t, x)
        saida[amigo][_ttresp] += 1 # adiciona 1 segundo no tempo total
      elif r_e_t == 'T':
        ## print("\t2 >>> ", j, r_e_t, x)
        saida[amigo][_ttresp] += x # adiciona x segundos no tempo total
      elif saida[amigo][_tmsgsnr] != 0 and r_e_t == 'E' and x == amigo:
        ## print("\t3 >>> ", j, r_e_t, x)
        if eventos[j - 1][0] != 'T':
          saida[amigo][_ttresp] += 1 # adiciona 1 segundo no tempo total
        saida[amigo][_tmsgsnr] -= 1 # uma mensagem respondida
        
        # tenta encontrar a próxima mensagem recebida do mesmo amigo
        j = j + 1
        while j < n:
          r_e_t = eventos[j][0] # R, E, T
          x = eventos[j][1] # amigo ou tempo
          if r_e_t == 'R' and x == amigo:
            saida[amigo][_tmsgsnr] += 1 # uma mensagem não respondida
            break
          else:
            j = j + 1
      j = j + 1

  # gerar o arquivo de saída
  # saida = { 12: [13, 0], 23: [8, 0], 34: [2, 0], 45: [8, 1]}
  for amigo in saida:
    fout.write(f'{amigo} {saida[amigo][_ttresp] if saida[amigo][_tmsgsnr] == 0 else -1}\n')
  
else:
  print("ERRO: Número de registros deve estar entre 1 e 20...")

# fechar os arquivos
fin.close
fout.close