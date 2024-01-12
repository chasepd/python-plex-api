import requests
from xml.etree import ElementTree

def get_libraries(ip_address, plex_token):
    url = f"http://{ip_address}:32400/library/sections/?X-Plex-Token={plex_token}"
    response = requests.get(url)

    if response.status_code == 200:
        tree = ElementTree.fromstring(response.content)

        # Extracting each Directory element which represents a library
        libraries = []
        for directory in tree.findall('Directory'):
            library_info = directory.attrib
            # Extracting Location elements within each Directory
            locations = [location.attrib for location in directory.findall('Location')]
            library_info['Locations'] = locations
            libraries.append(library_info)

        return libraries
    elif response.status_code == 401:
        return "Unauthorized: Check your Plex token."
    else:
        response.raise_for_status()

def get_library_details(ip_address, library_id, plex_token):
    url = f"http://{ip_address}:32400/library/sections/{library_id}?X-Plex-Token={plex_token}"
    response = requests.get(url)

    if response.status_code == 200:
        tree = ElementTree.fromstring(response.content)

        # Extracting the MediaContainer element and its attributes
        media_container = tree.attrib

        # Extracting each Directory element within the MediaContainer
        directories = []
        for directory in tree.findall('Directory'):
            directory_info = directory.attrib
            directories.append(directory_info)

        media_container['Directories'] = directories
        return media_container
    elif response.status_code == 401:
        return "Unauthorized: Check your Plex token."
    else:
        response.raise_for_status()