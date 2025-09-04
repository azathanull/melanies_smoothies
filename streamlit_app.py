# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Customize your Smoothie! :cup_with_straw:")
st.write(
  """Choose fruits you want in your custom Smoothie!
  """
)

name = st.text_input("Name on Smoothie:")
st.write("Name on smoothie will be", name)

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
ingridients_list = st.multiselect("Choose upto 5 ingridients", my_dataframe, max_selections=5)

if ingridients_list:
    ingredients_str = " ".join(ingridients_list)

    submit = st.button("Submit Order")

    if submit:
        my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_str + "','" + name + "')"
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
