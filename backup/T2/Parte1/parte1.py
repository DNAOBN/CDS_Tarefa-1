import sys
import os

def parsePermissionsLine(line):
  line = line.strip('\n')
  startIndex = line.find('<uses-permission')
  if startIndex != -1:
    startIndex = line.find('android.permission')
    line = line[startIndex:-1]
    endIndex = line.find('"')
    permission = line[0:endIndex].split('.')[-1]
    return permission
  return 0

def parseManifestName(name):
  return name.split('-')[-1].split('.')[0]

def getAppPermissions(file):
  permissions = []
  for line in file:
    permission = parsePermissionsLine(line)
    if permission:
      permissions.append(permission)
  return permissions

def getUniqueAppPermissions(appName):
  return [p for p in appPermissions[appName] if globalPermissionCount[p] == 1]

def getCommonAppPermissions(appCount):
  permissions = []
  for key, value in globalPermissionCount.items():
    if value == appCount:
      permissions.append(key)
  return permissions

def updateAppPermissionsDict(appName, permissions):
  appPermissions[appName] = permissions

def updateGlobalPermissionCount(permissions):
  for permission in permissions:
      if permission not in globalPermissionCount:
        globalPermissionCount[permission] = 1
      else:
        globalPermissionCount[permission] += 1

if len(sys.argv) < 2:
  print('ERRO: Diretório de entrada não encontrado')
  exit()

# Abertura do diretório
dirName = sys.argv[1]
dir = os.listdir(dirName)

# Cria um dicionário para salvar as
# permissões de cada aplicativo
appPermissions = {}

# Lista de nomes dos apps
appNames = []

# Cria um dicionário para salvar a
# contagem de ocorrências de cada
# permissão
globalPermissionCount = {}

print("==================\n")
print("Permissões por APK\n")
print("==================\n")

# Lê e processa os dados de entrada,
# popula os dicionários e imprime
# as permissões de cada app
for fileName in dir:
  file = open(f'{dirName}/{fileName}', 'r')
  appName = parseManifestName(fileName)
  appNames.append(appName)
  permissions = getAppPermissions(file)
  updateAppPermissionsDict(appName, permissions)
  updateGlobalPermissionCount(permissions)
  print(f'{appName}: {permissions}\n')

print("=========================\n")
print("Permissões únicas por APK\n")
print("=========================\n")

for name in appNames:
  print(f'{name}: {getUniqueAppPermissions(name)}\n')

print("==========================\n")
print("Permissões comuns das APKs\n")
print("==========================\n")

print(f'{getCommonAppPermissions(len(appNames))}\n')
