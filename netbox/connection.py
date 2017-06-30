import requests
import socket

class NetboxConnection(object):

    def __init__(self, ssl_verify=False, use_ssl=True, host=None, limit=1000, auth_token=None, port=80):
        self.use_ssl = use_ssl
        self.host = host
        self.limit = limit
        self.auth_token = auth_token
        self.port = port

        if use_ssl:
            self.port = 443

        self.base_url = 'http{s}://{host}:{p}/api'.format(s='s' if use_ssl else '', p=self.port, host=self.host)
        self.session = requests.Session()
        self.session.verify = ssl_verify

        if auth_token is not None:
            token = 'Token {}'.format(self.auth_token)
            self.session.headers.update({'Authorization': token})
            self.session.headers.update({'Accept': 'application/json'})
            self.session.headers.update({'Content-Type': 'application/json'})
        else:
            raise ValueError('Please enter authorization token when using api version 2')

    def __request(self, method, params=None, body=None):
        url = self.base_url + str(params)
        request = requests.Request(method=method, url=url, json=body)
        prepared_request = self.session.prepare_request(request)

        try:
            response = self.session.send(prepared_request)
        except socket.gaierror:
            err_msg = 'Unable to find address: {}'.format(self.host)
            raise socket.gaierror(err_msg)
        except requests.exceptions.ConnectionError:
            err_msg = 'Unable to connect to Netbox host: {}'.format(self.host)
            raise ConnectionError(err_msg)
        except requests.exceptions.Timeout:
            raise TimeoutError('Connection to Netbox host timed out')
        except Exception as e:
            raise Exception(e)
        finally:
            self.close()

        try:
            response_data = response.json()
        except:
            response_data = response.content

        return response.ok, response.status_code, response_data

    def get(self, params):
        self.session.params.update({'limit': self.limit})
        resp_ok, resp_status, resp_data = self.__request('GET', params)

        if resp_ok and resp_status == 200:
            return resp_data
        else:
            return list

    def put(self, params):
        return self.__request('PUT', params)

    def post(self, params, required_fields, **kwargs):
        body_data = {}

        for k, v in required_fields.items():
            body_data.update({k: v})

        if kwargs:
            for k, v in kwargs.items():
                body_data.update({k: v})

        resp_ok, resp_status, resp_data = self.__request('POST', params=params, body=body_data)

        if resp_ok and resp_status == 201:
            return resp_ok, resp_data
        else:
            return resp_ok, resp_data['name'][0]

    def delete(self, params, del_id):
        del_str = '{}{}'.format(params, del_id)
        resp_ok, resp_status, resp_data = self.__request('DELETE', del_str)

        if resp_ok and resp_status == 204:
            return True
        else:
            return False

    def close(self):

        self.session.close()