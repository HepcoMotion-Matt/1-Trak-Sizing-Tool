import streamlit as st
from calculations import carriage_geo
from pathlib import Path

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='1-Trak Sizing Tool',
    page_icon=':nut_and_bolt:',
)

#Left Margin
st.markdown("""
    <style>
        .block-container {
            text-align: left !important;
            padding-top: 2rem !important; 
            max-width: 1500px; /* widen or narrow the main body */
        }
    </style>
""", unsafe_allow_html=True)
# Top Margin
st.markdown("""
<style>
    .block-container {
        padding-top: 1rem !important;
    }
</style>
""", unsafe_allow_html=True)


st.title("1-Trak Sizing Tool")
st.write(
    "Configure the 1-Trak system below."
)

sb = st.sidebar

sb.header("1-Trak System Settings")
orientation = sb.selectbox("System Orientation", ["Inside", "Outside"], index=1)

path = Path("1-trak-sizing-tool").parent/"images"
match orientation:
    case "Outside":
        st.image(path/"System Orientation Illustrations - Outer.jpg")
    case "Inside":
        st.image(path/"System Orientation Illustrations - Inner.jpg")

with st.expander("Application Details - Inputs",expanded=True):
    match orientation:
        case "Outside":
            c1, c2, c3 = st.columns(3)
            with c1:
                outer_bearing = st.selectbox("Outer Bearing Size (G)", ["J25", "J34", "J40"], index=0, placeholder="Select Outer Bearing Size")
                inner_bearing = st.selectbox("Inner Bearing Size (H)", ["J25", "J34", "J40"], index=1, placeholder="Select Inner Bearing Size")
            with c2:
                bearing_spacing_x = st.number_input("Outer Bearing Spacing (D, mm)",min_value=0.0,max_value=500.0,step=0.1,value=50.0,key="spacing_outer")
                slide = st.selectbox("Slide Geometry", ["NS25", "NM44"],index=1, placeholder="Select Slide Geometry")
            with c3:
                ring_pcd = st.number_input("Ring PCD (mm)",min_value=100.0,max_value=5000.0,value=300.0)
        case "Inside":
            c1, c2, c3 = st.columns(3)
            with c1:
                inner_bearing = st.selectbox("Inner Bearing Size (G)", ["J25", "J34", "J40"], index=0, placeholder="Select Inner Bearing Size")
                outer_bearing = st.selectbox("Outer Bearing Size (H)", ["J25", "J34", "J40"], index=1, placeholder="Select Outer Bearing Size")
            with c2:
                bearing_spacing_x = st.number_input("Inner Bearing Spacing (D, mm)",min_value=0.0,max_value=500.0,step=0.1,value=50.0,key="spacing_inner")
                slide = st.selectbox("Slide Geometry", ["NS25", "NM44"],index=1, placeholder="Select Slide Geometry")
            with c3:
                ring_pcd = st.number_input("Ring PCD (mm)",min_value=100.0,max_value=5000.0,value=300.0)

match st.button("Calculate"):
    case True:
        bearing_spacing_y,outer_radius,outer_bearing_path_r,sector_angle,h,apex_r,inner_radius,inner_bearing_path_r,l1,l2,ms,mv,m = carriage_geo(outer_bearing,
                                                                    inner_bearing,
                                                                    bearing_spacing_x,
                                                                    slide,ring_pcd,
                                                                    orientation)
        with st.expander("Application Details - Outputs", expanded=True):
            c1, c2 = st.columns(2)
            with c1:
                st.subheader("Carriage Dimensions")
                st.metric("Inner to Outer Bearing Spacing (C, mm)", f'{bearing_spacing_y:.3f}')

                st.subheader("Carriage Capacities")
                d1,d2 = st.columns(2)
                with d1:
                    st.metric("L1 (N)", f'{l1:.0f}')
                    st.metric("Ms (Nm)", f'{ms:.1f}')
                    st.metric("Mv (Nm)", f'{mv:.1f}')
                with d2:
                    st.metric("L2 (N)", f'{l2:.0f}')
                    st.metric("M (Nm)", f'{m:.1f}')
            with c2:
                st.subheader("Ring Dimensions")
                d1, d2 = st.columns(2)
                with d1:
                    st.metric("Outer Ring Theo. Apex Radius (F, mm)", f'{outer_radius:.3f}')
                    st.metric("Inner Ring Theo. Apex Radius (E, mm)", f'{inner_radius:.3f}')
                    st.metric("Ring Theo. Apex (A, mm)", f'{apex_r:.3f}')
                    #st.metric("Sector Angle (°)", f'{sector_angle:.3f}')               
                with d2:
                    st.metric("Outer Bearing Radius Path (mm)", f'{outer_bearing_path_r:.3f}')
                    st.metric("Inner Bearing Radius Path (mm)", f'{inner_bearing_path_r:.3f}')
                    #st.metric("Sector Height (mm)", f'{h:.3f}')
    
    
result = carriage_geo(outer_bearing,inner_bearing,bearing_spacing_x,slide,ring_pcd,orientation)

st.write("outer_bearing:", outer_bearing)
st.write("carriage_geo result type:", type(result))
st.write("carriage_geo result:", result)

if result is None:
    st.error("carriage_geo() returned None")
    st.stop()

if not isinstance(result, (tuple, list)):
    st.error(f"carriage_geo() returned {type(result)}, expected tuple/list")
    st.stop()

st.write("Returned length:", len(result))

if len(result) != 13:
    st.error(f"carriage_geo() returned {len(result)} values, expected 13")
    st.stop()
