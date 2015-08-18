#coding: UTF-8

import math

def rad(d):
    return d*math.pi/180.0

def get_distance(lat1,lng1,lat2,lng2):
    radlat1=rad(float(lat1))
    radlat2=rad(float(lat2))
    a=radlat1-radlat2
    b=rad(float(lng1))-rad(float(lng2))
    s=2*math.asin(math.sqrt(math.pow(math.sin(a/2),2)+math.cos(radlat1)*math.cos(radlat2)*math.pow(math.sin(b/2),2)))
    earth_radius=6378.137
    s=s*earth_radius
    if s<0:
        return -s
    else:
        return s