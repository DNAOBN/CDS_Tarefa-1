# Projeto de Ciência de Dados em Segurança

## Alunos
- Daniel Neves: GRR20171603
- João Vitor Moreira: GRR20171621

## Tipos de Dados

Registros de emails considerados como "phishing", com propriedades majoritariamente textuais, mas também contendo combinações de letras e números (como por exemplo, endereços de email e versões de provedores de email).

## Objetivo

Extrair as principais características deste tipo de email de forma a encontrar correlações e padrões, facilitando a classificação de emails como "phishing" com base em atributos como o endereço do remetente, palavras recorrentes no assunto, horário de envio, provedor de email utilizado para o envio, entre outros dados definidos na seção "Colunas e atributos selecionados".

## Rotulação

Por ser um dataset exclusivamente composto por emails fraudulentos, o único rótulo de classificação dos emails em si é "phishing", pois não há emails benignos.

Os dados de cada email são rotulados no formato "rótulo: valor" (como por exemplo, "Subject: INHERITANCE CLAIM"), exceto pelo conteúdo do email, que vem logo em seguida à propriedade "Status", separado por pelo menos uma linha vazia.

## Distribuição de dados

Os dados estão distribuídos em uma lista em um único arquivo .txt, um seguido do outro. Nem todos os emails contém todas as informações, porém alguns dados estão presentes em todos os emails (por exemplo, o remetente).

## Colunas e atributos selecionados

As principais colunas que desejamos manter são:
- Message-Id: O identificador do email
- From: Endereço de email do remetente, com o objetivo de encontrar padrões nestes
- Date: Data de envio, com o objetivo de encontrar padrões
- Subject: Assunto do email, com o objetivo de encontrar palavras usadas com mais frequência
- X-Mailer: Plataforma de envio do email, com o objetivo de verificar se alguma plataforma é utilizada com mais frequência para phishing
- Content-Type: Tipo e codificação do conteúdo do email, com o objetivo verificar se algum destes é "preferido" para phishing
- Conteúdo do email: Com o objetivo de verificar a existência de padrões ou recorrência de palavras

As demais colunas foram consideradas menos importantes para a análise dos dados, pois contém majoritariamente meta-dados do email ou informações do destinatário, que não são tão úteis para identificar um email como phishing.

## Fonte do Dataset
```
Radev, D. (2008), CLAIR collection of fraud email, ACL Data and Code Repository, ADCR2008T001, http://aclweb.org/aclwiki
```
link: https://www.kaggle.com/rtatman/fraudulent-email-corpus
