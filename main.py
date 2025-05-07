import streamlit as st
import openai
import requests
import base64
from requests.auth import HTTPBasicAuth
import json
from Url2 import Url
import os

# Just adding comments and fixing minor errors
# https://services.onetcenter.org/ws/mnm/occupations?keyword=engineer&start=1&end=5
openai.api_key = "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"
onet_username = "career_chatbot1"
onet_password = "7335gtw"
credentials = HTTPBasicAuth(onet_username, onet_password)
# onet_url= "https://services.onetcenter.org/ws/mnm"

# credentials = f"{onet_username} : {onet_password}"
# credentials_2 = base64.b64encode(credentials.encode()).decode()
# headers = {"Authorization": f"Basic {credentials_2}"}


# streamlit
st.title("Career Recommendation Chatbot")
st.write("Answer the questions below to get recommendations on majors and careers!")
question_1 = st.text_area("What are your hobbies?")
question_2=st.selectbox("What are your salary expectations?",["Less than $40K", "$40K - $70K", "$70K - $100K", "Above $100K"])
question_3= st.selectbox("What standard school subject do you enjoy the most?", ["Math", "Arts", "Biology", "Chemistry", "Physics", "Technology", "Business", "Social Studies","Physical Education", "Other"])
question_4=st.text_area("Do you enjoy working in groups? Feel free to explain or just leave a yes or no.")
question_5=st.selectbox("Do you prefer:", ["Structured tasks", "Creative problem-solving", "A mix of both", "Neither"])
question_6=st.selectbox("What work environment do you prefer?", ["Office", "Outdoors", "Lab", "Remote", "Fieldwork"])
question_7=st.text_area("Do you like being the leader in projects? Feel free to explain or just leave a yes or no.")
question_8 = st.text_area("Do you have any interests? If so please state them below.")
question_9 = st.text_area("Would you say you have a creative mind?")
question_10 = st.text_area("What are your work values?")
question_11 = st.text_area("What are your talents and strengths?")
question_12 = st.multiselect("What industry would you like to work in?", ["Healthcare","Education", "Agriculture", "Construction", "Transportation", "Energy", "Entertainment", "Art", "Hospitality", "Software", "Hardware", "Finance", "Manufacturing", "Culinary", "Engineering", "Marketing", "Advising", "Research", "Sales", "Investing", "Law", "Business", "Aerospace", "Manual Labor"])
question_13 = st.selectbox("How much education are you willing to go through?", ["Bachelor's degree", "Master's degree", "Community college", "No college"])

user_input = f""" {question_1 if question_1 else "Not provided"} {question_2} {question_3} {question_4 if question_4 else "Not provided"} {question_5 if question_5 else "Not provided"} {question_6} {question_7} {question_8 if question_8 else "Not provided"} {question_9 if question_9 else "Not provided"} {question_10 if question_10 else "Not provided"} {question_11 if question_11 else "Not provided"} {question_12 if question_12 else "Not provided"} {", ".join(question_13) if question_13 else "Not specified"}"""

url1=Url("default","default","","","architect",5)
if st.button("Get Recommendations"):
    if user_input:
        # response = openai.chat.completions.create(
        #     model="gpt-4o",

        #     messages=[{"role": "system", "content": "Analyze user responses and suggest relevant careers."}, {"role": "user", "content": user_input}]
        # )
        # ai_response = response["choices"][0]["message"]["content"].lower()
        # careers = get_onet_careers(ai_response.split()[0])
        careers=url1.get_onet_careers()
        for i in range(len(os.listdir("data/"))):
            url1.decodeData(id=i)
        data=url1.sessionData()
        st.subheader("Here's what we reccomend:")

        for career_title, career_info in careers:
            st.write(f"### {career_title}")
            st.write(career_info)
    else:

        st.write("")

