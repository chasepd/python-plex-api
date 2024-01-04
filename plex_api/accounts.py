import requests
from xml.etree import ElementTree

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
