# -*- coding: utf-8 -*-
"""Copy of Copy of ML_Project_TCET.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-FsE5WnVCtt8u2y6wH4YmqZQ9RXElXrG

# Importing The DataSets
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from google.colab import files
uploaded = files.upload()

dataset=pd.read_csv('SPAM text message 20170820 - Data.csv',encoding='latin-1')
y = dataset.iloc[:,:-1].values #independent variable

"""# Checking For Missing Values"""

dataset.info()

"""# Analysing the Data"""

print(dataset.head())

print(y)

ham = dataset[dataset['Category'] == 'ham'] 
spam = dataset[dataset['Category'] == 'spam'] 
length = [len(ham),len(spam)]
print(length)

"""# Visualizing The Data"""

fig = plt.figure()
ax = fig.add_axes([0,0,1,1])
students = ['ham','spam']
ax.bar(students,length)
plt.show()

count_Class=pd.value_counts(dataset["Category"], sort= True)
count_Class.plot(kind = 'pie',  autopct='%1.0f%%')
plt.title('Pie chart')
plt.ylabel('')
plt.show()

from collections import Counter
count1 = Counter(" ".join(dataset[dataset['Category']=='ham']["Message"]).split()).most_common(20)
df1 = pd.DataFrame.from_dict(count1)
df1 = df1.rename(columns={0: "words in non-spam", 1 : "count"})
count2 = Counter(" ".join(dataset[dataset['Category']=='spam']["Message"]).split()).most_common(20)
df2 = pd.DataFrame.from_dict(count2)
df2 = df2.rename(columns={0: "words in spam", 1 : "count_"})

df1.plot.bar(legend = False)
y_pos = np.arange(len(df1["words in non-spam"]))
plt.xticks(y_pos, df1["words in non-spam"])
plt.title('More frequent words in non-spam messages')
plt.xlabel('words')
plt.ylabel('number')
plt.show()

df2.plot.bar(legend = False, color = 'orange')
y_pos = np.arange(len(df2["words in spam"]))
plt.xticks(y_pos, df2["words in spam"])
plt.title('More frequent words in spam messages')
plt.xlabel('words')
plt.ylabel('number')
plt.show()

"""# Label Encoding"""

from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
y=le.fit_transform(y)

y=y.reshape(len(y),1)
print(y)

"""#  Cleaning the texts and steming it"""

import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
corpus = []
for i in range(0, 5572):
  review = re.sub('[^a-zA-Z]', ' ', dataset['Message'][i])
  review = review.lower()
  review = review.split()
  ps = PorterStemmer()
  all_stopwords = stopwords.words('english')
  all_stopwords.remove('not')
  review = [ps.stem(word) for word in review if not word in set(all_stopwords)]
  review = ' '.join(review)
  corpus.append(review)

print(corpus)

"""# Creating the Bag of Words model"""

from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer(stop_words=all_stopwords, max_features = 1000)
print(vectorizer)
X = vectorizer.fit_transform(corpus).toarray()
print(X)

"""# Creating a DocumentTermMatrix"""

df2 = pd.DataFrame(X.transpose(),
                   index=vectorizer.get_feature_names())
print(df2)

"""# Making a WordCloud from Corpus Data"""

from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
stopwords = all_stopwords

def show_wordcloud(data, title = None):
    wordcloud = WordCloud(
        background_color='white',
        stopwords=all_stopwords,
        max_words=200,
        max_font_size=40, 
        scale=3,
        random_state=1 # chosen at random by flipping a coin; it was heads
    ).generate(str(data))

    fig = plt.figure(1, figsize=(12, 12))

    plt.imshow(wordcloud)

show_wordcloud(corpus)

"""# Applying KMeans Clustering Algorithm"""

from sklearn.cluster import KMeans
wcss=[]
for i in range(1,11):
  k_means=KMeans(n_clusters = i, init="k-means++", random_state=42)
  k_means.fit(X)
  wcss.append(k_means.inertia_)
plt.plot(range(1,11),wcss)
plt.title('The Elbow Method')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.show()
from sklearn.cluster import MiniBatchKMeans
cls = MiniBatchKMeans(n_clusters=5, random_state=0)
cls.fit(X)
cls.predict(X)
cls.labels_

# Recall
from sklearn.metrics import recall_score
recall_score(y_test, y_pred, average=None)
# Precision
from sklearn.metrics import precision_score
precision_score(y_test, y_pred, average=None)

from sklearn.metrics import f1_score
f1_score(y_test, y_pred, average=None)

#AUC-ROC
import numpy as np
from sklearn.metrics import roc_auc_score
roc_auc_score(y_test, y_pred)

"""# Linear dimensionality reduction"""

from sklearn.decomposition import PCA
pca = PCA(n_components=2, random_state=0)
reduced_features = pca.fit_transform(X)
print(reduced_features)
reduced_cluster_centers = pca.transform(cls.cluster_centers_)

"""# Visualizing The Clusters"""

plt.scatter(reduced_features[:,0], reduced_features[:,1], c=cls.predict(X))
plt.scatter(reduced_cluster_centers[:, 0], reduced_cluster_centers[:,1], marker='x', s=150, c='b')

"""# Splitting The Dataset into training and testing"""

from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test=train_test_split(X,y,test_size=0.2, random_state=0)

"""## Testing different Models

# Logistic Regression
"""

from sklearn.linear_model import LogisticRegression
log_reg=LogisticRegression()
log_reg.fit(x_train,y_train)

y_pred=log_reg.predict(x_test)
print(y_pred)
from sklearn.metrics import confusion_matrix,accuracy_score
cm = confusion_matrix(y_test,y_pred)
accuracy_score(y_test,y_pred)

import seaborn as sns
import matplotlib.pyplot as plt     

ax= plt.subplot()
sns.heatmap(cm, annot=True, ax = ax, cmap='Blues'); #annot=True to annotate cells

# labels, title and ticks
ax.set_xlabel('Predicted labels');ax.set_ylabel('True labels'); 
ax.set_title('Confusion Matrix'); 
ax.xaxis.set_ticklabels(['ham', 'spam']); ax.yaxis.set_ticklabels(['ham', 'spam']);



#Adjusted R square
import statsmodels.api as sm
from statsmodels.sandbox.regression.predstd import wls_prediction_std
model1=sm.OLS(y_train,x_train)
result=model1.fit()
print(result.summary())

from sklearn.metrics import mean_absolute_error
mean_absolute_error(y_test, y_pred)

# Recall
from sklearn.metrics import recall_score
recall_score(y_test, y_pred, average=None)
# Precision
from sklearn.metrics import precision_score
precision_score(y_test, y_pred, average=None)

from sklearn.metrics import f1_score
f1_score(y_test, y_pred, average=None)

#AUC-ROC
import numpy as np
from sklearn.metrics import roc_auc_score
roc_auc_score(y_test, y_pred)

"""# Random Forest Classifier"""

from sklearn.ensemble import RandomForestClassifier
Classifier = RandomForestClassifier(n_estimators = 10, criterion = 'entropy', random_state = 0)
Classifier.fit(x_train,y_train)

y_pred = Classifier.predict(x_test)
print(np.concatenate((y_pred.reshape(len(y_pred),1), y_test.reshape(len(y_test),1)),1))

from sklearn.metrics import confusion_matrix, accuracy_score
cm = confusion_matrix(y_test, y_pred)
print(cm)
accuracy_score(y_test, y_pred)

import seaborn as sns
import matplotlib.pyplot as plt     

ax= plt.subplot()
sns.heatmap(cm, annot=True, ax = ax, cmap='rainbow'); #annot=True to annotate cells

# labels, title and ticks
ax.set_xlabel('Predicted labels');ax.set_ylabel('True labels'); 
ax.set_title('Confusion Matrix'); 
ax.xaxis.set_ticklabels(['ham', 'spam']); ax.yaxis.set_ticklabels(['ham', 'spam']);

from sklearn.metrics import mean_absolute_error
mean_absolute_error(y_test, y_pred)

# Recall
from sklearn.metrics import recall_score
recall_score(y_test, y_pred, average=None)
# Precision
from sklearn.metrics import precision_score
precision_score(y_test, y_pred, average=None)

from sklearn.metrics import f1_score
f1_score(y_test, y_pred, average=None)

import numpy as np
from sklearn.metrics import roc_auc_score
roc_auc_score(y_test, y_pred)

"""#Naive Bayes Classifier"""

from sklearn.naive_bayes import GaussianNB
clas=GaussianNB()
clas.fit(x_train,y_train)

y_pred=clas.predict(x_test)
print(np.concatenate((y_pred.reshape(len(y_pred),1),y_test.reshape(len(y_test),1)),1))

from sklearn.metrics import confusion_matrix, accuracy_score
cm = confusion_matrix(y_pred,y_test)
print(cm)
accuracy_score(y_pred, y_test)

import seaborn as sns
import matplotlib.pyplot as plt     

ax= plt.subplot()
sns.heatmap(cm, annot=True, ax = ax, cmap='flag'); #annot=True to annotate cells

# labels, title and ticks
ax.set_xlabel('Predicted labels');ax.set_ylabel('True labels'); 
ax.set_title('Confusion Matrix'); 
ax.xaxis.set_ticklabels(['ham', 'spam']); ax.yaxis.set_ticklabels(['ham', 'spam']);

from sklearn.metrics import mean_absolute_error
mean_absolute_error(y_test, y_pred)

# Recall
from sklearn.metrics import recall_score
recall_score(y_test, y_pred, average=None)
# Precision
from sklearn.metrics import precision_score
precision_score(y_test, y_pred, average=None)

from sklearn.metrics import f1_score
f1_score(y_test, y_pred, average=None)

import numpy as np
from sklearn.metrics import roc_auc_score
roc_auc_score(y_test, y_pred)

"""# KNN Classifier"""

from sklearn.neighbors import KNeighborsClassifier
classifier = KNeighborsClassifier(n_neighbors = 5, metric = 'minkowski', p=2)
classifier.fit(x_train, y_train)

y_pred = classifier.predict(x_test)
print(np.concatenate((y_pred.reshape(len(y_pred),1),y_test.reshape(len(y_test),1)),1))

from sklearn.metrics import confusion_matrix, accuracy_score
cm = confusion_matrix(y_pred,y_test)
print(cm)
accuracy_score(y_pred, y_test)

import seaborn as sns
import matplotlib.pyplot as plt     

ax= plt.subplot()
sns.heatmap(cm, annot=True, ax = ax, cmap='gist_rainbow'); #annot=True to annotate cells

# labels, title and ticks
ax.set_xlabel('Predicted labels');ax.set_ylabel('True labels'); 
ax.set_title('Confusion Matrix'); 
ax.xaxis.set_ticklabels(['ham', 'spam']); ax.yaxis.set_ticklabels(['ham', 'spam']);

from sklearn.metrics import mean_absolute_error
mean_absolute_error(y_test, y_pred)

# Recall
from sklearn.metrics import recall_score
recall_score(y_test, y_pred, average=None)
# Precision
from sklearn.metrics import precision_score
precision_score(y_test, y_pred, average=None)

from sklearn.metrics import f1_score
f1_score(y_test, y_pred, average=None)

import numpy as np
from sklearn.metrics import roc_auc_score
roc_auc_score(y_test, y_pred)

"""# Support Vector Classifier"""

from sklearn.svm import SVC
svmclassifier = SVC(kernel = 'linear', random_state = 0)
svmclassifier.fit(x_train, y_train)

y_pred = svmclassifier.predict(x_test)
print(np.concatenate((y_pred.reshape(len(y_pred),1), y_test.reshape(len(y_test),1)),1))

from sklearn.metrics import confusion_matrix, accuracy_score
cm = confusion_matrix(y_test, y_pred)
print(cm)
accuracy_score(y_test, y_pred)

import seaborn as sns
import matplotlib.pyplot as plt     

ax= plt.subplot()
sns.heatmap(cm, annot=True, ax = ax); #annot=True to annotate cells

# labels, title and ticks
ax.set_xlabel('Predicted labels');ax.set_ylabel('True labels'); 
ax.set_title('Confusion Matrix'); 
ax.xaxis.set_ticklabels(['ham', 'spam']); ax.yaxis.set_ticklabels(['ham', 'spam']);

from sklearn.metrics import mean_absolute_error
mean_absolute_error(y_test, y_pred)

#F1-score max-1 min-0
from sklearn.metrics import f1_score
f1_score(y_test, y_pred, average=None)

# Recall
from sklearn.metrics import recall_score
recall_score(y_test, y_pred, average=None)
# Precision
from sklearn.metrics import precision_score
precision_score(y_test, y_pred, average=None)

import numpy as np
from sklearn.metrics import roc_auc_score
roc_auc_score(y_test, y_pred)

"""## Selected support Vector Machine Classifier

# Prediction on Manual Inputs
"""

p = [input("enter a string::")]
p = vectorizer.transform(p).toarray()
print(p)

print(p.shape[1], X.shape[1])

if svmclassifier.predict(p) == 0:
  print("Not Spam")
else :
  print(Spam)