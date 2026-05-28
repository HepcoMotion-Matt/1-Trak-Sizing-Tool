import streamlit as st
import numpy as np

def carriage_geo(outer_bearing,inner_bearing,bearing_spacing_x,slide,ring_pcd,orientation):
    match outer_bearing:
        case "J25":
            apex_o = 20.270
        case "J34":
            apex_o = 27.133
        case "J40":
            apex_o = 32.000
    match inner_bearing:
        case "J25":
            apex_i = 20.270
        case "J34":
            apex_i = 27.133
        case "J40":
            apex_i = 32.000
    match slide:
        case "NS25":
            apex_s = 25.74
        case "NM44":
            apex_s = 44.74
    
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
        case "Inside":
            inner_radius = (ring_pcd - apex_s)/2
            inner_bearing_path_r = inner_radius - (apex_i/2)
            sector_angle = np.rad2deg(np.arcsin((bearing_spacing_x/2)/inner_bearing_path_r))*2
            h = inner_bearing_path_r * (1 - (np.cos(np.deg2rad(sector_angle)/2)))
            apex_r = bearing_spacing_y - h - ((apex_i/2)+(apex_o/2))
            outer_radius = inner_radius + apex_r
            outer_bearing_path_r = outer_radius + (apex_o/2)
    
    return bearing_spacing_y,outer_radius,outer_bearing_path_r,sector_angle,h,apex_r,inner_radius,inner_bearing_path_r