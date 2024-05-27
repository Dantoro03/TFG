import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time
import pandas as pd
from datetime import datetime
import os
import json

SPOTIPY_CLIENT_ID = 'my-spotify-client-id'
SPOTIPY_CLIENT_SECRET = 'my-spotify-client-secret'

auth_manager = SpotifyClientCredentials(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)

llista_pl = pd.read_csv("playlists.csv")
playlists_name = llista_pl['0']
playlists_id = llista_pl['1']
#entro al arxiu de la llista de pl
for playlist_id, playlist_name in zip(playlists_id, playlists_name):
    song_doc = []
    pos = 0
    playlist = sp.playlist(playlist_id) #busco cada pl
    playlist_image = playlist['images'][0]['url'] #agafo la portada de la playlist
    playlist_followers = playlist['followers']['total'] #agafo els followers de la pl
    list_id = []
    for item in playlist['tracks']['items']: #agafo tota la informació que necessito de cada canço i l'anomeno
        pos = pos + 1
        album_name = item['track']['album']['name']
        album_type = item['track']['album']['album_type']
        album_id = item['track']['album']['id']
        cover = item['track']['album']['images'][0]['url']
        song_name = item['track']['name']
        song_id = item['track']['id']
        artist_name = item['track']['artists'][0]['name']
        artist_id = item['track']['artists'][0]['id']
        added_at = item['added_at']
        captured_at = datetime.now().date()
        release = item['track']['album']['release_date']
        song_pop = item['track']['popularity']
        precision = item['track']['album']['release_date_precision']
        #segons la precisió de la data faig un calcul segons l'any o el dia per calcular quant temps fa que va sortir la canço
        if precision == "day":
            diferencia = (captured_at - datetime.strptime(release, "%Y-%m-%d").date()).days
        elif precision == 'year':
            year = datetime(int(release), 1, 1)
            diferencia = (captured_at - year.date()).days
        else:
            diferencia = 'Null'
        gens = 'Null'
        gen = 'Null'
        art_pop = 'Null'
        followers = 'Null'
        image = 'Null'
        list_id.append(song_id)
        tup_canco = {"pos" : pos, "song" : song_name, "artist" : artist_name, "art id" : artist_id, "album" : album_name, "album type" : album_type, "release" : release, "diferencia" : diferencia, "popularity" : song_pop , "cover" : cover }
        song_doc.append(tup_canco)
    features = sp.audio_features(list_id)
    df_features = pd.DataFrame(features)
    print('bucle acabado')
    time.sleep(2)
    df_song = pd.DataFrame(song_doc)
    df_final = pd.concat([df_song, df_features], axis= 1)
    print(df_final)
    df_final.to_excel(f'data/playlist/{playlist_id}.xlsx', index=False)
