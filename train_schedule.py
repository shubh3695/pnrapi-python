from bs4 import BeautifulSoup
import requests
import re

class TrainSchedule:

    url_pnr = "http://www.indianrail.gov.in/cgi_bin/inet_trnpath_cgi.cgi"
    headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:19.0) Gecko/20100101 Firefox/19.0"}
    error = ""

    def __init__(self,train_number, month, day, day_count="0"):
        self.response_json = {}
        self.train_number = train_number
        self.month = month
        self.day = day
        self.day_count = day_count

    def request(self):
        request_data = {}
        request_data["lccp_submitpath"] = "Get Schedule"
        request_data["lccp_trn_no"] = self.train_number
        request_data["lccp_month"] = self.month
        request_data["lccp_day"] = self.day
        request_data["lccp_daycnt"] = self.day_count
        try:
            r = requests.post(self.url_pnr,request_data,headers=self.headers)
        except requests.exceptions.RequestException as e:
            self.error = str(e)
            return False
        if r.text.find("Please try again later") > 0:
            self.error = "Service unavailable"
            return False
        elif r.text.find("Facility Not Avbl due to Network Connectivity Failure") > 0:
            self.error = "Facility not available"
            return False
        elif r.text.find("TRAIN ROUTE") > 0:
            soup = BeautifulSoup(r.text)
            self.__getDetails(soup)
            return True
        else:
            self.error = "Some other error"
            return False

    def __getDetails(self,soup):
        #set pnr
        tables = soup.find_all("table",{"class":"table_border_both"})
        if tables:
            train_info = tables[0]#assumption. first four values train no, train name and source and days
            row = train_info.find("tr",{"class" : None}).find_all("td")
            self.response_json['train_number'] = str(row[0].text.strip())
            self.response_json['train_name'] = str(row[1].text.strip())
            self.response_json['source'] = str(row[2].text.strip())
            days_available = []
            for day in range(3,len(row)):
                days_available.append(str(row[day].text.strip()))
            self.response_json['days available'] = days_available

            #split into list of classes
            schedule_info = tables[1]
            schedule_rows = schedule_info.find_all("tr",{"class" : None})
            schedule_array = []
            for schedule in schedule_rows:
                schedule_object = {}
                values = schedule.find_all("td")
                if len(values) > 8:
                    schedule_object["sno"] = str(values[0].text.strip())
                    schedule_object["station code"] = str(values[1].text.strip())
                    schedule_object["station name"] = str(values[2].text.strip())
                    schedule_object["route number"] = str(values[3].text.strip())
                    schedule_object["arrival time"] = str(values[4].text.strip())
                    schedule_object["departure time"] = str(values[5].text.strip())
                    schedule_object["time halt"] = str(values[6].text.strip())
                    schedule_object["distance"] = str(values[7].text.strip())
                    schedule_object["day"] = str(values[8].text.strip())
                    if len(values) > 9 :
                        schedule_object["remarks"] = str(values[9].text.strip())
                    else:
                        schedule_object["remarks"] = ""
                schedule_array.append(schedule_object)
            self.response_json['schedule'] = schedule_array

    def get_json(self):
        return self.response_json
