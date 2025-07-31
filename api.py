# api.py

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, jsonify, request
from flask_cors import CORS
import numpy as np
import os

# --- VIBE CODING: FAKE PRODUCT CATALOG ---
# In a real application, this data would come from a database.
# For our proof of concept, we will use a hard-coded dictionary.
PRODUCT_CATALOG = {
    'B006ZW4IVE': {
        'name': 'Samsung 4K 55-inch TV',
        'image_url': 'https://m.media-amazon.com/images/I/71I3n0N6gKL._AC_SL1500_.jpg'
    },
    'B000YM2OIK': {
        'name': 'Sony WH-1000XM5 Headphones',
        'image_url': 'https://m.media-amazon.com/images/I/61r59C4X9iL._AC_SL1500_.jpg'
    },
    'B001N85NMI': {
        'name': 'AmazonBasics USB Cable',
        'image_url': 'https://m.media-amazon.com/images/I/613a-a5Vq-L._AC_SL1000_.jpg'
    },
    'B0002BEQN4': {
        'name': 'Bose SoundLink Speaker',
        'image_url': 'https://m.media-amazon.com/images/I/6121t6t81DL._AC_SL1500_.jpg'
    },
    'B003D3NEEU': {
        'name': 'Logitech MX Master 3 Mouse',
        'image_url': 'https://m.media-amazon.com/images/I/71Y-tL7pTUL._AC_SL1500_.jpg'
    },
    'B0083B3U3K': {
        'name': 'Anker PowerCore 10000',
        'image_url': 'https://m.media-amazon.com/images/I/610tq7v-ZPL._AC_SL1500_.jpg'
    },
    'B008F49T2Y': {
        'name': 'GoPro HERO11 Black',
        'image_url': 'https://m.media-amazon.com/images/I/61J6Q5R8qAL._AC_SL1500_.jpg'
    },
    'B003L49M7G': {
        'name': 'Apple AirPods Pro',
        'image_url': 'https://m.media-amazon.com/images/I/71Wl1V-10eL._AC_SL1500_.jpg'
    }
}

app = Flask(__name__)
CORS(app) 

user_item_matrix = None
item_similarity_df = None
processed_df = None

def build_recommender_model(data_path):
    global user_item_matrix, item_similarity_df, processed_df
    
    print("--- VIBE CODING: BUILDING RECOMMENDER MODEL ON SERVER STARTUP ---")
    
    try:
        df = pd.read_csv(data_path)
    except FileNotFoundError:
        print(f"Error: Processed data file not found at {data_path}. Please check the path.")
        return False
    
    sample_size = 150000 
    print(f"Taking a random sample of {sample_size} records from the full dataset.")
    df = df.sample(n=sample_size, random_state=42).reset_index(drop=True)
    
    min_interactions = 5
    user_counts = df['user_id'].value_counts()
    product_counts = df['product_id'].value_counts()
    
    filtered_users = user_counts[user_counts >= min_interactions].index
    filtered_products = product_counts[product_counts >= min_interactions].index
    
    df = df[df['user_id'].isin(filtered_users) & df['product_id'].isin(filtered_products)]
    print(f"Data sample after filtering sparse interactions: {len(df)} records")
    
    processed_df = df
    
    print("\nCreating the user-item matrix from the sample data...")
    user_item_matrix = df.pivot_table(index='product_id', columns='user_id', values='rating').fillna(0)
    
    print("User-Item matrix created. Shape:", user_item_matrix.shape)

    print("\nCalculating item similarity using Cosine Similarity...")
    item_similarity_matrix = cosine_similarity(user_item_matrix)
    
    item_similarity_df = pd.DataFrame(item_similarity_matrix, index=user_item_matrix.index, columns=user_item_matrix.index)
    
    print("\n--- Model build complete! The API is ready to serve requests. ---")
    return True

def get_recommendations_for_user(user_id, num_recommendations=5):
    if user_item_matrix is None or item_similarity_df is None:
        print("Model not loaded. Cannot generate recommendations.")
        return []

    if user_id not in user_item_matrix.columns:
        print(f"User ID '{user_id}' not found in the sample data. Cannot provide personalized recommendations.")
        return []

    user_ratings = user_item_matrix.loc[:, user_id]
    rated_products = user_ratings[user_ratings > 0].index.tolist()
    
    recommendation_scores = {}
    
    for rated_product in rated_products:
        if rated_product not in item_similarity_df.columns:
            continue
        
        similar_items = item_similarity_df[rated_product].sort_values(ascending=False)
        
        for similar_product, similarity_score in similar_items.items():
            if similar_product not in recommendation_scores:
                recommendation_scores[similar_product] = 0
            
            user_rating_for_product = user_ratings.loc[rated_product]
            recommendation_scores[similar_product] += similarity_score * user_rating_for_product

    for product in rated_products:
        if product in recommendation_scores:
            del recommendation_scores[product]

    recommended_products = sorted(recommendation_scores.items(), key=lambda x: x[1], reverse=True)
    
    return recommended_products[:num_recommendations]

@app.route('/recommendations/<user_id>', methods=['GET'])
def get_recommendations(user_id):
    print(f"API request received for user: {user_id}")
    
    recommendations = get_recommendations_for_user(user_id)

    if recommendations:
        formatted_recommendations = []
        for prod_id, score in recommendations:
            product_info = PRODUCT_CATALOG.get(prod_id, {
                'name': 'Product ' + prod_id,
                'image_url': 'https://via.placeholder.com/150'
            })
            formatted_recommendations.append({
                'product_id': prod_id,
                'name': product_info['name'],
                'image_url': product_info['image_url'],
                'score': float(score)
            })
        return jsonify(formatted_recommendations)
    else:
        return jsonify({"message": f"No recommendations found for user ID '{user_id}'."}), 404

# --- NEW API ENDPOINT ---
@app.route('/users', methods=['GET'])
def get_valid_users():
    """
    API endpoint to get a list of all user IDs in the current in-memory model.
    """
    if user_item_matrix is None:
        return jsonify({"message": "Model not loaded."}), 503 # Service Unavailable
    
    user_ids = user_item_matrix.columns.tolist()
    return jsonify(user_ids)

if __name__ == '__main__':
    processed_data_file = r'D:\Datasets\processed_ecommerce_data.csv'

    if build_recommender_model(processed_data_file):
        print("\nStarting Flask API...")
        os.environ['FLASK_APP'] = 'api.py'
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        print("\nError: Model failed to build. API will not start.")