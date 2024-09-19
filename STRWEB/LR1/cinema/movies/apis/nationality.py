import requests


class NationalityAPI:
    @staticmethod
    def get_ip(name):
        return requests.get(f'https://api.nationalize.io/?name={name}').json()
