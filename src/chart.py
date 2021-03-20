import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv("charts/MixedData.csv")

outbreak = data['OUTBREAK']
infections = data['INFECTED']
strategy = data['STRATEGY']

print(data)


sns.scatterplot(outbreak, infections, hue=strategy)
plt.title('Total infections by outbreak for each defence strategy')
plt.xlabel('Outbreak')
plt.ylabel('Infections')
# df.plot(kind='density')  # estimate density function
# df.plot(kind='hist')  # histogram
plt.show()
