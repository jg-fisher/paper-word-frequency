import os
import sys
import textract
import enchant
import pickle
from operator import itemgetter
import matplotlib.pyplot as plt

class Analyze:
    def __init__(self):
        self.d = enchant.Dict('en_US')
        self.frequencies = {}
        self.remove = ['the', 'and', 'that', 'for',
                        'are', 'from', 'can', 'not',
                        'what', 'with', 'this', 'which',
                        'such', 'have', 'been', 'would',
                        'they', 'these', 'our', 'had',
                        'how', 'most', 'were', 'only',
                        'has', 'their', 'will', 'when',
                        'using', 'use', 'used', 'more',
                        'than', 'but', 'each', 'also',
                        'where', 'was', 'all']

    def main(self, path='./'):

        files = [f for f in os.listdir(path) if f.endswith('.pdf')]

        if len(files) < 1:
            print('No PDF in specified {} directory'.format(path))
            return
        
        for f in files:

            # extract text
            print('Extracting {} ...'.format(f))
            try:
                text = textract.process(path + f)
            except:
                print('Extracting {} failed unexpectedly.'.format(f))
                continue
        
            # cleanup
            text = text.replace('\n', ' ')
            text = text.replace('.', '')
            text = [i.lower() for i in text.split(' ')]

            # count
            unique_words = sorted(set(text))
            for word in unique_words:
                if len([l for l in word]) > 2 and word not in self.remove and not self._are_nums(word):
                    try:
                        if self.d.check(word):
                            if word in self.frequencies.keys():
                                self.frequencies[word] = int(self.frequencies[word]) + int(text.count(word))
                            else:
                                self.frequencies[word] = int(text.count(word))
                    except:
                        continue

            self.show(n_items=25)


    def show(self, n_items=25):
        d_view = [ (v, k) for k, v in self.frequencies.iteritems() ]
        d_view.sort(reverse=True)
        for i, (v, k) in enumerate(d_view):
            if i == n_items:
                break
            else:
                print('{0}: {1}'.format(k, v))

    def save(self):
        with open('frequencies.pkl', 'wb') as f:
            pickle.dump(self.frequencies, f, protocol=pickle.HIGHEST_PROTOCOL)

    def load(self):
        with open('frequencies.pkl', 'rb') as f:
            self.frequencies = pickle.load(f)

    def visualize(self, n_words=25):
        # add trimming based on n_words

        n_words = range(n_words)
        d_view = [ (v, k) for k, v in self.frequencies.iteritems() ]
        d_view.sort(reverse=True)
        f_view = { k:v for i, (v, k) in enumerate(d_view) if i in n_words }

        plt.figure()
        plt.title('ML Paper Word Frequencies')
        plt.bar(range(len(f_view)), list(f_view.values()), align='center')
        plt.xticks(range(len(f_view)), list(f_view.keys()), rotation=90)
        plt.tight_layout()
        plt.savefig('barchart')
        plt.show()
    
    def _are_nums(self, string):
        return any(i.isdigit() for i in string)

if __name__ == '__main__':
    a = Analyze()
    #a.main(path='./papers/')
    a.load()
    a.visualize()
