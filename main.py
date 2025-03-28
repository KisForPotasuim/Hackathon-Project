import streamlit as st
import openai
import requests
import base64

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
user_input = st.text_area("")

if st.button("Get Recommendations"):
    if user_input:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": "Analyze user interests and suggest relevant fields."},
                      {"role": "user", "content": f"Here is the provided information:{user_input}"}]
        )
        ai_response = response["choices"][0]["message"]["content"].lower()
        careers = get_onet_careers(ai_response.split()[0])
        st.subheader("Recommended Careers from O*NET")
        for career_title, career_info in careers:
            st.write(f"### {career_title}")
            st.write(career_info)
    else:
        st.write("")