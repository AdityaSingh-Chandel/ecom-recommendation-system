E-commerce Product Recommender System
A full-stack, personalized product recommendation system built as a proof-of-concept for a final year Computer Science project.

This application demonstrates the end-to-end process of building an intelligent web service, from data preprocessing and machine learning model creation to API development and a responsive web frontend.

🌟 Key Features
Intelligent Recommendations: A machine learning model uses Item-Based Collaborative Filtering to suggest products based on user ratings and item similarities.

Full-Stack Architecture: A three-tier application consisting of a data-driven Python backend, a Flask API, and a dynamic HTML/CSS/JavaScript frontend.

Robust Data Handling: The project demonstrates how to handle a large, sparse dataset by using an intelligent sampling strategy for in-memory model training.

Scalable API Design: A RESTful API serves recommendations efficiently, with a separate endpoint to dynamically fetch valid user IDs, preventing "no data" errors.

Professional UI/UX: A clean, modern, and user-friendly web interface allows for seamless interaction with the recommendation engine.

⚙️ Technologies Used
Backend & ML: Python, Flask, Pandas, Scikit-learn

Frontend: HTML, CSS, JavaScript (Vanilla)

Deployment & Versioning: Git, GitHub, Flask-CORS

🏗️ Project Architecture
The project follows a standard client-server architecture:

Data Layer: The processed_ecommerce_data.csv file (a filtered sample of a much larger dataset) serves as the basis for the machine learning model.

Backend (Python/Flask API):

The api.py script loads the data and builds the recommendation model once on startup.

It exposes two REST API endpoints:

/users: Returns a list of valid user IDs for the frontend.

/recommendations/<user_id>: Takes a user_id and returns a list of recommended products with names, images, and scores.

Frontend (HTML/CSS/JS):

The index.html file, styled with styles.css, provides a user interface.

script.js dynamically fetches the list of valid user IDs from the backend API.

When the user clicks "Get Recommendations," the script calls the API and displays the results in an organized, visually appealing format.

🚀 How to Run the Project
Follow these simple steps to get the project running on your local machine.

Prerequisites
Python 3.x

pip (Python package installer)

Step 1: Clone the Repository
Clone this repository to your local machine using Git:

git clone [https://github.com/AdityaSingh-Chandel/ecom-recommendation-system.git](https://github.com/AdityaSingh-Chandel/ecom-recommendation-system.git)
cd ecom-recommendation-system

Step 2: Set Up the Backend
Create a Python Virtual Environment (Highly Recommended):

python -m venv venv

Activate the Virtual Environment:

On Windows: venv\Scripts\activate

On macOS/Linux: source venv/bin/activate

Install Dependencies:

pip install pandas scikit-learn Flask Flask-CORS

Download the Dataset:

The model needs a data file to run. For this project, you can use the data_preprocessing.py script to get the data. First, create a data folder:

mkdir data

Then download the original dataset into the data folder. You can find links to it on Kaggle or a similar data repository.

Make sure the data_preprocessing.py script is updated to point to the correct file path. Once you have the data, run:

python data_preprocessing.py

This will create the processed_ecommerce_data.csv file, which your API uses.

Step 3: Run the Backend API
Make sure your virtual environment is active, and then run the api.py script:

python api.py

You should see a message that the Flask server is running on http://127.0.0.1:5000.

Step 4: Run the Frontend
With the API running, simply open the index.html file in your web browser. The page will automatically load the list of user IDs from your API. Select an ID from the dropdown and click "Get Recommendations" to see your system in action!

🤝 Contribution
Feel free to fork this repository, add new features (like a content-based filter or a different recommendation algorithm), and submit pull requests.

📄 License
This project is open source and available under the MIT License.
