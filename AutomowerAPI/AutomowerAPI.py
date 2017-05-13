import logging
import requests
import json

logger = logging.getLogger("main")

class AutomowerAPI:
    _API_IM = 'https://iam-api.dss.husqvarnagroup.net/api/v3/'
    _API_TRACK = 'https://amc-api.dss.husqvarnagroup.net/v1/'
    _HEADERS = {'Accept': 'application/json', 'Content-type': 'application/json'}

    def __init__(self):
        self.logger = logging.getLogger("main.automower")
        self.session = requests.Session()
        self.device_id = None
        self.token = None

    def login(self, login, password):
        response = self.session.post(self._API_IM + 'token',
                                     headers=self._HEADERS,
                                     json={
                                         "data": {
                                             "attributes": {
                                                 "password": password,
                                                 "username": login
                                             },
                                             "type": "token"
                                         }
                                     })

        response.raise_for_status()
        self.logger.debug('Logged in successfully')

        json = response.json()
        self.token = json["data"]["id"]
        self.session.headers.update({
            'Authorization': "Bearer " + self.token,
            'Authorization-Provider': json["data"]["attributes"]["provider"]
        })

        self.select_first_robot()

    def logout(self):
        response = self.session.delete(self._API_IM + 'token/%s' % self.token)
        response.raise_for_status()
        self.device_id = None
        self.token = None
        del (self.session.headers['Authorization'])
        self.logger.debug('Logged out successfully')

    def list_robots(self):
        response = self.session.get(self._API_TRACK + 'mowers', headers=self._HEADERS)
        response.raise_for_status()

        return response.json()

    def select_first_robot(self):
        result = self.list_robots()
        self.device_id = result[0]['id']

    def status(self):
        response = self.session.get(self._API_TRACK + 'mowers/%s/status' % self.device_id, headers=self._HEADERS)
        response.raise_for_status()

        return response.json()

    def geo_status(self):
        response = self.session.get(self._API_TRACK + 'mowers/%s/geofence' % self.device_id, headers=self._HEADERS)
        response.raise_for_status()

        return response.json()

    def control(self, command):
        if command not in ['PARK', 'STOP', 'START']:
            raise Exception("Unknown command")

        response = self.session.post(self._API_TRACK + 'mowers/%s/control' % self.device_id,
                                    headers=self._HEADERS,
                                    json={
                                        "action": command
                                    })
        response.raise_for_status()

