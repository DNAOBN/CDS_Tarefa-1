import sys

# Extrai apenas o SO, tipo, família e variante
# de uma linha do arquivo
def parseLine(line):
  return line.strip('\n').split(':')[2].split('.')

# Extrai o id (tipo.família) e variante do vírus,
# retornando-os em um array
def parseVirusInfo(string):
  info = [string[1], *string[2].split('-')]
  return ['.'.join(info[0:2]), info[2]]

# Remove itens duplicados de um array
def removeDuplicates(array):
  return list(dict.fromkeys(array))

# Dicionário de vírus
virusDict = {}

# Caso o arquivo de entrada não seja passado
# por parâmetro, sai do programa
if len(sys.argv) < 2:
  print('ERRO: Arquivo de entrada não encontrado')
  exit()

# Abertura do arquivo
file = open(sys.argv[1], 'r')

# Para cada linha do arquivo,
# extrai as informações necessárias
for line in file:
  info = parseLine(line)
  # Verifica se a linha é válida
  if len(info) == 3:
    # Extrai o id e a variante
    id, variant = parseVirusInfo(info)
    # Adiciona a variante a um array de
    # variantes daquele tipo.família de vírus
    if id not in virusDict:
      virusDict[id] = []
    virusDict[id].append(variant)

# Abertura do arquivo final
summaryFile = open('T1p1a.txt', 'w')

# Escrita das informações processadas
for virus in sorted(virusDict):
  numVariants = len(removeDuplicates(virusDict[virus]))
  summaryFile.write(f'{virus},{numVariants}\n')

# Fechamento dos arquivos
file.close()
summaryFile.close()

