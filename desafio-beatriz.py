import configparser
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import html

# Passo 1: Ler o arquivo desafio.ini e carregar os 3 parâmetros

# Utilizei o módulo configparser (https://docs.python.org/3/library/configparser.html)
# Inicialmente encontrei o erro MissingSectionHeaderError: File contains no section headers
# Assumi que eu não poderia editar manualmente o arquivo desafio.ini, então apliquei um 
# "dummy header" default ao ler o arquivo
with open('desafio.ini', 'r') as f:
  config_string = '[default]\n' + f.read()
parser = configparser.ConfigParser()
parser.read_string(config_string)

url = parser['default']['url']             # https://quiteja.com.br?candidato=
inicio = parser['default']['inicio']       # con
fim = parser['default']['fim']             # e

f.close()

# Passo 2: Carregando o conteúdo da url com o parâmetro 'beatriz'
params = 'beatriz'
page = urlopen(url + params).read().decode('utf-8')

# Passo 3:
# 3.1) Remover todo o código JavaScript
# 3.2) Remover todas as tags HTML
# 3.3) Converter todos os caracteres HTML (&amp; -> &)

# Utilizei a biblioteca Beautiful Soup (https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
# Utilizei o método get_text() do BeautifulSoup para extrair somente o texto da página,
# sem código JS nem tags HTML
# Em seguida, utilizei o método unescape() para converter os oossíveis chars html para unicode
soup = BeautifulSoup(page, 'html.parser')
text = html.unescape(soup.get_text())

# 3.4) Manter apenas 1 quebra de linha
# Usei regex para remover as quebras de linha repetidas, substituindo por apenas uma quebra
# Adicionei o \s* pois em testes com outras páginas encontrei linhas não-vazias que continham
# apenas espaços
text = re.sub(r'\s*\n+', '\n', text)


# Passo 4: localizar palavras ignorando case
# Usando regular expressions -- uso o site regexr.com para testar expressões
# \b -> word boundary
# [^ \n]* -> sem espaços nem quebras de linha, 0 ou mais vezes
regex_expression = r'\b' + inicio + r'[^ \n]*' + fim + r'\b'
matches = re.findall(regex_expression, text, re.IGNORECASE)

# Passo 5
# Imprimir no console:
# 1) o conteúdo do HTML tratado
print(text)
# 2) a quantidade de palavras encontradas
print(f'Número de palavras encontradas: {len(matches)}')
# 3) a lista das palavras encontradas
print(f'Palavras encontradas: {matches}')
