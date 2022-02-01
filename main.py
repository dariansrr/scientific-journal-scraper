from website_scrapper import scrap_all_issues


#print('insert url of the journal in the issue/archive section')
#url = input()
url = 'http://publicacoes.fcc.org.br/index.php/eae/issue/archive'

scrap_all_issues(url)