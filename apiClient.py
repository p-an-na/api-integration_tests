import json
import requests
from requests.structures import CaseInsensitiveDict
import time
import logging

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


class BearerAuth(requests.auth.AuthBase):

    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers = CaseInsensitiveDict()
        r.headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
        r.headers['Authorization'] = self.token

        return r

def get_api_url(path):
    return 'https://restful-booker.herokuapp.com' + path

def post_reservation(booking, token):
    booking = booking_to_json(booking)
    response = requests.post(get_api_url('/booking'), auth=BearerAuth(token), data=booking)
    logging.debug('Response post reservation:', response.text, 'Response status code:', response.status_code)
    response = response.json()
    return response

def get_reservation_by_id(booking_id, token):
    response = requests.get(get_api_url('/booking/') + booking_id, auth=BearerAuth(token))
    logging.debug('Response get reservation by id:', response.text, 'Response status code:', response.status_code)
    response = response.json()
    return response

def get_reservation_by_name(params, token):
    response = requests.get(get_api_url('/booking/'), auth=BearerAuth(token), params=params)
    logging.debug('Response get reservation by name:', response.text, 'Response status code:', response.status_code)
    response = response.json()
    return response

def delete_reservation(booking_id, token):
    response = requests.delete(get_api_url('/booking/') + booking_id, auth=BearerAuth(token))
    logging.debug('Response delete reservation:', response.text, 'Response status code:', response.status_code)
    return response

def list_of_reservation(token):
    response = requests.get(get_api_url('/booking'),auth=BearerAuth(token))
    logging.debug('response get id',response.text, response.status_code)
    response_get_id = response.json()

    reservations_details = []

    for item in response_get_id:
        id = str(item['bookingid'])
        reservations_details.append(item['bookingid'])

        response_get_details = requests.get(get_api_url('/booking/')+ id,auth=BearerAuth(token))
        response_get_details = response_get_details.json()

        reservations_details.append((response_get_details['firstname']))
        reservations_details.append(response_get_details['lastname'])
        reservations_details.append(response_get_details['bookingdates']['checkin'])
        reservations_details.append(response_get_details['bookingdates']['checkout'])

    return (reservations_details)

def booking_to_json(booking):
    return json.dumps({
        'firstname': booking.first_name,
        'lastname': booking.last_name,
        'totalprice': booking.total_price,
        'depositpaid': booking.deposit_paid,
        'bookingdates': booking.booking_dates,
        'additionalneeds': booking.additional_needs
    })

def update_booking(data, booking_id, token):
    response = requests.put(get_api_url('/booking/') + booking_id, auth=BearerAuth(token), data=json.dumps(data))
    logging.debug('response update',response.text, response.status_code)
    response = response.json()

    return response