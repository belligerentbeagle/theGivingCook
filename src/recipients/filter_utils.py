import streamlit as st
import pydeck as pdk
import pandas as pd
from geopy.distance import geodesic
from streamlit_dynamic_filters import DynamicFilters
from .recipients_utils import *


def filter_by_beneficiary_type(beneficiaryType, df):
    filtered_df = df  
    if 'for_ngo' in df:
        if beneficiaryType == "NGOs":
            filtered_df = df[df['for_ngo'] == 1]  
        elif beneficiaryType == "Individuals":
            filtered_df = df[df['for_ngo'] == 0]  

    return filtered_df

def show_filters(postings, type):
    filter = {
        'Dietary Preferences': ['is_halal', 'is_vegetarian'],
        'Type of Food': ['cooked', 'packaged'],
    }

    selected_preferences = st.multiselect(
        f"Select {type}:",
        options=filter[type],
        default=[]
    )

    if selected_preferences:
        filtered_data = postings
        for preference in selected_preferences:
            if preference in filtered_data.columns:
                filtered_data = filtered_data[filtered_data[preference] == 1]

    else:
        # If no preference is selected, show all data
        filtered_data = postings

    return filtered_data

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
                'photo': row['photo'],
                'price': row['price']
            })

    return pd.DataFrame(filtered_postings)