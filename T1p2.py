import sys

# Extrai os campos "protocolo", "porta de destino"
# e SID da linha, retornando-os em um array
def parseInfoFromLine(line):
  info = line.strip('\n').split(' ')
  if len(info) < 8 or info[1] != 'alert':
    return None
  return [info[2], info[7], getSidFromLine(line)]

# Extrai o SID de uma linha da entrada
def getSidFromLine(line):
  startIndex = line.find(' sid:')
  endIndex = startIndex + line[startIndex:-1].find(';')
  return line[startIndex:endIndex].split(':')[1]

# Monta o mapa de SIDs a partir do
# arquivo sid-msg.map
def buildSidMap():
  file = open('sid-msg.map', 'r')
  sidMap = {}
  for line in file:
    sid, description = line.strip('\n').split(' || ')[0:2]
    sidMap[sid] = description
  return sidMap

# Mapa para transformação do
# protocolo em número
protocolMap = {
  'ip'  : 0,
  'tcp' : 1,
  'udp' : 2,
  'icmp': 3,
}

# Caso o arquivo de entrada não seja passado
# por parâmetro, sai do programa
if len(sys.argv) < 2:
  print('ERRO: Arquivo de entrada não encontrado')
  exit()

# Abertura do arquivo de entrada
file = open(sys.argv[1], 'r')

# Abertura do arquivo final
summaryFile = open('T1p2.txt', 'w')

# Monta o mapa de SIDs
sidMap = buildSidMap()

# Para cada linha do arquivo,
# extrai as informações necessárias
for line in file:
  info = parseInfoFromLine(line)
  # Verifica se a linha é válida
  if info != None:
    # Converte as informações obtidas
    protocol    = protocolMap[info[0]]
    port        = info[1]
    description = sidMap[info[2]]
    summaryFile.write(f'{protocol},{port},{description}\n')

# Fechamento dos arquivos
file.close()
summaryFile.close()

