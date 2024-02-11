import pandas as pd
import numpy as np 
#import requests
import csv

from io import BytesIO
#from glob import glob
from PIL import Image, ImageEnhance

import streamlit as st

import folium
from streamlit_folium import st_folium      # streamlitでfoliumを使う
import branca


st.title('Recommended Places')

if st.checkbox('※Registration,  登録する'):
    #画像取込み
    uploaded_file = st.file_uploader("send a picture,  画像取込み", type= "jpg")
    if uploaded_file != None:
        image = Image.open(uploaded_file)
        img_array = np.array(image)
        st.image(img_array, caption="thumbnail image,  サムネイル画像", use_column_width = True)
    
    
    with st.form(key='profile_form'):
    
        loc = st.text_input("Place name  観光場所名")
        lon = st.text_input("Longitude  経度")
        lat = st.text_input("Latitude緯度")
        note = st.text_input("Thoughts  感想")
        url = st.text_input("Reference picure  参考URL")
    
        #ﾎﾞﾀﾝ
        submit_btn = st.form_submit_button('Registration  登録')
        cancel_btn = st.form_submit_button('Cancel  キャンセル')
        if submit_btn:
            st.text(f'I added the location and photo to the map.')
            st.text(f'マップに場所と写真登録しました')
    
            dfnoo = pd.read_csv("./photos/regist.csv")
            noo = dfnoo.iloc[-1, 0] + 1
            #dfnoo.close()
    
            #入力したものをリストに代入する
            data = [[noo, loc, lon, lat, note, url]]
    
            #csvへの項目追記
            with open('./photos/regist.csv', 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                for row in data:
                    writer.writerow(row)
            
            #ファイルをクライアントから受ける
            fbytes = uploaded_file.getvalue()
            #modeをwb（バイナリ書き込みモード）にする。encodingを指定するとえらーになる
            with open(f'./photos/{loc}_{lon}_{lat}.jpg', mode="wb") as f:
                f.write(fbytes)


df = pd.read_csv("./photos/regist.csv")

lastno =  df.iloc[-1, 0]

if st.checkbox('※Delete  削除する'):
    delrow = st.selectbox('No', list(range(1, lastno+1)))
    del_btn = st.button('削除')

    delrow2 = delrow - 1
    
    #st.data_editor(df)
    
    if del_btn:
        droped_df = df.drop(delrow2) # まずは*行目だけを削除！
        st.table(droped_df)
        df = droped_df.reset_index(drop=True)
        df.to_csv("./photos/regist.csv", index=False, header=True, encoding='utf-8') #file saveS

st.table(df)
st.divider()


# 地図の中心の緯度/経度、タイル、初期のズームサイズを指定します。
m = folium.Map(
    # 地図の中心位置の指定(今回は栃木県の県庁所在地を指定)
    location=[36.56583, 139.88361], 
    # タイル、アトリビュートの指定
    tiles='https://cyberjapandata.gsi.go.jp/xyz/pale/{z}/{x}/{y}.png',
    attr='都道府県庁所在地、人口、面積(2016年)',
    # ズームを指定
    zoom_start=6
)


#loc = df.iloc[0, 0]
#lon = df.iloc[0, 1]
#lat = df.iloc[0, 2]
#note = df.iloc[0, 3]
#url = df.iloc[0, 4]
#img01 = Image.open(f'./photos/{loc}_{lon}_{lat}.JPG')
#st.image(img01, caption=loc, use_column_width=300)
#st.caption(f'{lon}, {lat}')
#if note != "":
#    st.caption(f'{note}')
#if url != "":
#    st.caption(f'{url}')

basho = "lon, lat:"
notee = "note:"
urll = "URL:"

for i, row in df.iterrows():
    img = Image.open(f'./photos/{row["No"]}_{row["loc"]}.jpg')
    st.image(img, caption=row["loc"], use_column_width=300)
    st.text(f'{basho}') 
    st.text(f'{row["lon"]}, {row["lat"]}') 
    #st.caption(f'{notee}')
    if row["note"] != "<NA>":
        st.text(f'{notee}{row["note"]}')
    if row["URL"] != "<NA>":
        st.caption(f'{urll}{row["URL"]}')
    st.divider()



