import streamlit as st
import pandas as pd
import plotly.express as px

# Load the CSV file
FILE_PATH = r"C:\Users\Public\rto.csv"
@st.cache_data
def load_data():
    df = pd.read_csv(FILE_PATH)
    return df

# Load the data
df = load_data()

# Dashboard title
st.title("RTO Dashboard")
st.markdown("Explore information about Registered Training Organisations (RTOs) in Australia.")

# Sidebar filters
st.sidebar.header("Filter Options")
states = st.sidebar.multiselect("Select States", df["Head Office Location State"].unique())
status = st.sidebar.multiselect("Select Status", df["Status"].unique())
delivery_approval = st.sidebar.multiselect(
    "Delivery Approval", 
    ["NSW Delivery Approved", "VIC Delivery Approved", "QLD Delivery Approved",
     "SA Delivery Approved", "WA Delivery Approved", "TAS Delivery Approved",
     "NT Delivery Approved", "ACT Delivery Approved", "International Delivery Approved"]
)

# Filter data based on selections
filtered_data = df.copy()
if states:
    filtered_data = filtered_data[filtered_data["Head Office Location State"].isin(states)]
if status:
    filtered_data = filtered_data[filtered_data["Status"].isin(status)]
if delivery_approval:
    approval_filters = filtered_data[delivery_approval].eq("TRUE").any(axis=1)
    filtered_data = filtered_data[approval_filters]

# Show filtered data
st.subheader("Filtered Data")
st.write(f"Displaying {len(filtered_data)} RTOs based on filters")
st.dataframe(filtered_data)

# Visualization
st.subheader("Visualizations")

# Map
st.markdown("### RTOs by Location")
if "Latitude" in filtered_data.columns and "Longitude" in filtered_data.columns:
    filtered_data = filtered_data.dropna(subset=["Latitude", "Longitude"])
    fig = px.scatter_mapbox(
        filtered_data,
        lat="Latitude",
        lon="Longitude",
        hover_name="Legal Name",
        hover_data={"Head Office Location State": True, "Status": True},
        color="Head Office Location State",
        zoom=3,
        height=600,
    )
    fig.update_layout(mapbox_style="open-street-map")
    st.plotly_chart(fig)

# Count by state
st.markdown("### Count of RTOs by State")
state_count = filtered_data["Head Office Location State"].value_counts()
fig = px.bar(
    state_count,
    x=state_count.index,
    y=state_count.values,
    labels={"x": "State", "y": "Number of RTOs"},
    title="Number of RTOs by State",
    color=state_count.values,
    color_continuous_scale="Viridis",
)
st.plotly_chart(fig)

# CEO Contact Information
st.subheader("CEO Contact Information")
st.markdown(
    """
    Use this table to find key contact information for RTOs.
    """
)
contact_cols = ["Legal Name", "CEO Contact Name", "CEO Email", "CEO Mobile", "CEO Phone"]
st.dataframe(filtered_data[contact_cols])

st.markdown("Developed with ❤️ using Streamlit.")
