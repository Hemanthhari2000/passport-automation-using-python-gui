# Import all from tkinter
from tkinter import *
# Import messagebox from tkinter
from tkinter import messagebox
# Import "ttk" from tkinter
from tkinter import ttk
# Import sqlite3
import sqlite3

# =========================== FOR BETTER UNDERSTANDING READ THE CODE FROM MAIN FUNCTION =========================

# Shows the detail page.


def details_page():
    top = Toplevel()
    top.title('Details')
    top.geometry("600x300")

    try:
        conn = sqlite3.connect('db.sql')
        c = conn.cursor()
        c.execute("select * from registration where name = (?)",
                  (login_name.get(),))
        val = c.fetchone()
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        conn.close()

    label_name = Label(top, text="Name", font=('bold', 13))
    label_name.place(relx=0.2, rely=0.2)

    fetch_name = Label(top, text=f"{val[1]}", font=('bold', 13))
    fetch_name.place(relx=0.2, rely=0.3)

    label_age = Label(top, text="Age", font=('bold', 13))
    label_age.place(relx=0.5, rely=0.2)

    fetch_age = Label(top, text=f"{val[2]}", font=('bolf', 13))
    fetch_age.place(relx=0.5, rely=0.3)

# You can add another window from here.


def admin():
    messagebox.showinfo("ADMIN", "ADD ADMIN PAGE")

# Gets the "radio" value and returns a string.


def selection():
    gender = ""
    selected = int(radio.get())
    if selected == 1:
        gender = "male"
    elif selected == 2:
        gender = "female"
    else:
        gender = "others"
    return gender

# Login Window


def login():
    try:
        conn = sqlite3.connect('db.sql')
        c = conn.cursor()
        c.execute("select * from registration where name = (?)",
                  (login_name.get(),))
        val = c.fetchone()
        if login_name.get() == val[1]:
            messagebox.showinfo("Success", "User Logged Successfully")
        conn.commit()
        details_page()
    except Exception as e:
        print(e)
    finally:
        conn.close()

# If User is already Registered.


def existing_user():
    top = Toplevel()
    top.title('Login')
    top.geometry("600x300")

    head = Label(top,
                 text='LOGIN',
                 font=('bold', 15))
    head.place(relx=0.5, rely=0.2, anchor=CENTER)

    b_name = Label(top,
                   text='NAME',
                   font=('bold', 15))
    # anchor=W indicates WEST Direction.
    b_name.place(relx=0.1, rely=0.4, anchor=W)

    global login_name
    login_name = Entry(top)
    # anchor=E indicates EAST Direction.
    login_name.place(relx=0.9, rely=0.4, anchor=E)
    login_name.config(width=30)

    b_auth = Label(top,
                   text='PASSWORD',
                   font=('bold', 15))
    b_auth.place(relx=0.1, rely=0.6, anchor=W)

    global login_password
    login_password = Entry(top, show="*")
    login_password.place(relx=0.9, rely=0.6, anchor=E)
    login_password.config(width=30)

    bname = Button(top,
                   text="SUBMIT",
                   font=("bold", 10), bg="white",
                   command=login)   # Triggers the "login" function.
    bname.place(relx=0.2, rely=0.8, anchor=W)
    bname.config(height=1, width=10)

    bauth = Button(top,
                   text="CANCEL",
                   font=("bold", 10), bg="white",
                   command=top.destroy)  # Window is destroyed.
    bauth.place(relx=0.8, rely=0.8, anchor=E)
    bauth.config(height=1, width=10)

# ========================== DATABASE (GET) ==================== #


def get_from_db():
    try:
        conn = sqlite3.connect('db.sql')
        c = conn.cursor()
        c.execute('select * from registration')
        data = c.fetchall()
        if data == []:
            detail_view
        # for i in data:
        #     print(i)
        return data
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        conn.close()

# =============================xxxx=========================== #


def payment():
    pass


def del_db():
    try:
        conn = sqlite3.connect('db.sql')
        c = conn.cursor()
        c.execute('delete from registration')
        conn.commit()
    except Exception as e:
        print(e)
    finally:
        conn.close()

# Detail View


def detail_view():
    top = Toplevel()
    top.title('Detail View')
    top.geometry('800x400')

    # Get the Data from the database.
    data = get_from_db()
    # print(data)

    # Used to display the data's into a table Format.
    tv = ttk.Treeview(top)

    # create a column
    tv['columns'] = ("NAME", "AGE", "DoB", "PoB", "GENDER",
                     "FATHER'S NAME", "MOTHER'S NAME", "ADDRESS")

    # Add the column
    tv.column("#0", width=0)  # --> This is a default empty column
    tv.column("NAME", anchor=W)
    tv.column("AGE", anchor=W)
    tv.column("DoB", anchor=W)
    tv.column("PoB", anchor=W)
    tv.column("GENDER", anchor=W)
    tv.column("FATHER'S NAME", anchor=W)
    tv.column("MOTHER'S NAME", anchor=W)
    tv.column("ADDRESS", anchor=W)

    # Add the Headings
    tv.heading("#0")  # --> Again this is a default column
    tv.heading("NAME", text="NAME", anchor=W)
    tv.heading("AGE", text='AGE', anchor=W)
    tv.heading("DoB", text='DoB', anchor=W)
    tv.heading("PoB", text='PoB', anchor=W)
    tv.heading("FATHER'S NAME", text="FATHER'S NAME", anchor=W)
    tv.heading("MOTHER'S NAME", text="MOTHER'S NAME", anchor=W)
    tv.heading("ADDRESS", text='ADDRESS', anchor=W)

    # It makes the "data" list as a iterator like ((0, [1,2,3,4]), (1, [5,6,7,8]))
    for i, row in enumerate(data):
        tv.insert(parent='', index='end', iid=i, values=(
            row[1], row[2], row[3], row[4], row[5], row[6], row[7]))

    # we pack all the widgets to the Table
    tv.pack()

    paymentBtn = Button(top,
                        text="PAYMENT", font=("bold", 10), bg="white",
                        command=payment)
    paymentBtn.place(x=200, y=300)
    exitBtn = Button(top, text="RESET", font=(
        "bold", 10), bg="white", command=del_db)
    exitBtn.place(x=400, y=300)


# ============================ DATABASE (ADD/INSERT) ============================== #

# --> This function adds the data to the database.

def add_to_db():
    # we "try" to connect to the database.
    try:
        # creating "conn" variable and connecting with the "db.sql"
        conn = sqlite3.connect('db.sql')
        # creating a "cursor()" which allows us to execute SQL commands through PYTHON Interface
        c = conn.cursor()
        # Thus, using "c = conn.cursor() we execute SQL commands"
        c.execute(
            # The "?" allows us to pass the value from python interface to sqlite3 database.
            "insert into registration (name, age, dob, pob, gender, fathername, mothername, address) values (?,?,?,?,?,?,?,?)", (
                nameField.get(),
                int(ageField.get()),
                dobField.get(),
                pobField.get(),
                selection(),
                fatherField.get(),
                motherField.get(),
                addrField.get(),
            ))
        # c.execute("select * from registration")

        # commit to the database.
        conn.commit()
        # show message if successful
        messagebox.showinfo(
            "Success", "Registration Complete"
        )
    # If the "try" was not successful then this executes.
    except Exception as e:
        # prints the error message.
        print(f"Error Has Occured Not able to connect to the Database :(\n{e}")
    # After completion of "try" or "except" we need to close the connection.
    finally:
        conn.close()


def check_fields():
    if nameField.get() == "":
        messagebox.showerror("Failed", "All Fields are Mandatory")
    else:
        return


def register():
    check_fields()
    add_to_db()

# Button "bname" triggers this Function "new_user"


def new_user():
    # Instantiates a child window and assigns to the variable "top".
    top = Toplevel()
    # This specifys the title of the child window using the object "top".
    top.title('Registration')
    # This specifys the dimensions of the child window using the object "top".
    top.geometry("500x500")
    # This Global Variable is used such that all the functions can access this variable.
    global radio
    # Set this variable to "IntVar()" datatype.
    radio = IntVar()
    # Creates a Frame or a container type to hold the widgets (like "div" used in HTML)
    frame1 = Frame(top, bg='white')
    # Specifys the position and the width, Height of the Frame.
    frame1.place(relx=0, rely=0, width=500, height=500)
    # We are creating a Label widget to display text and assigning to the variable "registerTitle".

    # --> We specify "frame1" to position the widget in the "frame1" Frame.
    registerTitle = Label(frame1,
                          # Specifys the text to de displayed in the Label "registerTitle".
                          text="REGISTRATION",
                          # Specifys the font, text size, background and font color.
                          font=("bold", 15), bg="white", fg="black")
    # It anchors the widget "id" to the CENTER and Specifys the position of label relative to the x and y axis.
    registerTitle.place(relx=0.5, rely=0.03, anchor=CENTER)

    # --> Name Label and Field

    # This Global Variable is used such that all the functions can access this variable.
    global nameField
    nameLabel = Label(frame1,
                      text="Name:",
                      font=("Helvetica", 13), bg="white", fg="gray")
    nameLabel.place(x=20, y=70)
    nameField = Entry(frame1, font=("Helvetica", 13), bg="white")
    nameField.place(x=150, y=70, width=250)

    # --> Age Label and Age Field
    global ageField
    ageLabel = Label(frame1,
                     text="Age:",
                     font=("Helvetica", 13), bg="white", fg="gray")
    ageLabel.place(x=20, y=110)

    ageField = Entry(frame1,
                     font=("Helvetica", 13), bg='white')
    ageField.place(x=150, y=110, width=250)

    # --> DoB Label and Field
    global dobField
    dobLabel = Label(frame1,
                     text="Date of Birth:",
                     font=("Helvetica", 13), bg="white", fg="gray")
    dobLabel.place(x=20, y=150)

    dobField = Entry(frame1,
                     font=("Helvetica", 13), bg='white')
    dobField.place(x=150, y=150, width=250)

    # --> PoB Label and Field
    global pobField
    pobLabel = Label(frame1,
                     text="Place of Birth:",
                     font=("Helvetica", 13), bg="white", fg="gray")
    pobLabel.place(x=20, y=190)

    pobField = Entry(frame1,
                     font=("Helvetica", 13), bg='white')
    pobField.place(x=150, y=190, width=250)

    # --> Gender Label and Field
    genderLabel = Label(frame1,
                        text="Gender:",
                        font=("Helvetica", 13), bg="white", fg="gray").place(x=20, y=230)

    maleField = Radiobutton(frame1,
                            text="Male",
                            variable=radio,
                            value=1,
                            command=selection,
                            bg='white').place(x=150, y=230)

    femaleField = Radiobutton(frame1,
                              text="Female",
                              variable=radio,
                              value=2,
                              command=selection,
                              bg='white').place(x=220, y=230)

    otherField = Radiobutton(frame1,
                             text="Others",
                             variable=radio,
                             value=3,
                             command=selection,
                             bg='white').place(x=290, y=230)

    # --> Father's name Label and Field
    global fatherField
    fatherLabel = Label(frame1,
                        text="Father's Name:",
                        font=("Helvetica", 13), bg="white", fg="gray").place(x=20, y=270)
    fatherField = Entry(frame1,
                        font=("Helvetica", 13), bg='white')
    fatherField.place(x=150, y=270, width=250)

    # --> mother's name Label and Field
    global motherField
    motherLabel = Label(frame1,
                        text="Mother's Name:", font=("Helvetica", 13), bg="white", fg="gray").place(x=20, y=310)

    motherField = Entry(frame1,
                        font=("Helvetica", 13), bg='white')
    motherField.place(x=150, y=310, width=250)

    # --> address Label and Age Field
    global addrField
    addrLabel = Label(frame1,
                      text="Address:", font=("Helvetica", 13), bg="white", fg="gray").place(x=20, y=350)

    addrField = Entry(frame1,
                      font=("Helvetica", 13), bg='white')
    addrField.place(x=150, y=350, width=250)

    # T&C
    tandc = Checkbutton(frame1,
                        text="I Agree to the Terms & Conditions", bg='white', font=("Times", 12),
                        onvalue=1,
                        offvalue=0).place(x=20, y=390)

    # Register
    registerBtn = Button(frame1,
                         text='Register',
                         font=('Helvetica', 13), padx=15, pady=5,
                         # This just changes the mouse pointer to a hand icon.
                         cursor="hand2",
                         # It Triggers the function "register" on click.
                         command=register
                         ).place(x=20, y=430)

    cancelBtn = Button(frame1,
                       text='Cancel',
                       font=('Helvetica', 13), padx=15, pady=5,
                       cursor="hand2",
                       # It simply destroys the window (or) closes it.
                       command=top.destroy
                       ).place(x=200, y=430)


# Button "a" triggers this Function "continue_window"
def continue_window():
    # Instantiates a child window and assigns to the variable "top".
    top = Toplevel()
    # This specifys the title of the child window using the object "top".
    top.title('Passport Automation')
    # This specifys the dimensions of the child window using the object "top".
    top.geometry("600x300")
    # We are creating a Label widget to display text and assigning to the variable "head".

    # --> We specify "top" to position the widget in the "top" window.
    head = Label(top,
                 # Specifys the text to de displayed in the Label "head".
                 text='USER AUTH',
                 font=('bold', 15))     # Specifys the font and the text size.
    # It anchors the widget "id" to the CENTER and Specifys the position of label relative to the x and y axis.
    head.place(relx=0.5, rely=0.2, anchor=CENTER)
    # Creates a Button Widget and Assigns it to a variable "bname"

    # --> We specify "top" to position the widget in the "top" window
    bname = Button(top,
                   # Specifys the text to de displayed in the Button.
                   text="NEW USER",
                   # Specifys the font and the text size.
                   font=("bold", 10), bg="white",
                   # Triggers the function "new_user" on button click.
                   command=new_user,
                   # Adds some Padding to x (padx) and y (pady) directions.
                   padx=15, pady=10)
    # Specifys the position of Button relative to the x and y axis.
    bname.place(relx=0.1, rely=0.4,)
    # Specifys the dimension of the button "bname"
    bname.config(height=1, width=10)

    # Creates a Button Widget and Assigns it to a variable "bauth"

    # --> We specify "top" to position the widget in the "top" window
    bauth = Button(top,
                   # Specifys the text to de displayed in the Button.
                   text="EXISTING USER",
                   # Specifys the font and the text size.
                   font=("bold", 10), bg="white",
                   # Triggers the function "existing_user" on button click
                   command=existing_user,
                   # Adds some Padding to x (padx) and y (pady) directions.
                   padx=15, pady=10)
    # Specifys the position of Button relative to the x and y axis.
    bauth.place(relx=0.4, rely=0.4)
    # Specifys the dimension of the button "bauth"
    bauth.config(height=1, width=10)

    # Creates a Button Widget and Assigns it to a variable "adminBtn"

    # --> We specify "top" to position the widget in the "top" window
    adminBtn = Button(top,
                      # Specifys the text to de displayed in the Button.
                      text="VIEW",
                      # Specifys the font and the text size.
                      font=("bold", 10), bg="white",
                      # Triggers the function "detail_view" on button click
                      command=detail_view,
                      # Adds some Padding to x (padx) and y (pady) directions.
                      padx=15, pady=10)
    # Specifys the position of Button relative to the x and y axis.
    adminBtn.place(relx=0.7, rely=0.4)


# =============================== Main ================================= #

# --> MAIN PROGRAM STARTS HERE.
def main():
    # This instantiates an object of Tk() class to create the base window.
    root = Tk()
    # This specifys the dimensions of theh base window using the object root.
    root.geometry("600x300")
    # This specifys the title of the base window using the object root.
    root.title("PASSPORT AUTOMATION")

    # We are creating a Label widget to display text and assigning to the variable "id".

    # --> We specify "root" to position the widget in the "root" window
    id = Label(root,
               # Specifys the text to de displayed in the Label.
               text='WELCOME TO THE PASSPORT AUTOMATION SYSTEM',
               font=('bold', 15))                                 # Specifys the font and the text size.
    # It anchors the widget "id" to the CENTER and Specifys the position of label relative to the x and y axis.
    id.place(relx=0.5, rely=0.2, anchor=CENTER)

    # Creates a Button Widget and Assigns it to a variable "a"

    # --> We specify "root" to position the widget in the "root" window
    a = Button(root,
               # Specifys the text to de displayed in the Button.
               text="DO YOU WANT TO CONTINUE",
               # Specifys the font and the text size.
               font=("bold", 10), bg="white",
               command=continue_window)                           # Triggers the function "continue_window" on button click.
    # It anchors the widget "a" to the CENTER and Specifys the position of Button relative to the x and y axis.
    a.place(relx=0.5, rely=0.4, anchor=CENTER)
    # Specifys the dimension of the button "a"
    a.config(height=1, width=30)

    # Creates a Button Widget and Assigns it to a variable "b"

    # --> We specify "root" to position the widget in the "root" window
    b = Button(root,
               # Specifys the text to de displayed in the Button.
               text="CANCEL",
               # Specifys the font and the text size.
               font=("bold", 10), bg="white",
               # Terminates / Closes the window on click.
               command=root.destroy)

    # It anchors the widget "b" to the CENTER and Specifys the position of Button relative to the x and y axis.
    b.place(relx=0.5, rely=0.6, anchor=CENTER)
    # Specifys the dimension of the button "b"
    b.config(height=1, width=10)

    # Keeps the Window Running.
    mainloop()


if __name__ == '__main__':
    main()
