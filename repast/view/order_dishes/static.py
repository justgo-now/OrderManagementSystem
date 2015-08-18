# coding: utf-8
from flask import render_template, request




def myTel():
    return render_template("reception/mytel.html")


def my():
    return render_template("reception/my.html")
