import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
wordclouddata=pd.read_csv('wordclouddata.csv')
d = {}
for a, x in wordclouddata.values:
    d[a] = x
wordcloud = WordCloud(width = 800, height = 800, 
                background_color ='white',  
                min_font_size = 10).generate_from_frequencies(frequencies=d)
# plot the WordCloud image                        
plt.figure(figsize = (8, 8), facecolor = None) 
plt.imshow(wordcloud) 
plt.axis("off") 
plt.tight_layout(pad = 0)
plt.title('All Count features Word Cloud')
plt.show() 
wordcloud.to_file('all.png')

PerClusterWordCounts=pd.read_csv('PerClusterWordCounts.csv')
PerClusterWordCounts['Word']=PerClusterWordCounts['Unnamed: 0']
PerClusterWordCounts=PerClusterWordCounts[PerClusterWordCounts['Word']!='label']
for i in range(7):
    t='cluster'+str(i)
    data=PerClusterWordCounts[['Word',t]]
    d={}
    for r in data.itertuples():
        d[r[1]]= r[2]
    wordcloud = WordCloud(width = 800, height = 800, 
                    background_color ='white',  
                    min_font_size = 10).generate_from_frequencies(frequencies=d)
    # plot the WordCloud image                        
    plt.figure(figsize = (8, 8), facecolor = None) 
    plt.imshow(wordcloud) 
    plt.axis("off") 
    plt.tight_layout(pad = 0)
    plt.title('cluster: '+str(i)+' counts word cloud')
    plt.show() 
    wordcloud.to_file('cluster'+str(i)+'.png')
