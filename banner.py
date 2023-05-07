import whois
import requests
import socket
import argparse
import tldextract
import dns
from urllib.parse import urljoin
from bs4 import BeautifulSoup

# Define command line arguments
parser = argparse.ArgumentParser(description='Website Scanner')
parser.add_argument('-u', '--url', type=str, required=True, help='The URL of the website to scan')
parser.add_argument('-w', '--whois', action='store_true', help='Retrieve WHOIS information')
parser.add_argument('-r', '--robots', action='store_true', help='Retrieve robots.txt file')
parser.add_argument('-i', '--ip', action='store_true', help='Retrieve IP address information')
parser.add_argument('-x', '--index', action='store_true', help='Retrieve index.html content')
parser.add_argument('-b', '--banner', action='store_true', help='Retrieve server banner information')
parser.add_argument('-d', '--dns', action='store_true', help='Retrieve DNS information')
args = parser.parse_args()

# Extract the domain name from the URL
domain = tldextract.extract(args.url).domain + '.' + tldextract.extract(args.url).suffix

# Retrieve WHOIS information if specified
if args.whois:
    print('Retrieving WHOIS information...')
    w = whois.whois(domain)
    print(w)

# Retrieve robots.txt file if specified
if args.robots:
    print('Retrieving robots.txt file...')
    response = requests.get(urljoin(args.url, '/robots.txt'))
    if response.status_code == 200:
        print(response.content.decode())

# Retrieve IP address information if specified
if args.ip:
    print('Retrieving IP address information...')
    try:
        ip = socket.gethostbyname(domain)
        print(f'IP address: {ip}')
    except socket.gaierror as e:
        print(f'Error retrieving IP address: {e}')

# Retrieve index.html content if specified
if args.index:
    print('Retrieving index.html content...')
    response = requests.get(args.url)
    soup = BeautifulSoup(response.content, 'html.parser')
    print(soup.prettify())

# Retrieve server banner information if specified
if args.banner:
    print('Retrieving server banner information...')
    response = requests.get(args.url)
    print(response.headers['server'])

# Retrieve DNS information if specified
if args.dns:
    print('Retrieving DNS information...')
    try:
        records = dns.resolver.query(domain, 'NS')
        for rdata in records:
            print(rdata)
    except dns.resolver.NXDOMAIN as e:
        print(f'Error retrieving DNS information: {e}')