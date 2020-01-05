import pandas as pd
import requests
import zipfile



# We want to limit ourselves to the area of Greater London.
# 
# Also, 'Accuracy' is defined as below:
# 
# ```
# Accuracy is an integer, the higher the better :
# 1 : estimated as average from numerically neigbouring postal codes
# 3 : same postal code, other name
# 4 : place name from geonames db
# 6 : postal code area centroid
# ```
# 
# Consequently we'll want to limit ourselves to codes with an Accuracy of greater than 4.  And because we're going to be using the Latitude/Longitude, we'll remove duplicate records of that and use only the first name.  As we said before, Postalcode will be tricky to use (it also happens to bridge Placenames) but we'll want to keep it around for reference.  Let's collapse the Postalcode into a single
 
url = 'http://download.geonames.org/export/zip/GB.zip'
zipname = 'GB.zip'
r = requests.get(url)

with open(zipname, 'wb') as f:
    f.write(r.content)

with zipfile.ZipFile(zipname, 'r') as f:
    f.extractall()

columns = ['Countrycode','Postalcode','Placename','Adminname1','Admincode1','Adminname2','Admincode2','Adminname3','Admincode3','Latitude','Longitude','Accuracy']
gb = pd.read_csv('GB.txt', sep='\t', header=None, names=columns)
gb.head()


ldn = gb[(gb['Adminname2']=='Greater London') & (gb['Accuracy'] >= 3.0)].copy()
ldn.drop(['Countrycode', 'Adminname1', 'Admincode1', 'Adminname2', 'Admincode2', 'Adminname3', 'Admincode3', 'Accuracy'], axis='columns', inplace=True)
ldn.drop_duplicates(subset=['Latitude', 'Longitude', 'Postalcode'], inplace=True)
ldn = ldn.groupby(['Latitude','Longitude']).agg({'Placename':'first', 'Postalcode': ','.join }).reset_index()
print('There are {} Places we will evaluate in London'.format(len(ldn.index)))
