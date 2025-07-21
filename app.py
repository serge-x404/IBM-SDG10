import streamlit as st
import google.generativeai as genai
import os

api_key = st.secrets["general"]["GOOGLE_API_KEY"]
genai.configure(api_key=api_key)


# Initialize model
model = genai.GenerativeModel("gemini-1.5-flash")

# UI
st.set_page_config(page_title="SDG 10 Chatbot – Reduced Inequalities", page_icon="🌍")
st.title("🌍 SDG 10 Chatbot – Reduced Inequalities")
st.markdown("Ask anything related to inequality — based on income, gender, education, disability, or global opportunities.")

user_input = st.text_area("What would you like to ask or discuss about inequality?", max_chars=500)

# Define category classifier
def classify_issue(query):
    prompt = f"""Classify the following user input into one of these categories:
    - Gender Inequality
    - Income Inequality
    - Disability Discrimination
    - Racial or Ethnic Inequality
    - Global/Regional Inequality
    - Education Gap
    - General Human Rights

    User Input: {query}
    Reply only with the most fitting category name.
    """
    response = model.generate_content(
        prompt,
        generation_config={"temperature": 0.4, "max_output_tokens": 100}
    ).text.strip().lower()

    categories = {
        "gender": "gender",
        "income": "income",
        "disability": "disability",
        "racial": "racial",
        "ethnic": "racial",
        "global": "global",
        "regional": "global",
        "education": "education",
        "human rights": "general"
    }

    for keyword, value in categories.items():
        if keyword in response:
            return value
    return "general"

# Response logic
def get_response(category):
    prompts = {
        "gender": "Explain how gender inequality affects individuals and give suggestions to promote equality.",
        "income": "Explain how income inequality arises and what can be done to reduce it.",
        "disability": "How does discrimination based on disability affect people? Suggest inclusive practices.",
        "racial": "Talk about racial or ethnic inequality and how to reduce such discrimination.",
        "global": "Discuss inequality between countries or regions and how it affects development.",
        "education": "Explain how unequal access to education creates social inequality. Suggest solutions.",
        "general": "Talk about human inequality and what actions can reduce inequality in general."
    }
    return model.generate_content(
        prompts[category],
        generation_config={"temperature": 0.7, "max_output_tokens": 300}
    ).text

# Run logic
if user_input:
    with st.spinner("Classifying and generating response..."):
        category = classify_issue(user_input)
        response = get_response(category)

    st.success(f"**Category Detected:** {category.capitalize()}")
    st.markdown(f"**Response:**\n{response}")
