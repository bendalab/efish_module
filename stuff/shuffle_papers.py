import numpy as np
import sys
from random import shuffle
from random import seed

if __name__ == '__main__':
    paper_nr = np.arange(12)
    seed(float(np.random.rand(1)))
    shuffle(paper_nr)

    paper_dict = {0: ['23.11', 'Hagedorn & Heiligenberg, 1985'],
                  1: ['23.11', 'v. d. Emde & Bleckmann, 1997'],
                  2: ['24.11', 'Stamper, 2010'],
                  3: ['24.11', 'Schumacher et al., 2016'],
                  4: ['28.11', 'Stoddard, 2008'],
                  5: ['28.11', 'Carlson, 2011'],
                  6: ['29.11', 'Catania, 2014'],
                  # 8: ['29.11', 'Catania, 2015'],
                  7: ['29.11', 'Zupanc et al., 2003'],
                  8: ['30.11', 'Hupe et al., 2008'],
                  9: ['30.11', 'Kawasaki, 1997'],
                  10: ['01.12', 'Rose, 2004'],
                  # 12: ['02.11', 'McAnnelly, 2000'],
                  11: ['01.12', 'Nelson, 1999']}
                  # 13: ['03.12', 'Kreysing, 2012']}

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
