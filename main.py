import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import pandas as pd
import pickle
import copy


app=FastAPI()
popular_df=pd.read_pickle("popular.pkl")
user_movie_df=pd.read_pickle("user_movie.pkl")
content_movie=pd.read_pickle("movie_list.pkl")
similarity=pd.read_pickle("similarity_content.pkl")


class Movierecommender(BaseModel):
    moviename: str


@app.get('/')
def popular():
    specific_column_data = popular_df['title']
    return{'popular_movie': specific_column_data.to_list()}


@app.post('/recommend')
def recommend_movie(data:Movierecommender):
    data=data.dict()
    movie_name=data['moviename']
    content_recommend=[]
    context_recommend=[]
    def recommend_content(movie_name):
        if movie_name not in content_movie['title'].values:
            print(f"Movie '{movie_name}' not found in the dataset.")
            return
        index = content_movie[content_movie['title'] == movie_name].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        for i in distances[1:6]:
            content_recommend.append(content_movie.iloc[i[0]].title)
            print(content_movie.iloc[i[0]].title)
    
    
    def check_film(movie_name, user_movie_df):
        result = [col for col in user_movie_df.columns if movie_name in col]
        context_recommend.extend(result[:5])


    from collections import defaultdict

    def top_three_frequent_words(lists_of_words):
        word_count = defaultdict(int)
        for word_list in lists_of_words:
            for word in word_list:
                word_count[word] += 1
        top_three_words = sorted(word_count, key=word_count.get, reverse=True)[:3]
        return top_three_words
    lists_of_words = [
        content_recommend,
        context_recommend
    ]
    recommend_content(movie_name=movie_name)
    check_film(movie_name=movie_name,user_movie_df=user_movie_df)
    recommended_options=top_three_frequent_words(lists_of_words)
    return {
        'recommended_options': recommended_options
    }



if __name__=='__main__':
    uvicorn.run(app,host='127.0.0.1',port=8000)



##working but recheck function call##
