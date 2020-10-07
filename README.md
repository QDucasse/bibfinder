# BibFinder

---
### Description

This project takes a list of pdf articles where the title corresponds to `YEAR_AUTHOR_ARTICLE TITLE WITH SPACES.pdf` then uses `selnium` to query both Google Scholar and BibTexSearch in order to find the `bibtex` and stores it in the corresponding `.bib`.

---
### Installation

* To download and install the source code of the project:

  ```bash
    $ cd <directory you want to install to>
    $ git clone https://github.com/QDucasse/bibfinder
    $ python setup.py install
  ```
* To download and install the source code of the project in a new virtual environment:  

  *Download of the source code & Creation of the virtual environment*
  ```bash
    $ cd <directory you want to install to>
    $ git clone https://github.com/QDucasse/bibfinder
    $ cd bibfinder
    $ mkvirtualenv -a . -r requirements.txt VIRTUALENV_NAME
  ```
  *Launch of the environment & installation of the project*
  ```bash
    $ workon VIRTUALENV_NAME
    $ pip install -e .
  ```
---
