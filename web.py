# -*- coding: utf-8 -*-
import AutoLogin
import json
from flask import Flask, render_template, request
def ToJson(a):
    js=json.dumps(a,encoding="UTF-8", ensure_ascii=False, sort_keys=False, indent=4)
    return js
def get(xh,password):
    L=AutoLogin.getScore(xh,password)
    a=ToJson(L)
    a=a.encode("utf-8")
    list=json.loads(a)
    return list
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')
@app.route("/score",methods=["POST"])
def score():
    username=request.form.get("username","")
    password=request.form.get("password","")
    list=get(username,password)
    length=len(list)
    return render_template("score.html",list=list,length=length)
if __name__ == '__main__':
    app.run(debug=True,port=80,host='0.0.0.0')


