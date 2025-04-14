import customtkinter as ctk
from tkinter import messagebox, Toplevel
from PIL import Image, ImageTk, ImageDraw, ImageFont, ImageFilter
import random #for captcha
import string #for captcha
import os

#admin creds(para sa login)
ADMIN_CREDENTIALS = {"gastosmeter": "admin123"}

captcha_code = ""
captcha_image_ref = None

#generate captcha(6 random letters and numbers, different sizes)
def generate_captcha():
    global captcha_code

    #makes 6 random letters and numbers
    captcha_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    width, height = 220, 100

    image = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    font_path = "arial.ttf"

    if not os.path.exists(font_path):
        font_path = None


    x_position = 10 #text placement

    for char in captcha_code:
        font_size = random.randint(30, 45)#radim size
        font = ImageFont.truetype(font_path, font_size) if font_path else ImageFont.load_default()
        y_position = random.randint(10, 40)

        #shadow fx for contrast
        draw.text((x_position + 2, y_position + 2), char, font=font, fill=(180, 180, 180))
        draw.text((x_position, y_position), char, font=font, fill=(0, 0, 0))
        x_position += font_size - random.randint(5, 10)

    image = image.filter(ImageFilter.GaussianBlur(radius=1)) #blur effect
    captcha_photo = ImageTk.PhotoImage(image) #tkinter to compatible img
    return captcha_photo

def validate_captcha(captcha_entry, captcha_label, captcha_window):
    #validates the entered captcha
    user_input = captcha_entry.get().strip()

    #if correct: closes window and open main page
    if user_input.upper() == captcha_code:
        captcha_window.destroy()
        show_main_page()
    #if wrong regen another captcha
    else:
        messagebox.showerror("Error", "Incorrect CAPTCHA. Try again.")
        update_captcha(captcha_label)

def update_captcha(captcha_label):
    #captcha update
    global captcha_image_ref
    captcha_image_ref = generate_captcha()

    captcha_label.configure(image=captcha_image_ref)
    captcha_label.image = captcha_image_ref #prevent garbage collection(freeing up memory that is no longer in use)

def open_captcha_window():
    #shows captcha window
    captcha_window = Toplevel(root)
    captcha_window.title("Gastos Meter - CAPTCHA Verification")
    captcha_window.geometry("350x380")
    captcha_window.configure(bg="white")

    global captcha_image_ref
    captcha_image_ref = generate_captcha()

    captcha_label = ctk.CTkLabel(captcha_window, image=captcha_image_ref, text="")
    captcha_label.pack(pady=10)

    captcha_entry = ctk.CTkEntry(captcha_window, placeholder_text="Enter CAPTCHA")
    captcha_entry.pack(pady=10)

    verify_button = ctk.CTkButton(captcha_window, text="Verify", command=lambda: validate_captcha(captcha_entry, captcha_label, captcha_window))
    verify_button.pack(pady=10)
    captcha_window.resizable(False, False)

def show_main_page():
    #shows main page after captcha verif (authentic)
    for widget in root.winfo_children():
        widget.destroy() # clear the current window before the new window
        root.title("Gastos Meter")

    #layout po ng main page
    header = ctk.CTkFrame(root, fg_color="black", height=80)
    header.pack(fill=ctk.X)

    logo = ctk.CTkLabel(header, text="GASTOS METER", fg_color="transparent", text_color="#d0637c", font=("Arial", 35, "bold"))
    logo.pack(side=ctk.LEFT, padx=20, pady=20)

    logout_button = ctk.CTkButton(header, text="Logout", font=("Arial", 14), fg_color="white", text_color="black", hover_color="#d0637c", command=show_login_page)
    logout_button.pack(side=ctk.RIGHT, padx=20, pady=15)

    content = ctk.CTkFrame(root, fg_color="#e1b5b5")
    content.pack(pady=20, padx=40, fill=ctk.BOTH, expand=True)

    heading = ctk.CTkLabel(content, text="Smart Tracking\nfor Smarter Spending", font=("Arial", 32, "bold"), text_color="black")
    heading.pack(pady=10)

    subtext = ctk.CTkLabel(content, text="Easily track your income, expenses, and savings in one place.\nGain insights, set goals, and take control of your financial future.", font=("Arial", 14), text_color="black")
    subtext.pack(pady=10)

    start_button = ctk.CTkButton(content, text="Get Started", font=("Arial", 16, "bold"), fg_color="black", hover_color="#d0637c", text_color="white")
    start_button.pack(anchor="center", pady=20)

    #inserts the image(hand with phone)
    image = Image.open("element.png")
    image = image.resize((300, 300))
    photo = ImageTk.PhotoImage(image)

    label = ctk.CTkLabel(content, image=photo)
    label.image = photo
    label.pack()

def login():
    #process po of login and opens the captcha window if correct admin login(credentials)
    username = username_entry.get()
    password = password_entry.get()

    #shows message box(if inputs are: left unfilled, correct credentials, wrong credentials)
    if not username or not password:
        messagebox.showerror("Error", "Please enter both username and password.")
        return
    if username in ADMIN_CREDENTIALS and ADMIN_CREDENTIALS[username] == password:
        messagebox.showinfo("Success", f"Admin Login successful! Welcome, {username}!")
        open_captcha_window()
    else:
        messagebox.showerror("Error", "Invalid username or password. Please try again.")

def show_login_page():
    #shows login window
    for widget in root.winfo_children():
        widget.destroy() # clear the current window before the new window
    root.title("Gastos Meter - Login")
    root.configure(bg="#FF7AA2")

    label_frame = ctk.CTkFrame(root, fg_color="transparent")
    label_frame.place(relx=0.5, rely=0.5, anchor="center")

    title = ctk.CTkLabel(root, text="GASTOS", fg_color="transparent", text_color="#d0637c", font=("Arial", 40, "bold"))
    title.place(relx=0.5, rely=0.15, anchor="center")

    title_meter = ctk.CTkLabel(root, text="Meter", fg_color="transparent", text_color="#dd868c", font=("Arial", 35))
    title_meter.place(relx=0.5, rely=0.22, anchor="center")

    global username_entry, password_entry
    username_entry = ctk.CTkEntry(label_frame, placeholder_text="Username")
    username_entry.grid(row=1, column=0, columnspan=2, padx=5, pady=10)

    password_entry = ctk.CTkEntry(label_frame, placeholder_text="Password", show="•")
    password_entry.grid(row=2, column=0, columnspan=2, padx=5, pady=10)

    login_button = ctk.CTkButton(label_frame, text='Log In', fg_color="#E899A2", text_color="black", font=("Arial", 12, "bold"),hover_color="#E6B2BA", command=login)
    login_button.grid(row=3, column=0, columnspan=2, pady=20)

ctk.set_appearance_mode("light") #we used customtkinter for the theme of our software.
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.geometry("600x625")
root.configure(bg="#e1b5b5")
root.resizable(False, False)
show_login_page()

root.mainloop()
