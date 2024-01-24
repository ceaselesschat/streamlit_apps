import streamlit as st
import gspread
from google.oauth2 import service_account

# Create a connection object.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive"
    ],
)
# conn = connect(credentials=credentials)
client = gspread.authorize(credentials)

# Define your risk categories
risk_categories = ["Low Risk", "Medium Risk", "Moderately-High Risk", "High Risk"]

# List of situations
situations = [
    "Dummy Situation 1: AI is just suggesting ideas.",
    "Dummy Situation 2: AI is making decisions for you.",
    # Add more situations as needed
]

# Define the correct answers
correct_answers = {
    "Situation 1": "Low Risk",
    "Situation 2": "High Risk",
    # Add correct answers for more situations as needed
}

COL_RANGE = 'A:D'

# Storing responses in google sheets


def store_query():
        # query: str,
        # response: str,
        # query_embed,
        # response_embed):

    sheet_url = st.secrets["private_gsheets_url"]  # this information should be included in streamlit secret
    sheet = client.open_by_url(sheet_url).get_worksheet(0)
    # existing_data = sheet.get(COL_RANGE)
    # existing_data.append([query, response])
    sheet.append_row(["1", "2", "3", "4"], table_range=COL_RANGE)
    # st.success('Data has been written to Google Sheets')
    return


# Function to display situations and dropdowns


def display_situations(situations):
    user_choices = {}
    for i, situation in enumerate(situations):
        st.text(situation)
        choice = st.selectbox(f"Choose category for Situation {i + 1}", risk_categories, key=i)
        user_choices[f"Situation {i + 1}"] = choice
    return user_choices

# Function to compare user choices with correct answers


def compare_choices(user_choices, correct_answers):
    results = {}
    for situation, user_choice in user_choices.items():
        correct_choice = correct_answers.get(situation)
        results[situation] = (user_choice, correct_choice)
    return results


# Main app
def main():
    st.title("AI Risk Evaluation Session")

    user_choices = display_situations(situations)
    show_feedback = False

    # if st.button("Reveal"):
    #     st.subheader("Your Selections:")
    #     for situation, choice in user_choices.items():
    #         st.write(f"{situation}: {choice}")

    if st.button("Reveal", on_click=store_query):
        show_feedback = True
        results = compare_choices(user_choices, correct_answers)
        for situation, (user_choice, correct_choice) in results.items():
            if user_choice == correct_choice:
                st.success(f"{situation}: Correct! You chose {user_choice}")
            else:
                st.error(
                    f"{situation}: Incorrect. You chose {user_choice}, but the correct category is {correct_choice}")
    # Text area for user feedback
    if show_feedback:
        st.subheader("Your Thoughts")
        user_feedback = st.text_area("What do you think about your results and the categorization exercise?")
        if user_feedback:
            st.write("Thank you for your feedback!")
        # Compare with correct answers (you need to define the correct answers)
        # Display comparison results and feedback


# Run the app
if __name__ == "__main__":
    main()
