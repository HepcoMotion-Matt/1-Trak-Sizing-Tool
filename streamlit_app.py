import streamlit as st
from calculations import carriage_geo

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='1-Trak Sizing Tool',
    page_icon=':gear:',
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
    "Configure the 1-Trak system below. Please consult the Help tab if you require any assistance."
)

sb = st.sidebar

sb.header("1-Trak System Settings")
orientation = sb.selectbox("System Orientation", ["Inside", "Outside"], index=1)

with st.expander("Application Details - Inputs",expanded=True):
    c1, c2, c3 = st.columns(3)
    with c1:
        outer_bearing = st.selectbox("Outer Bearing Size", ["J25", "J34", "J40"], index=0, placeholder="Select Outer Bearing Size")
        inner_bearing = st.selectbox("Inner Bearing Size", ["J25", "J34", "J40"], index=1, placeholder="Select Inner Bearing Size")
    with c2:
        bearing_spacing_o = st.number_input("Outer Bearing Spacing (mm)",min_value=0.0,max_value=500.0,step=0.1,value=50.0)
        slide = st.selectbox("Slide Geometry", ["NS25", "NM44"],index=1, placeholder="Select Slide Geometry")
    with c3:
        ring_pcd = st.number_input("Ring PCD (mm)",min_value=100.0,max_value=500.0,value=300.0)

match st.button("Calculate"):
    case True:
        bearing_spacing_y, inner_radius, inner_bearing_path_r, outer_bearing_path_r,bearing_to_bearing_path = carriage_geo(outer_bearing,
                                                                    inner_bearing,
                                                                    bearing_spacing_o,
                                                                    slide,ring_pcd,
                                                                    orientation)
        st.header("Application Details - Outputs")
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Carriage Dimensions")
            st.metric("Inner to Outer Bearing Spacing (mm)", f'{bearing_spacing_y:.3f}')
        with c2:
            st.subheader("Ring Dimensions")
            d1, d2 = st.columns(2)
            with d1:
                st.metric("Inner Ring Radius (mm)", f'{inner_radius:.3f}')
                st.metric("Outer Ring Radius (mm)", f'{outer_bearing_path_r:.3f}')
            with d2:
                st.metric("Inner Bearing Radius Path (mm)", f'{inner_bearing_path_r:.3f}')
                st.metric("Bearing to Bearing Path Length (mm)", f'{bearing_to_bearing_path:.3f}')

match orientation:
    case "Outside":
        st.write("The geometry is outside")
    case "Inside":
        st.write("The geometry is inside")