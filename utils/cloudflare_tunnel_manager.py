import requests
import os
# Set Cloudflare API credentials and IDs
cf_account_id = os.environ.get("CLOUDFLARE_ACCOUNT_ID")
cf_tunnel_id = os.environ.get("CLOUDFLARE_TUNNEL_ID")
cf_api_token = os.environ.get("CLOUDFLARE_API_TOKEN")
cf_dns_name = os.environ.get("CLOUDFLARE_DNS_NAME")

# Headers
headers = {
    "Authorization": f"Bearer {cf_api_token}",
    "Content-Type": "application/json"
}


# GET request to retrieve zones
zones = requests.get("https://api.cloudflare.com/client/v4/zones", headers=headers).json()["result"]
cf_zone_id = [z for z in zones if z['name'] == cf_dns_name][0]["id"] 

# API endpoints
configurations_url = f"https://api.cloudflare.com/client/v4/accounts/{cf_account_id}/cfd_tunnel/{cf_tunnel_id}/configurations"
dns_records_url = f"https://api.cloudflare.com/client/v4/zones/{cf_zone_id}/dns_records"

# GET current state to retrieve configurations
current_config_state = requests.get(configurations_url, headers=headers)



default_origin_request = {'bastionMode': False,
                        'caPool': '',
                        'connectTimeout': 30,
                        'disableChunkedEncoding': False,
                        'http2Origin': False,
                        'httpHostHeader': '',
                        'keepAliveConnections': 100,
                        'keepAliveTimeout': 90,
                        'noHappyEyeballs': False,
                        'noTLSVerify': False,
                        'originServerName': '',
                        'proxyAddress': '127.0.0.1',
                        'proxyPort': 0,
                        'proxyType': '',
                        'tcpKeepAlive': 30,
                        'tlsTimeout': 10
}

class CloudflareTunnelManager:
    """
    This class is responsible for managing Cloudflare Tunnel configurations and DNS records.
    example usage: 
    manager = CloudflareTunnelManager()
    example_tunnel = {'hostname': 'subdomain.domain_managed_by_cloudflare.com',
                    'service': 'http://ip_or_hostname_running_your_app:port'
    }
    manager.add_tunnel_configuration(example_tunnel)
    manager.delete_tunnel_configuration('subdomain.domain_managed_by_cloudflare.com')
    """
    def __init__(self):
        pass

    def add_tunnel_configuration(self, tunnel):
        default_origin_request['noTLSVerify'] = tunnel["service"].startswith("https")
        tunnel["originRequest"] = default_origin_request
        # POST request to create tunnel configuration
        config = current_config_state.json()['result']
        ingress = config["config"]["ingress"]
        duplicated_entry = [e for e in ingress if e.get("hostname", None) == tunnel["hostname"]]
        duplicated_entry_index = ingress.index(duplicated_entry[0]) if duplicated_entry else None
        if duplicated_entry:
            if duplicated_entry[0]["service"] == tunnel["service"]:
                print("Duplicated entry")
                return
            else:
                ingress[duplicated_entry_index] = tunnel
        ingress.insert(0, tunnel)
        response = requests.put(configurations_url, headers=headers, json=config)
        print("Created Tunnel Config:", response.json()["success"])

        # POST request to create DNS record
        dns_record_payload = {
            "type": "CNAME",
            "proxied": True,
            "name": tunnel["hostname"].split(".")[0],
            "zone_id": cf_zone_id,
            "content": f"{cf_tunnel_id}.cfargotunnel.com"
        }

        response = requests.post(dns_records_url, headers=headers, json=dns_record_payload)
        print("Created DNS:", response.json())

    def delete_tunnel_configuration(self, domain):
        # POST request to create tunnel configuration
        config = current_config_state.json()['result']
        ingress = config["config"]["ingress"]
        duplicated_entry = [e for e in ingress if e.get("hostname", None) == domain]
        duplicated_entry_index = ingress.index(duplicated_entry[0]) if duplicated_entry else None
        if not duplicated_entry:
            print("No Entry Found")
            return
        del ingress[duplicated_entry_index]
        config["config"]["ingress"] = ingress
        response = requests.put(configurations_url, headers=headers, json=config)
        print("Update Tunnel Config:", response)

        # GET request to retrieve DNS record
        dns_record_query_params = {
            "type": "CNAME",
            "name": domain,
            "content": f"{cf_tunnel_id}.cfargotunnel.com"
        }
        try:
            dns_id = requests.get(dns_records_url, headers=headers, params=dns_record_query_params).json()['result'][0]['id']
        except:
            print("No DNS Entry Found")
            return

        # DELETE request to delete DNS record
        delete_dns_record_url = f"{dns_records_url}/{dns_id}"
        response = requests.delete(delete_dns_record_url, headers=headers)
        print("Delete DNS Entry:", response.json())



