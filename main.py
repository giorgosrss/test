import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def perform_task(input_data):
    return f"Processed: {input_data}"

def get_fortnite_account_id(username, api_key):
    if not api_key:
        print("Error: API key is missing.")
        return None

    url = f"https://fortnite-api.com/v2/stats/br/v2?name={username}"
    headers = {
        'Authorization': api_key
    }

    # Configure retries for the session
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('https://', adapter)

    # Make the request
    response = session.get(url, headers=headers)

    # Handle responses
    if response.status_code == 200:
        try:
            data = response.json()
            # Check if the data contains the account ID
            if 'data' in data and 'account' in data['data']:
                return data['data']['account']['id']
            else:
                print("Unexpected data format:", data)
                return None
        except (ValueError, KeyError) as e:
            print("Error parsing JSON or finding account ID:", e)
            print("Response text:", response.text)
            return None
    elif response.status_code == 401:
        print("Error: Invalid or missing API key.")
        print("Response text:", response.text)
        return None
    else:
        print(f"Error: {response.status_code}")
        print("Response text:", response.text)
        return None

if __name__ == "__main__":
    # Use your API key directly
    api_key = "8b38f1c5-f0de-41c2-8dd8-935cc78b7f1d"  # Your provided API key

    username = input("Enter Fortnite username: ")
    account_id = get_fortnite_account_id(username, api_key)

    if account_id:
        print(f"The account ID for {username} is {account_id}")
    else:
        print("Could not find account ID.")
