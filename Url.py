class Url():
    def __init__(self,type,category,subcat,sortcat,keyword,prep,initial=21,end=40):
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

    def decode(self):
        if(not self.subcat):
            self.subcat=""
        return [self.serviceSplit[self.service],self.categorySplit[self.category],self.fineTuning[self.category][self.subcat]]

    def makeUrl(self):
        info=self.decode()
        return self.baseUrl+info[0]+info[1]+info[2]
    
    def handleUrl(self): #adds the variables, and handles special format. I'm ignoring the code subcat
        url=self.makeUrl()
        flag=False
        if(self.category=="prep"):
            url=url+f"{self.prep}"
        elif(self.category=="search"): #add sort(special exception)
            url=url+f"{self.keyword}"
            flag=True
        return url, flag
    
    def sortUrl(self):
        url=self.handleUrl()
        # flag=url[1]
        url=url[0]
        end=self.sortsplit["def"]
        end=(end[0:7]+f"{self.initial}"+end[8:13]+f"{self.end}")
        url=url+self.sortcatSplit[self.sort]+end
        self.url=url
        return url

    categorySplit={"default":"careers/","future":"bright_outlook/","prep":"job_preparation/","search":"search/"}
    serviceSplit={"default":"mnm/","web":"online/"}
    fineTuning={
            "":{"":""},
            "default":{"":""},
            "future":{"grow":"grow","openings":"openings","emerging":"emerging","code":""},
            "prep":{"ready":""},
            "search":{"keyword":"?keyword="}}
    sortcatSplit={"name":"?sort=name","future":"?sort=bright_outlook","search":""}
    sortsplit={"def":"&start=2&end=4"} #chars index is 7,13
    

a="artichect"
test1=Url("default","future","grow","name",a,5)
test2=Url("default","search","keyword","search",a,5)
test3=Url("default","prep","ready","future",a,5)
test4=Url("default","default","","name",a,5)
print(test1.sortUrl())
print(test2.sortUrl())
print(test3.sortUrl())
print(test4.sortUrl())