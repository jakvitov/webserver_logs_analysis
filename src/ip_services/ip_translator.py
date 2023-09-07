import pandas as pd
import requests


# Manages translation of access log ip addresses

def translateIps(ipList):
    result = []
    try :
        # We split the ipList to groups of 99 -> the external service limit
        for i in range(0, len(ipList), 99):
            api_url = "http://ip-api.com/batch?fields=city,country,countryCode,query,asname,proxy"
            body = ipList[i:i + 99]
            response = requests.post(api_url, json=body)
            result += (response.json())
        return pd.DataFrame(result)
    except Exception as e:
        print(f"Ip translation error error: {e}")
        exit(1)
