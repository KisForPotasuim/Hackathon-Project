import requests
import base64

# https://services.onetcenter.org/ws/mnm/occupations?keyword=engineer&start=1&end=5
onet_username = "career_chatbot1"
onet_password = "7335gtw"
onet_url= "https://services.onetcenter.org/ws/"

credentials = f"{onet_username} : {onet_password}"
credentials_2 = base64.b64encode(credentials.encode()).decode()
headers = {"Authorization": f"Basic {credentials_2}"}
categorySplit={"default":"mnm","future":"online/bright_outlook"}

def get_onet_careers(keyword,headers=headers,category="default",interval=40):
    category=categorySplit[category]
    if(category=="mnm"):
        url = f"{onet_url}{category}/occupations?keyword={keyword}&start=1&end=5"
    elif(category=="online/bright_outlook"):
        initial=0
        end=initial+interval
        url = f"{onet_url}{category}/grow?category_id=grow&sort=name&start={initial}&end={end}"
    print(url)
    response = requests.get(url, headers=headers)
    if response.status_code == 200: #add format type for this and should work
        data = response.json()
        careers = []
        for job in data.get("occupation_list", []):
            job_code = job["code"]
            job_title = job["title"]
            job_info = get_onet_job_details(job_code)
            careers.append((job_title, job_info))
        return careers if careers else [("No relevant careers found", "")]
    return [("Failed to fetch data from O*NET", "")]

def get_onet_job_details(job_code,headers=headers,category="mnm"):
    url = f"{onet_url}{category}/occupation/{job_code}/summary"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        description = data.get("description", "No description available.")
        wage_info = data.get("wages", {}).get("national_median", {})
        salary = wage_info.get("annual", "Salary data unavailable")
        return f"Description: {description}\nMedian Salary: ${salary}"
    return "Details unavailable."


print(get_onet_careers("bob",category="future"))