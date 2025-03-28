from datetime import datetime


class Room:
    """Class representing a hotel room."""

    def __init__(self, number, room_type, amenities, price):
        self._number = number
        self._room_type = room_type
        self._amenities = amenities
        self._price = price
        self._available = True

    def get_number(self):
        return self._number

    def set_available(self, status):
        self._available = status

    def is_available(self):
        return self._available

    def get_room_type(self):
        return self._room_type

    def get_amenities(self):
        return self._amenities

    def get_price(self):
        return self._price


class Guest:
    """Class representing a hotel guest."""

    def __init__(self, name, email, contact, loyalty_status):
        self._name = name
        self._email = email
        self._contact = contact
        self._loyalty_status = loyalty_status
        self._reservations = []

    def add_reservation(self, reservation):
        self._reservations.append(reservation)

    def get_reservations(self):
        return self._reservations

    def get_name(self):
        return self._name

    def get_email(self):
        return self._email

    def get_contact(self):
        return self._contact

    def get_loyalty_status(self):
        return self._loyalty_status


class Booking:
    """Class representing a booking."""

    def __init__(self, guest, room, check_in, check_out):
        self._guest = guest
        self._room = room
        self._check_in = check_in
        self._check_out = check_out
        self._status = "Confirmed"

    def generate_invoice(self):
        nights = (self._check_out - self._check_in).days
        total = nights * self._room.get_price()
        invoice = {
            "Guest": self._guest.get_name(),
            "Room": self._room.get_number(),
            "Nights": nights,
            "Price per Night": self._room.get_price(),
            "Total": total
        }
        return invoice

    def cancel_booking(self):
        self._status = "Cancelled"
        self._room.set_available(True)
        return f"Booking for room {self._room.get_number()} cancelled."

    def get_status(self):
        return self._status


# Main interaction
def main():
    rooms = [
        Room(101, "Single", ["WiFi", "TV"], 100),
        Room(102, "Double", ["WiFi", "TV", "Mini-bar"], 150),
        Room(201, "Suite", ["WiFi", "TV", "Mini-bar", "Jacuzzi"], 250)
    ]

    try:
        # Guest Account Creation
        print("=== Guest Account Creation ===")
        name = input("Name: ")
        email = input("Email: ")
        contact = input("Contact Number: ")
        loyalty_status = input("Loyalty Status: ")
        guest = Guest(name, email, contact, loyalty_status)
        print(f"Guest account created for {guest.get_name()}.\n")

        # Searching Available Rooms
        print("=== Room Search ===")
        room_type = input("Room Type (Single/Double/Suite): ")
        available_rooms = [room for room in rooms if
                           room.get_room_type().lower() == room_type.lower() and room.is_available()]
        if not available_rooms:
            print("No available rooms found.")
            return
        for room in available_rooms:
            print(f"Room {room.get_number()} at ${room.get_price()} per night with amenities: {room.get_amenities()}")

        # Room Reservation
        print("\n=== Making Reservation ===")
        try:
            room_number = int(input("Select room number to book: "))
            selected_room = next((room for room in available_rooms if room.get_number() == room_number), None)
            if not selected_room:
                raise ValueError("Invalid room number selected or room unavailable.")

            check_in_input = input("Check-in date (YYYY-MM-DD): ")
            check_out_input = input("Check-out date (YYYY-MM-DD): ")
            check_in = datetime.strptime(check_in_input, "%Y-%m-%d")
            check_out = datetime.strptime(check_out_input, "%Y-%m-%d")

            if check_in >= check_out:
                raise ValueError("Check-out date must be after check-in date.")

            booking = Booking(guest, selected_room, check_in, check_out)
            selected_room.set_available(False)
            guest.add_reservation(booking)
            print(f"Booking confirmed for Room {selected_room.get_number()}.\n")

            # Booking Confirmation Notification
            print(f"Notification sent to {guest.get_email()}: Booking confirmed.\n")

            # Invoice Generation
            print("=== Invoice ===")
            invoice = booking.generate_invoice()
            for key, value in invoice.items():
                print(f"{key}: {value}")
            print()

            # Payment Processing (Corrected part)
            print("=== Payment ===")
            allowed_methods = ["credit card", "mobile wallet"]
            payment_method = input("Payment Method (Credit Card/Mobile Wallet): ")

            if payment_method.strip().lower() not in allowed_methods:
                raise ValueError("Invalid payment method selected. Please choose Credit Card or Mobile Wallet.")

            print(f"Payment of ${invoice['Total']} received via {payment_method}.\n")

            # Reservation History
            print("=== Reservation History ===")
            for res in guest.get_reservations():
                print(
                    f"Room {res._room.get_number()} from {res._check_in.date()} to {res._check_out.date()}, Status: {res.get_status()}")
            print()

            # Cancellation
            cancel = input("Do you wish to cancel the reservation? (yes/no): ")
            if cancel.lower() == "yes":
                print(booking.cancel_booking())

        except ValueError as ve:
            print(f"Input Error: {ve}")
        except StopIteration:
            print("Error: Room not found or unavailable.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    except Exception as e:
        print(f"General Error occurred: {e}")


if __name__ == "__main__":
    main()
