import urlclustering
import json
import os
import base64
import random
import string
import json
import re
from collections import defaultdict


urls=["http://msec_lqd.com?15678900","http://msec_lqd.com?username=ffff===fff","http://msec_lqd.com?abc=def&dai=456&tuan=123=&khanh=567=","http://msec_lqd.com?id=1","http://msec_lqd.com?abc=def&dai=123"]
def url_parse(urls):
    by_params = defaultdict(list)
    for url in urls:
        if "&" in url : 
            param_values = url.split("?")[1].split("&")
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
                #by_params[uri_params].append(param_value.split("=")[param_value.find("=")+1:])
        else:
            param_value = url.split("?")[0]+"?" + url.split("?")[1]
            if "=" in param_value:
                uri_params = param_value[0:param_value.find("=")]
                by_params[uri_params].append(param_value[param_value.find("=")+1:])
            else:
                uri_params = param_value.split("?")[0]
                by_params[uri_params].append(param_value.split("?")[1])
    return by_params
for uri, value in url_parse(urls).items():
	print (uri+":"+str(value))
