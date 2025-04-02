import streamlit as st
import openai
import requests
import base64
# Just adding comments and fixing minor errors
# https://services.onetcenter.org/ws/mnm/occupations?keyword=engineer&start=1&end=5
openai.api_key = "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"
onet_username = "career_chatbot1"
onet_password = "7335gtw"
onet_url= "https://services.onetcenter.org/ws/mnm"

credentials = f"{onet_username} : {onet_password}"
credentials_2 = base64.b64encode(credentials.encode()).decode()
headers = {"Authorization": f"Basic {credentials_2}"}

def get_onet_careers(keyword,headers=headers):
    url = f"{onet_url}/occupations?keyword={keyword}&start=1&end=5"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        careers = []
        for job in data.get("occupation_list", []):
            job_code = job["code"]
            job_title = job["title"]
            job_info = get_onet_job_details(job_code)
            careers.append((job_title, job_info))
        return careers if careers else [("No relevant careers found", "")]
    return [("Failed to fetch data from O*NET", "")]

def get_onet_job_details(job_code,headers=headers):
    url = f"{onet_url}/occupation/{job_code}/summary"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        description = data.get("description", "No description available.")
        wage_info = data.get("wages", {}).get("national_median", {})
        salary = wage_info.get("annual", "Salary data unavailable")
        return f"Description: {description}\nMedian Salary: ${salary}"
    return "Details unavailable."

# streamlit
st.title("Career Recommendation Chatbot")
st.write("Answer the questions below to get recommendations on majors and careers!")
question_1 = st.text_area("What are your hobbies?")
question_2=st.selectbox("What are your salary expectations?",["Less than $40K", "$40K - $70K", "$70K - $100K", "Above $100K"])
question_3= st.selectbox(("What standard school subject do you enjoy the most?", ["Math", "Arts", "Biology", "Chemistry", "Physics", "Technology", "Business", "Social Studies","Physical Education", "Other"])
question_4=st.text_area("Do you enjoy talking to people? Feel free to explain or just leave a yes or no.")
question_5=st.text_area("Do you enjoy working in groups? Feel free to explain or just leave a yes or no.")
question_5=st.selectbox("Do you prefer:", ["Structured tasks", "Creative problem-solving", "A mix of both", "Neither"])
question_6=st.selectbox("What work environment do you prefer?", ["Office", "Outdoors", "Lab", "Remote", "Fieldwork"])
question_7=st.text_area("Do you like being the leader in projects?" Feel free to explain or just leave a yes or no.")
question_8 = st.text_area("Do you have any interests? If so please state them below.")
question_9 = st.text_area("Would you say you have a creative mind?")
question_10 = st.text_area("What are your work values?")
question_11 = st.text_area("What are your talents and strengths?")
question_12 = st.multiselect("What industry would you like to work in?", ["Healthcare","Education", "Agriculture", "Construction", "Transportation", "Energy", "Entertainment", "Art", "Hospitality", "Software" "Hardware", "Finance", "Manufacturing", "Culinary, "Engineering", "Marketing", "Advising", "Research, "Sales", "Investing", "Law", "Business", "Aerospace", "Manual Labor"])
question_13 = st.selectbox("How much education are you willing to go through?", ["Bachelor's degree", "Master's degree", "Community college, "No college"])

user_input = f""" {question_1 if question_1 else "Not provided"} {question_2} {question_3} {question_4 if question_4 else "Not provided"} {question_5 if question_5 else "Not provided"} {question_6} {question_7} {question_8 if question_8 else "Not provided"} {question_9 if question_9 else "Not provided"} {question_10 if question_10 else "Not provided"} {question_11 if question_11 else "Not provided"} {question_12 if question_12 else "Not provided"} {", ".join(question_13) if question_13 else "Not specified"} {question_14}"""

if st.button("Get Recommendations"):
    if user_input:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": "Analyze user responses and suggest relevant careers."}, {"role": "user", "content": user_input}]
        )
        ai_response = response["choices"][0]["message"]["content"].lower()
        careers = get_onet_careers(ai_response.split()[0])
        st.subheader("Here's what we reccomend:")
        for career_title, career_info in careers:
            st.write(f"### {career_title}")
            st.write(career_info)
    else:
        st.write("")
