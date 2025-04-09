import requests
import base64
from requests.auth import HTTPBasicAuth


# https://services.onetcenter.org/ws/mnm/occupations?keyword=engineer&start=1&end=5
onet_username = "career_chatbot1"
onet_password = "7335gtw"

credentials = HTTPBasicAuth(onet_username, onet_password)
# credentials_2 = base64.b64encode(credentials.encode()).decode()
# headers = {"Authorization": f"{credentials_2}"}

class Url():
    def __init__(self,type,category,subcat,sortcat,keyword,prep,initial=21,end=40,code=None):
        self.baseUrl="https://services.onetcenter.org/ws/"
        self.service=type
        self.category=category
        self.subcat=subcat
        self.sort=sortcat
        self.keyword=keyword
        self.prep=prep
        self.url=self.baseUrl
        self.initial=initial
        self.end=end
        self.code=code
        self.sortUrl()

    def decode(self):
        if(not self.subcat):
            self.subcat=""
        return [self.serviceSplit[self.service],self.categorySplit[self.category],self.fineTuning[self.category][self.subcat]]

    def makeUrl(self):
        info=self.decode()
        return self.baseUrl+info[0]+info[1],info[2]
    
    def handleUrl(self): #adds the variables, and handles special format. I'm ignoring the code subcat
        url=self.makeUrl()
        temp=url[1]
        url=url[0]
        flag=False
        if(self.category=="prep"):
            url=url+f"{self.prep}"
        elif(self.category=="search"): #add sort(special exception)
            url=url+temp+f"{self.keyword}"
            flag=True
        elif(self.category=="occ"):
            url=url+str(self.code)+str(self.fineTuning[self.category][""])
        else:
            url=url+temp
        return url, flag
    
    def sortUrl(self):
        url=self.handleUrl()
        url=url[0]
        if(self.category=="occ"):
            pass
        else:
            # flag=url[1]
            end=self.sortsplit["def"]
            end=(end[0:7]+f"{self.initial}"+end[8:13]+f"{self.end}")
            url=url+self.sortcatSplit[self.sort]+end
        self.url=url
        return url #for debugging i guess

    categorySplit={"default":"careers/","future":"bright_outlook/","prep":"job_preparation/","search":"search/","occ":"occupation/"}
    serviceSplit={"default":"mnm/","web":"online/"}
    fineTuning={
            "":{"":""},
            "default":{"":""},
            "future":{"grow":"grow","openings":"openings","emerging":"emerging","code":""},
            "prep":{"ready":""},
            "search":{"keyword":"?keyword="},
            "occ":{"":"/summary"}
            }
    sortcatSplit={"name":"?sort=name","future":"?sort=bright_outlook","search":""}
    sortsplit={"def":"&start=2&end=4"} #chars index is 7,13

def get_onet_careers(url,headers=credentials):
    response = requests.get(url.url, auth=headers)

    if response.status_code == 200:
        data = response.json()
        careers = []
        for job in data.get("occupation_list", []):
            url=Url("web","occ","","name",a,5,code=job_code)
            job_code = job["code"]
            job_title = job["title"]
            job_info = get_onet_job_details(url)
            careers.append((job_title, job_info))
        return careers if careers else [("No relevant careers found", "")]
    return [("Failed to fetch data from O*NET", "")]

# def get_onet_job_details(job_code,headers=headers):
#     url = f"{onet_url}/occupation/{job_code}/summary"
#     response = requests.get(url, headers=headers)
#     if response.status_code == 200:
#         data = response.json()
#         description = data.get("description", "No description available.")
#         wage_info = data.get("wages", {}).get("national_median", {})
#         salary = wage_info.get("annual", "Salary data unavailable")
#         return f"Description: {description}\nMedian Salary: ${salary}"
#     return "Details unavailable."


# def get_onet_careers(url,headers=headers):
#     response = requests.get(url.url, headers=headers)
#     if response.status_code == 200:
#         data = response.json()
#         careers = []
#         for job in data.get("occupation_list", []):
#             job_code = job["code"]
#             job_title = job["title"]
#             # job_info = get_onet_job_details(job_code)
#             # careers.append((job_title, job_info))
#         return job_code
#         return careers if careers else [("No relevant careers found", "")]
#     return [("Failed to fetch data from O*NET", "")]

def get_onet_job_details(url,headers=credentials):
    response = requests.get(url.url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        description = data.get("description", "No description available.")
        wage_info = data.get("wages", {}).get("national_median", {})
        salary = wage_info.get("annual", "Salary data unavailable")
        return f"Description: {description}\nMedian Salary: ${salary}"
    return "Details unavailable."


a="artichect"
test=[
Url("default","future","grow","name",a,5),
Url("web","search","keyword","search",a,5),
Url("default","prep","ready","future",a,5),
Url("default","default","","name",a,5),
Url("web","occ","","name",a,5,code="51-9191.00")
] #0,2,3 are good..

for i in test:
    print(i.url)
    print(get_onet_careers(i,headers=credentials))