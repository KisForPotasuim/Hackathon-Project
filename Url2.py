import requests
import base64
from requests.auth import HTTPBasicAuth
import json
from time import perf_counter
import os


# https://services.onetcenter.org/ws/mnm/occupations?keyword=engineer&start=1&end=5
onet_username = "career_chatbot1"
onet_password = "7335gtw"

credentials = HTTPBasicAuth(onet_username, onet_password)
# credentials_2 = base64.b64encode(credentials.encode()).decode()
# headers = {"Authorization": f"{credentials_2}"}


class Url():
    def __init__(self,type,category,subcat,sortcat,keyword,prep,initial=1,end=10,code=None,write=True,read=True,data={}):
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
        self.write=write
        self.read=read
        self.compiledData=data
        self.makeUrl()
        # self.careerInfo=self.get_onet_careers()

    def makeUrl(self):
        # makes most of the url
        if(not self.subcat):
            self.subcat=""
        info=[self.serviceSplit[self.service],self.categorySplit[self.category],self.fineTuning[self.category][self.subcat]]

        #handles special inputs 
        url=self.baseUrl+info[0]+info[1]
        temp=info[2]
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
 
        #add sort
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
                job_info = self.get_onet_job_details(temp,code=job_code)
                if job_info=="error":
                    return
                self.careers.append((job_title, job_info))
            # return data
            return self.careers if self.careers else [("test", "")]
        return [("Failed to fetch data from O*NET", "")]

    def get_onet_job_details(self,temp,headers=credentials,code=None):
        if(self.write):
        # https://services.onetcenter.org/v1.9/ws/mnm/careers/[O*NET-SOC Code]/job_outlook("salary")

            accept={"Accept" : "application/json"}
            accessList=[temp.url,temp.url+self.detailFindKey["salary"],temp.url+self.detailFindKey["school"]] #these are most important:general description,salary+brightoutlook, and prep needed
            file=None
            
            fileData={}
            for i in accessList:
                response = requests.get(i, auth=headers, headers=accept)
                if response.status_code == 200:
                    data = response.json()
                    tempList=[
                    data.get("what_they_do", None),
                    data.get("salary", {}).get("annual_median", None),
                    data.get("job_zone",None),
                    data.get("education_usually_needed",{}).get("category",None),
                    code]
                    title=data.get("title",None)
                    if(title):
                        savedTitle=title
                        if "/" in savedTitle:
                            return "NameError"
                    # if(not file):
                    #     file=open(f"{data.get("title","data")}.json","w+") #this works, but too much, so I change sort val
                    
                    for j in range(len(tempList)):
                        if tempList[j]:
                            fileData[self.tag[str(j)]]=tempList[j]
                            # file.write(tag[str(j)]+"\n"+str(tempList[j])+"\n")
            
            if(not savedTitle):
                savedTitle="data"
            with open(f"data/{savedTitle}.json","w+") as file:
                json.dump(fileData,file,indent=4)
            file.close()
        return "set self.write=True"

    def decodeData(self,index=None,title=None,code=None):
        if self.read:
            if not(title==None):
                pass
            if not(index==None):
                title=f"{sorted(os.listdir("data/"))[index]}"
                title=title[0:len(title)-len(".json")]
            if not(code==None):
                # I'll add programming for code later because it is ineffecient unless there is a sort for order based on the career code
                # name will be based first 2 chars of code ie. 15
                # then use the listdir to get a sorted list and open relevent files and check
                # potentially needed custom tagging system for more complex uses
                pass
            career={}
            with open(f"data/{title}.json","r") as file:
                    data=json.load(file)
                    for i in self.tag.values():
                        career[i]=data.get(i,None)
            self.compiledData[title]=career #saves data for session
            return career
        return {"Error":"Change Url.read to True"}
        
    def sessionData(self):
        return self.compiledData
    

    tag={"0":"Description:","1":"Salary:","2":"Prep:","3":"Education:","4":"Code:"}
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


# For testing, just import the Url class
a="artichect"
test=[
Url("default","future","grow","name",a,5,end=40),
Url("web","search","keyword","search",a,5),
Url("default","prep","ready","future",a,5),
Url("default","default","","",a,5,code="17-2071.00")
]

# for i in test:
#     print(i.url)
a=perf_counter()
test[0].get_onet_careers()
# print(perf_counter()-a)


dataLenght=len(os.listdir("data/"))
for i in range(dataLenght):
    test[0].decodeData(index=i)
print(test[0].sessionData())
b=perf_counter()
print(b-a)

# print(os.listdir("data/"))
# print(Url("default","default","","",a,5,code="17-2071.00").url