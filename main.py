import streamlit as st
import openai
import requests
import base64
from requests.auth import HTTPBasicAuth
import json
from Url2 import Url
import os

openai.api_key = st.secrets["db_ai"]
onet_username = st.secrets["db_username"]
onet_password = st.secrets["db_password"]



cont_limit=20
totalpages=len(os.listdir("data/"))//cont_limit
flag=False

if 'page' not in st.session_state:
    st.session_state['page'] = 1
if 'next' not in st.session_state:
    st.session_state["next"]=False
if 'prev' not in st.session_state:
    st.session_state["prev"]=False


credentials = HTTPBasicAuth(onet_username, onet_password)
# credentials = f"{onet_username} : {onet_password}"
# credentials_2 = base64.b64encode(credentials.encode()).decode()
# headers = {"Authorization": f"Basic {credentials_2}"}

url1=Url("default","default","","","architect",5,write=False)
url1.get_onet_careers()
key={"Name":"Name:","Salary(National Median)":"Salary","Job Zone":"Edu"}

for i in os.listdir("data/"):
    url1.decodeData(title=i)

with open("sort/sortKey.json","r") as file:
    temp=json.load(file)
    url1.compiledData=temp.get("BigData")
    sortingKey={"Name":temp.get("Name:"),"Salary(National Median)":temp.get("Salary"),"Job Zone":temp.get("Edu")}
file.close()
careers=url1.sessionData()


# streamlit
st.title("Career Recommendation Chatbot")
st.write("Answer the questions below to get recommendations on majors and careers!")
question_1 = st.text_area("What are your hobbies?")
question_2=st.selectbox("What are your salary expectations?",["Less than $40K", "$40K - $70K", "$70K - $100K", "Above $100K"])
question_3= st.selectbox("What standard school subject do you enjoy the most?", ["Math", "Arts", "Biology", "Chemistry", "Physics", "Technology", "Business", "Social Studies","Physical Education", "Other"])
question_4=st.text_area("Do you enjoy working in groups?")
question_5=st.selectbox("Do you prefer:", ["Structured tasks", "Creative problem-solving", "A mix of both", "Neither"])
question_6=st.selectbox("What work environment do you prefer?", ["Office", "Outdoors", "Lab", "Remote", "Fieldwork"])
question_7=st.text_area("Do you like being the leader in projects?")
question_8 = st.text_area("Do you have any interests? If so please state them below.")
question_9 = st.text_area("Would you say you have a creative mind?")
question_10 = st.text_area("What are your work values?")
question_11 = st.text_area("What are your talents and strengths?")
question_12 = st.multiselect("What industry would you like to work in?", ["Healthcare","Education", "Agriculture", "Construction", "Transportation", "Energy", "Entertainment", "Art", "Hospitality", "Software", "Hardware", "Finance", "Manufacturing", "Culinary", "Engineering", "Marketing", "Advising", "Research", "Sales", "Investing", "Law", "Business", "Aerospace", "Manual Labor"])
question_13 = st.selectbox("How much education are you willing to go throRugh?", ["Bachelor's degree", "Master's degree", "Community college", "No college"])

user_input = f""" {question_1 if question_1 else "Not provided"} {question_2} {question_3} {question_4 if question_4 else "Not provided"} {question_5 if question_5 else "Not provided"} {question_6} {question_7} {question_8 if question_8 else "Not provided"} {question_9 if question_9 else "Not provided"} {question_10 if question_10 else "Not provided"} {question_11 if question_11 else "Not provided"} {question_12 if question_12 else "Not provided"}"""

col1_, col2_, col3_ = st.columns([30,40,15])

with col1_:
    rec=st.button("Get Recommendations")
    
with col3_:
    sort=st.selectbox("Sort Options",["Name","Salary(National Median)","Job Zone"])

orginizer=st.container(border=True,height=500)


def stateful_buttons(key,button):
    if(button):
        st.session_state[key]= not st.session_state[key]

    return st.session_state[key]

def rec_botton_press(page,sortKey,careers=careers,button="rec"):
    st.session_state['page']=page
    
    start=(page-1)*cont_limit
    end=page*cont_limit
    
    if(len(sortKey)-end<0):
        end=len(sortKey)

    if(len(sortKey)-start<0):
        start=end-cont_limit

    with orginizer:

        st.subheader("Here's what we reccomend:")
        for j in range(start,end):
            with st.container(border=True):
                st.write(f"### {sortKey[j]}")
                st.write(careers[sortKey[j]]["Description:"])
                st.write(f"Salary: {careers[sortKey[j]]['Salary:']}")
                st.write(f"Job Zone: {careers[sortKey[j]]['Prep:']}")

try:
    sortType
except:
    sortType="changeMe"

with orginizer:
    
    if sort:
        if(not sort==sortType):
            sortType=sort
            rec_botton_press(1,sortingKey[sortType])

    if (rec and sort):
        if user_input:
            # response = openai.chat.completions.create(
            #     model="gpt-4o",

            #     messages=[{"role": "system", "content": "Analyze user responses and suggest relevant careers."}, {"role": "user", "content": user_input}]
            # )
            # ai_response = response["choices"][0]["message"]["content"].lower()
            # careers = get_onet_careers(ai_response.split()[0])

            #have ai return a code phrase(first two) or anything that conforms with decode data format
            rec_botton_press(1,sortingKey[sortType])

        else:
            st.write("")


orgcol1,orgcol2,orgcol3=st.columns([30,110,15])
with orgcol1:
    previous=st.button("Previous")
with orgcol3:
    next=st.button("Next")

if(stateful_buttons("prev",previous) and st.session_state['page']>1):
    rec_botton_press(st.session_state['page']-1,sortingKey[sortType])

if(stateful_buttons("next",next) and st.session_state['page']<=totalpages):
    rec_botton_press(st.session_state['page']+1,sortingKey[sortType])