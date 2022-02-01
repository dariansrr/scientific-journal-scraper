from bs4 import BeautifulSoup
import requests

def scrap_all_issues(url):
    print('starting to scrap', url)
    main_page = requests.get(url)

    if(main_page.status_code == 200):
        print('connection to main site: OK')

        # Parse main page
        main_soup = BeautifulSoup(main_page.content, 'lxml')

        # Get all issues
        list_of_issues = main_soup.find("ul", {"class": "issues_archive"}).find_all("a", {"class": "title"})
        print("Found", str(len(list_of_issues)), " issues")
        #print(list_of_issues)

        scrap_issue(list_of_issues)

    else:
        print("Coudn't connect to the main website")


def scrap_issue(issues_list):

    ######### ONLY FOR TEST #######
    issues_list = issues_list[:2]
    ###############################


    for issue in issues_list:

        print("-------- STARTINNG NEW ISSUE --------")
        # Get issue url    
        issue_url = issue['href']
        
        # Get issue page
        issue_page = requests.get(issue_url)
        
        if(issue_page.status_code == 200):
            # Parse issue page
            issue_soup = BeautifulSoup(issue_page.content, 'lxml')

            # Remove <span> tags for cleaned result in the h3 lists
            for s in issue_soup.select('span'):
                s.extract()
            
            # Get all articles
            list_of_articles =  issue_soup.findAll("h3", {"class": "title"})

            # Clean list of articles
            clean_list_of_articles = []
            for h3 in list_of_articles:
                clean_list_of_articles.append(h3.find("a"))

            print(clean_list_of_articles)

        else:
            print("Wasn't able to access the issue page " + str(issue_url) )