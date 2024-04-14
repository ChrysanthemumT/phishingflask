#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 17:58:48 2020

@author: hannousse
"""
from datetime import datetime
from bs4 import BeautifulSoup
import requests
import whois
import time
import re


#################################################################################################################################
#               Domain registration age 
#################################################################################################################################

def domain_registration_length(domain):
    try:
        res = whois.whois(domain)
        expiration_date = res.expiration_date
        today = time.strftime('%Y-%m-%d')
        today = datetime.strptime(today, '%Y-%m-%d')
        # Some domains do not have expiration dates. The application should not raise an error if this is the case.
        if expiration_date:
            if type(expiration_date) == list:
                expiration_date = min(expiration_date)
            return abs((expiration_date - today).days)
        else:
            return 0
    except:
        return -1

def domain_registration_length1(domain):
    v1 = -1
    v2 = -1
    try:
        host = whois.whois(domain)
        hostname = host.domain_name
        expiration_date = host.expiration_date
        today = time.strftime('%Y-%m-%d')
        today = datetime.strptime(today, '%Y-%m-%d')
        if type(hostname) == list:
            for host in hostname:
                if re.search(host.lower(), domain):
                    v1 = 0
            v1= 1
        else:
            if re.search(hostname.lower(), domain):
                v1 = 0
            else:
                v1= 1  
        if expiration_date:
            if type(expiration_date) == list:
                expiration_date = min(expiration_date)
            return abs((expiration_date - today).days)
        else:
            v2= 0
    except:
        v1 = 1
        v2 = -1
        return v1, v2
    return v1, v2

#################################################################################################################################
#               Domain recognized by WHOIS
#################################################################################################################################

 
def whois_registered_domain(domain):
    try:
        hostname = whois.whois(domain).domain_name
        if type(hostname) == list:
            for host in hostname:
                if re.search(host.lower(), domain):
                    return 0
            return 1
        else:
            if re.search(hostname.lower(), domain):
                return 0
            else:
                return 1     
    except:
        return 1

#################################################################################################################################
#               Unable to get web traffic (Page Rank)
#################################################################################################################################
import urllib

def web_traffic(short_url):
        try:
            rank = BeautifulSoup(urllib.request.urlopen("http://data.alexa.com/data?cli=10&dat=s&url=" + short_url).read(), "xml").find("REACH")['RANK']
        except:
            return 0
        return int(rank)


#################################################################################################################################
#               Domain age of a url
#################################################################################################################################

import json
from datetime import datetime, timezone

def domain_age(domain):
    url = domain.split("//")[-1].split("/")[0].split('?')[0]
    show = "https://www.whoisxmlapi.com/whoisserver/WhoisService?apiKey=at_bleAXcaGeYA8lZlgorjZQ4WRkYA3K&domainName=" + url + "&outputFormat=JSON"

    def convert_to_datetime(date_str):
        # List of formats your API might use
        date_formats = [
            "%a %b %d %Y", # Format for 'Tue Mar 3 2015'
            "%Y-%m-%dT%H:%M:%SZ", # Format for '2018-02-16T10:22:31Z'
            # Add more formats here as needed
        ]
        
        for fmt in date_formats:
            try:
                # Try to parse the date string with the current format
                return datetime.strptime(date_str, fmt)
            except ValueError:
                # If parsing fails, continue to the next format
                continue
        
        # If none of the formats work, raise an exception or return None
            
        raise ValueError(f"Date format not recognized: {date_str}")
    
    r = requests.get(show)
    if r.status_code == 200:
        data = r.text
        jsonToPython = json.loads(data)
        result = jsonToPython['WhoisRecord']['registryData']
        if result == None:
            return -2
        else:
            start = result['createdDate']
            date_obj = convert_to_datetime(start)

            # Get the current date and time as a datetime object
            current_date = datetime.now()

            # Calculate the difference in days
            difference = current_date - date_obj
            difference_days = difference.days
            return difference_days
    else:       
        return -1


#################################################################################################################################
#               Global rank
#################################################################################################################################

def global_rank(domain):
    rank_checker_response = requests.post("https://www.checkpagerank.net/index.php", {
        "name": domain
    })
    
    try:
        return int(re.findall(r"Global Rank: ([0-9]+)", rank_checker_response.text)[0])
    except:
        return -1


#################################################################################################################################
#               Google index
#################################################################################################################################


from urllib.parse import urlencode

def google_index(url):
    #time.sleep(.6)
    user_agent =  'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
    headers = {'User-Agent' : user_agent}
    query = {'q': 'site:' + url}
    google = "https://www.google.com/search?" + urlencode(query)
    data = requests.get(google, headers=headers)
    data.encoding = 'ISO-8859-1'
    soup = BeautifulSoup(str(data.content), "html.parser")
    try:
        if 'Our systems have detected unusual traffic from your computer network.' in str(soup):
            return -1
        check = soup.find(id="rso").find("div").find("div").find("a")
        #print(check)
        if check and check['href']:
            return 0
        else:
            return 1
        
    except AttributeError:
        return 1

#print(google_index('http://www.google.com'))
#################################################################################################################################
#               DNSRecord  expiration length
#################################################################################################################################

import dns.resolver

def dns_record(domain):
    try:
        nameservers = dns.resolver.query(domain,'NS')
        if len(nameservers)>0:
            return 0
        else:
            return 1
    except:
        return 1

#################################################################################################################################
#               Page Rank from OPR
#################################################################################################################################


def page_rank(key, domain):
    url = 'https://openpagerank.com/api/v1.0/getPageRank?domains%5B0%5D=' + domain
    try:
        request = requests.get(url, headers={'API-OPR':key})
        result = request.json()
        result = result['response'][0]['page_rank_integer']
        if result:
            return result
        else:
            return 0
    except:
        return -1


