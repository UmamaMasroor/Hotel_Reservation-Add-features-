import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry

class HotelReservationForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Reservation Form" )
        self.root.configure(bg='#8BB7BA') 
        self.reservations = []
        self.load_reservations()
        self.create_widgets()

    def create_widgets(self):
        frame = tk.Frame(self.root)
        frame.pack(padx=5, pady=5)

        # User Information
        user_info_frame = tk.LabelFrame(frame, text="User Information" ,font= ("Arial,30"))
        user_info_frame.grid(row=0, column=0, padx=7, pady=3)

        tk.Label(user_info_frame, text="First Name",font= ("Helvetica", 10)
).grid(row=0, column=0, padx=10, pady=10)
        self.first_name = tk.Entry(user_info_frame)
        self.first_name.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(user_info_frame, text="Last Name",font= ("Helvetica", 10)).grid(row=0, column=2, padx=10, pady=10)
        self.last_name = tk.Entry(user_info_frame)
        self.last_name.grid(row=0, column=3, padx=10, pady=10)

        tk.Label(user_info_frame, text="Email",font= ("Helvetica", 10)).grid(row=2, column=0, padx=10, pady=10)
        self.email = tk.Entry(user_info_frame)
        self.email.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(user_info_frame, text="Phone Number",font= ("Helvetica", 10)).grid(row=2, column=2, padx=10, pady=10)
        self.phone = tk.Entry(user_info_frame)
        self.phone.grid(row=2, column=3, padx=10, pady=10)

        tk.Label(user_info_frame, text="Address",font= ("Helvetica", 10)).grid(row=3, column=0, padx=10, pady=10)
        self.address = tk.Entry(user_info_frame)
        self.address.grid(row=3, column=1, padx=10, pady=10)

        tk.Label(user_info_frame, text="Number of Guests",font= ("Helvetica", 10)).grid(row=3, column=2, padx=10, pady=10)
        self.guests = tk.Entry(user_info_frame)
        self.guests.grid(row=3, column=3, padx=10, pady=10)

        tk.Label(user_info_frame, text="ID Number",font= ("Helvetica", 10)).grid(row=4, column=1, padx=10, pady=10)
        self.id_number = tk.Entry(user_info_frame)
        self.id_number.grid(row=4, column=2
        , padx=10, pady=10)

        # Room Information
        room_info_frame = tk.LabelFrame(frame, text="Room Information" ,font= ("Arial,30"), width=500)
        room_info_frame.grid(row=1, column=0, padx=10, pady=5)

        tk.Label(room_info_frame, text="Room Type:",font= ("Helvetica", 10), padx=10, pady=5).grid(row=1, column=0, sticky=tk.W)
        self.room_type = tk.StringVar()
        room_options = ["Single Room", "Double Room", "Deluxe Room", "Suite", "Family Room", "Executive Room", "Luxury Room"]
        self.room_menu = ttk.Combobox(room_info_frame, textvariable=self.room_type, values=room_options)
        self.room_menu.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(room_info_frame, text="Number of Beds:",font= ("Helvetica", 10)).grid(row=2, column=0, sticky=tk.W)
        self.num_beds = tk.IntVar(value=1)
        self.beds_spinbox = tk.Spinbox(room_info_frame, from_=1, to_=10, textvariable=self.num_beds, command=self.update_cost)
        self.beds_spinbox.grid(row=2, column=1, padx=10, pady=5)

        # Services
        services_frame = tk.LabelFrame(frame, text="Services" ,font= ("Arial,30"), width=100)
        services_frame.grid(row=2, column=0, padx=15, pady=15,sticky='ew')
        self.services_vars = {
            'Room Service': tk.BooleanVar(),
            'Laundry Service': tk.BooleanVar(),
            'Tour Booking': tk.BooleanVar(),
            'Airport Transfer': tk.BooleanVar(),
            'Concierge Service': tk.BooleanVar(),
            'Spa Service': tk.BooleanVar(),
            'Gym Access': tk.BooleanVar(),
            'Babysitting Service': tk.BooleanVar(),

        }
        
        for idx, (service, var) in enumerate(self.services_vars.items()):
            tk.Checkbutton(services_frame, text=service, variable=var, command=self.update_cost).grid(row=idx//3, column=idx%3, sticky=tk.W, padx=25, pady=5)

        # Facilities
        facilities_frame = tk.LabelFrame(frame, text="Facilities" ,font= ("Arial,30"), padx=10, pady=5)
        facilities_frame.grid(row=3, column=0, padx=10, pady=5)
        self.facilities_vars = {
            'WiFi': tk.BooleanVar(),
            'Swimming Pool': tk.BooleanVar(),
            'Food': tk.BooleanVar(),
            'Parking': tk.BooleanVar(),
            'Bar': tk.BooleanVar(),
            'Conference Room': tk.BooleanVar()
        }
        for idx, (facility, var) in enumerate(self.facilities_vars.items()):
            tk.Checkbutton(facilities_frame, text=facility, variable=var, command=self.update_cost).grid(row=idx//2, column=idx%2, sticky=tk.W , padx=25, pady=5)

       # Payment Method
        tk.Label(frame, text="Payment Method:").grid(row=4, column=0, sticky=tk.W)
        self.payment_method = tk.StringVar()
        payment_options = "Cash"
        self.payment_menu = ttk.Combobox(frame, textvariable=self.payment_method, values=payment_options)
        self.payment_menu.grid(row=4, column=1)

        # Check-in and Check-out Dates
        tk.Label(frame, text="Check-in Date:").grid(row=5, column=0, sticky=tk.W)
        self.checkin_date = DateEntry(frame, date_pattern='y-mm-dd')
        self.checkin_date.grid(row=5, column=1)

        tk.Label(frame, text="Check-out Date:").grid(row=6, column=0, sticky=tk.W)
        self.checkout_date = DateEntry(frame, date_pattern='y-mm-dd')
        self.checkout_date.grid(row=6, column=1)

        # Total Cost
        tk.Label(frame, text="Total Cost:").grid(row=7, column=0, sticky=tk.W)
        self.total_cost_var = tk.StringVar(value="0.0")
        tk.Label(frame, textvariable=self.total_cost_var).grid(row=7, column=1, sticky=tk.W)

        # Buttons
        buttons_frame = tk.Frame(frame)
        buttons_frame.grid(row=8, column=0, pady=10, columnspan=3)

        self.add_button = tk.Button(buttons_frame, text="Add Reservation", command=self.add_reservation)
        self.add_button.grid(row=0, column=0, padx=5)

        self.update_button = tk.Button(buttons_frame, text="Update Reservation", command=self.update_reservation)
        self.update_button.grid(row=0, column=1, padx=5)

        self.delete_button = tk.Button(buttons_frame, text="Delete Reservation", command=self.delete_reservation)
        self.delete_button.grid(row=0, column=2, padx=5)

        self.view_button = tk.Button(buttons_frame, text="View Reservations", command=self.view_reservations)
        self.view_button.grid(row=0, column=3, padx=5)

        self.receipt_button = tk.Button(buttons_frame, text="Generate Receipt", command=self.generate_receipt)
        self.receipt_button.grid(row=0, column=4, padx=5)

    def update_cost(self):
        room_cost = {
            "Single Room": 10000, "Double Room": 15000, "Deluxe Room": 20000, 
            "Suite": 25000, "Family Room": 30000, "Executive Room": 35000, 
            "Luxury Room": 40000
        }
        service_cost = {
            'Room Service': 5500, 'Laundry Service': 3000, 'Tour Booking': 10000,
            'Airport Transfer': 6500, 'Concierge Service': 6000, 'Spa Service': 20000,
            'Gym Access': 10000, 'Babysitting Service': 16000
        }
        facility_cost = {
            'WiFi': 2000, 'Swimming Pool': 2300, 'Food': 5000, 'Parking': 1000, 
            'Bar': 2000, 'Conference Room': 20000
        }

        cost = room_cost.get(self.room_type.get(), 0) + (self.num_beds.get() - 1) * 10
        for service, var in self.services_vars.items():
            if var.get():
                cost += service_cost[service]
        for facility, var in self.facilities_vars.items():
            if var.get():
                cost += facility_cost[facility]

        self.total_cost_var.set(f"PKR{cost:.2f}")

    def add_reservation(self):
        reservation_number = self.get_next_reservation_number()
        reservation = {
            "First Name": self.first_name.get(),
            "Last Name": self.last_name.get(),
            "Email": self.email.get(),
            "Phone": self.phone.get(),
            "Address": self.address.get(),
            "Number of Guests": self.guests.get(),
            "ID Number": self.id_number.get(),
            "Room Type": self.room_type.get(),
            "Number of Beds": self.num_beds.get(),
            "Services": [service for service, var in self.services_vars.items() if var.get()],
            "Facilities": [facility for facility, var in self.facilities_vars.items() if var.get()],
            "Payment Method": self.payment_method.get(),
            "Check-in Date": self.checkin_date.get(),
            "Check-out Date": self.checkout_date.get(),
            "Total Cost": self.total_cost_var.get(),

            "Reservation Number": reservation_number
        }
        self.reservations.append(reservation)
        self.save_reservations()
        messagebox.showinfo("Success", f"Reservation added successfully!\nYour reservation number is {reservation_number}")
        self.clear_fields()

    def view_reservations(self):
        view_window = tk.Toplevel(self.root)
        view_window.title("View Reservations")
        text = tk.Text(view_window)
        text.pack(expand=True, fill=tk.BOTH)

        for idx, reservation in enumerate(self.reservations, start=1):
            text.insert(tk.END, f"Reservation {idx}\n")
            for key, value in reservation.items():
                if isinstance(value, list):
                    value = ", ".join(value)
                text.insert(tk.END, f"{key}: {value}\n")
            text.insert(tk.END, "-"*30 + "\n")

    def update_reservation(self):
        update_window = tk.Toplevel(self.root)
        update_window.title("Update Reservation")
        
        tk.Label(update_window, text="Enter Reservation Number to update:").grid(row=0, column=0)
        reservation_number_entry = tk.Entry(update_window)
        reservation_number_entry.grid(row=0, column=1)
        
        def submit_update():
            idx = int(reservation_number_entry.get()) - 1
            if 0 <= idx < len(self.reservations):
                self.reservations[idx] = {
                    "First Name": self.first_name.get(),
                    "Last Name": self.last_name.get(),
                    "Email": self.email.get(),
                    "Phone": self.phone.get(),
                    "Address": self.address.get(),
                    "Number of Guests": self.guests.get(),
                    "ID Number": self.id_number.get(),
                    "Room Type": self.room_type.get(),
                    "Number of Beds": self.num_beds.get(),
                    "Services": [service for service, var in self.services_vars.items() if var.get()],
                    "Facilities": [facility for facility, var in self.facilities_vars.items() if var.get()],
                    "Payment Method": self.payment_method.get(),
                    "Check-in Date": self.checkin_date.get(),
                    "Check-out Date": self.checkout_date.get(),
                    "Total Cost": self.total_cost_var.get(),
                    "Reservation Number": idx + 1
                }
                self.save_reservations()
                messagebox.showinfo("Success", "Reservation updated successfully!")
                update_window.destroy()
            else:
                messagebox.showerror("Error", "Invalid reservation number!")
        
        tk.Button(update_window, text="Submit", command=submit_update).grid(row=1, columnspan=2)

    def delete_reservation(self):
        delete_window = tk.Toplevel(self.root)
        delete_window.title("Delete Reservation")

        tk.Label(delete_window, text="Enter Reservation Number to delete:").grid(row=0, column=0)
        reservation_number_entry = tk.Entry(delete_window)
        reservation_number_entry.grid(row=0, column=1)

        def submit_delete():
            idx = int(reservation_number_entry.get()) - 1
            if 0 <= idx < len(self.reservations):
                self.reservations.pop(idx)
                self.save_reservations()
                messagebox.showinfo("Success", "Reservation deleted successfully!")
                delete_window.destroy()
            else:
                messagebox.showerror("Error", "Invalid reservation number!")
        
        tk.Button(delete_window, text="Submit", command=submit_delete).grid(row=1, columnspan=2)

    def save_reservations(self):
        with open('reservations.txt', 'w') as file:
            for reservation in self.reservations:
                for key, value in reservation.items():
                    if isinstance(value, list):
                        value = ", ".join(value)
                    file.write(f"{key}: {value}\n")
                file.write("\n")

    def load_reservations(self):
        try:
            with open('reservations.txt', 'r') as file:
                reservation = {}
                for line in file:
                    line = line.strip()
                    if line:
                        if ": " in line:
                            key, value = line.split(': ', 1)
                            if key in ["Services", "Facilities"]:
                                value = value.split(', ')
                            elif key == "Number of Beds":
                                value = int(value)
                            reservation[key] = value
                    else:
                        if reservation:
                            self.reservations.append(reservation)
                            reservation = {}
                if reservation:  # Ensure the last reservation is added
                    self.reservations.append(reservation)
        except FileNotFoundError:
            pass

    def clear_fields(self):
        self.first_name.delete(0, tk.END)
        self.last_name.delete(0, tk.END)
        self.email.delete(0, tk.END)
        self.phone.delete(0, tk.END)
        self.address.delete(0, tk.END)
        self.guests.delete(0, tk.END)
        self.id_number.delete(0, tk.END)
        self.room_type.set('')
        self.num_beds.set(1)
        for var in self.services_vars.values():
            var.set(False)
        for var in self.facilities_vars.values():
            var.set(False)
        self.payment_method.set('')
        self.checkin_date.delete(0, tk.END)
        self.checkout_date.delete(0, tk.END)
        self.total_cost_var.set("0.0")

    def get_next_reservation_number(self):
        try:
            with open('reservation_number.txt', 'r') as file:
                content = file.read().strip()
                if content:
                    reservation_number = int(content)
                else:
                    reservation_number = 0
        except (FileNotFoundError, ValueError):
            reservation_number = 0

        reservation_number += 1

        with open('reservation_number.txt', 'w') as file:
            file.write(str(reservation_number))

        return reservation_number

    def generate_receipt(self):
        receipt_window = tk.Toplevel(self.root)
        receipt_window.title("Reservation Receipt")

        idx = len(self.reservations) - 1
        if idx >= 0:
            reservation = self.reservations[idx]
            receipt_text = f"Hotel Reservation Receipt\n"
            receipt_text += f"Reservation Number: {reservation['Reservation Number']}\n"
            receipt_text += f"First Name: {reservation['First Name']}\n"
            receipt_text += f"Last Name: {reservation['Last Name']}\n"
            receipt_text += f"Email: {reservation['Email']}\n"
            receipt_text += f"Number of Guests: {reservation['Number of Guests']}\n"
            receipt_text += f"ID Number: {reservation['ID Number']}\n"
            receipt_text += f"Room Type: {reservation['Room Type']}\n"
            receipt_text += f"Payment Method: {reservation['Payment Method']}\n"
            receipt_text += f"Check-in Date: {reservation['Check-in Date']}\n"
            receipt_text += f"Check-out Date: {reservation['Check-out Date']}\n"
            receipt_text += f"Total Cost: {reservation['Total Cost']}\n"

            text_widget = tk.Text(receipt_window, wrap=tk.WORD)
            text_widget.pack(expand=True, fill=tk.BOTH)
            text_widget.insert(tk.END, receipt_text)

            with open('receipt.txt', 'w') as file:
                file.write(receipt_text)

        else:
            messagebox.showerror("Error", "No reservations to generate a receipt for!")

if __name__ == "__main__":
    root = tk.Tk()
    app = HotelReservationForm(root)
    root.mainloop()
