# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests


# Page title, subtitle...
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("""Choose the fruits you want in your Custom Smoothie!""")


# Name on order:
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your smoothie will be:", name_on_order)


# Ingredients list + write-back to DB
cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.Stop()

pd_df = my_dataframe.to_pandas()
st.dataframe(pd_df)
st.Stop()


ingredient_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections=5
)


# Logic behind:
if ingredient_list:
    ingredients_string = ''

    for fruit_chosen in ingredient_list:
        ingredients_string += fruit_chosen + ' '
        st.subheader(fruit_chosen + ' nutrition information')
        # Add requests for API calls
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_chosen)
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """', '""" + name_on_order + """')"""

    ## Debugging:
    #st.write(my_insert_stmt)
    #st.stop()
    
    time_to_insert = st.button('Submit order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, ' + name_on_order + ' !', icon="✅")


