import pickle
import streamlit as st
import pandas as pd
from PIL import Image
import requests
from io import BytesIO

def run():  # Ensure this function exists
    # Title of the app
    st.header("E-commerce Product Recommendation System")

    # Welcome message
    st.write("Welcome to the E-commerce Product Recommendation System!")

    # Correctly load the pickled files
    try:
        with open('product_list.pkl', 'rb') as file:
            products = pickle.load(file)
    except Exception as e:
        st.error(f"Error loading product list: {str(e)}")
        return

    try:
        with open('similarity.pkl', 'rb') as file:
            similarity = pickle.load(file)
    except Exception as e:
        st.error(f"Error loading similarity matrix: {str(e)}")
        return

    # Load the dataset containing the image URLs
    try:
        dataset = pd.read_csv('new_dataset.csv')
    except Exception as e:
        st.error(f"Error loading dataset: {str(e)}")
        return

    # Get the list of products
    product_list = products['Name'].values

    # Display the selectbox
    selected_product = st.selectbox(
        'Type or select a product',
        product_list
    )

    # Function to fetch image URLs based on the product ID
    def fetch_posters(product_id):
        filtered_dataset = dataset[dataset['ID'] == product_id]
        if filtered_dataset.empty:
            return []
        img_urls = filtered_dataset['imgURL'].values[0].split('|')
        cleaned_img_urls = [url.strip() for url in img_urls]
        return cleaned_img_urls

    # Function to recommend products
    def recommend(product):
        index = products[products['Name'] == product].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recommended_product_names = []
        recommended_product_posters = []

        for i in distances[1:7]:  # Skipping the first one (selected product itself)
            recommended_product_names.append(products.iloc[i[0]]['Name'])
            product_id = products.iloc[i[0]]['ID']
            posters = fetch_posters(product_id)
            if posters:
                recommended_product_posters.append(posters[0])
            else:
                recommended_product_posters.append("https://via.placeholder.com/150")

        return recommended_product_names, recommended_product_posters

    # Function to display images
    def display_images(images, captions):
        num_columns = 3
        num_rows = 2
        for row in range(num_rows):
            cols = st.columns(num_columns)
            for col in range(num_columns):
                index = row * num_columns + col
                if index < len(images):
                    img_url = images[index]
                    try:
                        response = requests.get(img_url)
                        response.raise_for_status()
                        img = Image.open(BytesIO(response.content))
                        cols[col].image(img, caption=captions[index], width=150)
                    except requests.exceptions.RequestException as e:
                        st.write(f"Error loading image from URL: {img_url} - {str(e)}")
                        cols[col].image("https://via.placeholder.com/150", caption="Error loading image", width=150)
                else:
                    cols[col].empty()

    # Button to show the recommendations
    if st.button('Show Recommendation'):
        recommended_products_list, recommended_product_posters = recommend(selected_product)
        display_images(recommended_product_posters, recommended_products_list)

        # Update recent searches in user_data.csv
        if 'username' in st.session_state and st.session_state.username:
            username = st.session_state.username
            user_data = pd.read_csv('user_data.csv')

            # Update the recent searches
            user_row = user_data.loc[user_data['Username'] == username]
            if not user_row.empty:
                recent_searches = user_row['Recent Searches'].values[0]
                recent_search_list = recent_searches.split('|') if pd.notna(recent_searches) else []
                
                # Add the current search to recent searches
                if selected_product not in recent_search_list:
                    recent_search_list.append(selected_product)
                    if len(recent_search_list) > 5:  # Keep only the last 5 searches
                        recent_search_list.pop(0)  # Remove the oldest search
                
                # Update the Recent Searches column
                user_data.loc[user_data['Username'] == username, 'Recent Searches'] = '|'.join(recent_search_list)
                user_data.to_csv('user_data.csv', index=False)

# Only run the app logic if this script is executed directly
if __name__ == "__main__":
    run()


