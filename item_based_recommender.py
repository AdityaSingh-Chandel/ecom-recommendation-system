# item_based_recommender.py

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def build_and_recommend(data_path, num_recommendations=5):
    """
    Builds an item-based collaborative filtering recommender and generates recommendations.
    """
    print("--- Phase 2: Building an Item-Based Recommender with Scikit-learn ---")
    
    print("1. Loading processed data...")
    try:
        df = pd.read_csv(data_path)
    except FileNotFoundError:
        print(f"Error: Processed data file not found at {data_path}. Please check the path.")
        return None
    
    # Vibe Check: Make sure the data is ready
    print(f"Data loaded with {len(df)} records. Sample:")
    print(df.head())
    
    # --- VIBE CODING FIX: Sample a smaller portion of the data ---
    # We will work with a random sample to avoid memory overflow issues
    # A sample size of 100,000 to 200,000 is usually a good starting point for proof of concept
    sample_size = 150000 
    
    print(f"\nProblem-solving! The dataset is too large for a pivot table on this machine.")
    print(f"Taking a random sample of {sample_size} records to continue building the recommender.")
    
    # Use .sample() to get a random subset of the DataFrame
    df = df.sample(n=sample_size, random_state=42).reset_index(drop=True)
    
    # It's good practice to re-filter sparse users/products after sampling
    # to ensure each user/product in the sample has a decent number of ratings
    min_interactions = 5
    user_counts = df['user_id'].value_counts()
    product_counts = df['product_id'].value_counts()
    
    filtered_users = user_counts[user_counts >= min_interactions].index
    filtered_products = product_counts[product_counts >= min_interactions].index
    
    df = df[df['user_id'].isin(filtered_users) & df['product_id'].isin(filtered_products)]
    print(f"Data sample after filtering sparse interactions: {len(df)} records")
    
    # Let's check the new number of unique users and products
    print(f"Unique users in sample: {df['user_id'].nunique()}")
    print(f"Unique products in sample: {df['product_id'].nunique()}")

    print("\n2. Creating the user-item matrix from the sample data...")
    # This time, it should work because the number of unique users/products is much smaller
    user_item_matrix = df.pivot_table(index='product_id', columns='user_id', values='rating').fillna(0)
    
    print("User-Item matrix created. Shape (products, users):", user_item_matrix.shape)
    print("Sample of the matrix:")
    print(user_item_matrix.head())

    print("\n3. Calculating item similarity using Cosine Similarity...")
    item_similarity_matrix = cosine_similarity(user_item_matrix)
    
    item_similarity_df = pd.DataFrame(item_similarity_matrix, index=user_item_matrix.index, columns=user_item_matrix.index)
    
    print("Item-to-item similarity matrix created. Sample:")
    print(item_similarity_df.head().iloc[:, :5])

    def get_recommendations_for_user(user_id):
        print(f"\n4. Generating recommendations for user: {user_id}")
        
        # Get the products the user has already rated
        user_ratings = user_item_matrix.loc[:, user_id]
        rated_products = user_ratings[user_ratings > 0].index.tolist()
        
        recommendation_scores = {}
        
        for rated_product in rated_products:
            if rated_product not in item_similarity_df.columns:
                continue # Skip if the product is not in our similarity matrix
            
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
        
        print("Top recommended products:")
        for product, score in recommended_products[:num_recommendations]:
            print(f"  - Product ID: {product}, Score: {score:.4f}")
        
        return recommended_products[:num_recommendations]

    sample_user_id = df['user_id'].iloc[0]
    users_with_many_ratings = df['user_id'].value_counts()
    if users_with_many_ratings.shape[0] > 5:
        sample_user_id = users_with_many_ratings.index[1]
        
    get_recommendations_for_user(sample_user_id)
    
    return get_recommendations_for_user

# --- Main entry point ---
if __name__ == "__main__":
    processed_data_file = r'D:\Datasets\processed_ecommerce_data.csv'
    
    build_and_recommend(processed_data_file)