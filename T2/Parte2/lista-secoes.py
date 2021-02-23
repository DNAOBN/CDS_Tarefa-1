import sys
import os
import pefile


def parseExecutableName(name):
  return name[0:name.find('.exe')]

def getSectionName(section):
  endIndex = section.Name.decode('utf-8').find('\x00')
  return section.Name.decode('utf-8')[0:endIndex]

def updateExecSections(execName, sectionName):
  if execName in execSections:
    execSections[execName].append(sectionName)
  else:
    execSections[execName] = [sectionName]


if len(sys.argv) < 2:
  print('ERRO: Diretório de entrada não encontrado')
  exit()

# Abertura do diretório
dirName = sys.argv[1]
files = os.listdir(dirName)

# Dicionário para salvar as seções
# de cada binário
execSections = {}

# Lê e processa os dados de entrada
# e popula o dicionário
for fileName in files:
  execName = parseExecutableName(fileName)
  pe = pefile.PE(f'{dirName}/{fileName}')
  for section in pe.sections:
    sectionName = getSectionName(section)
    updateExecSections(execName, sectionName)

print("\n\n==================")
print("Seções por binário")
print("==================\n")

for execName, sections in execSections.items():
  print(f'{execName}: {sections}\n')
