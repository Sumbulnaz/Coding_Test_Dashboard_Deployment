import pandas as pd

dashboard_data = pd.read_csv('Data/combined_deployment_data.csv')

# create genre list
def convert_genre_list(genre):
    split_genre = genre.split(',')
    remove_spaces_genre_list = [x.strip() for x in split_genre]
    return remove_spaces_genre_list

# for forming the similar dataframe for tomatometer rating we can do so through following steps
list_genre = dashboard_data[['genre']].copy()
list_genre['genre_list'] = list_genre.apply(lambda row:convert_genre_list(row['genre']),axis=1)
list_genre.drop(['genre'],axis=1,inplace=True)
list_genre_explode = list_genre.explode('genre_list') 
list_genre_groupby = list_genre_explode.groupby('genre_list').size().reset_index().drop([0],axis=1)

# final genre lis
genre = list(list_genre_groupby['genre_list'].unique()) + ['All Genre']


#for rating
def custom_dashboard(score):
  if score >=80:
    return 'Popular'
  elif score>=50 and score <80:
    return 'Average'
  else:
    return 'low-rated'
dashboard_data['rating'] =dashboard_data.apply(lambda x: custom_dashboard(x['imdb_scaled']),axis=1)
rating_list = list(dashboard_data['rating'].unique()) + ['All movies']
