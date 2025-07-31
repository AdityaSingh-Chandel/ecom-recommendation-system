# # recommendation_engine.py

# import pandas as pd
# from surprise import Dataset, Reader, SVD
# from surprise.model_selection import train_test_split
# from surprise import accuracy

# def train_and_evaluate_recommender(data_path):
#     """
#     Trains an SVD-based recommendation model and evaluates its performance.
#     """
#     print("--- Phase 2: Building and Evaluating the Recommender Engine ---")
    
#     print("1. Loading processed data...")
#     try:
#         df = pd.read_csv(data_path)
#     except FileNotFoundError:
#         print(f"Error: Processed data file not found at {data_path}. Please check the path.")
#         return None
    
#     # Ensure the required columns exist
#     if not all(col in df.columns for col in ['user_id', 'product_id', 'rating']):
#         print("Error: DataFrame must contain 'user_id', 'product_id', and 'rating' columns.")
#         return None

#     # Vibe Check: Look at the data again to make sure it's what we expect
#     print(f"Data loaded with {len(df)} records. Sample:")
#     print(df.head())

#     # The Surprise library needs a specific data format
#     # We define a 'Reader' object with the rating scale
#     # Based on your data, Amazon ratings are typically on a 1-5 scale
#     reader = Reader(rating_scale=(1, 5))

#     # Load the data from the pandas DataFrame into a Surprise Dataset
#     data = Dataset.load_from_df(df[['user_id', 'product_id', 'rating']], reader)

#     print("\n2. Splitting data into training and testing sets...")
#     # Split data into a training set and a testing set (80/20 split)
#     # The random_state ensures that the split is the same every time we run the code
#     trainset, testset = train_test_split(data, test_size=0.20, random_state=42)

#     print("\n3. Training the SVD model (the magic part!)...")
#     # We'll use the SVD algorithm, a powerful matrix factorization technique
#     # SVD finds hidden 'latent' factors that explain user preferences
#     # For now, we'll stick with the default parameters.
#     algo = SVD()
    
#     # Train the algorithm on the training set
#     algo.fit(trainset)
#     print("Model training complete!")

#     print("\n4. Evaluating the model on the test set...")
#     # Run the trained model on the test set to get predictions
#     predictions = algo.test(testset)
    
#     # Compute and print the RMSE (Root Mean Squared Error) and MAE (Mean Absolute Error)
#     # These are common metrics to evaluate how well a model predicts ratings.
#     # Lower values for both are better!
#     rmse = accuracy.rmse(predictions, verbose=True)
#     mae = accuracy.mae(predictions, verbose=True)
    
#     print(f"\nModel performance: RMSE={rmse:.4f}, MAE={mae:.4f}")

#     # You can now use the trained model to make predictions for specific users and items.
#     return algo, df

# def get_top_n_recommendations(predictions, n=10):
#     """
#     Return the top-N recommendations for each user from a set of predictions.
#     This function is useful for turning raw predictions into a final list of recommendations.
#     """
#     # First map the predictions to each user.
#     top_n = {}
#     for uid, iid, true_r, est, _ in predictions:
#         if uid not in top_n:
#             top_n[uid] = []
#         top_n[uid].append((iid, est))
    
#     # Then sort the predictions for each user and retrieve the k highest ones.
#     for uid, user_ratings in top_n.items():
#         user_ratings.sort(key=lambda x: x[1], reverse=True)
#         top_n[uid] = user_ratings[:n]
    
#     return top_n

# # --- Main execution block ---
# if __name__ == "__main__":
#     # Point to the processed data file you saved earlier
#     processed_data_file = r'D:\Datasets\processed_ecommerce_data.csv'

#     # Train the model
#     trained_algo, processed_df = train_and_evaluate_recommender(processed_data_file)
    
#     if trained_algo:
#         # Example of getting recommendations for a user
#         # Let's pick a random user from our processed dataset
#         random_user = processed_df['user_id'].sample(n=1).iloc[0]
        
#         print(f"\n5. Getting recommendations for a sample user: {random_user}")
        
#         # Get all products that this user has NOT rated
#         all_products = processed_df['product_id'].unique()
#         user_products = processed_df[processed_df['user_id'] == random_user]['product_id'].unique()
#         products_to_predict = [prod for prod in all_products if prod not in user_products]
        
#         # Predict ratings for these unseen products
#         unseen_predictions = [trained_algo.predict(random_user, prod) for prod in products_to_predict]
        
#         # Sort predictions by estimated rating
#         unseen_predictions.sort(key=lambda x: x.est, reverse=True)
        
#         print(f"Top 5 product recommendations for user '{random_user}':")
#         for pred in unseen_predictions[:5]:
#             # The .est attribute gives the predicted rating
#             print(f"  - Product ID: {pred.iid}, Predicted Rating: {pred.est:.4f}")

            