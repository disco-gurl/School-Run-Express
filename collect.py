
import tkinter as tk
from tkinter import ttk
from passlib.hash import bcrypt
import json
import base64
from tkinter import messagebox
import re
from datetime import datetime
import smtplib
import pgeocode

def getchildren(): 
    #reads the information of all the children who are being picked up from the json file and returns it

    with open('children.json', 'r') as file:
        json_file = json.load(file)
        children = json_file['children']
    return children

def getparents(): 
    #read the information of all the parents who are picking up children and returns it

    with open('parents.json', 'r') as file:
        json_file = json.load(file)
        parents = json_file['parents']
    return parents

def validpostcode(postcode): 
    #gets the postcode and verifies if it matches the requirements of a standard UK postcode

    code = re.compile('^[A-Z]{1,2}[0-9]{1,2} [0-9][A-Z]{2}$') 
    #set of requirements the code needs to pass
    return code.match(postcode)

def validnames(noofchild, nameofchild): 
    #checks in the names entered matches the number stated

    if ',' in nameofchild: 
        #splits the names entered using comma in a list
        number = nameofchild.split(',')  
        #stored split list

        return len(number) == noofchild. 
        #comparision of if the list matches 
    
    else:
        if noofchild == 1:
            return True
        
        elif noofchild != 1:
            return False

def thankmessage(root, current_frame): 
    #displays thank you message at the end

    homepage = tk.Frame(root)
    current_frame.destroy()
    current_frame = homepage

    sent_label = ttk.Label(current_frame, text="SchoolRun Express", font=("Bell MT", 16), foreground="green")
    sent_label.grid(row=1, column=1, pady=10)

    time_label = ttk.Label(current_frame, text="An email will be sent around 8pm informing you of all the details required for the journey", font=("Bell MT", 14), foreground="green")
    time_label.grid(row=3, column=1, pady=10)

    save_label = ttk.Label(current_frame, text="We hope you continue to use our services and reduce the production of CO2 gases in out atmosphere", font=("Bell MT", 12), foreground="green")
    save_label.grid(row=5, column=1, pady=10)

    thank_label = ttk.Label(current_frame, text="Thank you for using School Run Expreess", font=("Bell MT", 12), foreground="green")
    thank_label.grid(row=7, column=1, pady=10)
  
    current_frame.pack()    

def verify2(root, current_frame, name, address, postcode, nameofchild, noofchild, email): 
    #verification system for all the data entered by the user based on the verification requirements in validation section
    decision = True
    code = validpostcode(postcode)
    names = validnames(noofchild, nameofchild)

    if len(address) < 11:
        decision = False
        messagebox.showerror("Error", "Invalid Address") 
        #shows error box when user enters wrong information
    
    elif '@' not in email or email[-1] != 'm' or email[-2] != 'o' or email[-3] != 'c' or email[-4] != '.':
        decision = False
        messagebox.showerror("Error", "Invalid Email address")
    
    elif isinstance(noofchild, int):
        decision = False
        messagebox.showerror("Error", "Invalid Number of Children")
    
    elif not code:
        decision = False
        messagebox.showerror("Error", "Invalid Postcode")
    
    elif not names: 
        decision = False
        messagebox.showerror("Error", "Invalid Names")
        messagebox.showinfo("Information", "The names must be separated by a comma")
    
    if decision:
        drop(root, current_frame, name, address, postcode, nameofchild, noofchild, email)
    
    elif not decision:
        pickup(root, current_frame, name) 
        #clears page and has user re-enter information

def verify1(root, current_frame, name, address, postcode, seats, email, phonenumber):
    decision = True
    code = validpostcode(postcode)

    if len(address) < 11:
        decision = False
        messagebox.showerror("Error", "Invalid Address")
    
    elif len(phonenumber) > 11 or isinstance(phonenumber, int):
        decision = False
        messagebox.showerror("Error", "Invalid Phone Number")
    
    elif isinstance(seats, int):
        decision = False
        messagebox.showerror("Error", "Invalid Number of Seats")
    
    elif '@' not in email or email[-1] != 'm' or email[-2] != 'o' or email[-3] != 'c' or email[-4] != '.':
        decision = False
        messagebox.showerror("Error", "Invalid Email address")
    
    elif not code:
        decision = False
        messagebox.showerror("Error", "Invalid Postcode")
    
    if decision:
        pick(root, current_frame, name, address, postcode, seats, email, phonenumber)
    
    elif not decision:
        dropoff(root, current_frame, name)

def drop(current_frame, name, address, postcode, nameofchild, noofchildren, email): 
    #collects the information of children being picked up

    with open('children.json', 'r') as file:
        json_file = json.load(file) 
        #reads the current information being stored
        children = json_file['children']

    children.append({'parentname': name, 'address': address, 'postcode': postcode, 'childrennames': nameofchild, 'noofchildren' : noofchildren ,'distancetoparent' : [] , 'email': email}) #add the new information of the parent being registered 

    with open('children.json', 'w') as file:
        json.dump(json_file, file) 
        #writes the new information into the json file
        #stores the information in the form of a dictionary

    current_frame.destroy()  
    thankmessage(root, current_frame) 
    #goes back to the main frame
  

def pick(current_frame, name, address, postcode, seats, email, phonenumber):

    with open('parents.json', 'r') as file:
        json_file = json.load(file)
        parents = json_file['parents']

    parents.append({'name': name, 'address': address, 'postcode': postcode, 'availableseats': seats, 'collecting' : [] , 'email': email, 'phonenumber' : phonenumber})

    with open('parents.json', 'w') as file:
        json.dump(json_file, file)

    current_frame.destroy()  
    thankmessage(root, current_frame)

def pickup(root, current_frame, name): 
    #collects the information of the children being picked up
 
    homepage = tk.Frame(root) 
    #put new frame on the screen
    current_frame.destroy() 
    #removes previous frame
    current_frame = homepage

    comment_label = ttk.Label(current_frame, text="Please enter your details here", font=("Bell MT", 14), foreground="green")
    comment_label.grid(row=0, column=1, pady=10)

    address_label = ttk.Label(current_frame, text= "Specific address:", font=("Arial", 14), foreground="green")
    address_label.grid(row=1, column=0, pady=10, sticky="e")

    address_entry = ttk.Entry(current_frame, font=("Helvetica", 14)) 
    #collects data and stores it into a variable
    address_entry.grid(row=1, column=1, pady=5, sticky="w")

    postcode_label = ttk.Label(current_frame, text="Postcode: ", font=("Arial", 14), foreground="green")
    postcode_label.grid(row=2, column=0, pady=10, sticky="e")

    postcode_entry = ttk.Entry(current_frame, font=("Helvetica", 14))
    postcode_entry.grid(row=2, column=1, pady=5, sticky="w")

    noofchild_label = ttk.Label(current_frame, text="Number of children to be picked up: ", font=("Arial", 14), foreground="green")
    noofchild_label.grid(row=3, column=0, pady=10, sticky="e")

    noofchild_entry = ttk.Entry(current_frame, font=("Helvetica", 14))
    noofchild_entry.grid(row=3, column=1, pady=5, sticky="w")

    nameofchild_label = ttk.Label(current_frame, text="Children's Names:", font=("Arial", 14), foreground="green")
    nameofchild_label.grid(row=4, column=0, pady=10, sticky="e")

    nameofchild_entry = ttk.Entry(current_frame, font=("Helvetica", 14))
    nameofchild_entry.grid(row=4, column=1, pady=5, sticky="w")
    
    email_label = ttk.Label(current_frame, text="Email:", font=("Arial", 14), foreground="green")
    email_label.grid(row=5, column=0, pady=10, sticky="e")

    email_entry = ttk.Entry(current_frame, font=("Helvetica", 14))
    email_entry.grid(row=5, column=1, pady=5, sticky="w")
    
    enter_button = ttk.Button(current_frame, text="Enter", command=lambda:verify2(root, current_frame, name, address_entry.get(), postcode_entry.get(), nameofchild_entry.get(), noofchild_entry.get(), email_entry.get())) 
    #passes the data gotten to the drop function when the enter butten it clicked
    #goes to the drop function when clicked
    enter_button.grid(row=7, column=2, pady=10)

    back_button = ttk.Button(current_frame, text="Back", command=lambda: options(root, current_frame, name))  
    back_button.grid(row=7, column=1, pady=10)

    current_frame.pack() 
    #keeps the current frame running on the screen

def dropoff(root, current_frame, name):
  
    homepage = tk.Frame(root)
    current_frame.destroy()
    current_frame = homepage

    comment_label = ttk.Label(current_frame, text="Please enter your details here", font=("Bell MT", 14), foreground="green")
    comment_label.grid(row=0, column=1, pady=10)

    address_label = ttk.Label(current_frame, text= "Specific address:", font=("Arial", 14), foreground="green")
    address_label.grid(row=1, column=0, pady=10, sticky="e")

    address_entry = ttk.Entry(current_frame, font=("Helvetica", 14))
    address_entry.grid(row=1, column=1, pady=5, sticky="w")

    postcode_label = ttk.Label(current_frame, text="Postcode: ", font=("Arial", 14), foreground="green")
    postcode_label.grid(row=2, column=0, pady=10, sticky="e")

    postcode_entry = ttk.Entry(current_frame, font=("Helvetica", 14))
    postcode_entry.grid(row=2, column=1, pady=5, sticky="w")

    availableseats_label = ttk.Label(current_frame, text="Number of available seats minus your child : ", font=("Arial", 14), foreground="green")
    availableseats_label.grid(row=3, column=0, pady=10, sticky="e")

    availableseats_entry = ttk.Entry(current_frame, font=("Helvetica", 14))
    availableseats_entry.grid(row=3, column=1, pady=5, sticky="w")

    email_label = ttk.Label(current_frame, text="Email:", font=("Arial", 14), foreground="green")
    email_label.grid(row=4, column=0, pady=10, sticky="e")

    email_entry = ttk.Entry(current_frame, font=("Helvetica", 14))
    email_entry.grid(row=4, column=1, pady=5, sticky="w")

    number_label = ttk.Label(current_frame, text="Phone number:", font=("Arial", 14), foreground="green")
    number_label.grid(row=5, column=0, pady=10, sticky="e")

    number_entry = ttk.Entry(current_frame, font=("Helvetica", 14))
    number_entry.grid(row=5, column=1, pady=5, sticky="w")

    enter_button = ttk.Button(current_frame, text="Enter", command=lambda:verify1(root, current_frame, name, address_entry.get(), postcode_entry.get(), availableseats_entry.get(), email_entry.get(), number_entry.get()))
    enter_button.grid(row=7, column=2, pady=10)

    back_button = ttk.Button(current_frame, text="Back", command=lambda: options(root, current_frame, name))
    back_button.grid(row=7, column=1, pady=10)

    current_frame.pack()

def options(root, current_frame, name):
    homepage = tk.Frame(root)
    current_frame.destroy()
    current_frame = homepage

    display_label = ttk.Label(current_frame, text="Please select one of the 2 options", font=("Bell MT", 14), foreground="green")
    display_label.grid(row=0, column=1, pady=10)

    pickup_button = ttk.Button(current_frame, text="Want child to be picked", command=lambda:pickup(root, current_frame, name))
    pickup_button.grid(row=1, column=1, pady=10)

    dropoff_button = ttk.Button(current_frame, text="Can pick up children", command=lambda: dropoff(root, current_frame, name))
    dropoff_button.grid(row=2, column=1, pady=10)

    current_frame.pack()

def log(root, current_frame, name, password): 
    #verifies the login
    decrypt = base64.b64encode(password.encode('utf-8')) 
    #encodes the gotten password
    collectedpassword = ""

    with open('users.json', 'r') as file:
        json_data = json.load(file)
        users = json_data['users']

        for user in users: 
            #checks if the user is in the database
            if user['name'] == name:
            collectedpassword = user['password'] 
            #gets the stored encrypted password
    
    
    if bcrypt.verify(decrypt, collectedpassword): 
        #compares the stored password to the encoded password
        options(root, current_frame, name)
  
    else:
        messagebox.showerror("Error", "Incorrect name or password")
        login(root,current_frame) 
        #if either name or password is wrong, clears the page and has the user enter the information again

def regi(current_frame, name, password): 
    #registers users
    encode = base64.b64encode(password.encode('utf-8')) 
    #encodes the password into its ASCII format

    encrypt = bcrypt.hash(encode) 
    #encrypt the password using passlib brycrpt

    with open('users.json', 'r') as file:
        json_file = json.load(file)
        users = json_file['users']
  
    users.append({'name': name, 'password': encrypt})

    with open('users.json', 'w') as file:
        json.dump(json_file, file)
  
    current_frame.destroy()  
    main(current_frame)
    

def register(root, current_frame):
    homepage = tk.Frame(root)
    current_frame.destroy()
    current_frame = homepage

    register_label = ttk.Label(current_frame, text="Register", font=("Bell MT", 14), foreground="green")
    register_label.grid(row=0, column=1, pady=10)
  
    username_label = ttk.Label(current_frame, text="Name:", font=("Arial", 14), foreground="green")
    username_label.grid(row=1, column=0, pady=10, sticky="e")

    username_entry = ttk.Entry(current_frame, font=("Helvetica", 14))
    username_entry.grid(row=1 column=1, pady=5, sticky="w")

    password_label = ttk.Label(current_frame, text="Password:", font=("Arial", 14), foreground="green")
    password_label.grid(row=2, column=0, pady=10, sticky="e")

    password_entry = ttk.Entry(current_frame, font=("Helvetica", 14))
    password_entry.grid(row=2, column=1, pady=10, sticky="w")

    register_button = ttk.Button(current_frame, text="Register", command=lambda: regi(current_frame, username_entry.get(), password_entry.get()))
    register_button.grid(row=4, column=2, pady=10)

    back_button = ttk.Button(current_frame, text="Back", command=lambda: main(current_frame))
    back_button.grid(row=4, column=1, pady=10)

    current_frame.pack()

def login(root, current_frame):
    homepage = tk.Frame(root)
    current_frame.destroy()
    current_frame = homepage

    login_label = ttk.Label(current_frame, text="Login", font=("Bell MT", 14), foreground="green")
    login_label.grid(row=0, column=1, pady=10)
    
    name_label = ttk.Label(current_frame, text="Name:", font=("Bell MT", 14), foreground="green")
    name_label.grid(row=1, column=0, pady=10, sticky="e")
    
    name_entry = ttk.Entry(current_frame, font=("Helvetica", 14))
    name_entry.grid(row=1, column=1, pady=5, sticky="w")

    password_label = ttk.Label(current_frame, text="Password:", font=("Arial", 14), foreground="green")
    password_label.grid(row=2, column=0, pady=10, sticky="e")
    
    password_entry = ttk.Entry(current_frame, show="*", font=("Helvetica", 14))
    password_entry.grid(row=2, column=1, pady=10, sticky="w")

    login_button = ttk.Button(current_frame, text="Login", command=lambda: log(root, current_frame, name_entry.get(), password_entry.get()))
    login_button.grid(row=4, column=2, pady=10)

    back_button = ttk.Button(current_frame, text="Back", command=lambda: main(current_frame))
    back_button.grid(row=4, column=1, pady=10)

    current_frame.pack()

def main(current_frame):
    global root

    root = tk.Tk() 
    #opens a window
    root.geometry("1000x500") 
    #sets the width and height the window will have
    root.title("School Run Express") 
    #set a title page for all windows

    home_page_frame = tk.Frame(root)
    current_frame = home_page_frame

    name_label = ttk.Label(home_page_frame, text="School Run Express", font=("Bell MT", 16), foreground="green")
    name_label.grid(row=1, column=1, pady=10)

    login_button = ttk.Button(home_page_frame, text="Login", command=lambda : login(root, current_frame))
    login_button.grid(row=4, column=1, pady=10)

    register_button = ttk.Button(home_page_frame, text="Register", command=lambda : register(root, current_frame))
    register_button.grid(row=4, column=2, pady=10)

    home_page_frame.pack()

    root.mainloop()
