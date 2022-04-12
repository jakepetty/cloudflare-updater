import urllib2
import time
import subprocess
import json

# Settings
CLOUDFLARE_EMAIL = "" # The email address you use to loginto Cloudflare's website
CLOUDFLARE_API_KEY = "" # The Global API Key found under My Profile on Cloudflare's website'

# Ignored Domains
ignore = []

# Functions


def getWanIP():
    """Makes an API call to a 3rd party to obtain your WAN address

    Returns:
        Your current WAN IP

    """
    request = urllib2.Request("https://api.ipify.org/?format=json")
    response = urllib2.urlopen(request)
    return json.loads(response.read())["ip"]


def get(url):
    """Makes a GET request

    Args:
        url: The URL you wish to GET to
    Returns:
        JSON object
    """
    request = urllib2.Request(url)
    request.add_header("Content-Type", "application/json")
    request.add_header("X-Auth-Key", CLOUDFLARE_API_KEY)
    request.add_header("X-Auth-Email", CLOUDFLARE_EMAIL)
    response = urllib2.urlopen(request)
    return json.loads(response.read())


def put(url, data):
    """Initiates a PUT request

    Args:
        url: The URL you wish to PUT to
        data: The data you wish to PUT
    Returns:
        JSON object
    """
    try:
        # Start CURL Process
        proc = subprocess.Popen(["curl", "-X", "PUT", url, "-s", "-H", "X-Auth-Email: " + CLOUDFLARE_EMAIL, "-H", "X-Auth-Key: " + CLOUDFLARE_API_KEY, "-H", "Content-Type: application/json", "--data", data], stdout=subprocess.PIPE)
        (out, err) = proc.communicate()
        if err:
            print(err.decode())
    except:
        print("ERROR: Failed to start curl process")
        
    return json.loads(out)


# Processor
try:
    # GET IP ADDRESS
    current_ip = getWanIP()

    # Obtain a list of ZONES from Cloudflare
    data = get("https://api.cloudflare.com/client/v4/zones")

    # Check if request was successful
    if data["success"]:

        # Loop through each zone
        for zone in data["result"]:

            # Check to make sure the domain is not in the ignore list
            if zone["name"] not in ignore:

                # Obtain DNS Records for domain
                data = get("https://api.cloudflare.com/client/v4/zones/{}/dns_records".format(zone["id"]))

                # Check if request was successful
                if data["success"]:

                    # Loop through each DNS record
                    for record in data["result"]:

                        # Find the A record
                        if record["type"] == "A":

                            # Check IP address against the current IP
                            if record["content"] != current_ip:

                                # Update DNS record IP address with the new IP
                                record["content"] = current_ip

                                # Push new data to Cloudflare
                                data = put("https://api.cloudflare.com/client/v4/zones/{}/dns_records/{}".format(zone["id"], record["id"]), json.dumps(record))

                                # Check if request was successful
                                if data["success"]:
                                    print("{} updated".format(record["name"]))
                                else:
                                    print("{} failed".format(record["name"]))
                            else:
                                print("{} up-to-date".format(record["name"]))
except Exception as e:
    print("An exception occurred with cloudflare: " + str(e))
