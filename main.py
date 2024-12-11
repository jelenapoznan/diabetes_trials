import requests
from urllib.parse import urlencode

# Base URL for API
base_url = "https://clinicaltrials.gov/api/v2/studies"

# Define query parameters
query_params = {
    "query.cond": "diabetes",
    "filter.advanced": "AREA[StartDate]2019+",
    "countTotal": "true"
}

# Encode query parameters properly
encoded_params = urlencode(query_params, safe="[]+")

# Full URL with encoded parameters
full_url = f"{base_url}?{encoded_params}"

# Debugging: Print the full URL to verify
print("Full URL:", full_url)

# Initial API request
response = requests.get(full_url)
if response.status_code != 200:
    print(f"Error: {response.status_code}, {response.text}")
    exit()

# Parse the response JSON
data = response.json()


# Extract studies and paginate if necessary
study_ids = []
next_page_token = data.get("nextPageToken")

# Handle pagination
while True:
    studies = data.get("studies", [])
    for study in studies:
        locations = (
            study.get("protocolSection", {})
            .get("contactsLocationsModule", {})
            .get("locations", [])
        )
        for location in locations:
            city = location.get("city")
    
            if city:
              study_ids.append(city)

    # Check for the next page
    if not next_page_token:
        break

    # Request the next page
    next_params = {
        "query.cond": "diabetes",
        "filter.advanced": "AREA[StartDate]2019+",
        "pageToken": next_page_token,
    }
    next_encoded_params = urlencode(next_params, safe="[]+")
    next_url = f"{base_url}?{next_encoded_params}"

    response = requests.get(next_url)
    if response.status_code != 200:
        print(f"Error on next page: {response.status_code}, {response.text}")
        break

    data = response.json()
    next_page_token = data.get("nextPageToken")

# Print the collected study IDs
print("Collected Study IDs:", study_ids)
print(len(study_ids))