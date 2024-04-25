# -*- coding: utf-8 -*-
"""DS 110: Final Project!

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1LA8UtiLV94shOdzYOsM5wf93DGlVxm-A

We will first upload our cleaned STEM and non-STEM data onto our Python Notebook.
"""

from google.colab import files

uploaded = files.upload()

from google.colab import files

uploaded = files.upload()

import numpy as np
import pandas as pd
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt

stem_df = pd.read_csv("STEM - STEM Data.csv", index_col=0)
non_stem_df = pd.read_csv("Non-STEM - Non-STEM Data.csv", index_col=0)

non_stem_df = non_stem_df.replace(',', '', regex=True)
non_stem_df

stem_df = stem_df.replace(',', '', regex=True)
stem_df

non_stem_df['Minutes Listened'] = non_stem_df['Minutes Listened'].astype(int)
stem_df['Minutes Listened'] = stem_df['Minutes Listened'].astype(int)

import scipy.stats
_, p = scipy.stats.ttest_ind(stem_df["Minutes Listened"],non_stem_df["Minutes Listened"])
p

stem_df.reset_index(inplace=True)
non_stem_df.reset_index(inplace=True)
combined_data = pd.concat([stem_df,non_stem_df], join = 'outer')
top_genres = combined_data[["Top Genres"]]
wordcloud = WordCloud().generate(str(top_genres))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()

contingency = pd.crosstab(non_stem_df["Top Genres"], stem_df["Top Genres"])
_, p, _, _ = scipy.stats.chi2_contingency(contingency)
p

contingency = pd.crosstab(non_stem_df["Stress Levels"], stem_df["Stress Levels"])
_, p, _, _ = scipy.stats.chi2_contingency(contingency)
p

import sklearn.linear_model as lm
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt

total_stress_stem = stem_df['Stress Levels'].tolist()
total_stress_nonstem = non_stem_df['Stress Levels'].tolist()
total_stress = total_stress_stem + total_stress_nonstem
total_stress = np.array(total_stress)
total_stress = total_stress.reshape(-1,1)
total_stress

stem_mins = stem_df['Minutes Listened'].tolist()
non_stem_mins = (non_stem_df['Minutes Listened'].tolist())
total_mins = stem_mins + non_stem_mins
total_mins = np.array(total_mins)
total_mins

linear_model = LinearRegression()
linear_model.fit(total_stress,total_mins)
y_hat = linear_model.predict(total_stress)
plt.plot(total_stress,total_mins,'o')
plt.plot(total_stress,y_hat,'r')
coef_determination = r2_score(total_mins, y_hat)
print(linear_model.coef_)
print(coef_determination)

import seaborn as sns

sns.set_theme(style="whitegrid")
g = sns.catplot(
    data=combined_data, kind="bar",
    x="Stress Levels", y="Minutes Listened",
)

g.despine(left=True)
g.set_axis_labels("Average Stress Level", "Quantity of Music Consumed")

data = combined_data
g = sns.jointplot(data=combined_data, x="Stress Levels", y="Minutes Listened", hue="Music Heaviness")
g.ax_joint.set_xlim(left=0, right=5)
g.ax_joint.set_ylim(bottom=0)

stem_heaviness = stem_df['Music Heaviness'].tolist()
non_stem_heaviness = non_stem_df['Music Heaviness'].tolist()
total_heaviness = stem_heaviness + non_stem_heaviness
total_heaviness = np.array(total_heaviness)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(total_mins, total_stress, total_heaviness, color = 'red')

x = np.concatenate((total_mins.reshape(-1, 1), total_stress), axis=1)
temp_model = LinearRegression()
temp_model.fit(x, total_heaviness)
print(temp_model.coef_)
print(temp_model.intercept_)

#output = since first coef is less than 0, this data suggests that the amount of music consumed does not have a strong correlation with the heaviness of music consumed. the other coef is greater than 0 and is large, which suggets that there may be a correlation between total stress and the heaviness of music consumed
#intercept suggets that when the values of music consumed and amount of stress is 0, students will still listen to heavier music

total_mins = total_mins.reshape(-1, 1)
totals = np.concatenate((total_mins, total_stress, total_heaviness.reshape(-1, 1)), axis=1)
correlation = np.corrcoef(totals, rowvar=False)
correlation
#correlation denotes how strongly two variables are related