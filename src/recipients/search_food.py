from .recipients_utils import *
from .map_utils import *
from .filter_utils import *
from src.db_utils.db_recipients import retrieveAvailableInventory, updateUserCredits, updateInventoryAfterBooking, createNewOrder, retrieveUserCredits

import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

import streamlit as st
import pydeck as pdk
import pandas as pd
from geopy.distance import geodesic
from streamlit_dynamic_filters import DynamicFilters


def view_postings():
    col1, col2, col3 = st.columns([4, 1, 1])
    user_location = [None, None]

    st.header('Explore food vendors')
    with st.container():
        col1, col2 = st.columns([1, 5])
        with col1:
            st.write("Locate Me! -->")
        with col2:
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


def show_posting(filtered_data):
    cols = st.columns(3)
    col_index = 0

    for index, data in filtered_data.iterrows():
        current_col = cols[col_index]

        with current_col:
            with st.container(border=True, height=450):
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

                    qtySelected = 0

                    qtySelected = st.number_input(
                        " ", min_value=0, step=1, placeholder="Enter quantity", key=counter_key)
                    print(qtySelected)

                    if st.button('Book Now ✅', key=book_key):
                        if qtySelected > 0:
                            user_id = st.session_state.user_id
                            qtyBooked = qtySelected
                            creditsSpent = qtyBooked * \
                                convertPriceToCredits(data['price'])
                            booking_successful(data, qtyBooked)

                            # Update database
                            qtyLeft = data['quantity'] - qtyBooked
                            updateInventoryAfterBooking(
                                data['inventory_id'], qtyLeft)
                            createNewOrder(
                                data['inventory_id'], user_id, qtyBooked, creditsSpent, False)
                            finalCredits = retrieveUserCredits(
                                user_id) - creditsSpent
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
    distance_filter = st.slider('Select maximum distance (km)', 0, 50, 10)

    postings = retrieve_inventory()
    col1, col2, col3 = st.columns(3)

    with col1:
        filtered_data = show_filters(postings, 'Dietary Preferences')

    with col2:
        if not filtered_data.empty:
            dynamic_filters = DynamicFilters(
                filtered_data, filters=['food_type'])
            dynamic_filters.display_filters()
            filtered_data = dynamic_filters.filter_df()

    with col3:
        beneficiaryType = st.selectbox(
            "Select Beneficiary Type",
            ("NGOs", "Individuals"),
            index=None,
            placeholder="Beneficiary Type",
        )

        filtered_data = filter_by_beneficiary_type(beneficiaryType, postings)

    # st.write("Included table for visualization for now (rm ltr)")
    # st.dataframe(filtered_data)

    return distance_filter, filtered_data


# def show_map_with_location(postings, user_location, distance_filter):
#     print("USER LOCATION", user_location)

#     user_location_data = [{
#         "name": 'user',
#         "url": 'https://p7.hiclipart.com/preview/457/630/559/location-computer-icons-symbol-clip-art-location-thumbnail.jpg',
#         "latitude": user_location[0],
#         "longitude": user_location[1]
#     }
#     ]
#     user_df = pd.DataFrame(user_location_data)

#     # st.write(f"User coordinates: {user_location}")
#     vendors = filter_by_distance(postings, user_location, distance_filter)
#     # remove photo from df for scatterplot processing

#     if 'photo' in vendors.columns:
#         vendors_no_photo = vendors.drop(columns=['photo'])
#     else:
#         vendors_no_photo = vendors

#     # max_distance = max([geodesic(user_location, (res['latitude'], # shouldnt include this so that we can still see postings outside of indicated radius
#     #                     res['longitude'])).km for res in vendors], default=0)
#     zoom_level = calculate_zoom_level(distance_filter)
#     view_state = pdk.ViewState(
#         latitude=user_location[0], longitude=user_location[1], zoom=zoom_level)

#     # User's location layer
#     print(user_df)
#     print(postings)


#     layers = []
#     user_layer = pdk.Layer(
#         'ScatterplotLayer',
#         data=user_df,
#         get_position='[longitude, latitude]',
#         get_color='[0, 0, 0, 200]',
#         get_radius=100,
#         pickable=True,
#         auto_highlight=True,
#         tooltip={"text": "{latitude}, {longitude}"}
#     )

#     layers.append(user_layer)

#     # Vendor locations layer
#     if not vendors_no_photo.empty:
#         vendor_layer = pdk.Layer(
#             'ScatterplotLayer',
#             data=vendors_no_photo,
#             get_position='[longitude, latitude]',
#             get_color='[200, 30, 0, 160]',
#             get_radius=100,
#         )
#         layers.append(vendor_layer)
#     else:
#         st.write("There are no available items now.")

#     # Circle layer
#     circle = create_geojson_circle(user_location, distance_filter)
#     circle_layer = pdk.Layer(
#         "GeoJsonLayer",
#         data=circle,
#         opacity=0.1,
#         filled=True,
#         get_fill_color=[255, 180, 0, 140]
#     )
#     layers.append(circle_layer)

#     st.pydeck_chart(pdk.Deck(map_style='mapbox://styles/mapbox/streets-v12',
#                              initial_view_state=view_state,
#                              layers=layers))
#     return vendors


# def show_default_map(postings):
#     singapore = [1.3521, 103.8198]
#     # remove photo from df for scatterplot processing

#     if 'photo' in postings.columns:
#         vendors_no_photo = postings.drop(columns=['photo'])
#     else:
#         vendors_no_photo = postings

#     view_state = pdk.ViewState(
#         latitude=singapore[0], longitude=singapore[1], zoom=10.5)

#     layer = []
#     # Vendor locations layer
#     if not vendors_no_photo.empty:
#         vendor_layer = pdk.Layer(
#             'ScatterplotLayer',
#             data=vendors_no_photo,
#             get_position='[longitude, latitude]',
#             get_color='[200, 30, 0, 160]',
#             get_radius=200,
#         )
#         layer.append(vendor_layer)


#     st.pydeck_chart(pdk.Deck(map_style='mapbox://styles/mapbox/streets-v12',
#                              initial_view_state=view_state,
#                              layers=layer))

def show_default_map(postings):
    singapore = [1.3521, 103.8198]
    f = folium.Figure(width=725)
    m = folium.Map(location=singapore, zoom_start=12,
                   tiles='openstreetmap').add_to(f)
    marker_cluster = MarkerCluster().add_to(m)

    for idx, row in postings.iterrows():
        popup_html = f"""
        <div style='width:200px;'><strong>{row['food_name']}</strong><br>
            Address: {row['address']}<br>
        </div>
        """
        popup = folium.Popup(popup_html, max_width=265)
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=popup,
            icon=folium.Icon(icon='info-sign', color='green')
        ).add_to(marker_cluster)

    st_folium(m, width=725)


def show_map_with_location(postings, user_location, distance_filter):
    f = folium.Figure(width=725)
    m = folium.Map(location=user_location, zoom_start=calculate_zoom_level(
        distance_filter), tiles='openstreetmap').add_to(f)
    marker_cluster = MarkerCluster().add_to(m)

    folium.Marker(
        user_location,
        icon=folium.Icon(icon='home', color='blue'),
    ).add_to(m)

    folium.CircleMarker(
        location=user_location,
        radius=distance_filter,
        color="cornflowerblue",
        stroke=False,
        fill=True,
        fill_opacity=0.2,
        opacity=1,
        popup="{} pixels".format(distance_filter),
    ).add_to(m)

    for idx, row in postings.iterrows():
        popup_html = f"""
        <div style='width:200px;'><strong>{row['food_name']}</strong><br>
            Credits: {int(row['price'])}<br>
            Address: {row['address']}<br>
        </div>
        """
        popup = folium.Popup(popup_html, max_width=265)
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=popup,
            icon=folium.Icon(icon='info-sign', color='green')
        ).add_to(marker_cluster)

    st_folium(m, width=725)
    return postings


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

    return pd.DataFrame(postings)
