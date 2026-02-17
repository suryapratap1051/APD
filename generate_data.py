import pandas as pd
import numpy as np
import random

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

# Number of products
n_products = 1000

# Categories and their typical price ranges
categories = {
    'Electronics': (100, 2000),
    'Books': (5, 50),
    'Clothing': (10, 150),
    'Home & Kitchen': (15, 300),
    'Sports': (20, 500),
    'Toys': (5, 100),
    'Beauty': (8, 80)
}

# Adjectives and product types for generating names
adjectives = ['Amazing', 'Premium', 'Eco-friendly', 'Compact', 'Advanced', 
              'Stylish', 'Durable', 'Affordable', 'Lightweight', 'Ergonomic']
product_types = {
    'Electronics': ['Laptop', 'Smartphone', 'Headphones', 'Tablet', 'Camera'],
    'Books': ['Novel', 'Cookbook', 'Biography', 'Guide', 'Textbook'],
    'Clothing': ['T-Shirt', 'Jeans', 'Jacket', 'Sweater', 'Dress'],
    'Home & Kitchen': ['Blender', 'Toaster', 'Pillow', 'Pan', 'Lamp'],
    'Sports': ['Yoga Mat', 'Dumbbell', 'Bicycle', 'Tent', 'Soccer Ball'],
    'Toys': ['Action Figure', 'Board Game', 'Puzzle', 'Doll', 'Car'],
    'Beauty': ['Shampoo', 'Moisturizer', 'Lipstick', 'Perfume', 'Face Wash']
}

# Generate data
data = []
for i in range(1, n_products + 1):
    cat = random.choice(list(categories.keys()))
    min_price, max_price = categories[cat]
    actual_price = round(np.random.uniform(min_price, max_price), 2)
    
    # Discount between 0% and 40%
    discount_pct = np.random.randint(0, 41)
    discounted_price = round(actual_price * (1 - discount_pct / 100), 2)
    
    rating = round(np.random.uniform(1, 5), 1)
    rating_count = np.random.randint(0, 10000)
    
    # Generate product name
    adj = random.choice(adjectives)
    prod_type = random.choice(product_types[cat])
    product_name = f"{adj} {prod_type}"
    
    data.append({
        'product_id': f'P{i:04d}',
        'product_name': product_name,
        'category': cat,
        'actual_price': actual_price,
        'discounted_price': discounted_price,
        'discount_percentage': discount_pct,
        'rating': rating,
        'rating_count': rating_count
    })

# Create DataFrame and save to CSV
df = pd.DataFrame(data)
df.to_csv('amazon_products.csv', index=False)
print("✅ Synthetic Amazon product data saved to 'amazon_products.csv'")