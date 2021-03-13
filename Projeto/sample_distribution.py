from percentage_split import *
from utils import *
import matplotlib.pyplot as plt

labels = 'Fraudulentos', 'Benignos'

# Extracts classes from each dataset
_, dataset80 = extractDataAndTargetValues(getDataset80())
_, dataset20 = extractDataAndTargetValues(getDataset20())

# Counts number of fraudulent and benign emails in each dataset
quantities80 = [sum([x == 1 for x in dataset80]), sum([x == 0 for x in dataset80])]
quantities20 = [sum([x == 1 for x in dataset20]), sum([x == 0 for x in dataset20])]

# Plots graphs
fig, [ax1, ax2] = plt.subplots(2, 1)

ax1.set_title('80% of dataset')
ax2.set_title('20% of dataset')

ax1.pie(quantities80, labels=labels, autopct='%1.1f%%',
        startangle=90, )
ax1.axis('equal')

ax2.pie(quantities20, labels=labels, autopct='%1.1f%%',
        startangle=90, )
ax2.axis('equal')

plt.show()