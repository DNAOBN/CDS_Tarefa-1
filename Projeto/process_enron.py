import os

# Script utilizado apenas para a extração de emails
# válidos do dataset da enron e criação de um dataset
# único (benign_emails.txt)


MAX_EMAILS_PER_PERSON = 100
MAX_EMAILS = 4000

# Verifica se o email não é encaminhado,
# uma resposta a outro email ou contém outro
# email no corpo
def isEmailValid(content):
  isForwarded = content.find('Forwarded') != -1
  isReply = content.find('Original Message') != -1
  hasOtherEmailInside = content.count('Subject: ') > 1
  return not isForwarded and not isReply and not hasOtherEmailInside

# Método usado para analisar a distribuição de emails
# e encontrar um número máximo adequado de emails por
# pessoa
def countSentEmails(dir):
  emailsPerPerson = {}
  count = 0
  for personName in dir:

    try:
      dir = os.listdir(f'./dataset/maildir/{personName}/sent')
    except:
      continue

    emailsPerPerson[personName] = 0

    for fileName in dir:

      if (emailsPerPerson[personName] == MAX_EMAILS_PER_PERSON):
        break

      try:
        file = open(f'./dataset/maildir/{personName}/sent/{fileName}')
      except:
        continue

      try:
        content = file.read()
      except:
        file.close()
        continue

      if isEmailValid(content):
        count += 1
        emailsPerPerson[personName] += 1

      file.close()
  return count, emailsPerPerson

# Main Program

dir = os.listdir('./dataset/maildir')
results = open('./dataset/benign_emails.txt', 'w')

emailsPerPerson = {}
totalCount = 0
for personName in dir:

  try:
    dir = os.listdir(f'./dataset/maildir/{personName}/sent')
  except:
    continue

  emailsPerPerson[personName] = 0

  for fileName in dir:

    if (emailsPerPerson[personName] == MAX_EMAILS_PER_PERSON):
      break

    if (totalCount == MAX_EMAILS):
      results.close()
      quit()

    try:
      file = open(f'./dataset/maildir/{personName}/sent/{fileName}')
    except:
      continue

    try:
      content = file.read()
    except:
      file.close()
      continue

    if isEmailValid(content):
      results.write(content)
      results.write('\n\n')
      totalCount += 1
      emailsPerPerson[personName] += 1

    file.close()
