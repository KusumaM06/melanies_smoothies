# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

# Input for the smoothie name
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name of your Smoothie will be:", name_on_order)

# Snowflake connection
cnx = st.connection("snowflake")
session = cnx.session()

# Fetch fruit options from Snowflake
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

# Allow the user to select up to 5 ingredients
ingredients_list = st.multiselect('Choose up to 5 ingredients:'
                                  ,my_dataframe.collect()
                                  ,max_selections=5)

if ingredients_list:
    # Create a string of chosen ingredients
    ingredients_string = ' '
    for fruit_chose in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        

    # Create an INSERT SQL statement
    my_insert_stmt = f"""INSERT INTO smoothies.public.orders(ingredients)
                         VALUES ('{ingredients_string}')"""

    st.write(my_insert_stmt)

# Button to submit the order
time_to_insert = st.button('Submit Order')
if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered!', icon="✅")
import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response)


