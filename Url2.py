import requests
import base64
from requests.auth import HTTPBasicAuth
import json


# https://services.onetcenter.org/ws/mnm/occupations?keyword=engineer&start=1&end=5
onet_username = "career_chatbot1"
onet_password = "7335gtw"

credentials = HTTPBasicAuth(onet_username, onet_password)
# credentials_2 = base64.b64encode(credentials.encode()).decode()
# headers = {"Authorization": f"{credentials_2}"}


class Url():
    def __init__(self,type,category,subcat,sortcat,keyword,prep,initial=1,end=2,code=None):
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
        # self.careerInfo=self.get_onet_careers()

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
        elif(self.category=="default" and self.code):
            url+=self.code
        else:
            url=url+temp
        return url, flag
    
    def sortUrl(self):
        url=self.handleUrl()
        url=url[0]
        if(self.category=="default"):
            pass
        else:
            # flag=url[1]
            end=self.sortsplit["def"]
            end=(end[0:7]+f"{self.initial}"+end[8:13]+f"{self.end}")
            url=url+self.sortcatSplit[self.sort]+end
        self.url=url
        return url #for debugging i guess

    def get_onet_careers(self,headers=credentials):
        self.careers=[]
        accept={"Accept" : "application/json"}
        response = requests.get(self.url, auth=headers, headers=accept)

        if response.status_code == 200:
            data = response.json()
            careers = []
            for job in data.get(self.jsonKey[self.category], []):
                job_code = job["code"]
                job_title = job["title"]
                temp=Url("default","default","","",a,5,code=job_code)
                job_info = self.get_onet_job_details(temp)
                self.careers.append((job_title, job_info))
            # return data
            return self.careers if self.careers else [("test", "")]
        return [("Failed to fetch data from O*NET", "")]

    def get_onet_job_details(self,temp,headers=credentials):
        # https://services.onetcenter.org/v1.9/ws/mnm/careers/[O*NET-SOC Code]/job_outlook("salary")

        accept={"Accept" : "application/json"}
        accessList=[temp.url,temp.url+self.detailFindKey["salary"],temp.url+self.detailFindKey["school"]] #these are most important:general description,salary+brightoutlook, and prep needed
        file=None
        tag={"0":"Description:","1":"Salary:","2":"Prep:","3":"Education:"}
        for i in accessList:
            response = requests.get(i, auth=headers, headers=accept)
            
            if response.status_code == 200:
                data = response.json()
                tempList=[
                data.get("what_they_do", None),
                data.get("salary", {}).get("annual_median", None),
                data.get("job_zone",None),
                data.get("education_usually_needed",{}).get("category",None)]
                if(not file):
                    file=open(f"{data.get("title","data")}.txt","w+") #this works, but too much, so I change sort val
                
                for j in range(len(tempList)):
                    if not tempList[j]==None:
                        file.write(tag[str(j)]+"\n"+str(tempList[j])+"\n")
        file.close()
            # return f"Description: {description}\nMedian Salary: ${salary}\n"
        #     return "Details unavailable." #422 error code



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
    sortcatSplit={"name":"?sort=name","future":"?sort=bright_outlook","search":"","":""}
    sortsplit={"def":"&start=1&end=2","":""} #chars index is 7,13
    jsonKey={"default":"career","future":"career","prep":"career","search":"occupation","occ":"occupation"}
    detailFindKey={"salary":"/job_outlook","prep":"/knowledge","skills":"/skills","school":"/education"}


a="artichect"
test=[
Url("default","future","grow","name",a,5),
Url("web","search","keyword","search",a,5),
Url("default","prep","ready","future",a,5),
Url("default","default","","",a,5,code="17-2071.00"),
] #0,1,2,3 are good..

# for i in test:
#     print(i.url)

print(test[0].get_onet_careers())
# print(Url("default","default","","",a,5,code="17-2071.00").url)