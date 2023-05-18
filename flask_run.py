#------------------------------------------------
# pip install Flask,  requests
#------------------------------------------------

from flask import Flask, session, render_template, make_response, jsonify, request, redirect, url_for

import cx_Oracle
import pandas as pd
import numpy as np
import random

import folium
from folium import plugins
import re
import googlemaps
import pprint

app = Flask(__name__)
app.secret_key = "1111122222"

def data_clean_once():
    dataset = pd.read_csv("./datasets/제주관광공사_여행장소_20220322.csv", encoding="cp949")
    df = dataset[dataset['장소상세설명'].isin(['숙박', '카페', '식당', '호텔', '렌트카', '관광'])]
    print( df['장소상세설명'].value_counts() )
    df.to_csv("./datasets/제주관광_cate6.csv", index=False)
# data_clean_once()


# 카페     50
# 숙박     28
# 식당     23
# 호텔     23
# 렌트카    21
# 관광     11
def search_map_html(cate='숙박'):
    df = pd.read_csv("./datasets/제주관광_cate6.csv")
    df = df[df['장소상세설명'] == cate]

    geo_list = []
    name_list = []
    for i in range(len(df)):
        lat = df.iloc[i]['위도']
        lng = df.iloc[i]['경도']
        sname = df.iloc[i]['장소명']
        # print(lat, lng, sname)
        geo_list.append((lat, lng))
        name_list.append(sname)
    # ---------------------------------------------------
    # folium map
    map = folium.Map(location=[33.41041350000001, 126.4913534], zoom_start=11,
                     tiles='OpenStreetMap')  # Stamen Terrain')
    plugins.MarkerCluster(geo_list, popups=name_list).add_to(map)
    # ---------------------------------------------------
    # web browser에 보이기 위한 준비
    map.get_root().width = "800px"
    map.get_root().height = "600px"
    html_str = map.get_root()._repr_html_()
    # <iframe style="display:block; height: 60vh" style="border:0" allowfullscreen>
    # ---------------------------------------------------
    return html_str


@app.route('/')
def index():
    # tel = str(random.randint(10, 99)) + str(random.randint(10, 99))
    # session['MY_TEL_SESSION'] = tel
    html_str = search_map_html(cate='숙박')

    return render_template('index.html', KEY_MAP_HTML=html_str)

@app.route('/detail')
def detail():
    return render_template('detail.html')

@app.route('/chart')
def chart():
    return render_template('chart_test.html')


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8877)