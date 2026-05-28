import streamlit as st
import numpy as np

def carriage_geo(outer_bearing,inner_bearing,bearing_spacing_o,slide,ring_pcd,orientation):
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
    inner_radius = (ring_pcd - apex_s)/2
    inner_bearing_path_r = inner_radius - (apex_i/2)
    bearing_to_bearing_path = np.sqrt(bearing_spacing_y**2 + (bearing_spacing_o/2)**2)
    outer_bearing_path_r = inner_bearing_path_r + bearing_to_bearing_path
    outer_radius = outer_bearing_path_r
    
    match orientation:
        case "Outside":
            st.write("test")
    
    return bearing_spacing_y,inner_radius,inner_bearing_path_r,outer_bearing_path_r,bearing_to_bearing_path