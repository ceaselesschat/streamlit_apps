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
if 'user_name' not in st.session_state:
    st.session_state['user_name'] = ""

if 'feedback' not in st.session_state:
    st.session_state['feedback'] = ""

if "choices" not in st.session_state:
    st.session_state['choices'] = {}

if "displayon" not in st.session_state:
    st.session_state['displayon'] = False


# def submit():
#     st.session_state.feedback = st.session_state.widget
#     st.session_state.widget = ""

def submit():
    st.session_state.feedback = st.session_state.widget
    sheet_url = st.secrets["private_gsheets_url"]["spreadsheet"]  # this information should be included in streamlit secret
    sheet = client.open_by_url(sheet_url).get_worksheet(0)
    q_list = sheet.col_values(1)
    rows = len(q_list)
    # print(st.session_state.query)
    if q_list[rows - 1] == st.session_state['user_name']:
        sheet.update(f'D{rows}', st.session_state.feedback)
    return


# Storing responses in google sheets


def store_query():
    sheet_url = st.secrets["private_gsheets_url"]["spreadsheet"]
    sheet = client.open_by_url(sheet_url).get_worksheet(0)
    for situation, user_choice in st.session_state["choices"].items():
        sheet.append_row([st.session_state['user_name'], situation, user_choice, ""], table_range=COL_RANGE)
    st.session_state.displayon = True
    return



# Function to display situations and dropdowns


def display_situations(situations):
    user_choices = {}
    for i, situation in enumerate(situations):
        st.text(situation)
        choice = st.selectbox(f"Choose category for Situation {i + 1}", risk_categories, key=i, disabled=st.session_state.displayon)
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

    st.session_state['user_name'] = st.text_input("Please enter your name:")

    if st.session_state['user_name']:
        st.write(f"Welcome, {st.session_state['user_name']}!")

    st.session_state["choices"] = display_situations(situations)
    st.button("Reveal", key="reveal", on_click=store_query)

    if st.session_state.displayon:
        results = compare_choices(st.session_state["choices"], correct_answers)
        for situation, (user_choice, correct_choice) in results.items():
            if user_choice == correct_choice:
                st.success(f"{situation}: Correct! You chose {user_choice}")
            else:
                st.error(
                    f"{situation}: Incorrect. You chose {user_choice}, but the correct category is {correct_choice}")
    st.subheader("Your Thoughts")
    st.text_input("Please provide feedback!", key="widget", on_change=submit)
    if st.session_state.feedback:
        st.write(f"Thank you for your feedback: {st.session_state.feedback}")


# Run the app
if __name__ == "__main__":
    main()
