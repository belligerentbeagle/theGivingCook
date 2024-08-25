from .recipients_utils import *
from .map_utils import *
from .filter_utils import *
from src.db_utils.db_recipients import retrieveAvailableInventory, updateUserCredits, updateInventoryAfterBooking, createNewOrder, retrieveUserCredits

# import folium
# from folium.plugins import MarkerCluster
# from streamlit_folium import st_folium

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
        filtered_data = show_map_with_location(
            filtered_data, user_location, distance_filter)

    show_posting(filtered_data)


def setup_custom_buttons():
    st.markdown("""
    <style>
    @media (max-width: 768px) {
        .block-container {
            padding: 1rem !important;
        }
        .stButton>button {
            width: 100%;
            margin: 0;
        }
        .stMarkdown {
            padding: 0 !important;
        }
    }
    .button-container {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .count-display {
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 20px;
    }
    </style>
    """, unsafe_allow_html=True)


def show_posting(filtered_data):
    setup_custom_buttons()  

    cols = st.columns(3)
    col_index = 0

    for index, data in filtered_data.iterrows():
        current_col = cols[col_index]

        with current_col:
            with st.container(border=True, height=500):
                # Display content and custom buttons
                st.image(
                    data['photo'], use_column_width=True) if 'photo' in data else None
                st.markdown(f"##### {data['food_name']}")
                st.markdown(
                    f"<div style='font-size: small;'>{data['description']}</div>", unsafe_allow_html=True)
                st.caption(
                    f"{convertPriceToCredits(data['price'])} Credit | Expiry: {data['expiry_date']} | Quantity Left: {data['quantity']} units")
                st.markdown(
                    f"<div style='font-size: small;'>{data['address']}</div>", unsafe_allow_html=True)

                # Interaction buttons with custom functionality
                with st.container():
                    counter_key = f"counter_{data['inventory_id']}"
                    book_key = f"book_{data['inventory_id']}"

                    qtyButton, bookBtn = st.columns([3, 0.5])
                    qtySelected = 0

                    with qtyButton:
                        qtySelected = st.number_input("", min_value=1, step=1, placeholder="Enter quantity", key=counter_key)
                        print(qtySelected)

                    with bookBtn:
                        if st.button('Book Now ✅', key=book_key):
                            if qtySelected > 0:
                                # user_id = st.session_state.user_id
                                user_id = 1
                                qtyBooked = qtySelected
                                creditsSpent = qtyBooked * convertPriceToCredits(data['price'])
                                booking_successful(data, qtyBooked)

                                # Update database
                                qtyLeft = data['quantity'] - qtyBooked
                                updateInventoryAfterBooking(data['inventory_id'], qtyLeft)
                                createNewOrder(data['inventory_id'], user_id, qtyBooked, creditsSpent, False)
                                finalCredits = retrieveUserCredits(user_id) - creditsSpent
                                updateUserCredits(user_id, finalCredits)

                                # Reset after booking
                                st.rerun()
                            else:
                                booking_error()

                    col_index = (col_index + 1) % len(cols)


@st.dialog("Booking Error!")
def booking_error():
    st.error("You must select at least one item to book.")


@st.dialog("Thank you for booking!")
def booking_successful(item, qty):
    st.write(
        f"You have successfully booked {qty} units of {item['food_name']}. This costs {qty * convertPriceToCredits(item['price'])} credits.")
    st.write(f"Please scan the QR code at the venue upon collection.")
    st.write(f"Your collection point is:")
    st.write(item['address'])


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
            filtered_data = dynamic_filters.filter_df()

    # st.write("Included table for visualization for now (rm ltr)")
    # st.dataframe(filtered_data)

    return distance_filter, filtered_data


def show_map_with_location(postings, user_location, distance_filter):
    # st.write(f"User coordinates: {user_location}")
    vendors = filter_by_distance(postings, user_location, distance_filter)
    # remove photo from df for scatterplot processing
    vendors_no_photo = vendors.drop(columns=['photo'])
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
        data=vendors_no_photo,
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
    return vendors


def show_default_map(postings):
    singapore = [1.3521, 103.8198]
    # remove photo from df for scatterplot processing
    vendors_no_photo = postings.drop(columns=['photo'])
    view_state = pdk.ViewState(
        latitude=singapore[0], longitude=singapore[1], zoom=10.5)

    # Vendor locations layer
    vendor_layer = pdk.Layer(
        'ScatterplotLayer',
        data=vendors_no_photo,
        get_position='[longitude, latitude]',
        get_color='[200, 30, 0, 160]',
        get_radius=200,
    )

    st.pydeck_chart(pdk.Deck(map_style='mapbox://styles/mapbox/streets-v12',
                             initial_view_state=view_state,
                             layers=[vendor_layer]))

# def show_default_map(postings):
#     singapore = [1.3521, 103.8198]
#     # Create a map centered around Singapore
#     m = folium.Map(location=singapore, zoom_start=12, tiles='CartoDB positron')

#     # If your dataframe has columns named 'latitude' and 'longitude', this will work directly
#     # Create a MarkerCluster to add all your vendors
#     marker_cluster = MarkerCluster().add_to(m)

#     # Loop through the data frame
#     for idx, row in postings.iterrows():
#         # Create an HTML string for the popup
#         popup_html = f"""
#         <div style='width:200px;'><strong></strong><br>
#             {row['description']}<br>
#             Price: {row['price']}<br>
#             Address: {row['address']}<br>
#         </div>
#         """
#         popup = folium.Popup(popup_html, max_width=265)
#         folium.Marker(
#             location=[row['latitude'], row['longitude']],
#             popup=popup,
#             icon=folium.Icon(icon='info-sign', color='red')
#         ).add_to(marker_cluster)

#     # Display the map
#     st_folium(m, width=725)




def retrieve_inventory(user_location=None, max_distance=None):
    allInventory = retrieveAvailableInventory(get_todays_date())

    postings = []
    for (inv_id, food_name, food_type, description, is_halal, is_veg, expiry,
        date_of_entry, qty_left_after_booking, qty_left_after_scanning, for_ngo, vendor_id, photo, address, price) in allInventory:

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
                'quantity': qty_left_after_booking,
                'for_ngo': for_ngo,
                'address': address,
                'latitude': lat,
                'longitude': lon,
                'vendor_id': vendor_id,
                'photo': photo,
                'price': price

            })

    # print(postings)
    return pd.DataFrame(postings)
