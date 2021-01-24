import json
import logging
from configparser import ConfigParser
import requests
from requests.structures import CaseInsensitiveDict
from apiClient import *
from bookingBuilder import BookingBuilder


def main():
    config = ConfigParser()
    config.read('config.ini')
    token = config['client_secret']['Authorization']

    reservations = list_of_reservation(token)
    print(reservations)

    bookingBuilder = BookingBuilder(first_name='Jan',last_name='Nowak',total_price=200,deposit_paid=False,booking_dates={'checkin':'2021-06-19', 'checkout':'2021-06-20'}, additional_needs='breakfast')
    booking = bookingBuilder.build()

    response = post_reservation(booking, token)
    booking_id = str(response['bookingid'])

    if response['bookingid'] != None:
        print('Your booking is done.')
    else:
        print('Something went wrong. Please try again.')

    response_get_by_id = get_reservation_by_id(booking_id, token)

    data = {
        "firstname": "Julia",
        "lastname": "Nowak",
        "totalprice": 111,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2018-01-01",
            "checkout": "2019-01-01"
        },
        "additionalneeds": "Breakfast"
    }

    response_update = update_booking(data, booking_id, token)


    data = response['booking']['lastname']
    params = {'lastname': data}
    response = get_reservation_by_name(params, token)

    response = delete_reservation(booking_id, token)

    if response.status_code == 201:
        print('Your booking is canceled.')
    else:
        print('Something went wrong. Please try again.')



if __name__ == '__main__':
   main()
