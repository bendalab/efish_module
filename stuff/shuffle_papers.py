import numpy as np
import sys
from random import shuffle
from random import seed
if sys.version_info > (2,):
    Raw_input = input

if __name__ == '__main__':
    paper_nr = np.arange(15)
    seed(float(np.random.rand(1)))
    shuffle(paper_nr)

    paper_dict = {1: ['21.11', 'Hagedorn & Heiligenberg, 1985'],
                  2: ['21.11', 'v. d. Emde & Blackman, 1997'],
                  3: ['22.11', 'Stamper, 2010'],
                  4: ['22.11', 'Post & v. d. Emde, 1999'],
                  5: ['23.11', 'Stoddard, 2008'],
                  6: ['23.11', 'Carlson, 2011'],
                  7: ['24.11', 'Catania, 2014'],
                  8: ['24.11', 'Catania, 2015'],
                  9: ['28.11', 'Zupanc et al., 2003'],
                  10: ['28.11', 'Hupe et al., 2008'],
                  11: ['29.11', 'Kawasaki, 1997'],
                  12: ['29.11', 'Rose, 2004'],
                  13: ['30.11', 'McAnnelly, 2000'],
                  14: ['30.11', 'Nelson, 1999'],
                  15: ['01.12', 'Kreysing, 2012']}

    for enu, curr_nr in enumerate(paper_nr):
        paper_date = paper_dict[curr_nr][0]
        paper_name = paper_dict[curr_nr][1]
        if sys.version_info < (3,):
            name = raw_input("\nHello there! What's your name?")
        else:
            name = input("Hello there! What is your name?")
        if name == "q" or name == "quit":
            break
        print('\nNice to meet you, ' + name + ', you have to present paper # ' + str(curr_nr))
        print("The paper's name is " + paper_name + " and you will present it on " + paper_date)

        print('\nNow the next one...!\n')

        print('\n')
        # fig, ax = plt.figure(figsize=(15, 15))
        # ax.text(0.5, 0.5, str()
