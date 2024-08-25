from .recipients_utils import *
from .map_utils import *
from src.db_utils.db_recipients import retrieveAllVendors, retrieveAvailableInventory

import streamlit as st
import pydeck as pdk
import pandas as pd
from geopy.distance import geodesic
from streamlit_dynamic_filters import DynamicFilters


def view_postings():
    user_location = retrieve_current_location()
    distance_filter, filtered_data = show_map_elems()

    if 'user_latlong' not in st.session_state:
        st.session_state['user_latlong'] = user_location

    if all(x is None for x in user_location):
        show_default_map(filtered_data)
    else:
        show_map_with_location(filtered_data, user_location, distance_filter)


def show_map_elems():
    st.header('Explore food vendors')
    distance_filter = st.slider('Select maximum distance (km)', 0, 50, 10)

    postings = retrieve_inventory()
    col1, col2 = st.columns(2)

    with col1:
        filtered_data = show_filters(postings, 'Dietary Preferences')

    with col2:
        if not filtered_data.empty:
            dynamic_filters = DynamicFilters(
                filtered_data, filters=['food_type'])
            dynamic_filters.display_filters()

    st.write("Included table for visualization for now (rm ltr)")
    st.dataframe(filtered_data)

    return distance_filter, filtered_data


def show_filters(postings, type):
    filter = {
        'Dietary Preferences': ['is_halal', 'is_vegetarian'],
        'Type of Food': ['cooked', 'packaged']
    }

    selected_preferences = st.multiselect(
        f"Select {type}:",
        options=filter[type],
        default=[]
    )

    if selected_preferences:
        filtered_data = postings
        for preference in selected_preferences:
            filtered_data = filtered_data[filtered_data[preference] == 1]
    else:
        # If no preference is selected, show all data
        filtered_data = postings

    return filtered_data


def show_map_with_location(postings, user_location, distance_filter):
    # st.write(f"User coordinates: {user_location}")
    vendors = filter_by_distance(postings, user_location, distance_filter)
    # max_distance = max([geodesic(user_location, (res['latitude'], # shouldnt include this so that we can still see postings outside of indicated radius
    #                     res['longitude'])).km for res in vendors], default=0)
    zoom_level = calculate_zoom_level(distance_filter)
    view_state = pdk.ViewState(
        latitude=user_location[0], longitude=user_location[1], zoom=zoom_level)

    # User's location layer
    user_location_layer = pdk.Layer(
        'ScatterplotLayer',
        data=[{"latitude": user_location[0], "longitude": user_location[1]}],
        get_position='[longitude, latitude]',
        get_color='[255, 100, 100, 180]',
        get_radius=150,
        pickable=True,
        tooltip="User Location"
    )

    # Vendor locations layer
    vendor_layer = pdk.Layer(
        'ScatterplotLayer',
        data=vendors,
        get_position='[longitude, latitude]',
        get_color='[200, 30, 0, 160]',
        get_radius=200,
    )

    # Circle layer
    circle = create_geojson_circle(user_location, distance_filter)
    circle_layer = pdk.Layer(
        "GeoJsonLayer",
        data=circle,
        opacity=0.2,
        filled=True,
        get_fill_color=[255, 180, 0, 140]
    )

    st.pydeck_chart(pdk.Deck(map_style='mapbox://styles/mapbox/streets-v12',
                             initial_view_state=view_state,
                             layers=[user_location_layer, vendor_layer, circle_layer]))


def show_default_map(postings):
    singapore = [1.3521, 103.8198]
    vendors = postings
    view_state = pdk.ViewState(
        latitude=singapore[0], longitude=singapore[1], zoom=10.5)

    # Vendor locations layer
    vendor_layer = pdk.Layer(
        'ScatterplotLayer',
        data=vendors,
        get_position='[longitude, latitude]',
        get_color='[200, 30, 0, 160]',
        get_radius=200,
    )

    st.pydeck_chart(pdk.Deck(map_style='mapbox://styles/mapbox/streets-v12',
                             initial_view_state=view_state,
                             layers=[vendor_layer]))


def filter_by_distance(postings, user_location, max_distance):
    filtered_postings = []

    for index, row in postings.iterrows():
        lat, lon = convert_address_to_latlong(row['address'])

        if lat is not None and lon is not None:
            if max_distance is not None and user_location is not None:
                distance = geodesic(user_location, (lat, lon)).km
                # if distance > max_distance:
                #     continue  # Skip this posting if it's outside the max distance

            filtered_postings.append({
                'inventory_id': row['inventory_id'],
                'food_name': row['food_name'],
                'food_type': row['food_type'],
                'description': row['description'],
                'is_halal': row['is_halal'],
                'is_vegetarian': row['is_vegetarian'],
                'expiry_date': row['expiry_date'],
                'date_of_entry': row['date_of_entry'],
                'quantity': row['quantity'],
                'address': row['address'],
                'latitude': lat,
                'longitude': lon,
                'vendor_id': row['vendor_id'],
                # 'photo': row['photo']
            })

    return filtered_postings


def retrieve_inventory(user_location=None, max_distance=None):
    allInventory = retrieveAvailableInventory(get_todays_date())

    postings = []
    for (inv_id, food_name, food_type, description, is_halal, is_veg, expiry,
         date_of_entry, qty, vendor_id, photo, address) in allInventory:

        lat, lon = convert_address_to_latlong(address)
        if lat is not None and lon is not None:
            if max_distance is not None and user_location is not None:
                distance = geodesic(user_location, (lat, lon)).km
                if distance > max_distance:
                    continue  # Skip this posting if it's outside the max distance

            postings.append({
                'inventory_id': inv_id,
                'food_name': food_name,
                'food_type': food_type,
                'description': description,
                'is_halal': is_halal,
                'is_vegetarian': is_veg,
                'expiry_date': expiry,
                'date_of_entry': date_of_entry,
                'quantity': qty,
                'address': address,
                'latitude': lat,
                'longitude': lon,
                'vendor_id': vendor_id
                # 'photo': photo
            })

    # print(postings)
    return pd.DataFrame(postings)
