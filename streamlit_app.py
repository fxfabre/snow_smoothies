import requests
import streamlit as st
from snowflake.snowpark.functions import col

#option = st.selectbox("Choose your favorite fruit :", ["aa", "bb"])
#st.write("You selected:", option)
#st.dataframe(data=df_fuits, use_container_width=True)

st.title(":cup_with_straw: Customize your smoothie ! :cup_with_straw:")
st.write("""Choose fruits you want""")

name_on_order = st.text_input("Your name")
st.write(f"The name on your smoothie will be {name_on_order}")

# Get the current credentials
cnx = st.connection("snowflake")
session = cnx.session()

# List of fruits
df_fuits = session.table("smoothies.public.fruit_options").to_pandas()
fruits_chosen = st.multiselect(
    "Select up to 5 ingrédients",
    df_fuits["FRUIT_NAME"].tolist(),
    max_selections=5,
)
search_on = df_fuits.set_index("FRUIT_NAME")["SEARCH_ON"].to_dict()

# Display the nutritional information
for fruit in fruits_chosen:
    search_fruit = search_on[fruit]
    fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{search_fruit}")

    # Display dataframe
    st.title(f"{fruit} Nutritional information")
    st.dataframe(fruityvice_response.json(), use_container_width=True)

if fruits_chosen:
    fruits_to_insert = ' '.join(sorted(fruits_chosen))

    insert_stmt = f"""
        insert into smoothies.public.orders(INGREDIENTS, NAME_ON_ORDER)
        values ('{fruits_to_insert}', '{name_on_order}')
    """.strip()
    # st.write(insert_stmt)

    do_insert = st.button("Submit order")
    if do_insert:
        session.sql(insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
