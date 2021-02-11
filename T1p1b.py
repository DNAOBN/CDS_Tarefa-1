import sys

# Extrai os campos "Plataforma/Linguagem", "Tipo",
# "Subtipo" e "Variante" de uma linha do arquivo,
# retornando-os em um array
def parseInfoFromLine(line):
  info = line.strip('\n').split(':')[0].split('.')[1:4]
  return [*info[0:2], *info[2].split('-', 1)]

# Caso o arquivo de entrada não seja passado
# por parâmetro, sai do programa
if len(sys.argv) < 2:
  print('ERRO: Arquivo de entrada não encontrado')
  exit()

# Abertura do arquivo
file = open(sys.argv[1], 'r')
# Abertura do arquivo final
summaryFile = open('T1p1b.txt', 'w')

# Para cada linha do arquivo,
# extrai as informações necessárias
for line in file:
  info = parseInfoFromLine(line)
  # Verifica se a quantidade de informações está correta
  if len(info) == 4:
    # Escreve no arquivo as informações processadas
    summaryFile.write(f'{",".join(info)}\n')

# Fechamento dos arquivos
file.close()
summaryFile.close()

