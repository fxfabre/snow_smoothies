# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
from snowflake.snowpark.context import get_active_session

#option = st.selectbox("Choose your favorite fruit :", ["aa", "bb"])
#st.write("You selected:", option)
#st.dataframe(data=df_fuits, use_container_width=True)


# Write directly to the app
st.title(":cup_with_straw: Customize your smoothie ! :cup_with_straw:")
st.write("""Choose fruits you want""")

name_on_order = st.text_input("Your name")
st.write(f"The name on your smoothie will be {name_on_order}")

# Get the current credentials
session = get_active_session()

# list of fruits
df_fuits = session.table("smoothies.public.fruit_options")

options = st.multiselect(
    "Select up to 5 ingrédients",
    df_fuits.select(col("FRUIT_NAME")),
    max_selections=5,
)

if options:
    ings = ' '.join(sorted(options))
    st.write("options : " + ings)

    insert_stmt = f"""
        insert into smoothies.public.orders(INGREDIENTS, NAME_ON_ORDER)
        values ('{ings}', '{name_on_order}')
    """.strip()
    st.write(insert_stmt)

    do_insert = st.button("Submit order")
    if do_insert:
        session.sql(insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")



