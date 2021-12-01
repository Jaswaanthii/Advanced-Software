""" ClientService to ClientAPI"""
import requests


class ClientService:
    @staticmethod
    def get_clients():
        response = requests.get('http://localhost:5001')
        clients = response.json()
        return clients

    @staticmethod
    def get_client(key):
        response = requests.request(method="GET", url='http://localhost:5001/' + key)
        client = response.json()
        return client




