import streamlit as st
import numpy as np

def carriage_geo(outer_bearing,inner_bearing,bearing_spacing_x,slide,ring_pcd,orientation):
    match outer_bearing:
        case "J25":
            apex_o = 20.270
            la_max_o = 370
            lr_max_o = 1350
        case "J34":
            apex_o = 27.133
            la_max_o = 710
            lr_max_o = 2000
        case "J40":
            apex_o = 32.000
            la_max_o = 1200
            lr_max_o = 2300
    match inner_bearing:
        case "J25":
            apex_i = 20.270
            la_max_i = 370
            lr_max_i = 1350
            mv = 1350/2 * (bearing_spacing_x/1000)
            m = 370 * (bearing_spacing_x/1000)
        case "J34":
            apex_i = 27.133
            la_max_i = 710
            lr_max_i = 2000
            mv = 2000/2 * (bearing_spacing_x/1000)
            m = 710 * (bearing_spacing_x/1000)
        case "J40":
            apex_i = 32.000
            la_max_i = 1200
            lr_max_i = 2300
            mv = 2300/2 * (bearing_spacing_x/1000)
            m = 1200 * (bearing_spacing_x/1000)
    match slide:
        case "NS25":
            apex_s = 25.74
            d = 0.0225
        case "NM44":
            apex_s = 44.74
            d = 0.04056
    
    bearing_spacing_y = apex_s + ((apex_o + apex_i)/2)

    match orientation:
        case "Outside":
            outer_radius = (ring_pcd + apex_s)/2
            outer_bearing_path_r = outer_radius + (apex_o/2)
            sector_angle = np.rad2deg(np.arcsin((bearing_spacing_x/2)/outer_bearing_path_r))*2
            h = outer_bearing_path_r * (1 - (np.cos(np.deg2rad(sector_angle)/2)))
            apex_r = bearing_spacing_y + h - ((apex_i/2)+(apex_o/2))
            inner_radius = outer_radius - apex_r
            inner_bearing_path_r = inner_radius - (apex_i/2)
            l1 = 2 * la_max_o + la_max_i
            l2 = lr_max_i
            ms = min(la_max_i,2*la_max_o)*d
        case "Inside":
            inner_radius = (ring_pcd - apex_s)/2
            inner_bearing_path_r = inner_radius - (apex_i/2)
            sector_angle = np.rad2deg(np.arcsin((bearing_spacing_x/2)/inner_bearing_path_r))*2
            h = inner_bearing_path_r * (1 - (np.cos(np.deg2rad(sector_angle)/2)))
            apex_r = bearing_spacing_y - h - ((apex_i/2)+(apex_o/2))
            outer_radius = inner_radius + apex_r
            outer_bearing_path_r = outer_radius + (apex_o/2)
            l1 = 2 * la_max_i + la_max_o
            l2 = lr_max_o
            ms = min(la_max_o,2*la_max_i)*d
    
    return bearing_spacing_y,outer_radius,outer_bearing_path_r,sector_angle,h,apex_r,inner_radius,inner_bearing_path_r,l1,l2,ms,mv,m