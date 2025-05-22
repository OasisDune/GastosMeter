import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk
import psycopg2
import random
import smtplib
from email.message import EmailMessage
import bcrypt

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






def send_otp_email(to_email):
    """Generate a 6-digit OTP and send it to the specified email address."""
    otp = ''.join(str(random.randint(0, 9)) for _ in range(6))
    from_mail = 'gabooo0319@gmail.com'
    app_password = 'sbhu wfke ymea gmzy'  # Use your app password

    msg = EmailMessage()
    msg['Subject'] = "OTP Verification"
    msg['From'] = from_mail
    msg['To'] = to_email
    msg.set_content(f"Your OTP is: {otp}")

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_mail, app_password)
        server.send_message(msg)
        server.quit()
        print("Email sent successfully")
        return otp
    except Exception as e:
        print("Failed to send OTP:", e)
        return None






def show_otp_verification_page(user_email, user_name):
    for widget in root.winfo_children():
        widget.destroy()
    otp_label = ctk.CTkLabel(root, text="Enter the OTP sent to your email", text_color="#d0637c", font=("Arial", 20, "bold"))
    otp_label.place(relx=0.5, rely=0.2, anchor="center")
    otp_entry = ctk.CTkEntry(root, placeholder_text="OTP")
    otp_entry.place(relx=0.5, rely=0.3, anchor="center")
    error_label = ctk.CTkLabel(root, text="", text_color="red")
    error_label.place(relx=0.5, rely=0.4, anchor="center")
    def verify_otp():
        entered_otp = otp_entry.get()
        if entered_otp == root.generated_otp:
            messagebox.showinfo("Success", f"Login successful! Welcome, {user_name}!")
            # Proceed to main app page here
        else:
            error_label.configure(text="Invalid OTP. Please try again.")
    verify_button = ctk.CTkButton(root, text="Verify OTP", command=verify_otp)
    verify_button.place(relx=0.5, rely=0.5, anchor="center")






def show_otp_verification_page(user_email, user_name):
    for widget in root.winfo_children():
        widget.destroy()
    otp_label = ctk.CTkLabel(root, text="Enter the OTP sent to your email", text_color="#d0637c", font=("Arial", 20, "bold"))
    otp_label.place(relx=0.5, rely=0.2, anchor="center")
    otp_entry = ctk.CTkEntry(root, placeholder_text="OTP")
    otp_entry.place(relx=0.5, rely=0.3, anchor="center")
    error_label = ctk.CTkLabel(root, text="", text_color="red")
    error_label.place(relx=0.5, rely=0.4, anchor="center")
    def verify_otp():
        entered_otp = otp_entry.get()
        if entered_otp == root.generated_otp:
            # Show the post-login financial setup window
            post_signup = PostSignupWindow()
            post_signup.mainloop()
            # After setup, proceed to your main app/dashboard here
            # e.g., show_dashboard_page(user_name)
        else:
            error_label.configure(text="Invalid OTP. Please try again.")
    verify_button = ctk.CTkButton(root, text="Verify OTP", command=verify_otp)
    verify_button.place(relx=0.5, rely=0.5, anchor="center")






# Function to toggle password
def center_window(window, width, height):
    # Get the screen dimensions
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calculate the position to center the window
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    # Set the window geometry
    window.geometry(f'{width}x{height}+{x}+{y}')








def register_user(name, email, password):
    conn = connect_to_db()
    if conn:
        try:
            cur = conn.cursor()
            # Hash the password before storing
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            cur.execute("""
                INSERT INTO users (name, email, password)
                VALUES (%s, %s, %s)
            """, (name, email, hashed_password.decode('utf-8')))
            conn.commit()
            cur.close()
            messagebox.showinfo("Success", "Registration successful!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            conn.close()







def show_sign_up_page():
    global signup_password_entry, signup_confirm_password_entry
    global signup_password_icon_button, signup_confirm_password_icon_button
    global email_entry

    for widget in root.winfo_children():
        widget.destroy()

    title = ctk.CTkLabel(root, text="Sign Up", fg_color="transparent", text_color="#d0637c", font=("Arial", 40, "bold"))
    title.place(relx=0.5, rely=0.15, anchor="center")

    name_entry = ctk.CTkEntry(root, placeholder_text="Full Name")
    name_entry.place(relx=0.5, rely=0.3, anchor="center")

    email_entry = ctk.CTkEntry(root, placeholder_text="Email")
    email_entry.place(relx=0.5, rely=0.37, anchor="center")

    signup_password_entry = ctk.CTkEntry(root, placeholder_text="Password", show="•")
    signup_password_entry.place(relx=0.5, rely=0.51, anchor="center")

    signup_confirm_password_entry = ctk.CTkEntry(root, placeholder_text="Confirm Password", show="•")
    signup_confirm_password_entry.place(relx=0.5, rely=0.58, anchor="center")

    # Flags for password visibility
    signup_password_visible_flag = [False]
    signup_confirm_password_visible_flag = [False]

    def toggle_signup_password_visibility():
        if signup_password_visible_flag[0]:
            signup_password_entry.configure(show="•")
            signup_password_icon_button.configure(image=eye_slash_icon_tk)
            signup_password_visible_flag[0] = False
        else:
            signup_password_entry.configure(show="")
            signup_password_icon_button.configure(image=eye_icon_tk)
            signup_password_visible_flag[0] = True

    def toggle_signup_confirm_password_visibility():
        if signup_confirm_password_visible_flag[0]:
            signup_confirm_password_entry.configure(show="•")
            signup_confirm_password_icon_button.configure(image=eye_slash_icon_tk)
            signup_confirm_password_visible_flag[0] = False
        else:
            signup_confirm_password_entry.configure(show="")
            signup_confirm_password_icon_button.configure(image=eye_icon_tk)
            signup_confirm_password_visible_flag[0] = True

    signup_password_icon_button = ctk.CTkButton(
        root,
        image=eye_slash_icon_tk,
        fg_color="transparent",
        width=30,
        height=30,
        command=toggle_signup_password_visibility,
        hover_color="#e0e0e0",
        text=""
    )
    signup_password_icon_button.place(relx=0.68, rely=0.51, anchor="center")

    signup_confirm_password_icon_button = ctk.CTkButton(
        root,
        image=eye_slash_icon_tk,
        fg_color="transparent",
        width=30,
        height=30,
        command=toggle_signup_confirm_password_visibility,
        hover_color="#e0e0e0",
        text=""
    )
    signup_confirm_password_icon_button.place(relx=0.68, rely=0.58, anchor="center")

    error_label = ctk.CTkLabel(root, text="", text_color="red")
    error_label.place(relx=0.5, rely=0.66, anchor="center")

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
            error_label.configure(text="")
            otp = send_otp_email(email)
            if otp:
                root.generated_otp = otp
                show_otp_verification_page_signup(email, name, password)
            else:
                error_label.configure(text="Failed to send OTP. Check your email address.")

    sign_up_button = ctk.CTkButton(
        root,
        text="Sign Up",
        fg_color="#E899A2",
        text_color="black",
        font=("Arial", 12, "bold"),
        hover_color="#E6B2BA",
        command=on_sign_up
    )
    sign_up_button.place(relx=0.5, rely=0.73, anchor="center")

    back_to_login = ctk.CTkButton(root, text="Back to Login", fg_color="transparent", text_color="#333",
                                   command=show_login_page)
    back_to_login.place(relx=0.5, rely=0.80, anchor="center")






class PostSignupWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Financial Setup")
        self.geometry("600x500")
        self.configure(bg="#1c2b1b")
        self.envelopes = []
        ctk.CTkLabel(self, text="Welcome! Let's set up your finances.",
                     font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)
        self.balance_entry = ctk.CTkEntry(self, placeholder_text="Enter your current balance")
        self.balance_entry.pack(pady=10, ipady=5, ipadx=5)
        ctk.CTkLabel(self, text="Create Envelopes for Essential Expenses",
                     font=ctk.CTkFont(size=16)).pack(pady=10)
        input_frame = ctk.CTkFrame(self, fg_color="#2e4730")
        input_frame.pack(pady=5, padx=10)
        self.envelope_name = ctk.CTkEntry(input_frame, placeholder_text="Envelope Name (e.g., Water)")
        self.envelope_name.pack(side="left", padx=10, pady=10)
        self.envelope_amount = ctk.CTkEntry(input_frame, placeholder_text="Amount")
        self.envelope_amount.pack(side="left", padx=10, pady=10)
        add_btn = ctk.CTkButton(input_frame, text="Add", command=self.add_envelope)
        add_btn.pack(side="left", padx=10, pady=10)
        self.scroll_frame = ctk.CTkScrollableFrame(self, height=200)
        self.scroll_frame.pack(padx=20, pady=10, fill="both", expand=True)
        self.submit_btn = ctk.CTkButton(self, text="Submit", command=self.submit_data)
        self.submit_btn.pack(pady=20)

    def add_envelope(self):
        name = self.envelope_name.get()
        amount = self.envelope_amount.get()
        if name and amount:
            label = ctk.CTkLabel(self.scroll_frame, text=f"{name}: ₱{amount}", font=("Arial", 14))
            label.pack(anchor="w", padx=10, pady=5)
            self.envelopes.append((name, amount))
            self.envelope_name.delete(0, 'end')
            self.envelope_amount.delete(0, 'end')

    def submit_data(self):
        balance = self.balance_entry.get()
        print("Balance:", balance)
        print("Envelopes:")
        for name, amount in self.envelopes:
            print(f"{name}: ₱{amount}")
        # Add DB save logic here if needed
        self.destroy()
        show_login_page()






def login():
    email = email_entry.get()
    password = password_entry.get()
    if not email or not password:
        messagebox.showerror("Error", "Please enter both username and password.")
        return
    conn = connect_to_db()
    if not conn:
        messagebox.showerror("Error", "Failed to connect to the database.")
        return
    cur = conn.cursor()
    cur.execute("SELECT email, password, name FROM users WHERE email = %s", (email,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    if user and bcrypt.checkpw(password.encode('utf-8'), user[1].encode('utf-8')):
        name = user[2]
        otp = send_otp_email(email)
        if otp:
            root.generated_otp = otp
            show_otp_verification_page(email, name)
        else:
            messagebox.showerror("Error", "Failed to send OTP. Please try again.")
    else:
        messagebox.showerror("Error", "Invalid username or password. Please try again.")





def show_login_page():
    global email_entry, password_entry, password_icon_button

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

    email_entry = ctk.CTkEntry(label_frame, placeholder_text="Email")
    email_entry.grid(row=1, column=0, columnspan=2, padx=5, pady=10)

    password_visible_flag = [False]  # Mutable flag

    password_entry = ctk.CTkEntry(label_frame, placeholder_text="Password", show="•")
    password_entry.grid(row=2, column=0, padx=5, pady=10)

    def toggle_password_visibility():
        if password_visible_flag[0]:
            password_entry.configure(show="•")
            password_icon_button.configure(image=eye_slash_icon_tk)
            password_visible_flag[0] = False
        else:
            password_entry.configure(show="")
            password_icon_button.configure(image=eye_icon_tk)
            password_visible_flag[0] = True

    password_icon_button = ctk.CTkButton(
        label_frame,
        image=eye_slash_icon_tk,
        fg_color="transparent",
        width=30,
        height=30,
        command=toggle_password_visibility,
        hover_color="#e0e0e0",
        text=""
    )
    password_icon_button.grid(row=2, column=2, padx=2, pady=10)

    login_button = ctk.CTkButton(label_frame, text='Log In', fg_color="#E899A2", text_color="black",
                                 font=("Arial", 12, "bold"), hover_color="#E6B2BA", command=login)
    login_button.grid(row=3, column=0, columnspan=1, pady=10)

    sign_up_button = ctk.CTkButton(label_frame, text='Sign Up', fg_color="#E899A2", text_color="black",
                                   font=("Arial", 12, "bold"), hover_color="#E6B2BA", command=show_sign_up_page)
    sign_up_button.grid(row=4, column=0, columnspan=2, pady=10)

    forgot_password_button = ctk.CTkButton(label_frame, text="Forgot Password?", fg_color="transparent",
                                           text_color="black", font=("Arial", 12, "italic"),
                                           command=show_forgot_password_page)
    forgot_password_button.grid(row=5, column=0, columnspan=2, pady=10)







def show_forgot_password_page():
    global email_entry
    for widget in root.winfo_children():
        widget.destroy()

    title = ctk.CTkLabel(root, text="Forgot Password", fg_color="transparent", text_color="#d0637c",
                         font=("Arial", 40, "bold"))
    title.place(relx=0.5, rely=0.15, anchor="center")

    email_entry = ctk.CTkEntry(root, placeholder_text="Enter your email")
    email_entry.place(relx=0.5, rely=0.3, anchor="center")

    error_label = ctk.CTkLabel(root, text="", text_color="red")
    error_label.place(relx=0.5, rely=0.37, anchor="center")

    def on_submit():
        email = email_entry.get().strip()
        if not email:
            error_label.configure(text="Please enter your email.")
            return
        otp = send_otp_email(email)
        if otp:
            root.generated_otp = otp
            show_otp_verification_page_forgot(email)
        else:
            error_label.configure(text="Failed to send OTP. Check your email address.")

    submit_button = ctk.CTkButton(root, text="Submit", fg_color="#E899A2", text_color="black",
                                  font=("Arial", 12, "bold"), hover_color="#E6B2BA",
                                  command=on_submit)
    submit_button.place(relx=0.5, rely=0.45, anchor="center")

    back_button = ctk.CTkButton(root, text="Back to Login", fg_color="#E899A2", text_color="black",
                                font=("Arial", 12, "bold"), hover_color="#E6B2BA", command=show_login_page)
    back_button.place(relx=0.5, rely=0.55, anchor="center")





def show_otp_verification_page_forgot(user_email):
    for widget in root.winfo_children():
        widget.destroy()
    otp_label = ctk.CTkLabel(root, text="Enter the OTP sent to your email", text_color="#d0637c", font=("Arial", 20, "bold"))
    otp_label.place(relx=0.5, rely=0.2, anchor="center")
    otp_entry = ctk.CTkEntry(root, placeholder_text="OTP")
    otp_entry.place(relx=0.5, rely=0.3, anchor="center")
    error_label = ctk.CTkLabel(root, text="", text_color="red")
    error_label.place(relx=0.5, rely=0.4, anchor="center")
    def verify_otp():
        entered_otp = otp_entry.get()
        if entered_otp == root.generated_otp:
            show_reset_password_page(user_email)
        else:
            error_label.configure(text="Invalid OTP. Please try again.")
    verify_button = ctk.CTkButton(root, text="Verify OTP", command=verify_otp)
    verify_button.place(relx=0.5, rely=0.5, anchor="center")







def show_reset_password_page(user_email):
    global reset_password_visible, reset_confirm_password_visible
    reset_password_visible = False
    reset_confirm_password_visible = False

    for widget in root.winfo_children():
        widget.destroy()
    title = ctk.CTkLabel(root, text="Reset Password", fg_color="transparent", text_color="#d0637c",
                         font=("Arial", 30, "bold"))
    title.place(relx=0.5, rely=0.15, anchor="center")

    # New Password Entry
    new_password_entry = ctk.CTkEntry(root, placeholder_text="New Password", show="•")
    new_password_entry.place(relx=0.5, rely=0.3, anchor="center")

    # Confirm Password Entry
    confirm_password_entry = ctk.CTkEntry(root, placeholder_text="Confirm Password", show="•")
    confirm_password_entry.place(relx=0.5, rely=0.37, anchor="center")

    # Error Label
    error_label = ctk.CTkLabel(root, text="", text_color="red")
    error_label.place(relx=0.5, rely=0.25, anchor="center")

    # Show/Hide password logic
    password_visible_flag = [False]
    confirm_password_visible_flag = [False]

    def toggle_new_password_visibility():
        if password_visible_flag[0]:
            new_password_entry.configure(show="•")
            new_password_icon_btn.configure(image=eye_slash_icon_tk)
            password_visible_flag[0] = False
        else:
            new_password_entry.configure(show="")
            new_password_icon_btn.configure(image=eye_icon_tk)
            password_visible_flag[0] = True

    def toggle_confirm_password_visibility():
        if confirm_password_visible_flag[0]:
            confirm_password_entry.configure(show="•")
            confirm_password_icon_btn.configure(image=eye_slash_icon_tk)
            confirm_password_visible_flag[0] = False
        else:
            confirm_password_entry.configure(show="")
            confirm_password_icon_btn.configure(image=eye_icon_tk)
            confirm_password_visible_flag[0] = True

    new_password_icon_btn = ctk.CTkButton(
        root,
        image=eye_slash_icon_tk,
        fg_color="transparent",
        width=30,
        height=30,
        command=toggle_new_password_visibility,
        hover_color="#e0e0e0",
        text=""
    )
    new_password_icon_btn.place(relx=0.68, rely=0.3, anchor="center")

    confirm_password_icon_btn = ctk.CTkButton(
        root,
        image=eye_slash_icon_tk,
        fg_color="transparent",
        width=30,
        height=30,
        command=toggle_confirm_password_visibility,
        hover_color="#e0e0e0",
        text=""
    )
    confirm_password_icon_btn.place(relx=0.68, rely=0.37, anchor="center")

    def on_reset():
        new_password = new_password_entry.get()
        confirm_password = confirm_password_entry.get()
        if not new_password or not confirm_password:
            error_label.configure(text="Please fill out all fields.")
        elif new_password != confirm_password:
            error_label.configure(text="Passwords do not match.")
        else:
            if update_user_password(user_email, new_password):
                messagebox.showinfo("Success", "Password reset successful!")
                show_login_page()
            else:
                error_label.configure(text="Failed to reset password.")

    reset_button = ctk.CTkButton(root, text="Reset Password", command=on_reset)
    reset_button.place(relx=0.5, rely=0.52, anchor="center")

    back_button = ctk.CTkButton(root, text="Back to Login", fg_color="#E899A2", text_color="black",
                                font=("Arial", 12, "bold"), hover_color="#E6B2BA", command=show_login_page)
    back_button.place(relx=0.5, rely=0.60, anchor="center")







def update_user_password(email, new_password):
    conn = connect_to_db()
    if conn:
        try:
            cur = conn.cursor()
            # Hash the new password before updating
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            cur.execute("UPDATE users SET password = %s WHERE email = %s", (hashed_password.decode('utf-8'), email))
            conn.commit()
            cur.close()
            return True
        except Exception as e:
            print("Error updating password:", e)
            return False
        finally:
            conn.close()
    return False







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
