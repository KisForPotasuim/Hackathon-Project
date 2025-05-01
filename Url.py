from Url2 import Url


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