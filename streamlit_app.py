# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
#removed above line for working in snis
from snowflake.snowpark.functions import col



# Write directly to the app
st.title("Customizee your Smoothie :cup_with_straw:")
st.write(
    """Replace this example with your own code!
    **And if you're new to Streamlit,** check
    out our easy-to-follow guides at
    [docs.streamlit.io](https://docs.streamlit.io).
    """
)

#option=st.selectbox('What\'s your favourite fruit?',('Banana','Strawberries','Peaches'))

#st.write('you selected :',option)
name_on_order=st.text_input("Enter Order name:")
st.write('The name of your smoothie will be :',name_on_order)

#session = get_active_session()
#add for snis
cnx=st.connection("snowflake")
session=cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingridients_list = st.multiselect('select upto 5 ingredients ',my_dataframe)

if ingridients_list:
    #st.text(ingridients_list);
    #st.write(ingridients_list)
    ingridients_string=''
    
    for each_fruit in ingridients_list:
        ingridients_string += each_fruit + ' '
        
    st.write(ingridients_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingridients_string +  """','""" + name_on_order + """') """

    #st.write(my_insert_stmt)
    #st.stop
    my_submit_button=st.button('Submit Order')
    if my_submit_button:
    #if ingridients_string:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!' + name_on_order , icon="✅" ) 
