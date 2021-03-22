import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read in data using pandas and print to verify
data = pd.read_csv("charts/MixedData.csv")
print(data)

# Scatter plot using seaborn to colour data points by strategy
sns.scatterplot(x=data['OUTBREAK'], y=data['INFECTED'], hue=data['STRATEGY'])

# Setting the chart title and axis labels
font = {'fontname': 'Helvetica Neue'}
plt.title('Total infections by outbreak for each defence strategy', **font)
plt.xlabel('Outbreak', **font)
plt.ylabel('Infections', **font)
plt.show()
