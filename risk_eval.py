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

r1 = "Low Risk"
r2 = "Medium Risk"
r3 = "Moderately-High Risk"
r4 = "High Risk"

risk_categories = [r1, r2, r3, r4]

sit1 = """Automated Job Candidate Selection: An AI system that makes final hiring decisions by evaluating candidates'
     resumes and interview performances."""

sit2 = """Automated Insurance Claim Adjudication: AI systems that evaluate and make final decisions on insurance 
    claims."""

sit3 = """Skills Development Conversation Preparation for Managers using Generative AI."""

sit4 = """Gigs Suggestions to Workers on Career Hub."""

sit5 = """GenAI tools for generating job descriptions."""

sit6 = """Skill suggestions to workers."""

sit7 = """Expenditure trend analysis using AI"""

sit8 = """Monitoring financial transactions for fraud and anomalies"""

sit9 = """Employee Engagement Analysis: AI can analyze employee feedback from surveys"""

sit10 = """Employee Layoff Predictions and Decisions: AI that not only predicts which employees might be at risk of 
layoffs but also makes recommendations or decisions about layoffs. """

# List of situations
situations = [globals()[f"sit{i}"] for i in range(1, 10)]

# Define the correct answers
correct_answers = {
    sit1: r4,
    sit2: r4,
    sit3: r3,
    sit4: r3,
    sit5: r2,
    sit6: r2,
    sit7: r1,
    sit8: r1,
    sit9: r1,
    sit10: r4
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
        sheet.update(range_name=f'D{rows}', values=[[st.session_state.feedback]])
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
        st.write(f"Situation {i+1}: " + situation)
        choice = st.selectbox(f"Choose category for Situation {i + 1}", risk_categories, key=i, disabled=st.session_state.displayon)
        user_choices[globals()[f"sit{i+1}"]] = choice
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

        st.write("In the following, you will see a bunch of situations and a drop down menu for you to choose the risk category of the situation. Make the appropriate choices and then reveal the answers and see how many you got right!")

        st.session_state["choices"] = display_situations(situations)
        st.button("Reveal", key="reveal", on_click=store_query)

        if st.session_state.displayon:
            results = compare_choices(st.session_state["choices"], correct_answers)
            for i, (situation, (user_choice, correct_choice)) in enumerate(results.items()):
                if user_choice == correct_choice:
                    st.success(f"For Situation {i+1}: Correct! You chose {user_choice}")
                else:
                    st.error(
                        f"For Situation {i+1}: Incorrect. You chose {user_choice}, but the correct category is {correct_choice}")
            st.subheader("Your Thoughts")
            st.text_input("Please provide feedback!", key="widget", on_change=submit)
            if st.session_state.feedback:
                st.write(f"Thank you for your feedback: {st.session_state.feedback}")


# Run the app
if __name__ == "__main__":
    main()
