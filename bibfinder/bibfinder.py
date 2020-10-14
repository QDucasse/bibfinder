# -*- coding: utf-8 -*-

# bibfinder
# author - Quentin Ducasse
# https://github.com/QDucasse
# quentin.ducasse@ensta-bretagne.org

import os
from scholarly import scholarly, ProxyGenerator

class ScholarBibFinder(object):
    ARTICLES_FOLDER = "/Users/qducasse/Desktop/Research/Mixed-Precision/"
    BIB_FOLDER      = "/Users/qducasse/Desktop/Research/Bib_Mixed-Precision/"

    def __init__(self):
        pg = ProxyGenerator()
        pg.FreeProxies()
        scholarly.use_proxy(pg)

    def extract_infos_from_filename (self,filename):
        year = re.findall("^[0-9]{4}",filename)[0]
        author_title = re.findall("(?<=_)[a-zA-Z -]*(?=.)",filename)
        author = author_title[0]
        title = author_title[1]
        return year, author, title

    def process_file_name(self,filename):
        return filename.split(".")[0].replace("_"," ")

    def search_bibtex(self, keywords):
        query = scholarly.search_pubs(keywords)
        pub = next(query)
        bib = pub.bibtex
        if bib is None:
            bib = "No BibTex found!"
        return bib

    def create_bib_for_file(self,filename):
        kw = self.process_file_name(filename)
        bib = self.search_bibtex(kw)
        bib_filename = filename.split(".")[0] + ".bib"
        with open(self.BIB_FOLDER + bib_filename,"w") as f:
            f.write(bib)

    def process_all_articles(self):
        for filename in os.listdir(self.ARTICLES_FOLDER):
            if filename.endswith(".pdf"):
                self.create_bib_for_file(filename)

if __name__=="__main__":

    bibfinder = ScholarBibFinder()
    bibfinder.process_all_articles()
