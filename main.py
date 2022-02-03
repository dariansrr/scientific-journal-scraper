from website_scrapper import scrap_all_issues


#print('insert url of the journal in the issue/archive section')
#url = input()
url = 'http://publicacoes.fcc.org.br/index.php/eae/issue/archive'


# Creates a matrix (list of lists) and the header for final document
article_data = []
article_data.append(['Ano', 'Revista', 'Titulo', 'Autores', 'Resumo', 'Palavras-chave'])

# Scraps the data and concats it to the final list
article_data += scrap_all_issues(url)

print(article_data)