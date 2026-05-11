import streamlit as st
import plotly.express as px

# --- Calculations for Metrics ---
avg_price = df['price'].mean()
avg_area = df['area'].mean()
total_houses = len(df)

# --- Sidebar Filters ---
st.sidebar.header("Data Filters")
f_status = st.sidebar.multiselect(
    "Furnishing Status select karein:",
    options=df['furnishingstatus'].unique(),
    default=df['furnishingstatus'].unique()
)

air_con = st.sidebar.radio("Air Conditioning:", ['All', 'yes', 'no'])

# Filtering logic
df_selection = df[df['furnishingstatus'].isin(f_status)]
if air_con != 'All':
    df_selection = df_selection[df_selection['airconditioning'] == air_con]

# --- Main Dashboard ---
st.title("🏡 Housing Market Analysis Dashboard")
st.markdown("Yeh dashboard housing dataset ke prices aur features ko analyze karta hai.")

# Summary Metrics
m1, m2, m3 = st.columns(3)
m1.metric("Total Properties", total_houses)
m2.metric("Avg. Price", f"₹{avg_price:,.0f}")
m3.metric("Avg. Area (sqft)", f"{avg_area:.0f}")

st.divider()

# --- Visuals Section ---
col1, col2 = st.columns(2)

with col1:
    # Price vs Area Scatter Plot
    fig_scatter = px.scatter(
        df_selection, x="area", y="price",
        color="furnishingstatus",
        title="<b>Area vs Price (by Furnishing Status)</b>",
        hover_data=['bedrooms', 'bathrooms'],
        template="plotly_dark"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

with col2:
    # Price Distribution by Stories
    fig_box = px.box(
        df_selection, x="stories", y="price",
        title="<b>Price Range by Number of Stories</b>",
        color="stories",
        template="plotly_dark"
    )
    st.plotly_chart(fig_box, use_container_width=True)

# --- Features Analysis ---
st.markdown("### Feature-wise Average Price")
feat_cols = st.columns(2)

# Mainroad vs Price
fig_road = px.histogram(
    df_selection, x="mainroad", y="price", histfunc="avg",
    title="Avg Price: Mainroad Access vs No Access",
    color="mainroad"
)
feat_cols[0].plotly_chart(fig_road, use_container_width=True)

# AC vs Price
fig_ac = px.pie(
    df_selection, names='airconditioning', values='price',
    title="Price Contribution by AC availability",
    hole=0.4
)
feat_cols[1].plotly_chart(fig_ac, use_container_width=True)

# --- Searchable Table ---
st.markdown("### Raw Data Explorer")
st.dataframe(df_selection, use_container_width=True)
