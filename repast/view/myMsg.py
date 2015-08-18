#coding:UTF-8
from flask import render_template
from repast.util.session_common import *

def myMsg():
    return render_template('myMsg.html')