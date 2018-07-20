import arxiv
import requests
import re
import os

class Download:
    def __init__(self):
        self.url = 'http://www.arxiv-sanity.com/top?timefilter=alltime&vfilter=all'

    def get(self):
        r = requests.get(self.url)
        self.r_text = str(r.text)

    def extract(self):
        self.pdf_links = re.findall(r'(?<=thumbs/)(.*?)(?=.jpg)', self.r_text)

    def download(self):
        """
        Changes to paper directory.
        Downlaods pdfs for each paper.
        """

        if not os.path.exists('./papers'):
            os.mkdir('./papers')

        os.chdir('./papers')

        base_url = 'https://arxiv.org/pdf/'
        for link in self.pdf_links:
            print('Downloading: {}'.format(link))
            paper = {'pdf_url': base_url + link,
                     'title': link.split('.pdf')[0]}
            try:
                arxiv.download(paper)
            except:
                print('Download: {} failed unexpectedly.'.format(link))
                pass

if __name__ == '__main__':
    dl = Download()
    dl.get()
    dl.extract()
    dl.download()
