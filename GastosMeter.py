import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
import psycopg2

# Initialize global variables

email_entry = None
password_entry = None
password_icon_button = None
signup_password_entry = None
signup_confirm_password_entry = None
signup_password_icon_button = None
signup_confirm_password_icon_button = None

# Flag to track the current state of the password visibility
password_visible = False
signup_password_visible = False
signup_confirm_password_visible = False


# Function to connect to the PostgreSQL database
def connect_to_db():
    try:
        # Replace with your actual credentials
        conn = psycopg2.connect(
            dbname="finance_track",
            user="postgres",  # your PostgreSQL username
            password="rednaxela",  # your PostgreSQL password
            host="localhost",  # or your database server IP
            port="5432"  # default PostgreSQL port
        )
        return conn
    except Exception as e:
        print("Database connection failed:", e)
        return None


# Function to toggle password
def toggle_password():
    global password_visible
    if password_visible:
        password_entry.configure(show="•")  # Hide password
        password_icon_button.configure(image=eye_slash_icon_tk)  # Change icon to eye-slash
    else:
        password_entry.configure(show="")  # Show password
        password_icon_button.configure(image=eye_icon_tk)  # Change icon to eye

    password_visible = not password_visible


def center_window(window, width, height):
    # Get the screen dimensions
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calculate the position to center the window
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    # Set the window geometry
    window.geometry(f'{width}x{height}+{x}+{y}')


def register_user(name, email,password):
    conn = connect_to_db()  # Make sure the connection is established
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO users (name, email, password)
                VALUES (%s, %s, %s)
            """, (name, email, password))
            conn.commit()
            cur.close()
            messagebox.showinfo("Success", "Registration successful!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            conn.close()


def toggle_signup_password(field_type):
    global signup_password_visible, signup_confirm_password_visible
    global signup_password_entry, signup_confirm_password_entry
    global signup_password_icon_button, signup_confirm_password_icon_button

    if field_type == "password":
        if signup_password_visible:
            signup_password_entry.configure(show="•")
            signup_password_icon_button.configure(image=eye_slash_icon_tk)
        else:
            signup_password_entry.configure(show="")
            signup_password_icon_button.configure(image=eye_icon_tk)
        signup_password_visible = not signup_password_visible
    else:  # confirm password
        if signup_confirm_password_visible:
            signup_confirm_password_entry.configure(show="•")
            signup_confirm_password_icon_button.configure(image=eye_slash_icon_tk)
        else:
            signup_confirm_password_entry.configure(show="")
            signup_confirm_password_icon_button.configure(image=eye_icon_tk)
        signup_confirm_password_visible = not signup_confirm_password_visible


def show_sign_up_page():
    global signup_password_entry, signup_confirm_password_entry
    global signup_password_icon_button, signup_confirm_password_icon_button
    global email_entry

    # clear existing widgets
    for widget in root.winfo_children():
        widget.destroy()

    title = ctk.CTkLabel(root, text="Sign Up", fg_color="transparent", text_color="#d0637c", font=("Arial", 40, "bold"))
    title.place(relx=0.5, rely=0.15, anchor="center")

    # Name entry field
    name_entry = ctk.CTkEntry(root, placeholder_text="Full Name")
    name_entry.place(relx=0.5, rely=0.3, anchor="center")

    # Email entry field
    email_entry = ctk.CTkEntry(root, placeholder_text="Email")
    email_entry.place(relx=0.5, rely=0.37, anchor="center")

    # Password entry field with eye icon
    signup_password_entry = ctk.CTkEntry(root, placeholder_text="Password", show="•")
    signup_password_entry.place(relx=0.5, rely=0.51, anchor="center")

    signup_password_icon_button = ctk.CTkButton(
        root,
        image=eye_slash_icon_tk,
        fg_color="transparent",
        command=lambda: toggle_signup_password("password"),
        width=30,
        height=30,
        hover_color="#e0e0e0"
    )
    signup_password_icon_button.place(relx=0.65, rely=0.51, anchor="center")

    # Confirm Password entry field with eye icon
    signup_confirm_password_entry = ctk.CTkEntry(root, placeholder_text="Confirm Password", show="•")
    signup_confirm_password_entry.place(relx=0.5, rely=0.58, anchor="center")

    signup_confirm_password_icon_button = ctk.CTkButton(
        root,
        image=eye_slash_icon_tk,
        fg_color="transparent",
        command=lambda: toggle_signup_password("confirm"),
        width=30,
        height=30,
        hover_color="#e0e0e0"
    )
    signup_confirm_password_icon_button.place(relx=0.65, rely=0.58, anchor="center")

    # Error label
    error_label = ctk.CTkLabel(root, text="", text_color="red")
    error_label.place(relx=0.5, rely=0.66, anchor="center")

    # Function for when the user clicks sign up
    def on_sign_up():
        name = name_entry.get()
        email = email_entry.get()
        password = signup_password_entry.get()
        confirm_password = signup_confirm_password_entry.get()

        if password != confirm_password:
            error_label.configure(text="Passwords do not match!")
        elif not all([name, email, password, confirm_password]):
            error_label.configure(text="Please fill out all fields.")
        else:
            error_label.configure(text="")  # clear error
            register_user(name, email, password)
            show_login_page()  # Redirect to login page after registration

    # Sign Up button
    sign_up_button = ctk.CTkButton(root, text="Sign Up", command=on_sign_up)
    sign_up_button.place(relx=0.5, rely=0.73, anchor="center")


def login():
    email = email_entry.get()
    password = password_entry.get()

    if not email or not password:
        messagebox.showerror("Error", "Please enter both username and password.")
        return

    # Connect to the database
    conn = connect_to_db()
    if not conn:
        messagebox.showerror("Error", "Failed to connect to the database.")
        return

    # Query the database for user credentials (username and password)
    cur = conn.cursor()
    cur.execute("SELECT email, password, name FROM users WHERE email = %s AND password = %s",
                (email, password))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if user:
        name = user[2]  # `name` is the 3rd column in the result (index 2)
        messagebox.showinfo("Success", f"Login successful! Welcome, {name}!")

    else:
        messagebox.showerror("Error", "Invalid username or password. Please try again.")


# Function to show the login page
def show_login_page():
    global email_entry, password_entry, password_icon_button

    # Clear the current window before the new window
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Gastos Meter - Login")
    root.configure(bg="#FF7AA2")

    label_frame = ctk.CTkFrame(root, fg_color="transparent")
    label_frame.place(relx=0.5, rely=0.5, anchor="center")

    title = ctk.CTkLabel(root, text="GASTOS", fg_color="transparent", text_color="#d0637c", font=("Arial", 40, "bold"))
    title.place(relx=0.5, rely=0.15, anchor="center")

    title_meter = ctk.CTkLabel(root, text="Meter", fg_color="transparent", text_color="#dd868c", font=("Arial", 35))
    title_meter.place(relx=0.5, rely=0.22, anchor="center")

    # Username entry field
    email_entry = ctk.CTkEntry(label_frame, placeholder_text="Email")
    email_entry.grid(row=1, column=0, columnspan=2, padx=5, pady=10)

    # Password entry field
    password_entry = ctk.CTkEntry(label_frame, placeholder_text="Password", show="•")
    password_entry.grid(row=2, column=0, columnspan=2, padx=5, pady=10)

    # Add the show/hide password button (eye icon) with proper alignment inside the password field
    password_icon_button = ctk.CTkButton(label_frame, image=eye_slash_icon_tk, fg_color="transparent",
                                         command=toggle_password, width=30, height=30, hover_color="#e0e0e0")
    password_icon_button.place(relx=1.1, rely=0.3, anchor="center")  # Align the icon inside the entry field

    # Login button
    login_button = ctk.CTkButton(label_frame, text='Log In', fg_color="#E899A2", text_color="black",
                                 font=("Arial", 12, "bold"), hover_color="#E6B2BA", command=login)
    login_button.grid(row=3, column=0, columnspan=1, pady=10)

    # Add a Sign Up button
    sign_up_button = ctk.CTkButton(label_frame, text='Sign Up', fg_color="#E899A2", text_color="black",
                                   font=("Arial", 12, "bold"), hover_color="#E6B2BA", command=show_sign_up_page)
    sign_up_button.grid(row=4, column=0, columnspan=2, pady=10)

    forgot_password_button = ctk.CTkButton(label_frame, text="Forgot Password?", fg_color="transparent",
                                           text_color="black", font=("Arial", 12, "italic"),
                                           command=show_forgot_password_page)
    forgot_password_button.grid(row=5, column=0, columnspan=2, pady=10)


def show_forgot_password_page():
    # Clear the current window
    global email_entry
    for widget in root.winfo_children():
        widget.destroy()

    title = ctk.CTkLabel(root, text="Forgot Password", fg_color="transparent", text_color="#d0637c",
                         font=("Arial", 40, "bold"))
    title.place(relx=0.5, rely=0.15, anchor="center")

    # Email or Username entry field
    email_entry = ctk.CTkEntry(root, placeholder_text="Enter your email/username")
    email_entry.place(relx=0.5, rely=0.3, anchor="center")

    # Submit button for reset
    submit_button = ctk.CTkButton(root, text="Submit", fg_color="#E899A2", text_color="black",
                                  font=("Arial", 12, "bold"), hover_color="#E6B2BA",
                                  command=lambda: reset_password(email_entry.get()))
    submit_button.place(relx=0.5, rely=0.4, anchor="center")

    # Back to login button
    back_button = ctk.CTkButton(root, text="Back to Login", fg_color="#E899A2", text_color="black",
                                font=("Arial", 12, "bold"), hover_color="#E6B2BA", command=show_login_page)
    back_button.place(relx=0.5, rely=0.5, anchor="center")


def reset_password(email_or_username):
    if not email_or_username:
        messagebox.showerror("Error", "Please enter your email or username.")
        return

    # Here you can implement logic to send a reset email or generate a temporary password
    # For now, we'll just show a success message.
    messagebox.showinfo("Success", f"Password reset instructions have been sent to {email_or_username}.")
    show_login_page()  # After reset, go back to the login page


ctk.set_appearance_mode("light")  # we used customtkinter for the theme of our software.
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.geometry("600x625")
center_window(root, 600, 625)
root.configure(bg="#e1b5b5")
root.resizable(False, False)

eye_icon = Image.open("assets/eye.png")
eye_slash_icon = Image.open("assets/eye-slash.png")

# Resize images to fit the button
eye_icon = eye_icon.resize((20, 20))
eye_slash_icon = eye_slash_icon.resize((20, 20))

# Convert images to a format Tkinter can use
eye_icon_tk = ImageTk.PhotoImage(eye_icon)
eye_slash_icon_tk = ImageTk.PhotoImage(eye_slash_icon)

show_login_page()

root.mainloop()
# still fixing captcha window(should be centered)
# signup capthca prblem
# add sjow/hide pass
