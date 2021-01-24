import unittest
from configparser import ConfigParser
import apiClient
from bookingBuilder import BookingBuilder
from main import booking_to_json


class TestApi(unittest.TestCase):

    def setUp(self):
        config = ConfigParser()
        config.read('config.ini')
        self.token = config['client_secret']['Authorization']

        bookingBuilder = BookingBuilder(first_name='Jan', last_name='Nowak', total_price=200, deposit_paid=False,
                                        booking_dates={'checkin': '2021-06-19', 'checkout': '2021-06-20'},
                                        additional_needs='breakfast')
        self.booking = bookingBuilder.build()


    def tearDown(self):
        pass

    def test_post_booking(self):
        response = apiClient.post_reservation(self.booking, self.token)

        self.assertIsNotNone(response['bookingid'])

    def test_post_name(self):
        response = apiClient.post_reservation(self.booking, self.token)

        self.assertEqual(response['booking']['firstname'], 'Jan')

    def test_update_booking(self):
        response = apiClient.post_reservation(self.booking, self.token)
        booking_id = str(response['bookingid'])
        data = {
            "firstname": "Jim",
            "lastname": "Brown",
            "totalprice": 111,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2018-01-01",
                "checkout": "2019-01-01"
            },
            "additionalneeds": "Breakfast"
        }
        response_update = apiClient.update_booking(data, booking_id, self.token)

        self.assertEqual(response_update['lastname'], 'Brown')


    def test_post_get_delete_booking(self):
        response = apiClient.post_reservation(self.booking, self.token)
        booking_id = str(response['bookingid'])
        response_get_by_id = apiClient.get_reservation_by_id(booking_id, self.token)
        response = apiClient.delete_reservation(booking_id, self.token)

        self.assertEqual(response.status_code, 201)






if __name__ == '__main__':
    unittest.main()