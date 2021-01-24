from booking import Booking


class BookingBuilder():
    def __init__(self,first_name, last_name, total_price, deposit_paid, booking_dates, additional_needs):

        self.first_name = first_name
        self.last_name = last_name
        self.total_price = total_price
        self.deposit_paid = deposit_paid
        self.booking_dates = booking_dates
        self.additional_needs = additional_needs


    def build(self):
        b = Booking()
        b.first_name = self.first_name
        b.last_name = self.last_name
        b.total_price = self.total_price
        b. deposit_paid = self.deposit_paid
        b.booking_dates = self.booking_dates
        b.additional_needs = self.additional_needs

        return b