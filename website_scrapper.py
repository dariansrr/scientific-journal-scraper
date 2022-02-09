from bs4 import BeautifulSoup
import re
import requests

def scrap_all_issues(url):
    print("starting to scrap", url)
    main_page = requests.get(url)

    if(main_page.status_code == 200):
        print("connection to main site: OK")

        # Parse main page
        main_soup = BeautifulSoup(main_page.content, "lxml")

        # Get all issues
        list_of_issues = main_soup.find("ul", {"class": "issues_archive"}).find_all("a", {"class": "title"})
        print("Found", str(len(list_of_issues)), " issues")
        #print(list_of_issues)

        return scrap_issue(list_of_issues)

    else:
        print("Coudn't connect to the main website")


def scrap_issue(issues_list):

    ######### ONLY FOR TEST #######
    #issues_list = issues_list[:2]
    ###############################

    all_issue_list = []


    for issue in issues_list:

        print("-------- STARTINNG NEW ISSUE --------")
        # Get issue url    
        issue_url = issue["href"]
        
        # Get issue page
        issue_page = requests.get(issue_url)
        
        if(issue_page.status_code == 200):
            # Parse issue page
            issue_soup = BeautifulSoup(issue_page.content, "lxml")

            # Remove <span> tags for cleaned result in the h3 lists
            for s in issue_soup.select("span"):
                s.extract()
            
            # Get all articles
            list_of_articles =  issue_soup.findAll("h3", {"class": "title"})

            # Clean list of articles
            clean_list_of_articles = []
            for h3 in list_of_articles:
                clean_list_of_articles.append(h3.find("a"))

            # Contacts the current issue in to the list with all the issues
            all_issue_list += scrap_article(clean_list_of_articles)

        else:
            print("Wasn't able to access the issue page " + str(issue_url) )
    
    return all_issue_list


def scrap_article(article_list):
    
    ######### ONLY FOR TEST #######
    #article_list = article_list[:2]
    ###############################

    all_article_list = []

    for article in article_list:
        # Get issue url
        article_url = article["href"]

        # Get issue page
        article_page = requests.get(article_url)
        if(article_page.status_code == 200):
            # Parse article page
            article_soup = BeautifulSoup(article_page.content, "lxml")

            # Creates empty list with defined size, using '' as default for empty
            article_data = [""] * 6

            # Get year
            article_data[0] = article_soup.find("div", {"class": "csl-entry"}).text
            article_data[0] = re.findall("\(([0-9]{4})", article_data[0])[0]
                        
            # Get title
            article_data[2] = article_soup.find("h1", {"class": "page_title"}).text.strip()

            # Get author
            author_tags = article_soup.findAll("span", {"class": "name"})
            for author in author_tags:
                article_data[3] += (author.text.strip() + ", ")
            article_data[3] = article_data[3][:-2] #removes the last ','

            # Get abstract
            abstract_tag = article_soup.find("section", {"class": "item abstract"}).text
            article_data[4] = abstract_tag.replace("Resumo\n", "").strip()

            # Get key-words
            article_data[5] = article_soup.find("section", {"class": "item keywords"}).text.split(":")[1]
            article_data[5] = " ".join(article_data[5].split()) # removes tabs and new lines
            article_data[5].replace(" , ", ", ")

            print("ANO:", article_data[0])
            print("TITULO:", article_data[2])
            print("AUTORES:", article_data[3])
            print("RESUMO:", article_data[4])
            print("PALAVRAS-CHAVE:", article_data[5], "\n\n")
            
            # appends the current article in to the list with all the articles
            all_article_list.append(article_data)

        else:
            print("Wasn't able to access the article page " + str(article_url) )
    
    return all_article_list