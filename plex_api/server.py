import requests
from xml.etree import ElementTree

def get_server_capabilities(ip_address, plex_token):
    url = f"http://{ip_address}:32400/?X-Plex-Token={plex_token}"
    response = requests.get(url)

    if response.status_code == 200:
        tree = ElementTree.fromstring(response.content)

        # Parse the attributes of the MediaContainer
        media_container_attribs = tree.attrib

        # Parse each Directory element and its attributes
        directories = []
        for directory in tree.findall('Directory'):
            directory_attribs = directory.attrib
            directories.append(directory_attribs)

        # Combine the data
        capabilities = {
            'MediaContainer': media_container_attribs,
            'Directories': directories
        }
        
        return capabilities
    elif response.status_code == 401:
        raise ValueError("Unauthorized: Check your Plex token.")
    else:
        response.raise_for_status()

def get_server_basic_info(ip_address, plex_token=None):
    # Construct the URL. The Plex token is optional for this endpoint.
    url = f"http://{ip_address}:32400/identity"
    if plex_token:
        url += f"?X-Plex-Token={plex_token}"

    response = requests.get(url)

    if response.status_code == 200:
        tree = ElementTree.fromstring(response.content)

        # Parse the attributes of the MediaContainer
        basic_info = tree.attrib

        return basic_info
    else:
        response.raise_for_status()

def get_server_preferences(ip_address, plex_token):
    url = f"http://{ip_address}:32400/:/prefs?X-Plex-Token={plex_token}"
    response = requests.get(url)

    if response.status_code == 200:
        tree = ElementTree.fromstring(response.content)

        # Extracting each Setting element
        preferences = []
        for setting in tree.findall('Setting'):
            preference_info = setting.attrib
            preferences.append(preference_info)

        return preferences
    elif response.status_code == 401:
        raise ValueError("Unauthorized: Check your Plex token.")
    else:
        response.raise_for_status()

def get_server_accounts(ip_address, plex_token):
    url = f"http://{ip_address}:32400/accounts/?X-Plex-Token={plex_token}"
    response = requests.get(url)

    if response.status_code == 200:
        tree = ElementTree.fromstring(response.content)

        # Extracting each Account element
        accounts = []
        for account in tree.findall('Account'):
            account_info = account.attrib
            accounts.append(account_info)

        return accounts
    elif response.status_code == 401:
        raise ValueError("Unauthorized: Check your Plex token.")
    else:
        response.raise_for_status()



def get_accessed_devices(ip_address, plex_token):
    url = f"http://{ip_address}:32400/devices/?X-Plex-Token={plex_token}"
    response = requests.get(url)

    if response.status_code == 200:
        tree = ElementTree.fromstring(response.content)

        # Extracting each Device element
        devices = []
        for device in tree.findall('Device'):
            device_info = device.attrib
            devices.append(device_info)

        return devices
    elif response.status_code == 401:
        raise ValueError("Unauthorized: Check your Plex token.")
    else:
        response.raise_for_status()


def get_single_device(ip_address, device_id, plex_token):
    url = f"http://{ip_address}:32400/devices/{device_id}?X-Plex-Token={plex_token}"
    response = requests.get(url)

    if response.status_code == 200:
        tree = ElementTree.fromstring(response.content)

        # Assuming there is only one Device element in the response
        device = tree.find('Device')
        if device is not None:
            device_info = device.attrib
            return device_info
        else:
            return None
    elif response.status_code == 401:
        raise ValueError("Unauthorized: Check your Plex token.")
    else:
        response.raise_for_status()


def get_all_activities(ip_address, plex_token):
    url = f"http://{ip_address}:32400/activities/?X-Plex-Token={plex_token}"
    response = requests.get(url)

    if response.status_code == 200:
        tree = ElementTree.fromstring(response.content)

        # Extracting each Activity element
        activities = []
        for activity in tree.findall('Activity'):
            activity_info = activity.attrib
            # Extract Context child elements if any
            context_elements = activity.findall('Context')
            contexts = [context.attrib for context in context_elements]
            activity_info['Contexts'] = contexts
            activities.append(activity_info)

        return activities
    elif response.status_code == 401:
        raise ValueError("Unauthorized: Check your Plex token.")
    else:
        response.raise_for_status()

def stop_activity(ip_address, activity_id, plex_token):
    url = f"http://{ip_address}:32400/activities/{activity_id}?X-Plex-Token={plex_token}"
    response = requests.delete(url)

    if response.status_code == 200:
        return
    elif response.status_code == 401:
        raise ValueError("Unauthorized: Check your Plex token.")
    elif response.status_code == 404:
        return ValueError("Not Found: The activity for the provided UUID was not running.")
    else:
        response.raise_for_status()

def get_transient_token(ip_address, plex_token):
    url = f"http://{ip_address}:32400/security/token?X-Plex-Token={plex_token}"
    response = requests.get(url)

    if response.status_code == 200:
        tree = ElementTree.fromstring(response.content)

        # Extracting the token attribute from MediaContainer
        token = tree.get('token')
        return token if token else "No token found."
    elif response.status_code == 401:
        return "Unauthorized: Check your Plex token."
    else:
        response.raise_for_status()

def perform_search(ip_address, plex_token, query, limit=None, section_id=None):
    url = f"http://{ip_address}:32400/hubs/search/?X-Plex-Token={plex_token}&query={query}"
    
    if limit:
        url += f"&limit={limit}"
    if section_id:
        url += f"&sectionId={section_id}"

    response = requests.get(url)

    if response.status_code == 200:
        tree = ElementTree.fromstring(response.content)

        # Extracting each Hub element
        hubs = []
        for hub in tree.findall('Hub'):
            hub_info = {
                'title': hub.get('title'),
                'type': hub.get('type'),
                'size': hub.get('size'),
                'items': []
            }
            # Extracting items within each Hub
            for item in hub:
                item_info = item.attrib
                hub_info['items'].append(item_info)
            hubs.append(hub_info)

        return hubs
    elif response.status_code == 401:
        return "Unauthorized: Check your Plex token."
    else:
        response.raise_for_status()

def listen_for_events(ip_address, plex_token, filters=None):
    url = f"http://{ip_address}:32400/:/eventsource/notifications?X-Plex-Token={plex_token}"
    if filters:
        url += f"&filters={filters}"

    try:
        with requests.get(url, stream=True) as response:
            if response.status_code == 200:
                for line in response.iter_lines():
                    if line:
                        decoded_line = line.decode('utf-8')
                        print(decoded_line)  # Process each line here
            elif response.status_code == 401:
                print("Unauthorized: Check your Plex token.")
            else:
                response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error: {e}")

def check_for_updates(ip_address, plex_token, download=False):
    download_param = '1' if download else '0'
    url = f"http://{ip_address}:32400/updater/check?download={download_param}&X-Plex-Token={plex_token}"

    response = requests.put(url)

    if response.status_code == 200:
        return "Success: The update check was successful." + (" Update downloaded." if download else "")
    elif response.status_code == 400:
        raise ValueError("Bad Request: A parameter was not specified or the value was not valid.")
    elif response.status_code == 401:
        raise ValueError("Unauthorized: Check your Plex token.")
    else:
        response.raise_for_status()
