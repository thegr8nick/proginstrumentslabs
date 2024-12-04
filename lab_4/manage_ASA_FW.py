#!/usr/bin/python3
import getpass
import os
import json
import time
import sys
import argparse
import logging
import base64
from urllib import request, error
import random

# Настройка логирования
logging.basicConfig(
    filename='logging_FW_Script.log',
    format='%(asctime)s : %(levelname)s : %(message)s',
    level=logging.INFO,
    datefmt='%m/%d/%Y %I:%M:%S %p'
)

os.system('clear')
change = 0
headers = {'Content-Type': 'application/json'}
server = {'vpn': 'https://10.10.10.1'}
api_path = {'object': '/api/objects/networkobjects/', 'object-group': '/api/objects/networkobjectgroups/'}
url = server
f = None
username = os.getlogin()

logging.info("Script started by user: %s", username)

firewall = input((
    '\nPlease choose which FW to connect to:\n\n'
    '1. Calgary Edge FW(cf)\n'
    '2. Victoria Edge FW(vf)\n'
    '3. DUS Edge FW(df)\n'
    '4. Victoria VPN FW(vicvpn)\n'
    '5. Calgary OPS VPN FW(opsvpn)\n\n'
    'Choose the firewall code:')).lower()

if firewall not in server.keys():
    logging.error("Wrong firewall selection: %s", firewall)
    print('\n################### Wrong selection. Exiting the script! ##########################\n')
    sys.exit(-2)

server = server[firewall]
logging.info("Selected firewall: %s (%s)", firewall, server)

print(f'\nEnter the password to connect to {server}:')
password = getpass.getpass()

def set_server(path):
    global req
    url = server + path
    req = request.Request(url, None, headers)
    base64string = base64.encodebytes(f'{username}:{password}'.encode()).decode('utf-8').replace('\n', '')
    req.add_header("Authorization", f"Basic {base64string}")
    logging.info("Request initialized for path: %s", path)
    return req

def read_data(req, value):
    try:
        with request.urlopen(req) as f:
            status_code = f.getcode()
            if status_code != 200:
                logging.warning("Non-200 status code: %d", status_code)
                print(f'Error in GET. Got status code: {status_code}')
            resp = f.read()
            json_resp = json.loads(resp.decode('utf-8'))
            logging.info("Data successfully read from server")
            if value == 1:
                print(json.dumps(json_resp, sort_keys=True, indent=4, separators=(',', ': ')))
            return json_resp
    except error.HTTPError as err:
        logging.error("HTTP Error: %d, Details: %s", err.code, err.read().decode('utf-8'))
        print(f"HTTP Error: {err.code}")
        print(err.read().decode('utf-8'))
    except Exception as e:
        logging.exception("An unexpected error occurred: %s", str(e))

def search_data():
    temp = 0
    search_type = input('Do you want to search with value or name?')
    value = input('Enter the value or name: ')
    logging.info("Searching for item: %s", value)
    print(f'\nSearching for item: {value}....')
    json_resp = read_data(set_server(api_path['object']), 0)
    for item in json_resp.get('items', []):
        if value in item.get('host', {}).get('value', ''):
            print(item['objectId'])
            logging.info("Item found: %s", item['objectId'])
            temp = 1
    if temp != 1:
        logging.warning("Item not found: %s", value)
        print(f'The item: {value} not found\n')
        return 0
    return 1

def write_data(post_data, url):
    global change
    print('\n---------------- CONFIGURATION ----------------')
    print(json.dumps(post_data, sort_keys=True, indent=4, separators=(',', ': ')))
    print('\n---------------------------------------------')
    choice = input('\nWould you want to push the above config to the firewall? [yes/no]').lower()
    if choice == 'yes':
        req = request.Request(url, data=json.dumps(post_data).encode('utf-8'), headers=headers)
        base64string = base64.encodebytes(f'{username}:{password}'.encode()).decode('utf-8').replace('\n', '')
        req.add_header("Authorization", f"Basic {base64string}")
        try:
            with request.urlopen(req) as f:
                status_code = f.getcode()
                if status_code == 201:
                    logging.info("Configuration successfully pushed to firewall: %s", url)
                    print("\nConfiguration pushed to firewall successfully.")
                    change = 1
        except error.HTTPError as err:
            logging.error("HTTP Error while pushing config. Code: %d", err.code)
            try:
                json_error = json.loads(err.read().decode('utf-8'))
                if json_error:
                    print(json.dumps(json_error, sort_keys=True, indent=4, separators=(',', ': ')))
            except ValueError:
                logging.exception("Error while reading JSON error response")
        except Exception as e:
            logging.exception("An unexpected error occurred while pushing config: %s", str(e))
    else:
        logging.info("Configuration push skipped by user")

def main(argv):
    parser = argparse.ArgumentParser(description='FW Management')
    parser.add_argument('-c', '--config', dest='config', type=str, required=False, help='configuration file')
    parser.add_argument('-a', '--action', dest='action', type=str, required=True, help='action to perform [read|search|write]')
    args = parser.parse_args()

    logging.info("Action selected: %s", args.action)
    if args.action == 'read':
        read_data(set_server(api_path['object']), 1)
    elif args.action == 'search':
        search_data()
    elif args.action == 'write':
        # Implement the make_data() logic here if needed
        pass

    if change == 1:
        choice = input('\nThe device configuration has been changed by the script. Save to NVRAM? [yes/no]').lower()
        if choice in ('', 'yes'):
            json_data = {'commands': ["write memory"]}
            write_data(json_data, server + '/api/cli')
            logging.info("Configuration saved to NVRAM")
        else:
            logging.info("Configuration changes discarded by user")
            print('\nExiting the script without saving the configuration.')

if __name__ == "__main__":
    try:
        main(sys.argv[1:])
        logging.info("Script executed successfully")
    except Exception as e:
        logging.exception("Fatal error during execution: %s", str(e))
        sys.exit(1)
