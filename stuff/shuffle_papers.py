__author__ = 'jan'

import numpy as np
import matplotlib.pyplot as plt
from random import shuffle
from random import seed
from IPython import embed

if __name__ == '__main__':

    paper_nr = np.arange(15)
    seed(float(np.random.rand(1)))
    shuffle(paper_nr)

    paper_dict = {1: ['14. 12', 'Hagedorn & Heiligenberg, 1985'],
                  2: ['14. 12', 'v. d. Emde & Blackman, 1997'],
                  3: ['15. 12', 'Stamper, 2010'],
                  4: ['15. 12', 'Post & v. d. Emde, 1999'],
                  5: ['16. 12', 'Stoddard, 2008'],
                  6: ['16. 12', 'Carlson, 2011'],
                  7: ['17. 12', 'Catania, 2014'],
                  8: ['17. 12', 'Catania, 2015'],
                  9: ['11. 01', 'Zupanc et al., 2003'],
                  10: ['11. 01', 'Hupe et al., 2008'],
                  11: ['12. 01', 'Kawasaki, 1997'],
                  12: ['12. 01', 'Rose, 2004'],
                  13: ['13. 01', 'McAnnelly, 2000'],
                  14: ['13.01', 'Nelson, 1999'],
                  15: ['14. 01', 'Kreysing, 2012']}

    for enu, curr_nr in enumerate(paper_nr):

        paper_date = paper_dict[curr_nr][0]
        paper_name = paper_dict[curr_nr][1]
        name = raw_input("\nHello there! What's your name?")
        print('\nNice to meet you, ' + name + ', you have to present paper # ' + str(curr_nr))
        print("The paper's name is " + paper_name + " and you will present it on " + paper_date)

        print('\nNow the next one...!\n')

        print('\n')
        # fig, ax = plt.figure(figsize=(15, 15))
        # ax.text(0.5, 0.5, str()