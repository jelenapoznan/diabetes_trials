import requests
import csv
from urllib.parse import urlencode
from dataclasses import dataclass, asdict


@dataclass
class Study:
  study_id: str
  city: str
  state: str
  country: str
  lat: float
  lon: float
  status: str
  start_date: str
  start_date_type: str
  completion_date: str
  completion_date_type: str
  study_type: str
  phases: str
  allocation:str
  intervention_model:str
  primary_purpose: str
  masking: str
  healty_volunteers: bool
  sex:str
  min_age:str
  max_age:str

base_url = "https://clinicaltrials.gov/api/v2/studies"
query_params = {
    "query.cond": "diabetes",
    "filter.advanced": "AREA[StartDate]RANGE[2019-01-01,MAX]",
    "pageSize": "100"
}
encoded_params = urlencode(query_params, safe="[]+")
full_url = f"{base_url}?{encoded_params}"

def get_response(url):
  response = requests.get(url)
  resp = response.json()
  return resp

def get_sudies_info(resp):
  next_page_token=resp.get("nextPageToken")
  studies_info=[]

  while True:
     studies = resp.get("studies", [])
  
     for study in studies:
        
        study_id=study.get("protocolSection",{}).get("identificationModule",{}).get("nctId")
        locations=study.get("protocolSection",{}).get("contactsLocationsModule", {}).get("locations",[])
        status=study.get("protocolSection",{}).get("statusModule",{}).get("overallStatus")
        start_date=study.get("protocolSection",{}).get("statusModule",{}).get("startDateStruct",{}).get("date")
        start_date_type=study.get("protocolSection",{}).get("statusModule",{}).get("startDateStruct",{}).get("type")
        completion_date=study.get("protocolSection",{}).get("statusModule",{}).get("completionDateStruct",{}).get("date")
        completion_date_type=study.get("protocolSection",{}).get("statusModule",{}).get("completionDateStruct",{}).get("type")
        study_type=study.get("protocolSection",{}).get("designModule",{}).get("studyType")
        phases=study.get("protocolSection",{}).get("designModule",{}).get("phases",[])
        allocation=study.get("protocolSection",{}).get("designModule",{}).get("designInfo",{}).get("allocation")
        intervention_model=study.get("protocolSection",{}).get("designModule",{}).get("designInfo",{}).get("interventionModel")
        primary_purpose=study.get("protocolSection",{}).get("designModule",{}).get("designInfo",{}).get("primaryPurpose")
        masking=study.get("protocolSection",{}).get("designModule",{}).get("designInfo",{}).get("maskingInfo",{}).get("masking")
        healty_volunteers=study.get("protocolSection",{}).get("eligibilityModule",{}).get("healthyVolunteers")
        sex=study.get("protocolSection",{}).get("eligibilityModule",{}).get("sex")
        min_age=study.get("protocolSection",{}).get("eligibilityModule",{}).get("minimumAge")
        max_age=study.get("protocolSection",{}).get("eligibilityModule",{}).get("maximumAge")
        
        for location in locations:
          city=location.get("city","")
          state=location.get("state","")
          country=location.get("country","")
          lat=location.get("geoPoint",{}).get("lat")
          lon=location.get("geoPoint",{}).get("lon")


          new_study = Study(
            study_id=study_id,
            city=city,
            state=state,
            country=country,
            lat=lat,
            lon=lon,
            status=status,
            start_date=start_date,
            start_date_type=start_date_type,
            completion_date=completion_date,
            completion_date_type=completion_date_type,
            study_type=study_type,
            phases=phases,
            allocation=allocation,
            intervention_model=intervention_model,
            primary_purpose=primary_purpose,
            masking=masking,
            healty_volunteers=healty_volunteers,
            sex=sex,
            min_age=min_age,
            max_age=max_age
          )
          studies_info.append(asdict(new_study))
      
     if not next_page_token:
        break
     
     next_query_params = {
        "query.cond": "diabetes",
        "filter.advanced": "AREA[StartDate]RANGE[2019-01-01,MAX]",
        "pageToken": next_page_token,
        "pageSize": "100"
        }
     
     encoded_params = urlencode(next_query_params, safe="[]+")

     nex_url = f"{base_url}?{encoded_params}"

     resp = get_response(nex_url)

     studies = resp.get("studies", [])
     next_page_token=resp.get("nextPageToken")
     print(next_page_token)

  return studies_info

def save_to_csv(locations_info, file_name="locations.csv"):
    if locations_info:
        keys = locations_info[0].keys()  # Get headers from the first dictionary
        with open(file_name, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=keys)
            writer.writeheader()
            writer.writerows(locations_info)
        print(f"Data saved to {file_name}")
    else:
        print("No data to save.")

if __name__ == "__main__":
  studies = get_response(full_url)
  studies_info = get_sudies_info(studies)
  print(len(studies_info))
  save_to_csv(locations_info=studies_info)