import requests

# Replace with the actual API endpoint for the EM133 meter
api_endpoint = "https://satec-global.com/api/device/data"

# Replace with your actual device ID, if needed for the API
device_id = "1153673"

# Replace with your actual API key or token, if the API requires authentication

# Make a GET request to the API to retrieve data for your device
headers = {
    "Authorization": "Bearer YOUR_API_KEY"
}
response = requests.get(f"{api_endpoint}/{device_id}", headers=headers)


# Check if the request was successful
if response.status_code == 200:
    # If successful, print out the response data
    print(response.json())
else:
    # If not successful, print out the error
    print(f"Error: {response.status_code}")
    print(response.text)
