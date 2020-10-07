# -*- coding: utf-8 -*-

# bibfinder
# author - Quentin Ducasse
# https://github.com/QDucasse
# quentin.ducasse@ensta-bretagne.org

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BibFinder(object):

    def __init__(self, headless=True):
        chrome_options = Options()
        if headless:
            chrome_options.add_argument('headless')

        # Initialize the driver
        self.driver = webdriver.Chrome(executable_path=os.path.abspath("./drivers/chromedriver"), options=chrome_options)

    # ==================
    # BROWSER OPERATIONS
    # ==================

    def close_browser(self):
        self.driver.close()

    def get_googlescholar_bib(self, article_keywords):
        '''
        Parameters
        ----------
        article_keywords: string
            String with all keywords separated by spaces
        '''
        try:
            article_keywords = article_keywords.replace(" ","+")
            self.driver.get("https://scholar.google.com/scholar?q=" + article_keywords)
            self.driver.find_element_by_xpath('/html/body/div/div[10]/div[2]/div[2]/div[2]/div[1]/div[2]/div[3]/a[2]').click()

            bibtex_button_xpath = '/html/body/div/div[4]/div/div[2]/div/div[2]/a[1]'
            WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.XPATH,bibtex_button_xpath)))
            self.driver.find_element_by_xpath(bibtex_button_xpath).click()

            bib_xpath = '/html/body/pre'
            WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH,bib_xpath)))
            bib = self.driver.find_element_by_xpath(bib_xpath).text
            return bib
        except:
            print("Google Scholar: Bib not found for " + article_keywords)

    def get_bibtexsearch_bib(self, article_keywords):
        '''
        Parameters
        ----------
        article_keywords: string
            String with all keywords separated by spaces
        '''
        try:
            self.driver.get("http://www.bibtexsearch.com/")
            input = self.driver.find_element_by_xpath("/html/body/center/table/tbody/tr/td[2]/form/input[1]")
            input.send_keys(article_keywords)
            self.driver.find_element_by_xpath("/html/body/center/table/tbody/tr/td[2]/form/input[2]").click()

            bib_xpath = "/html/body/center/div[1]/div/pre"
            WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH,bib_xpath)))
            bib = self.driver.find_element_by_xpath(bib_xpath).text
            return bib

        except:
            print("BibTex search: Bib not found for " + article_keywords)

    # ===============
    # FILE OPERATIONS
    # ===============

    def extract_keywords_from_article(self, article_file):
        article_file_without_extension = article_file.split(".")[0]
        date, author, title = article_file_without_extension.split("_")
        title_elements = title.split(" ")
        article_keywords = " ".join([date, author] + title_elements[:min(len(title_elements),3)])
        return article_keywords

    def create_bib_file(self, article_file, bibs):
        bib_file = open(article_file.split(".")[0] + ".bib", "x")
        for bib in bibs:
            if bib is None:
                pass
            else:
                bib_file.write(bib + "\n\n")
        bib_file.close()

    # ====
    # MAIN
    # ====

    def find_bib_and_write_to_file(self, article_file, bib_folder):
        article_keywords = self.extract_keywords_from_article(article_file)
        print(article_keywords)
        bib_gs = self.get_googlescholar_bib(article_keywords)
        bib_bs = self.get_bibtexsearch_bib(article_keywords)
        bibs = [bib_gs, bib_bs]
        self.create_bib_file(bib_folder + "/" + article_file, bibs)



if __name__=="__main__":
    import os
    articles_folder = "/home/quentin/Desktop/Research/VM/Articles"
    bibs_folder     = "/home/quentin/Desktop/Research/VM/Bibliography"
    articles = os.listdir(articles_folder)

    finder = BibFinder(headless=True)

    for article in articles:
        finder.find_bib_and_write_to_file(article, bibs_folder)
