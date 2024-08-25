from datetime import datetime


def calculate_expiry_impact(expiry_date):
    days_until_expiry = (expiry_date - datetime.today().date()).days

    if days_until_expiry <= 0:
        return -5.0
    elif days_until_expiry <= 3:
        return -3.0 + (days_until_expiry / 3) * 1.0
    elif days_until_expiry <= 7:
        return -2.0 + (days_until_expiry - 3) / 4 * 1.0
    else:
        return 0


def get_item_price(food_name, food_type, description, is_halal, is_vegetarian, quantity, expiry_date):
    min_price_per_item = 0.5
    max_price_per_item = 12.0

    # Food type base values
    food_type_base = {
        "Cooked": 3.0,
        "Packaged": 4.0
    }

    small_food_multiplier = 1
    if any(ingredient in food_name.lower() or ingredient in description.lower() for ingredient in ['tidbits', 'snack']) and food_type == "Packaged":
        # small tidbits, snacks
        small_food_multiplier = 0.1
    if any(ingredient in food_name.lower() or ingredient in description.lower() for ingredient in ['drink', 'packet', 'milo', 'horlicks', 'milk']) and food_type == "Packaged":
        # packet drinks
        small_food_multiplier = 0.2

    # Check for keywords in food name and description for pricing adjustments
    ingredient_price_increase = 0
    if any(ingredient in food_name.lower() or ingredient in description.lower() for ingredient in ["chicken"]):
        ingredient_price_increase += 0.5
    if any(ingredient in food_name.lower() or ingredient in description.lower() for ingredient in ["pork"]):
        ingredient_price_increase += 0.7
    if any(ingredient in food_name.lower() or ingredient in description.lower() for ingredient in ["beef"]):
        ingredient_price_increase += 1.0
    if any(ingredient in food_name.lower() or ingredient in description.lower() for ingredient in ["fish"]):
        ingredient_price_increase += 1.2

    halal_impact = 0.5 if is_halal else 0
    vegetarian_impact = 0.5 if is_vegetarian else 0

    # expiry date impact
    expiry_impact = calculate_expiry_impact(expiry_date)

    total_score = (food_type_base.get(food_type, 0) +
                   halal_impact +
                   vegetarian_impact +
                   expiry_impact +
                   ingredient_price_increase) * small_food_multiplier

    # scaling factor for quantity to reduce price per unit as quantity increases
    quantity_discount_factor = 1 / (1 + 0.1 * quantity)
    total_score *= quantity_discount_factor

    # Normalization of score
    normalized_score = (total_score - 0) / 5
    price_per_item = min_price_per_item + normalized_score * (max_price_per_item - min_price_per_item)

    # Ensure the price per item stays within the min and max bounds
    price_per_item = max(min_price_per_item, min(price_per_item, max_price_per_item))

    return round(price_per_item, 2)

