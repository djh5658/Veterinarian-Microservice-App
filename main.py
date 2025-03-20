import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
import zmq 
import json
from datetime import datetime, timedelta, time

class App(tk.Tk):
    """Main application class."""
    def __init__(self):
        super().__init__()
        self.title("PetCare +")
        self.geometry("500x300")
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.logged_in = False
        self.create_Login_Form()

    def center_window(self):
        """Centers the window on the screen."""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

    """Form Element Functions."""

    def create_Login_Form(self):
        """Creates the login page."""
        self.clear_window()
        self.center_window()
        brand = tk.Label(self, text="PetCare +")
        brand.config(font =("Aptos", 20))
        brand.pack()

        tk.Label(self, text="Login to view current patient information and add new patients").pack()

        login_frame = tk.Frame(self)
        login_frame.pack()

        tk.Label(login_frame, text="Username:").grid(row= 0, column=0, padx=3, pady=3)
        tk.Entry(login_frame, textvariable=self.username).grid(row= 0, column=1, padx=3, pady=3)
        tk.Label(login_frame, text="Password:").grid(row= 1, column=0, padx=3, pady=3)
        tk.Entry(login_frame, textvariable=self.password, show="*").grid(row= 1, column=1, padx=3, pady=3)

        tk.Button(self, text="Login", bg='teal', command=self.login).pack(padx=3, pady=3)

    def create_Home_Screen(self):
        """Creates the home screen."""
        self.clear_window()
        self.center_window()
        self.geometry("650x300")

        brand = tk.Label(self, text="PetCare +")
        brand.config(font =("Aptos", 20))
        brand.pack()
        tk.Label(self, text="Welcome!").pack()
        tab_frame = tk.Frame(self)
        tab_frame.pack()

        tk.Button(tab_frame, text="Add Patient", bg='teal', command=self.add_Patient).grid(row= 0, column=0, padx=5, pady=5)
        tk.Button(tab_frame, text="Search for Patient Record", bg='teal', command=self.search_Records).grid(row= 1, column=0, padx=5, pady=5)
        tk.Button(tab_frame, text="Create Appointment", bg='teal', command=self.create_Appointment).grid(row= 2, column=0, padx=5, pady=5)
        tk.Button(tab_frame, text="View Scheduled Appointments", bg='teal', command=self.view_Appointments).grid(row= 3, column=0, padx=5, pady=5)
        tk.Button(tab_frame, text="Logout", bg='teal', command=self.logout).grid(row= 4, column=0, padx=5, pady=5)

    def home_Screen_Header(self, window_size):
        """Creates navigation tabs for each screen."""
        self.geometry(window_size)
        brand = tk.Label(self, text="PetCare +")
        brand.config(font =("Aptos", 20))
        brand.pack()
        tk.Label(self, text="Welcome!").pack()
        tab_frame = tk.Frame(self)
        tab_frame.pack()

        tk.Button(tab_frame, text="Home", bg='teal', command=self.create_Home_Screen).grid(row= 0, column=0, padx=5, pady=5)
        tk.Button(tab_frame, text="Add Patient", bg='teal', command=self.add_Patient).grid(row= 0, column=1, padx=5, pady=5)
        tk.Button(tab_frame, text="Search for Patient Record", bg='teal', command=self.search_Records).grid(row= 0, column=2, padx=5, pady=5)
        tk.Button(tab_frame, text="Create Appointment", bg='teal', command=self.create_Appointment).grid(row= 0, column=3, padx=5, pady=5)
        tk.Button(tab_frame, text="View Scheduled Appointments", bg='teal', command=self.view_Appointments).grid(row= 0, column=4, padx=5, pady=5)
        tk.Button(tab_frame, text="Logout", bg='teal', command=self.logout).grid(row= 0, column=5, padx=5, pady=5)

    def add_Patient(self):
        """Creates the form to add a new patient."""
        self.clear_window()
        size = "650x700"
        self.home_Screen_Header(size)
        self.center_window()

        frame = tk.Frame(self)
        frame.pack()

        add_info_label = tk.Label(frame, text="Fill out the required(*) fields below to add a new patient.")
        add_info_label.grid(row=1, column=0)
    
        # Saving Owner Info
        owner_info_frame =tk.LabelFrame(frame, text="Owner Information")
        owner_info_frame.grid(row= 2, column=0, padx=20, pady=10)

        first_name_label = tk.Label(owner_info_frame, text="*Owner - First Name")
        first_name_label.grid(row=0, column=0)
        last_name_label = tk.Label(owner_info_frame, text="*Owner - Last Name")
        last_name_label.grid(row=0, column=1)

        self.first_name_entry = tk.Entry(owner_info_frame)
        self.last_name_entry = tk.Entry(owner_info_frame)
        self.first_name_entry.grid(row=1, column=0)
        self.last_name_entry.grid(row=1, column=1)

        address_label = tk.Label(owner_info_frame, text="*Owner - Address")
        address_label.grid(row=2, column=0)

        self.address_entry = tk.Entry(owner_info_frame)
        self.address_entry.grid(row=3, column=0)
        
        phone_number_label = tk.Label(owner_info_frame, text="*Owner - Phone Number")
        phone_number_label.grid(row=2, column=1)

        self.phone_number_entry = tk.Entry(owner_info_frame)
        self.phone_number_entry.grid(row=3, column=1)

        for widget in owner_info_frame.winfo_children():
            widget.grid_configure(padx=10, pady=5)

        # Saving Pet Info
        pet_info_frame = tk.LabelFrame(frame, text="Pet Information")
        pet_info_frame.grid(row=3, column=0, sticky="news", padx=20, pady=10)

        pet_name_label = tk.Label(pet_info_frame, text="*Pet - Name: ")
        pet_name_label.grid(row=0, column=0)
        self.pet_name_entry = tk.Entry(pet_info_frame)
        self.pet_name_entry.grid(row=0, column=1)

        pet_type_label = tk.Label(pet_info_frame, text="Pet - Type: ")
        self.pet_type_combobox = ttk.Combobox(pet_info_frame, values=["", "Cat", "Dog", "Fish"])
        pet_type_label.grid(row=1, column=0)
        self.pet_type_combobox.grid(row=1, column=1)                                 

        for widget in pet_info_frame.winfo_children():
            widget.grid_configure(padx=10, pady=5)

        # Saving Other Info
        add_info_frame = tk.LabelFrame(frame, text="Other")
        add_info_frame.grid(row=4, column=0, sticky="news", padx=20, pady=10)
        add_info_label = tk.Label(add_info_frame, text="Additional Information: ")
        add_info_label.grid(row=0, column=0)

        self.add_info_textbox = tk.Text(add_info_frame, height = 10, width = 35)
        self.add_info_textbox.grid(row=1, column=0)
        
        for widget in add_info_frame.winfo_children():
            widget.grid_configure(padx=10, pady=5)

        button = tk.Button(frame, text="Add Patient", command= self.enter_patient)
        button.grid(row=5, column=0, sticky="news", padx=20, pady=10)

    def search_Records(self):
        """Creates the page to view patient records."""
        self.clear_window()
        size = "1700x450"
        self.home_Screen_Header(size)
        self.center_window()

        # Retrieve all patient data
        current_patients = self.get_records()
        current_patients.pop(0)

        self.tree = ttk.Treeview(self, columns=("col1", "col2", "col3", "col4", "col5", "col6", "col7", "col8"), show="headings")
        self.tree.heading("col1", text="Patient ID")
        self.tree.heading("col2", text="Owner - First Name")
        self.tree.heading("col3", text="Owner - Last Name")
        self.tree.heading("col4", text="Owner - Address")
        self.tree.heading("col5", text="Owner - Phone Number")
        self.tree.heading("col6", text="Pet - Name")
        self.tree.heading("col7", text="Pet - Type")
        self.tree.heading("col8", text="Additional Information")

        for item in current_patients:
            self.tree.insert("", tk.END, values=(item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7]))

        self.tree.pack()

        self.tree.bind("<Double-Button-1>", self.on_double_click)

    def create_Appointment(self):
        """Creates the form to create a new appointment."""
        self.clear_window()
        size = "550x650"
        self.home_Screen_Header(size)
        self.center_window()

        frame = tk.Frame(self)
        frame.pack()

        add_info_label = tk.Label(frame, text="Fill out the required(*) fields below to create a new appointment.")
        add_info_label.grid(row=1, column=0)
    
        # Saving Owner Info
        owner_info_frame =tk.LabelFrame(frame, text="Owner Information")
        owner_info_frame.grid(row= 2, column=0, padx=20, pady=10)

        first_name_label = tk.Label(owner_info_frame, text="*Owner - First Name")
        first_name_label.grid(row=0, column=0)
        last_name_label = tk.Label(owner_info_frame, text="*Owner - Last Name")
        last_name_label.grid(row=0, column=1)

        self.first_name_entry = tk.Entry(owner_info_frame)
        self.last_name_entry = tk.Entry(owner_info_frame)
        self.first_name_entry.grid(row=1, column=0)
        self.last_name_entry.grid(row=1, column=1)

        pet_name_label = tk.Label(owner_info_frame, text="*Pet - Name: ")
        pet_name_label.grid(row=0, column=2)
        self.pet_name_entry = tk.Entry(owner_info_frame)
        self.pet_name_entry.grid(row=1, column=2)

        for widget in owner_info_frame.winfo_children():
            widget.grid_configure(padx=10, pady=5)

        # Saving Pet Info
        appt_info_frame = tk.LabelFrame(frame, text="Appointment Information")
        appt_info_frame.grid(row=3, column=0, sticky="news", padx=20, pady=10)

        month_label = tk.Label(appt_info_frame, text="Date: ")
        month_label.grid(row=1, column=0)

        self.date_entry = DateEntry(appt_info_frame, width=12, background='darkblue',
                    foreground='white', borderwidth=2)
        self.date_entry.grid(row=1, column=1)

        time_label = tk.Label(appt_info_frame, text="Time: ")
        time_label.grid(row=2, column=0)

        self.time_combo = ttk.Combobox(appt_info_frame, values=[], state="readonly")
        self.time_combo.grid(row=2, column=1)
        self.update_time()

        for widget in appt_info_frame.winfo_children():
            widget.grid_configure(padx=10, pady=5)

        button = tk.Button(frame, text="Add Appointment", command= self.enter_appointment)
        button.grid(row=5, column=0, sticky="news", padx=20, pady=10)

    def view_Appointments(self):
        """Creates the page to view all scheduled appointments."""
        self.clear_window()
        size = "1300x650"
        self.home_Screen_Header(size)
        self.center_window()

        current_appointments = self.get_appointments()
        current_appointments .pop(0)

        self.appt_tree = ttk.Treeview(self, columns=("col1", "col2", "col3", "col4", "col5", "col6"), show="headings")
        self.appt_tree.heading("col1", text="Appointment ID")
        self.appt_tree.heading("col2", text="Owner - First Name")
        self.appt_tree.heading("col3", text="Owner - Last Name")
        self.appt_tree.heading("col4", text="Pet - Name")
        self.appt_tree.heading("col5", text="Date")
        self.appt_tree.heading("col6", text="Time")
       

        for appt_item in current_appointments :
            self.appt_tree.insert("", tk.END, values=(appt_item[0], appt_item[1], appt_item[2], appt_item[3], appt_item[4], appt_item[5]))

        self.appt_tree.pack()

        self.appt_tree.bind("<Double-Button-1>", self.on_double_click_appt)

    """Admin Screen Form Elements."""

    def create_Admin_Screen(self):
        """Creates the admin home screen."""
        self.clear_window()
        self.center_window()
        self.geometry("650x300")

        brand = tk.Label(self, text="PetCare +")
        brand.config(font =("Aptos", 20))
        brand.pack()
        tk.Label(self, text="Welcome!").pack()
        tab_frame = tk.Frame(self)
        tab_frame.pack()

        tk.Button(tab_frame, text="Add Vet", bg='teal', command=self.add_Vet).grid(row= 0, column=0, padx=5, pady=5)
        tk.Button(tab_frame, text="Remove Vet", bg='teal', command=self.remove_Vet).grid(row= 1, column=0, padx=5, pady=5)
        tk.Button(tab_frame, text="Import Records", bg='teal', command=self.import_Data).grid(row= 2, column=0, padx=5, pady=5)
        tk.Button(tab_frame, text="Export Records", bg='teal', command=self.export_Data).grid(row= 3, column=0, padx=5, pady=5)
        tk.Button(tab_frame, text="Logout", bg='teal', command=self.logout).grid(row= 4, column=0, padx=5, pady=5)

    def admin_Screen_Header(self, window_size):
        """Creates navigation tabs for each admin screen."""
        self.geometry(window_size)
        brand = tk.Label(self, text="PetCare +")
        brand.config(font =("Aptos", 20))
        brand.pack()
        tk.Label(self, text="Welcome!").pack()
        tab_frame = tk.Frame(self)
        tab_frame.pack()

        tk.Button(tab_frame, text="Home", bg='teal', command=self.create_Admin_Screen).grid(row= 0, column=0, padx=5, pady=5)
        tk.Button(tab_frame, text="Add Vet", bg='teal', command=self.add_Vet).grid(row= 0, column=1, padx=5, pady=5)
        tk.Button(tab_frame, text="Remove Vet", bg='teal', command=self.remove_Vet).grid(row= 0, column=2, padx=5, pady=5)
        tk.Button(tab_frame, text="Import Records", bg='teal', command=self.import_Data).grid(row= 0, column=3, padx=5, pady=5)
        tk.Button(tab_frame, text="Export Records", bg='teal', command=self.export_Data).grid(row= 0, column=4, padx=5, pady=5)
        tk.Button(tab_frame, text="Logout", bg='teal', command=self.logout).grid(row= 0, column=5, padx=5, pady=5)

    def add_Vet(self):
        """Creates the form to add a new vet."""
        self.clear_window()
        size = "600x650"
        self.admin_Screen_Header(size)
        self.center_window()

        frame = tk.Frame(self)
        frame.pack()

        add_info_label = tk.Label(frame, text="Fill out the required(*) fields below to add a new vet.")
        add_info_label.grid(row=1, column=0)
    
        # Saving Owner Info
        vet_info_frame =tk.LabelFrame(frame, text="New Vet Information")
        vet_info_frame.grid(row= 2, column=0, padx=20, pady=10)

        vet_name_label = tk.Label(vet_info_frame, text="*Vet Username:")
        vet_name_label.grid(row=0, column=0)
        vet_password_label = tk.Label(vet_info_frame, text="*Vet Password:")
        vet_password_label.grid(row=0, column=1)

        self.vet_name_entry = tk.Entry(vet_info_frame)
        self.vet_password_entry = tk.Entry(vet_info_frame)
        self.vet_name_entry.grid(row=1, column=0)
        self.vet_password_entry.grid(row=1, column=1)

        for widget in vet_info_frame.winfo_children():
            widget.grid_configure(padx=10, pady=5)

        button = tk.Button(frame, text="Add Vet", command= self.enter_vet)
        button.grid(row=5, column=0, sticky="news", padx=20, pady=10)

    def remove_Vet(self):
        """Creates the form to remove a vet."""
        self.clear_window()
        size = "600x650"
        self.admin_Screen_Header(size)
        self.center_window()

        frame = tk.Frame(self)
        frame.pack()

        remove_vet_label = tk.Label(frame, text="Enter the vet's ID to remove them from the system.")
        remove_vet_label.grid(row=0, column=0)

        self.r_vet_id_label = tk.Label(frame, text="Vet ID: ")
        self.r_vet_id_label.grid(row=1, column=0)
        self.r_vet_id_entry = tk.Entry(frame)
        self.r_vet_id_entry.grid(row=1, column=1)

        # Add Remove Vet Button
        button = tk.Button(frame, text="Remove Vet", command= self.delete_vet)
        button.grid(row=2, column=0, sticky="news", padx=20, pady=10)

    def import_Data(self):
        """Creates the form to import data."""
        self.clear_window()
        size = "600x650"
        self.admin_Screen_Header(size)
        self.center_window()

        frame = tk.Frame(self)
        frame.pack()

        f_path_desc_label = tk.Label(frame, text="Enter the file path below for the file you would like to import.")
        f_path_desc_label.grid(row=0, column=1)

        self.f_path_label = tk.Label(frame, text="File Path: ")
        self.f_path_label.grid(row=1, column=0)
        self.f_path_entry = tk.Entry(frame, width=50)
        self.f_path_entry.grid(row=1, column=1)

        button = tk.Button(frame, text="Import Data", command= self.import_data_action)
        button.grid(row=1, column=2, sticky="news", padx=10, pady=10)

    def export_Data(self):
        """Creates the form to export data."""
        self.clear_window()
        size = "600x650"
        self.admin_Screen_Header(size)
        self.center_window()

        frame = tk.Frame(self)
        frame.pack()

        export_desc_label = tk.Label(frame, text="Select the button below to export the patient database to a CSV file.")
        export_desc_label.grid(row=0, column=0)

        export_desc_label2 = tk.Label(frame, text="File will be available in the downloads folder upon completion.")
        export_desc_label2.grid(row=1, column=0)

        button = tk.Button(frame, text="Export Data", command= self.export_data_action)
        button.grid(row=2, column=0, sticky="news", padx=20, pady=10)

    """Helper Functions for Form Elements."""

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()
  
    def login(self):
        """Handles the login process."""
        user_cred = self.verify_credentials(self.username.get())
        password_cred = self.verify_credentials(self.password.get())

        if user_cred == True and password_cred == True:
            self.logged_in = True
            if self.username.get() == "admin" and self.password.get() == "admin":
                self.create_Admin_Screen()
            else:
                self.create_Home_Screen()
        else:
            messagebox.showerror("Error", "Incorrect username or password.")
            self.username.set("")
            self.password.set("")

    def logout(self):
        """Handles the logout process."""
        self.response = messagebox.askyesno("Logout", "Are you sure that you would like to logout?")
        if self.response:
            self.geometry("500x300")
            self.logged_in = False
            self.username.set("")
            self.password.set("")
            self.create_Login_Form()

    def connect_to_microservice(self, port_number, msg):
        """Handles communication between microservices."""   
        context = zmq.Context()
        print("Attempting to connect to 'Credentials' server...")
        socket = context.socket(zmq.REQ)
        socket.connect(port_number)

        print("Connection Successful")
        print(f"Sending request to server...")

        socket.send_string(json.dumps(msg))
            
        message = socket.recv()

        print(f"Reply from server: {message}")
        print("Closing Connection...")
        socket.send_string(json.dumps("Quit")) 

        return message

    def enter_patient(self):
        """Handles the process to add a patient."""
        self.confirm_response = messagebox.askyesno("Add Patient", "Add patient to database?")
        if self.confirm_response:
            owner_f_name = self.first_name_entry.get()
            owner_l_name = self.last_name_entry.get()
            owner_addr = self.address_entry.get()
            owner_number = self.phone_number_entry.get()
            pet_name = self.pet_name_entry.get()
            pet_type = self.pet_type_combobox.get()
            add_info = self.add_info_textbox.get(1.0, "end-1c")
            new_entry = [owner_f_name, owner_l_name, owner_addr, owner_number, pet_name, pet_type, add_info]
            print(new_entry)

            # Call patient_database microservice
            port_number = "tcp://localhost:5556"
            msg = {'add' : new_entry}
            self.connect_to_microservice(port_number, msg)

            messagebox.showinfo("Success", "Patient Successfully Added!!!")
            self.create_Home_Screen()

    def on_double_click(self, event):
        """Handles the process of selecting a patient"""
        item = self.tree.selection()[0]
        values = self.tree.item(item, "values")
        Edit_Patient_Window(self, item, values)

    def get_records(self):
        """Handles the process of retrieving all patient records."""
        # Microservice A - Call Patient Database to get info
        port_number = "tcp://localhost:5556"
        msg = {'all': []}
        return json.loads(self.connect_to_microservice(port_number, msg))
         
    def update_time(self):
        """Handles the process of providing appointment times."""
        now = datetime.now()
        nine_am = datetime.combine(now, time(9, 0))
        print(now)
        times = [(nine_am + timedelta(minutes=30*i)).strftime("%H:%M") for i in range(16)]
        self.time_combo['values'] = times

    def enter_appointment(self):
        """Handles the process of adding an appointment."""
        self.confirm_response = messagebox.askyesno("Add Appointment", "Add appointment to database?")
        if self.confirm_response:
            owner_f_name = self.first_name_entry.get()
            owner_l_name = self.last_name_entry.get()
            pet_name = self.pet_name_entry.get()
            selected_month = self.date_entry.get_date().strftime('%Y-%m-%d')
            selected_time = self.time_combo.get()
            
            new_entry = [owner_f_name, owner_l_name, pet_name, selected_month, selected_time]
            print(new_entry)

            port_number = "tcp://localhost:5559"
            msg = {'add' : new_entry}
            self.connect_to_microservice(port_number, msg)

            messagebox.showinfo("Success", "Appointment Successfully Added!!!")
            self.create_Home_Screen()
    
    def on_double_click_appt(self, event):
        """Handles the process of selecting an appointment."""
        appt_item = self.appt_tree.selection()[0]
        appt_values = self.appt_tree.item(appt_item, "values")
        Edit_Appointment_Window(self, appt_item, appt_values)
    
    def get_appointments(self):
        """Handles the process of retrieving all appointments."""
        # Microservice A - Call Patient Database to get info
        port_number = "tcp://localhost:5559"
        msg = {'all': []}
        return json.loads(self.connect_to_microservice(port_number, msg))

    """Admin Screen Helper Functions"""

    def verify_credentials(self, credential):
        """Handles the process to verify a user's credentials."""
        port_number = "tcp://localhost:5557"
        msg = {'verify' : credential}
        return json.loads(self.connect_to_microservice(port_number, msg))

    def enter_vet(self):
        """Handles the process to add a vet."""
        self.confirm_response = messagebox.askyesno("Add vet", "Add vet to database?")
        if self.confirm_response:
            vet_name = self.vet_name_entry.get()
            vet_password = self.vet_password_entry.get()
            
            new_entry = [vet_name, vet_password]
            port_number = "tcp://localhost:5557"
            msg = {'add' : new_entry}
            self.connect_to_microservice(port_number, msg)

            messagebox.showinfo("Success", "Vet Successfully Added!!!")
            self.create_Admin_Screen()
    
    def delete_vet(self):
        """Handles the process to remove a vet."""
        self.confirm_response = messagebox.askyesno("Remove vet", "Remove vet from database?")
        if self.confirm_response:
            vet_id = int(self.r_vet_id_entry.get())
            print(vet_id)

            port_number = "tcp://localhost:5557"
            msg = {'remove' : vet_id}
            self.connect_to_microservice(port_number, msg)

            messagebox.showinfo("Success", "Vet Successfully Removed!!!")
            self.create_Admin_Screen()    
     
    def import_data_action(self):
        """Handles the process of importing data."""
        # Call to Import_export to convert csv
        port_number = "tcp://localhost:5558"
        msg = {'import' : self.f_path_entry.get()}
        response = json.loads(self.connect_to_microservice(port_number, msg))

        # Call to patient_database to replace database
        port_number = "tcp://localhost:5556"
        msg = {'import' : response}
        self.connect_to_microservice(port_number, msg)

        messagebox.showinfo("Success", "Data Import Successful!!!")
        self.create_Admin_Screen()

    def export_data_action(self):
        """Handles the process of exporting data."""
        # Microservice A - Call Patient Database to get info
        port_number = "tcp://localhost:5556"
        msg = {'all': []}
        response = json.loads(self.connect_to_microservice(port_number, msg))

        # Microservice B - Call Import_Export to send data to excel file
        port_number = "tcp://localhost:5558"
        msg = {'export' : response}
        self.connect_to_microservice(port_number, msg)

        messagebox.showinfo("Success", "Database Successfully Exported")
        self.create_Admin_Screen()

class Edit_Patient_Window(tk.Toplevel):
    """Popup Window for Editing a Patient."""
    def __init__(self, parent, item, values):
        super().__init__(parent.master)
        self.parent = parent
        self.item = item
        self.edit_items = values
        self.title("Edit Row")

        frame = tk.Frame(self)
        frame.pack()

        add_info_label = tk.Label(frame, text="Fill out the required(*) fields below and click save when finished.")
        add_info_label.grid(row=1, column=0)
    
        # Saving Owner Info
        owner_info_frame =tk.LabelFrame(frame, text="Owner Information")
        owner_info_frame.grid(row= 2, column=0, padx=20, pady=10)

        first_name_label = tk.Label(owner_info_frame, text="*Owner - First Name")
        first_name_label.grid(row=0, column=0)
        last_name_label = tk.Label(owner_info_frame, text="*Owner - Last Name")
        last_name_label.grid(row=0, column=1)
        self.first_name_entry = tk.Entry(owner_info_frame)
        self.last_name_entry = tk.Entry(owner_info_frame)
        
        self.first_name_entry.insert(0, values[1])
        self.last_name_entry.insert(0, values[2])
        self.first_name_entry.grid(row=1, column=0)
        self.last_name_entry.grid(row=1, column=1)

        address_label = tk.Label(owner_info_frame, text="*Owner - Address")
        address_label.grid(row=2, column=0)

        self.address_entry = tk.Entry(owner_info_frame)
        self.address_entry.insert(0, values[3])
        self.address_entry.grid(row=3, column=0)
        
        phone_number_label = tk.Label(owner_info_frame, text="*Owner - Phone Number")
        phone_number_label.grid(row=2, column=1)

        self.phone_number_entry = tk.Entry(owner_info_frame)
        self.phone_number_entry.insert(0, values[4])
        self.phone_number_entry.grid(row=3, column=1)

        for widget in owner_info_frame.winfo_children():
            widget.grid_configure(padx=10, pady=5)

        # Saving Pet Info
        pet_info_frame = tk.LabelFrame(frame, text="Pet Information")
        pet_info_frame.grid(row=3, column=0, sticky="news", padx=20, pady=10)

        pet_name_label = tk.Label(pet_info_frame, text="*Pet - Name: ")
        pet_name_label.grid(row=0, column=0)
        self.pet_name_entry = tk.Entry(pet_info_frame)
        self.pet_name_entry.insert(0, values[5])
        self.pet_name_entry.grid(row=0, column=1)

        pet_type_label = tk.Label(pet_info_frame, text="Pet - Type: ")
        self.pet_type_combobox = ttk.Combobox(pet_info_frame, values=["", "Cat", "Dog", "Fish"])
        pet_type_label.grid(row=1, column=0)
        self.pet_type_combobox.insert(0, values[6])
        self.pet_type_combobox.grid(row=1, column=1)                                 

        for widget in pet_info_frame.winfo_children():
            widget.grid_configure(padx=10, pady=5)

        # Saving Other Info
        add_info_frame = tk.LabelFrame(frame, text="Other")
        add_info_frame.grid(row=4, column=0, sticky="news", padx=20, pady=10)
        add_info_label = tk.Label(add_info_frame, text="Additional Information: ")
        add_info_label.grid(row=0, column=0)

        self.add_info_textbox = tk.Text(add_info_frame, height = 10, width = 35)
        self.add_info_textbox.insert(tk.END, values[7])
        self.add_info_textbox.grid(row=1, column=0)
        
        for widget in add_info_frame.winfo_children():
            widget.grid_configure(padx=10, pady=5)

        # Add Patient Button
        button = tk.Button(frame, text="Save", command= self.save)
        button.grid(row=5, column=0, sticky="news", padx=20, pady=10)

    def connect_to_microservice(self, port_number, msg):
        """Handles the process of connecting to a microservice."""
        context = zmq.Context()
        print("Attempting to connect to 'Credentials' server...")
        socket = context.socket(zmq.REQ)
        socket.connect(port_number)

        print("Connection Successful")
        print(f"Sending request to server...")

        socket.send_string(json.dumps(msg))
            
        message = socket.recv()

        print(f"Reply from server: {message}")
        print("Closing Connection...")
        socket.send_string(json.dumps("Quit")) 

        return message

    def save(self):
        """Handles the process of updating the tree view for patients."""
        self.edit_data()
        new_values = (int(self.edit_items[0]), self.first_name_entry.get(), self.last_name_entry.get(),  
                        self.address_entry.get(), self.phone_number_entry.get(),
                        self.pet_name_entry.get(), self.pet_type_combobox.get(),
                        self.add_info_textbox.get("1.0", tk.END),)
        self.parent.tree.item(self.item, values=new_values)
        self.destroy()

    def edit_data(self):
        """Handles the process of updating a patients information."""
        self.confirm_response = messagebox.askyesno("Edit Patient", "Edit patient in the database? This action cannot be undone!")
        if self.confirm_response:
            owner_f_name = self.first_name_entry.get()
            owner_l_name = self.last_name_entry.get()
            owner_addr = self.address_entry.get()
            owner_number = self.phone_number_entry.get()
            pet_name = self.pet_name_entry.get()
            pet_type = self.pet_type_combobox.get()
            add_info = self.add_info_textbox.get(1.0, "end-1c")
            edit_entry = [int(self.edit_items[0]) + 1, [int(self.edit_items[0]), owner_f_name, owner_l_name, owner_addr, owner_number, pet_name, pet_type, add_info]]
            print(edit_entry)

            # Connect to the patient_data microservice
            port_number = "tcp://localhost:5556"
            msg = {'edit' : edit_entry}
            self.connect_to_microservice(port_number, msg)

            messagebox.showinfo("Success", "Patient Successfully Edited!!!")

class Edit_Appointment_Window(tk.Toplevel):
    """Popup Window for Editing an Appointment."""
    def __init__(self, parent, item, values):
        super().__init__(parent.master)
        self.parent = parent
        self.item = item
        self.edit_items = values
        self.title("Edit Appointment")

        frame = tk.Frame(self)
        frame.pack()

        add_info_label = tk.Label(frame, text="Fill out the fields below to create a new appointment.")
        add_info_label.grid(row=1, column=0)
    
        # Saving Owner Info
        owner_info_frame =tk.LabelFrame(frame, text="Owner Information")
        owner_info_frame.grid(row= 2, column=0, padx=20, pady=10)

        first_name_label = tk.Label(owner_info_frame, text="*Owner - First Name")
        first_name_label.grid(row=0, column=0)
        last_name_label = tk.Label(owner_info_frame, text="*Owner - Last Name")
        last_name_label.grid(row=0, column=1)

        self.first_name_entry = tk.Entry(owner_info_frame)
        self.last_name_entry = tk.Entry(owner_info_frame)

        self.first_name_entry.insert(0, values[1])
        self.last_name_entry.insert(0, values[2])
        self.first_name_entry.grid(row=1, column=0)
        self.last_name_entry.grid(row=1, column=1)

        pet_name_label = tk.Label(owner_info_frame, text="*Pet - Name: ")
        pet_name_label.grid(row=0, column=2)
        self.pet_name_entry = tk.Entry(owner_info_frame)
        self.pet_name_entry.insert(0, values[3])
        self.pet_name_entry.grid(row=1, column=2)

        for widget in owner_info_frame.winfo_children():
            widget.grid_configure(padx=10, pady=5)

        # Saving Pet Info
        appt_info_frame = tk.LabelFrame(frame, text="Appointment Information")
        appt_info_frame.grid(row=3, column=0, sticky="news", padx=20, pady=10)

        month_label = tk.Label(appt_info_frame, text="Date: ")
        month_label.grid(row=1, column=0)

        self.date_entry = DateEntry(appt_info_frame, width=12, background='darkblue',
                    foreground='white', borderwidth=2)
        self.date_entry.grid(row=1, column=1)

        time_label = tk.Label(appt_info_frame, text="Time: ")
        time_label.grid(row=2, column=0)

        self.time_combo = ttk.Combobox(appt_info_frame, values=[], state="readonly")
        self.time_combo.grid(row=2, column=1)
        self.update_time()

        for widget in appt_info_frame.winfo_children():
            widget.grid_configure(padx=10, pady=5)

        # Save Appointment Button
        button = tk.Button(frame, text="Save", command= self.save)
        button.grid(row=5, column=0, sticky="news", padx=20, pady=10)

    def connect_to_microservice(self, port_number, msg):
        """Handles the process of connecting to a microservice."""
        context = zmq.Context()
        print("Attempting to connect to 'Credentials' server...")
        socket = context.socket(zmq.REQ)
        socket.connect(port_number)

        print("Connection Successful")
        print(f"Sending request to server...")

        socket.send_string(json.dumps(msg))
            
        message = socket.recv()

        print(f"Reply from server: {message}")
        print("Closing Connection...")
        socket.send_string(json.dumps("Quit")) 

        return message

    def update_time(self):
        """Handles the process of providing appointment times."""
        now = datetime.now()
        nine_am = datetime.combine(now, time(9, 0))
        print(now)
        times = [(nine_am + timedelta(minutes=30*i)).strftime("%H:%M") for i in range(16)]
        self.time_combo['values'] = times
                        
    def save(self):
        """Handles the process of updating the tree view for patients."""
        self.edit_data()
        new_values = (int(self.edit_items[0]), self.first_name_entry.get(), self.last_name_entry.get(),  
                        self.pet_name_entry.get(), self.date_entry.get_date(),
                        self.time_combo.get())
        self.parent.appt_tree.item(self.item, values=new_values)
        self.destroy()

    def edit_data(self):
        """Handles the process of updating the appointment."""
        self.confirm_response = messagebox.askyesno("Edit Appointment", "Edit appointment in the database?")
        if self.confirm_response:
            owner_f_name = self.first_name_entry.get()
            owner_l_name = self.last_name_entry.get()
            pet_name = self.pet_name_entry.get()
            selected_month = self.date_entry.get_date().strftime('%Y-%m-%d')
            selected_time = self.time_combo.get()
            
            edit_entry = [int(self.edit_items[0]) + 1, [int(self.edit_items[0]), owner_f_name, owner_l_name, pet_name, selected_month, selected_time]]
            print(edit_entry)

            # Connect to the appointments microservice
            port_number = "tcp://localhost:5559"
            msg = {'edit' : edit_entry}
            self.connect_to_microservice(port_number, msg)

            messagebox.showinfo("Success", "Appointment Successfully Edited!!!")

if __name__ == "__main__":
    app = App()
    app.mainloop()