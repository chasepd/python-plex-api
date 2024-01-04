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