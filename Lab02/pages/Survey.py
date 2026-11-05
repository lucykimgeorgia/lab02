# This creates the page for users to input data.
# The collected data should be appended to the 'data.csv' file.

import streamlit as st
import pandas as pd
import os # The 'os' module is used for file system operations (e.g. checking if a file exists).

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Survey",
    page_icon="📝",
)

# PAGE TITLE AND USER DIRECTIONS
st.title("Ideal Temperature Survey 📝")
st.write("Please fill out the form below to add your data to the dataset.")

# DATA INPUT FORM
with st.form("survey_form"):
    category_input = st.text_input("What city do you live in?")
    value_input = st.text_input("What is your ideal outdoor temperature (°F)?")

    submitted = st.form_submit_button("Submit Data")

    if submitted:
        # Clean the inputs so they're stored consistently
        category = category_input.strip().title().replace(",", "")   # commas would break CSV columns
        value_text = value_input.strip()

        if category == "":
            st.error("Please enter a city.")
        else:
            try:
                value = float(value_text)
            except ValueError:
                st.error("Please enter your ideal temperature as a number (e.g., 72).")
            else:
                with open("data.csv", "r") as f:
                    content = f.read()
                needs_newline = content != "" and not content.endswith("\n")

                with open("data.csv", "a") as f:
                    if needs_newline:
                        f.write("\n")
                    f.write(f"{category},{value}\n")

                st.success("Your data has been submitted!")
                st.write(f"You entered: **City:** {category}, **Ideal Temperature:** {value}°F")


# DATA DISPLAY
# This section shows the current contents of the CSV file, which helps in debugging.
st.divider()
st.header("Current Data in CSV")

# Check if the CSV file exists and is not empty before trying to read it.
if os.path.exists('data.csv') and os.path.getsize('data.csv') > 0:
    # Read the CSV file into a pandas DataFrame.
    current_data_df = pd.read_csv('data.csv')
    # Display the DataFrame as a table.
    st.dataframe(current_data_df)
else:
    st.warning("The 'data.csv' file is empty or does not exist yet.")


