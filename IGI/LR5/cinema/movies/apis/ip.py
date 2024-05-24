import requests


class IpAPI:
    @staticmethod
    def get_ip():
        return requests.get('https://api.ipify.org/?format=json').json()
