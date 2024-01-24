import streamlit as st

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

    # if st.button("Reveal"):
    #     st.subheader("Your Selections:")
    #     for situation, choice in user_choices.items():
    #         st.write(f"{situation}: {choice}")

    if st.button("Reveal"):
        results = compare_choices(user_choices, correct_answers)
        for situation, (user_choice, correct_choice) in results.items():
            if user_choice == correct_choice:
                st.success(f"{situation}: Correct! You chose {user_choice}")
            else:
                st.error(
                    f"{situation}: Incorrect. You chose {user_choice}, but the correct category is {correct_choice}")

        # Compare with correct answers (you need to define the correct answers)
        # Display comparison results and feedback


# Run the app
if __name__ == "__main__":
    main()
