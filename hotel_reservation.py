import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry

root = tk.Tk()
root.title("Hotel Reservation System")   # top title
root.configure(bg='#b5e9ea')    # bg color of window

# root.grid_rowconfigure(0, weight=1)
# root.grid_rowconfigure(1, weight=0)
# root.grid_columnconfigure(0, weight=1)


def load_reservations():
    reservations = []
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
                        reservations.append(reservation)
                        reservation = {}
            if reservation:  # Ensure the last reservation is added
                reservations.append(reservation)
    except FileNotFoundError:
        pass
    return reservations

def save_reservations(reservations):
    with open('reservations.txt', 'w') as file:
        for reservation in reservations:
            for key, value in reservation.items():
                if isinstance(value, list):
                    value = ", ".join(value)
                file.write(f"{key}: {value}\n")
            file.write("\n")

def clear_fields():
    first_name_entry.delete(0, tk.END)
    last_name_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END)
    guests_entry.delete(0, tk.END)
    id_number_entry.delete(0, tk.END)
    room_type.set('')
    num_beds.set(1)
    for var in services_vars.values():
        var.set(False)
    for var in facilities_vars.values():
        var.set(False)
    payment_method.set('')
    checkin_date_entry.delete(0, tk.END)
    checkout_date_entry.delete(0, tk.END)
    total_cost_var.set("0.0")

def get_next_reservation_number():
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

def update_cost():
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

    cost = room_cost.get(room_type.get(), 0) + (num_beds.get() - 1) * 10
    for service, var in services_vars.items():
        if var.get():
            cost += service_cost[service]
    for facility, var in facilities_vars.items():
        if var.get():
            cost += facility_cost[facility]

    total_cost_var.set(f"PKR {cost:.2f}")

def add_reservation():
    reservation_number = get_next_reservation_number()
    reservation = {
        "First Name": first_name_entry.get(),
        "Last Name": last_name_entry.get(),
        "Email": email_entry.get(),
        "Phone": phone_entry.get(),
        "Address": address_entry.get(),
        "Number of Guests": guests_entry.get(),
        "ID Number": id_number_entry.get(),
        "Room Type": room_type.get(),
        "Number of Beds": num_beds.get(),
        "Services": [service for service, var in services_vars.items() if var.get()],
        "Facilities": [facility for facility, var in facilities_vars.items() if var.get()],
        "Payment Method": payment_method.get(),
        "Check-in Date": checkin_date_entry.get(),
        "Check-out Date": checkout_date_entry.get(),
        "Total Cost": total_cost_var.get(),
        "Reservation Number": reservation_number
    }
    reservations.append(reservation)
    save_reservations(reservations)
    messagebox.showinfo("Success", f"Reservation added successfully!\nYour reservation number is {reservation_number}")
    clear_fields()

def view_reservations():
    view_window = tk.Toplevel(root)
    view_window.title("View Reservations")
    text = tk.Text(view_window)
    text.pack(expand=True, fill=tk.BOTH)

    for idx, reservation in enumerate(reservations, start=1):
        text.insert(tk.END, f"Reservation {idx}\n")
        for key, value in reservation.items():
            if isinstance(value, list):
                value = ", ".join(value)
            text.insert(tk.END, f"{key}: {value}\n")
        text.insert(tk.END, "-"*30 + "\n")

def update_reservation():
    update_window = tk.Toplevel(root)
    update_window.title("Update Reservation")
    
    tk.Label(update_window, text="Enter Reservation Number to update:").grid(row=0, column=0)
    reservation_number_entry = tk.Entry(update_window)
    reservation_number_entry.grid(row=0, column=1)
    
    def submit_update():
        idx = int(reservation_number_entry.get()) - 1
        if 0 <= idx < len(reservations):
            reservations[idx] = {
                "First Name": first_name_entry.get(),
                "Last Name": last_name_entry.get(),
                "Email": email_entry.get(),
                "Phone": phone_entry.get(),
                "Address": address_entry.get(),
                "Number of Guests": guests_entry.get(),
                "ID Number": id_number_entry.get(),
                "Room Type": room_type.get(),
                "Number of Beds": num_beds.get(),
                "Services": [service for service, var in services_vars.items() if var.get()],
                "Facilities": [facility for facility, var in facilities_vars.items() if var.get()],
                "Payment Method": payment_method.get(),
                "Check-in Date": checkin_date_entry.get(),
                "Check-out Date": checkout_date_entry.get(),
                "Total Cost": total_cost_var.get(),
                "Reservation Number": idx + 1
            }
            save_reservations(reservations)
            messagebox.showinfo("Success", "Reservation updated successfully!")
            update_window.destroy()
        else:
            messagebox.showerror("Error", "Invalid reservation number!")
    
    tk.Button(update_window, text="Submit", command=submit_update).grid(row=1, columnspan=2)

def delete_reservation():
    delete_window = tk.Toplevel(root)
    delete_window.title("Delete Reservation")

    tk.Label(delete_window, text="Enter Reservation Number to delete:").grid(row=0, column=0)
    reservation_number_entry = tk.Entry(delete_window)
    reservation_number_entry.grid(row=0, column=1)

    def submit_delete():
        idx = int(reservation_number_entry.get()) - 1
        if 0 <= idx < len(reservations):
            reservations.pop(idx)
            save_reservations(reservations)
            messagebox.showinfo("Success", "Reservation deleted successfully!")
            delete_window.destroy()
        else:
            messagebox.showerror("Error", "Invalid reservation number!")
    
    tk.Button(delete_window, text="Submit", command=submit_delete).grid(row=1, columnspan=2)

def generate_receipt():
    receipt_window = tk.Toplevel(root)
    receipt_window.title("Reservation Receipt")

    idx = len(reservations) - 1
    if idx >= 0:
        reservation = reservations[idx]
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
        messagebox.showerror("Error", "No reservation found!")

# Load reservations at startup
reservations = load_reservations()




services_vars = {
    'Room Service': tk.BooleanVar(),
    'Laundry Service': tk.BooleanVar(),
    'Tour Booking': tk.BooleanVar(),
    'Airport Transfer': tk.BooleanVar(),
    'Concierge Service': tk.BooleanVar(),
    'Spa Service': tk.BooleanVar(),
    'Gym Access': tk.BooleanVar(),
    'Babysitting Service': tk.BooleanVar()
}
facilities_vars = {
    'WiFi': tk.BooleanVar(),
    'Swimming Pool': tk.BooleanVar(),
    'Food': tk.BooleanVar(),
    'Parking': tk.BooleanVar(),
    'Bar': tk.BooleanVar(),
    'Conference Room': tk.BooleanVar()
}

# GUI
header_frame = tk.Frame(root, bg='#b5e9ea')
header_frame.grid(row=0, column=4, columnspan=6, pady=20)

personal_info_frame = tk.LabelFrame(root, text="Personal Information", bg='#b5e9ea' )
personal_info_frame.grid(row=1, column=4, padx=10, pady=30)

booking_info_frame = tk.LabelFrame(root, text="Booking Information", bg='#b5e9ea')
booking_info_frame.grid(row=2, column=4, padx=10, pady=10)

services_frame = tk.LabelFrame(root, text="Additional Services", bg='#b5e9ea')
services_frame.grid(row=1, column=5, padx=10, pady=10)

facilities_frame = tk.LabelFrame(root, text="Facilities", bg='#b5e9ea')
facilities_frame.grid(row=2, column=5, padx=10, pady=10)

payment_info_frame = tk.LabelFrame(root, text="Payment Information", bg='#b5e9ea')
payment_info_frame.grid(row=3, column=3, columnspan=2, padx=10, pady=10)

total_cost_frame = tk.Frame(root, bg='#b5e9ea')
total_cost_frame.grid(row=3, column=5, columnspan=2, pady=10)

buttons_frame = tk.Frame(root, bg='#b5e9ea')
buttons_frame.grid(row=4, column=4, columnspan=4, pady=10)

# Heading
tk.Label(header_frame, text="Hotel Reservation System", font=("Arial", 24, "bold"), bg='#b5e9ea').pack()

# Personal Information
tk.Label(personal_info_frame, text="First Name:", bg='#b5e9ea' ).grid(row=0, column=0, sticky="e")
first_name_entry = tk.Entry(personal_info_frame)
first_name_entry.grid(row=0, column=1)

tk.Label(personal_info_frame, text="Last Name:", bg='#b5e9ea').grid(row=1, column=0, sticky="e")
last_name_entry = tk.Entry(personal_info_frame)
last_name_entry.grid(row=1, column=1)

tk.Label(personal_info_frame, text="Email:", bg='#b5e9ea').grid(row=2, column=0, sticky="e")
email_entry = tk.Entry(personal_info_frame)
email_entry.grid(row=2, column=1)

tk.Label(personal_info_frame, text="Phone:", bg='#b5e9ea').grid(row=3, column=0, sticky="e")
phone_entry = tk.Entry(personal_info_frame)
phone_entry.grid(row=3, column=1)

tk.Label(personal_info_frame, text="Address:", bg='#b5e9ea').grid(row=4, column=0, sticky="e")
address_entry = tk.Entry(personal_info_frame)
address_entry.grid(row=4, column=1)

tk.Label(personal_info_frame, text="Number of Guests:", bg='#b5e9ea').grid(row=5, column=0, sticky="e")
guests_entry = tk.Entry(personal_info_frame)
guests_entry.grid(row=5, column=1)

tk.Label(personal_info_frame, text="ID Number:", bg='#b5e9ea').grid(row=6, column=0, sticky="e")
id_number_entry = tk.Entry(personal_info_frame)
id_number_entry.grid(row=6, column=1)

# Booking Information
tk.Label(booking_info_frame, text="Room Type:", bg='#b5e9ea').grid(row=0, column=0, sticky="e")
room_type = ttk.Combobox(booking_info_frame, values=["Single Room", "Double Room", "Deluxe Room",
                                                     "Suite", "Family Room", "Executive Room", "Luxury Room"])
room_type.grid(row=0, column=1)
room_type.bind('<<ComboboxSelected>>', lambda e: update_cost())

tk.Label(booking_info_frame, text="Number of Beds:", bg='#b5e9ea').grid(row=1, column=0, sticky="e")
num_beds = tk.IntVar(value=1)
beds_spinbox = tk.Spinbox(booking_info_frame, from_=1, to=10, textvariable=num_beds, command=update_cost)
beds_spinbox.grid(row=1, column=1)

tk.Label(booking_info_frame, text="Check-in Date:", bg='#b5e9ea').grid(row=2, column=0, sticky="e")
checkin_date_entry = DateEntry(booking_info_frame, date_pattern='dd/mm/yyyy')
checkin_date_entry.grid(row=2, column=1)

tk.Label(booking_info_frame, text="Check-out Date:", bg='#b5e9ea').grid(row=3, column=0, sticky="e")
checkout_date_entry = DateEntry(booking_info_frame, date_pattern='dd/mm/yyyy')
checkout_date_entry.grid(row=3, column=1)

# Additional Services
services_vars = {
    'Room Service': tk.BooleanVar(),
    'Laundry Service': tk.BooleanVar(),
    'Tour Booking': tk.BooleanVar(),
    'Airport Transfer': tk.BooleanVar(),
    'Concierge Service': tk.BooleanVar(),
    'Spa Service': tk.BooleanVar(),
    'Gym Access': tk.BooleanVar(),
    'Babysitting Service': tk.BooleanVar()
}
for idx, (service, var) in enumerate(services_vars.items()):
    tk.Checkbutton(services_frame, text=service, variable=var, command=update_cost, bg='#b5e9ea').grid(row=idx, column=0, sticky="w")

# Facilities
facilities_vars = {
    'WiFi': tk.BooleanVar(),
    'Swimming Pool': tk.BooleanVar(),
    'Food': tk.BooleanVar(),
    'Parking': tk.BooleanVar(),
    'Bar': tk.BooleanVar(),
    'Conference Room': tk.BooleanVar()
}
for idx, (facility, var) in enumerate(facilities_vars.items()):
    tk.Checkbutton(facilities_frame, text=facility, variable=var, command=update_cost, bg='#b5e9ea').grid(row=idx, column=0, sticky="w")

# Payment Information
tk.Label(payment_info_frame, text="Payment Method:", bg='#b5e9ea').grid(row=0, column=0, sticky="e")
payment_method = ttk.Combobox(payment_info_frame, values="Cash")
payment_method.grid(row=0, column=1)

# Total Cost
tk.Label(total_cost_frame, text="Total Cost:", font=("Arial", 14, "bold"), bg='#b5e9ea').grid(row=0, column=0, sticky="e")
total_cost_var = tk.StringVar(value="0.0")
tk.Label(total_cost_frame, textvariable=total_cost_var, font=("Arial", 14, "bold"), bg='#b5e9ea').grid(row=0, column=1, sticky="w")

# Buttons
tk.Button(buttons_frame, text="Add Reservation", command=add_reservation, bg='#005f73', fg='#ffffff').pack(side=tk.LEFT, padx=10)
tk.Button(buttons_frame, text="View Reservations", command=view_reservations, bg='#005f73', fg='#ffffff').pack(side=tk.LEFT, padx=10)
tk.Button(buttons_frame, text="Update Reservation", command=update_reservation, bg='#005f73', fg='#ffffff').pack(side=tk.LEFT, padx=10)
tk.Button(buttons_frame, text="Delete Reservation", command=delete_reservation, bg='#005f73', fg='#ffffff').pack(side=tk.LEFT, padx=10)
tk.Button(buttons_frame, text="Generate Receipt", command=generate_receipt, bg='#005f73', fg='#ffffff').pack(side=tk.LEFT, padx=10)

root.mainloop()