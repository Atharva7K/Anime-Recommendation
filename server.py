# -*- coding: utf-8 -*-
"""
Created on Sun Mar 28 21:42:49 2021

@author: Atharva 
"""

from flask import Flask, render_template, request
import json
import sqlite3

with open('CONFIG.json') as f:
    config = json.load(f)

db_path = config['sqlite_db_path']

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('base.html')


def get_cursor(db_name = 'Anime-Rec.sqlite'):
    try:
        conn = sqlite3.connect(db_name)
    except:
        print('Error reading database')
        return
    cur = conn.cursor()

    return cur
 

def get_data_frm_id(id_list, cursor):

    names = []
    for i in id_list[2:]:
        name = cursor.execute('SELECT Anime_Name FROM ANIME WHERE Anime_id = (?)', (i, )).fetchall()[0][0]
        rating = cursor.execute('SELECT Rating FROM ANIME WHERE Anime_id == (?)', (i, )).fetchall()[0][0]
        type_ = cursor.execute('SELECT Type FROM ANIME WHERE Anime_id == (?)', (i, )).fetchall()[0][0]
        names.append((name, rating, type_))
    return names

def get_id(name, cursor):
    _id = cursor.execute('SELECT Anime_id FROM ANIME WHERE Anime_Name == (?)',(name, )).fetchall()[0][0]
    return _id
    


@app.route('/recommend', methods = ['POST', 'GET'])

def recommend():
    cur = get_cursor()
    try:
        name = request.form.get('Anime Name')
        print(name)
        _id = get_id(name, cur)
        rec_list = cur.execute('SELECT * FROM Recommendations WHERE Anime_id = (?)', (_id, )).fetchall()[0]
        recs = get_data_frm_id(rec_list, cur)
        
        print(recs)
        return render_template('recommend.html', anime_recs = recs)
    except:
        return render_template('recommend.html', error = 'Entered name not found in Database. Try a different name')
    

if __name__ == "__main__":
    
    app.run(debug = True)
    #app.run()
    
    
