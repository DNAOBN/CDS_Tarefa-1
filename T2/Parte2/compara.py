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

def updateGlobalSectionCount(sectionName):
  if sectionName in globalSectionCount:
    globalSectionCount[sectionName] += 1
  else:
    globalSectionCount[sectionName] = 1

def getUniqueExecSections(execName):
  return [s for s in execSections[execName] if globalSectionCount[s] == 1]

def getCommonSections(execCount):
  sections = []
  for sectionName, count in globalSectionCount.items():
    if count == execCount:
      sections.append(sectionName)
  return sections

if len(sys.argv) < 3:
  print('ERRO: Número incorreto de parâmetros')
  print('Uso: python3 compara.py <arquivo1> <arquivo2>')
  exit()

# Leitura dos arquivos
fileNames = sys.argv[1:3]

execSections = {}

globalSectionCount = {}

# Lê e processa os dados de entrada
# e popula os dicionários
for fileName in fileNames:
  pe = pefile.PE(fileName)
  execName = parseExecutableName(fileName)
  for section in pe.sections:
    sectionName = getSectionName(section)
    updateExecSections(execName, sectionName)
    updateGlobalSectionCount(sectionName)

print("\n\n==========================")
print("Seções comuns aos binários")
print("==========================\n")

print(f'{getCommonSections(len(execSections.keys()))}\n')

print("\n\n=============================")
print("Seções únicas de cada binário")
print("=============================\n")

for execName in execSections.keys():
  print(f'{execName}: {getUniqueExecSections(execName)}\n')
