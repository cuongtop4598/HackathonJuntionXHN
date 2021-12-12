#!/usr/bin/env python
from __future__ import print_function
from genregex.generator import generator
from collections import defaultdict
import urlclustering
import json
import os
import base64
import random
import string
import json
import re
import sys
import csv
import pandas as pd

POPULATION = 100
GENERATION = 20
url = []
#
uri_regex={}
if len(sys.argv) != 3:
    print("Error")
    sys.exit(0)
fileLog=str(sys.argv[1])
fileRule=str(sys.argv[2])

file =open(fileRule,"r")

data=file.read().splitlines()
if data:
    print("Data")
    for line in data:
        l=json.loads(line)
        if l['signature']=="clustered":
            t = l['pattern']
            uri_regex[l['uri_par']]=t
        else:
            url.append("http://msec_lqd.com"+json.loads(line)['pattern'])
    file.close()

file =open(fileRule,"w")
#   
def url_parameters(urls):
    by_params = defaultdict(list)
    for url in urls:
        if "&" in url : 
            param_values = url.split("?")[1].split("&")
            print(param_values)
            uri_params = url.split("?")[0]+"?"
            for param_value in param_values:
                uri_params += param_value[0:param_value.find("=")]+"&"
            uri_params = uri_params[0:-1]
            parameters=uri_params[20:].split("&")
            for i in range(0,len(param_values)):
                param_value=param_values[i]
                if "=" in param_value:
                    by_params[uri_params].append((parameters[i%len(parameters)],param_value[param_value.find("=")+1:]))
                else:
                    by_params[uri_params].append((parameters[i%len(parameters)],param_value.split("?")[1]))
        else:
            param_value = url.split("?")[0]+"?" + url.split("?")[1]
            if "=" in param_value:
                uri_params = param_value[0:param_value.find("=")]
                by_params[uri_params].append(param_value[param_value.find("=")+1:])
            else:
                uri_params = param_value.split("?")[0]
                by_params[uri_params].append(param_value.split("?")[1])
    return by_params
#          
def process(clusters):
    for key, urls in clusters.items():
        print(urls)
        print("***********************************")
        if ("?" in urls[0] ) and ("=" in urls[0]): #co tham so
            for uri, value in url_parameters(urls).items():
                uri=uri.replace("http://msec_lqd.com","")
                if uri not in uri_regex:
                    if "&" in uri: #>=2 tham so
                        parameters=uri[uri.index("?")+1:].split("&")
                        pattern=uri[0:uri.index("?")+1]
                        for parameter in parameters:
                            target=[]
                            for a in value:
                                if a[0]==parameter:
                                    target.append(a[1])
                            try:
                                print(uri)
                                result = generator(target, POPULATION, GENERATION)[0][1]
                                print("Generate Success")
                            except:
                                result = generator(target[:5], POPULATION, GENERATION)[0][1]
                                target.append(result)
                                result=str(target)
                            pattern=pattern+parameter+"="+result+"&"
                        uri_regex[uri]=pattern[:-1]
                    else: # 1 tham so
                        try:
                            target=[]
                            print (uri)
                            result = generator(value, POPULATION, GENERATION)[0][1]
                            print("Generate Success")
                            if "$" != result[-1:]:
                                result+="$"
                            if "?" not in uri:
                                uri_regex[uri]=uri+"?"+result
                            else:
                                target=[]
                                target.append(result)
                                uri_regex[uri]=uri+"="+str(target)
                        except:
                            result = generator(value[:5], POPULATION, GENERATION)[0][1]
                            target=value
                            target.append(result)
                            
                            uri_regex[uri]=uri+"="+str(target)
                else: # uri ton tai trong regex cu
                    try:
                        regex_temp="http://msec_lqd.com"+uri_regex[uri]
                        url_not_check=[]
                        for url in urls:
                            check=re.findall(regex_temp,url)
                            if check:
                                continue
                            else:
                                url_not_check.append(url)
                        for uri2, value2 in url_parameters(urls).items():
                            uri2=uri2.replace("http://msec_lqd.com","")
                            if "&" in uri2:
                                parameters=uri2[uri2.index("?")+1:].split("&")
                                pattern=uri2[0:uri2.index("?")+1]
                                for parameter in parameters:
                                    target=[]
                                    for a in value2:
                                        if a[0]==parameter:
                                            target.append(a[1])
                                    try:
                                        print(uri2)
                                        result = generator(target, POPULATION, GENERATION)[0][1]
                                        print("Generate Success")
                                    except:
                                        result = generator(target[:5], POPULATION, GENERATION)[0][1]
                                        target.append(result)
                                        result=str(target)
                                    pattern=pattern+parameter+"="+result+"&"
                                uri_regex[uri2]=uri_regex[uri2]+"|"+pattern[:-1]
                            else:
                                target=[]
                                for a in value2:
                                    target.append(a[1])
                                try:
                                    print(uri2)
                                    result = generator(target, POPULATION, GENERATION)[0][1]
                                    print("Generate Success")
                                except:
                                    result = generator(target[:20], POPULATION, GENERATION)[0][1]
                                    target.append(result)
                                    result=str(target)
                                uri_regex[uri2]=uri_regex[uri2]+"|"+result
                    except:
                        print("Check new log in old regex")
        else: # khong co tham so
            temp = key[1][0:key[1].rfind("/")+1].replace("http://msec_lqd.com","")
            if temp not in uri_regex:
                target=[]
                for url in urls:
                    target.append(url[len("http://msec_lqd.com"+temp):])
                try:
                    print(temp)
                    result = generator(target, POPULATION, GENERATION)[0][1]
                    print("Generate Success")
                    if "$" != result[-1:]:
                        result+="$"
                except:
                    result = generator(target[:5], POPULATION, GENERATION)[0][1]
                    target.append(result)
                    result=str(target)
                
                uri_regex[temp]=temp+result
            else:
                regex_temp="http://msec_lqd.com"+uri_regex[temp]
                target2=[]
                for url in urls:
                    check=re.findall(regex_temp,url)
                    if check:
                        continue
                    else:
                        target2.append(url[len(temp)+19:])
                if len(target2)!=0:
                    try:
                        print(temp)
                        result2 = generator(target2, POPULATION, GENERATION)[0][1]
                        print("Generate Success")
                    except:
                        result = generator(target2[:5], POPULATION, GENERATION)[0][1]
                        target2.append(result)
                        result2=str(target2)
                    if "$" != result2[-1:]:
                        result2+="$"
                    new_regex=uri_regex[temp]+"|"+result2
                    uri_regex[temp]=new_regex
#
data=open(fileLog,"rb").read().splitlines()
for line in data:
    t = 'http://msec_lqd.com'+json.loads(line)['request']['request_uri']
    if t not in url:
         url.append(t)


# csv= pd.read_csv(fileLog)
# for i in range(0,len(csv['fullurl'])):
#     t = 'http://msec_lqd.com'+csv['fullurl'][i].replace("http://localhost:8080","")
#     if t not in url:
#          url.append(t)
try:
    c = urlclustering.cluster(url,2)
except:
    print("Data Error")
#
process(c["clusters"])
#
for i in uri_regex:
    str_='"'+"method"+'"'+":"+'"'+"GET"+'"'+","
    str_=str_+'"'+"pattern"+'"'+":"+'"'+uri_regex[i]+'"'+","+'"'+"signature"+'"'+":"+'"'+"clustered"+'"'
    str_=str_+","+'"'+"uri_par"+'"'+":"+'"'+i+'"'
    if "?" in uri_regex[i]:
        index=uri_regex[i].index("?")
        parameters=uri_regex[i][index+1:]
        uri=uri_regex[i][:index+1]
        if "&" in parameters:
            print(parameters)
            parameters=parameters.split("&")
            param=""
            for parameter in parameters:
                parameter=parameter.split("=")
                param=param+ parameter[0]+":"+parameter[1]+","
            param=param[:-1]
        else:
            if "=" in parameters:
                param=parameters.split("=")[0]+":"+parameters.split("=")[1]
            else:
                param=parameters
        str_=str_+","+'"'+"params"+'"'+":"+'{'+param+'}'
    else:
        uri=i
    str_=str_+","+'"'+"uri"+'"'+":"+'"'+uri+'"'
    file.write("{"+str_+"}\n")
for temp in c['unclustered']:
    temp=temp[19:]
    if temp not in uri_regex:
        str_='"'+"method"+'"'+":"+'"'+"GET"+'"'+","
        str_='"'+"pattern"+'"'+":"+'"'+temp+'"'+","+'"'+"signature"+'"'+":"+'"'+"unclustered"+'"'
        str_=str_+","+'"'+"uri_par"+'"'+":"+'"'+temp+'"'
        if "?" in temp:
            index=temp.index("?")
            parameters=temp[index+1:]
            if "&" in parameters:
                parameters=parameters.split("&")
                param=""
                for parameter in parameters:
                    parameter=parameter.split("=")
                    param=param+ parameter[0]+":"+parameter[1]+","
                param=param[:-1]
            else:
                if "=" in parameters:
                    param=parameters.split("=")[0]+":"+parameters.split("=")[1]
                else:
                    param=parameters
            str_=str_+","+'"'+"params"+'"'+":"+"{"+str(param)+"}"
        else:
            uri=temp
        str_=str_+","+'"'+"uri"+'"'+":"+'"'+uri+'"'
        file.write("{"+str_+"}\n")


