
import customtkinter as ctk
from tkinter import PhotoImage
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter.messagebox
from PIL import Image, ImageTk

# theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class OverviewPage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#11161e")

        header = ctk.CTkFrame(self, fg_color="#23c36b", height=210)
        header.pack(fill="x", side="top")

        # wallet
        alex_love_brittany = ctk.CTkFrame(self, width=300, height=150, fg_color="#19212C")
        alex_love_brittany.place(relx=0.5, rely=0.2, anchor="n")

        lextanny_ever = ctk.CTkLabel(alex_love_brittany, text="Wallet", font=("Arial", 15), text_color="white")
        lextanny_ever.place(relx=0.1, rely=0.1)

        self.current_balance = 0.0  # Initialize balance
        self.balance_label = ctk.CTkLabel(
            alex_love_brittany,
            text=f"₱{self.current_balance:,.2f}",  # Format currency
            font=("Arial", 14, "bold"),
            text_color="white"
        )
        self.balance_label.place(relx=0.5, rely=0.5, anchor="center")

        # Edit Balance Button
        edit_balance_btn = ctk.CTkButton(
            alex_love_brittany,
            text="Edit Balance",
            fg_color="#355e46",
            hover_color="#3d6e50",
            font=("Arial", 12, "bold"),
            command=self.open_edit_balance_dialog
        )
        edit_balance_btn.place(relx=0.5, rely=0.8, anchor="center")

        # contentframe
        content_frame = ctk.CTkFrame(self, fg_color="#19212C")
        content_frame.pack(expand=True, fill="both", pady=(170, 70), padx=50)
        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_columnconfigure((0, 1, 2), weight=1)

        # recent transactions part
        transaction_frame = ctk.CTkFrame(content_frame, fg_color="#ffc700", corner_radius=5)
        transaction_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(transaction_frame, text="Transaction History", font=("Arial", 16, "bold"),
                     text_color="white").pack(pady=10)

        # income n expenses part
        income_box = ctk.CTkFrame(content_frame, fg_color="#1b2f55", corner_radius=5)
        income_box.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(income_box, text="Income VS Expenses", font=("Arial", 16, "bold"), text_color="white").pack(
            pady=10)
        fig, ax = plt.subplots(figsize=(4, 3), dpi=100)
        ax.set_title("")
        canvas = FigureCanvasTkAgg(fig, master=income_box)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(expand=True, fill="both", padx=10, pady=10)

        # remainingbudget
        remaining_budget_box = ctk.CTkFrame(content_frame, fg_color="#ffa652", corner_radius=5)
        remaining_budget_box.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        ctk.CTkLabel(remaining_budget_box, text="Remaining Budget", font=("Arial", 16, "bold"),
                     text_color="white").pack(pady=(7, 5))

        remaining_amount = 0.0
        ctk.CTkLabel(remaining_budget_box, text=f"₱{remaining_amount:,.2f}", font=("Arial", 15, "bold"),
                     text_color="white").pack(pady=(0, 5))

    def open_edit_balance_dialog(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Edit Balance")
        dialog.geometry("300x150")
        dialog.grab_set()

        # Center the dialog
        dialog.update_idletasks()
        w = 300
        h = 150
        x = self.winfo_rootx() + (self.winfo_width() // 2) - (w // 2)
        y = self.winfo_rooty() + (self.winfo_height() // 2) - (h // 2)
        dialog.geometry(f"{w}x{h}+{x}+{y}")

        ctk.CTkLabel(dialog, text="New Balance (₱):", font=("Arial", 14)).pack(pady=(20, 5))
        balance_entry = ctk.CTkEntry(dialog, width=200)
        balance_entry.insert(0, str(self.current_balance))
        balance_entry.pack(pady=5)

        def save_balance():
            try:
                new_balance = float(balance_entry.get())
                self.current_balance = new_balance
                self.balance_label.configure(text=f"₱{self.current_balance:,.2f}")
                dialog.destroy()
            except ValueError:
                tkinter.messagebox.showerror("Error", "Please enter a valid number.")

        save_btn = ctk.CTkButton(dialog, text="Save", fg_color="#23c36b", font=("Arial", 14, "bold"), command=save_balance)
        save_btn.pack(pady=20)


class ProfilePage(ctk.CTkFrame):
    def __init__(self, master, user_data=None):
        super().__init__(master, fg_color="#181c1b")
        if user_data is None:
            user_data = {
                "name": "Alex",
                "email": "alex@email.com",
                "joined": "2024-01-01",
                "password": "password123",  # For demonstration only
            }
        self.user_data = user_data

        self.avatar = ctk.CTkLabel(self, text="\U0001F464", font=("Arial", 80), text_color="#2e7d32")
        self.avatar.pack(pady=(40, 10))
        self.name_label = ctk.CTkLabel(self, text=self.user_data["name"], font=("Arial", 28, "bold"), text_color="white")
        self.name_label.pack(pady=(0, 5))
        self.email_label = ctk.CTkLabel(self, text=self.user_data["email"], font=("Arial", 16), text_color="#a4ac86")
        self.email_label.pack(pady=(0, 15))
        self.joined_label = ctk.CTkLabel(self, text=f"Joined: {self.user_data['joined']}", font=("Arial", 14), text_color="#b0b0b0")
        self.joined_label.pack(pady=(0, 30))
        self.edit_btn = ctk.CTkButton(self, text="Edit Profile", fg_color="#355e46", hover_color="#3d6e50", font=("Arial", 16, "bold"), command=self.open_edit_dialog)
        self.edit_btn.pack(pady=10)

    def open_edit_dialog(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Edit Profile")
        dialog.geometry("400x320")
        dialog.grab_set()

        # Center the dialog
        dialog.update_idletasks()
        w = 400
        h = 320
        x = self.winfo_rootx() + (self.winfo_width() // 2) - (w // 2)
        y = self.winfo_rooty() + (self.winfo_height() // 2) - (h // 2)
        dialog.geometry(f"{w}x{h}+{x}+{y}")

        ctk.CTkLabel(dialog, text="Name:", font=("Arial", 14)).pack(pady=(20, 5))
        name_entry = ctk.CTkEntry(dialog, width=300)
        name_entry.insert(0, self.user_data["name"])
        name_entry.pack()

        ctk.CTkLabel(dialog, text="Email:", font=("Arial", 14)).pack(pady=(15, 5))
        email_entry = ctk.CTkEntry(dialog, width=300)
        email_entry.insert(0, self.user_data["email"])
        email_entry.pack()

        ctk.CTkLabel(dialog, text="New Password:", font=("Arial", 14)).pack(pady=(15, 5))
        password_entry = ctk.CTkEntry(dialog, width=300, show="*")
        password_entry.pack()

        def save():
            self.user_data["name"] = name_entry.get()
            self.user_data["email"] = email_entry.get()
            new_password = password_entry.get()
            if new_password:
                self.user_data["password"] = new_password  # In real apps, hash and store securely
            self.name_label.configure(text=self.user_data["name"])
            self.email_label.configure(text=self.user_data["email"])
            dialog.destroy()

        save_btn = ctk.CTkButton(dialog, text="Save", fg_color="#23c36b", font=("Arial", 14, "bold"), command=save)
        save_btn.pack(pady=30)


class EnvelopeBudgetingFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.envelopes = {}
        self.transactions = []

        # ----- Envelope Creation Section -----
        frame_left = ctk.CTkFrame(self)
        frame_left.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        title1 = ctk.CTkLabel(frame_left, text="Create Envelope", font=("Arial", 20, "bold"))
        title1.pack(pady=10)

        self.envelope_name_entry = ctk.CTkEntry(frame_left, placeholder_text="Envelope Name")
        self.envelope_name_entry.pack(pady=5)

        self.envelope_amount_entry = ctk.CTkEntry(frame_left, placeholder_text="Amount (₱)")
        self.envelope_amount_entry.pack(pady=5)

        add_envelope_btn = ctk.CTkButton(frame_left, text="Add Envelope", command=self.add_envelope)
        add_envelope_btn.pack(pady=10)

        envelope_list_label = ctk.CTkLabel(frame_left, text="Envelope List", font=("Arial", 16, "bold"))
        envelope_list_label.pack(pady=(15, 2))

        self.envelope_list_frame = ctk.CTkScrollableFrame(frame_left, height=200)
        self.envelope_list_frame.pack(fill="both", expand=True, padx=0, pady=(0, 10))

        # ----- Expense Entry & Transaction History Section -----
        frame_right = ctk.CTkFrame(self)
        frame_right.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        title2 = ctk.CTkLabel(frame_right, text="Add Transaction", font=("Arial", 20, "bold"))
        title2.pack(pady=10)

        self.envelope_var = ctk.StringVar()
        self.envelope_dropdown = ctk.CTkOptionMenu(frame_right, variable=self.envelope_var, values=[])
        self.envelope_dropdown.pack(pady=5)

        self.transaction_details_entry = ctk.CTkEntry(frame_right, placeholder_text="Transaction Details")
        self.transaction_details_entry.pack(pady=5)

        self.transaction_amount_entry = ctk.CTkEntry(frame_right, placeholder_text="Amount (₱)")
        self.transaction_amount_entry.pack(pady=5)

        add_expense_btn = ctk.CTkButton(frame_right, text="Add Expense", command=self.add_expense)
        add_expense_btn.pack(pady=10)

        transaction_history_label = ctk.CTkLabel(frame_right, text="Transaction History", font=("Arial", 16, "bold"))
        transaction_history_label.pack(pady=(15, 2))

        self.transaction_history_frame = ctk.CTkScrollableFrame(frame_right, height=250)
        self.transaction_history_frame.pack(fill="both", expand=True, padx=0, pady=(0, 10))

        self.total_expenses_label = ctk.CTkLabel(frame_right, text="Total Expenses: ₱0.00", font=("Arial", 16, "bold"))
        self.total_expenses_label.pack(pady=(5, 10))

        self.update_envelope_list()
        self.update_transaction_history()

    def add_envelope(self):
        name = self.envelope_name_entry.get()
        amount = self.envelope_amount_entry.get()
        if name and amount:
            try:
                amount = float(amount)
                self.envelopes[name] = amount
                tkinter.messagebox.showinfo("Success", f"Envelope '{name}' added with ₱{amount:.2f}")
                self.envelope_name_entry.delete(0, ctk.END)
                self.envelope_amount_entry.delete(0, ctk.END)
                self.update_envelope_menu()
                self.update_envelope_list()
            except ValueError:
                tkinter.messagebox.showerror("Error", "Amount must be a number.")
        else:
            tkinter.messagebox.showerror("Error", "Please fill in all fields.")

    def update_envelope_menu(self):
        self.envelope_dropdown.configure(values=list(self.envelopes.keys()))

    def add_expense(self):
        selected_envelope = self.envelope_var.get()
        details = self.transaction_details_entry.get()
        amount = self.transaction_amount_entry.get()
        if selected_envelope and details and amount:
            try:
                amount = float(amount)
                if self.envelopes[selected_envelope] >= amount:
                    self.envelopes[selected_envelope] -= amount
                    self.transactions.append({
                        "envelope": selected_envelope,
                        "details": details,
                        "amount": amount
                    })
                    tkinter.messagebox.showinfo("Expense Added",
                        f"₱{amount:.2f} deducted from '{selected_envelope}'. Remaining: ₱{self.envelopes[selected_envelope]:.2f}")
                    self.transaction_details_entry.delete(0, ctk.END)
                    self.transaction_amount_entry.delete(0, ctk.END)
                    self.update_envelope_list()
                    self.update_transaction_history()
                    self.update_total_expenses()
                else:
                    tkinter.messagebox.showerror("Error", "Not enough balance in envelope.")
            except ValueError:
                tkinter.messagebox.showerror("Error", "Amount must be a number.")
        else:
            tkinter.messagebox.showerror("Error", "Please complete all fields.")

    def update_envelope_list(self):
        for widget in self.envelope_list_frame.winfo_children():
            widget.destroy()
        if not self.envelopes:
            ctk.CTkLabel(self.envelope_list_frame, text="No envelopes yet.", text_color="gray").pack()
        else:
            for name, amount in self.envelopes.items():
                ctk.CTkLabel(self.envelope_list_frame, text=f"{name}: ₱{amount:,.2f}", anchor="w", font=("Arial", 14)).pack(fill="x", padx=10, pady=2)

    def update_transaction_history(self):
        for widget in self.transaction_history_frame.winfo_children():
            widget.destroy()
        if not self.transactions:
            ctk.CTkLabel(self.transaction_history_frame, text="No transactions yet.", text_color="gray").pack()
        else:
            for tx in self.transactions[::-1]:
                ctk.CTkLabel(
                    self.transaction_history_frame,
                    text=f"{tx['envelope']} | {tx['details']} | ₱{tx['amount']:,.2f}",
                    anchor="w",
                    font=("Arial", 13)
                ).pack(fill="x", padx=10, pady=1)
        self.update_total_expenses()

    def update_total_expenses(self):
        total_expenses = sum(tx['amount'] for tx in self.transactions)
        self.total_expenses_label.configure(text=f"Total Expenses: ₱{total_expenses:,.2f}")


class Navigation(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Navigation")
        self.geometry("1200x700")

        self.sidebar_visible = False

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar_frame = ctk.CTkFrame(self, width=180, fg_color="#19212C")
        self.nav_buttons_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.content_frame = ctk.CTkFrame(self, fg_color="#19212C")
        self.content_frame.grid(row=0, column=1, sticky="nsew")

        self.toggle_button_floating = ctk.CTkButton(
            self, text="☰", font=("Arial", 24), width=50, height=50,
            corner_radius=5, fg_color="#19212C", hover_color="#23c36b",
            text_color="white", command=self.toggle_sidebar
        )
        self.toggle_button_floating.place(x=10, y=10)

        self.toggle_button_sidebar = ctk.CTkButton(
            self.sidebar_frame, text="☰", font=("Arial", 24), width=60, height=50,
            corner_radius=12, fg_color="#23c36b", hover_color="#1e1e1e",
            text_color="white", command=self.toggle_sidebar
        )

        self.nav_buttons = []
        nav_texts = ["Overview", "Profile", "Edit Info", "Settings"]
        for text in nav_texts:
            btn = ctk.CTkButton(
                self.nav_buttons_frame, text=text, font=("Arial", 18),
                height=30, fg_color="#23c36b", hover_color="#1e1e1e",
                text_color="white", command=lambda t=text: self.navigate_to(t)
            )
            self.nav_buttons.append(btn)

        self.logout_button = ctk.CTkButton(
            self.sidebar_frame, text="Logout", font=("Arial", 18),
            height=55, fg_color="#a53939", hover_color="#b04040",
            text_color="white", command=lambda: self.navigate_to("Logout")
        )

        self.navigate_to("Overview")

    def toggle_sidebar(self):
        if self.sidebar_visible:
            self.sidebar_frame.grid_forget()
            self.toggle_button_floating.place(x=10, y=10)
            self.sidebar_visible = False
        else:
            self.sidebar_frame.grid(row=0, column=0, sticky="ns")
            self.toggle_button_sidebar.pack(pady=30, padx=15, fill="x")
            self.nav_buttons_frame.pack(fill="both", expand=True, pady=(0, 10))
            for btn in self.nav_buttons:
                btn.pack(fill="x", padx=20, pady=12)
            self.logout_button.pack(side="bottom", fill="x", padx=20, pady=20)
            self.toggle_button_floating.place_forget()
            self.sidebar_visible = True

    def navigate_to(self, page_name):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        if page_name == "Overview":
            overview_page = OverviewPage(self.content_frame)
            overview_page.pack(fill="both", expand=True)

        elif page_name == "Profile":
            profile_page = ProfilePage(self.content_frame)
            profile_page.pack(fill="both", expand=True)

        elif page_name == "Edit Info":
            budgeting_frame = EnvelopeBudgetingFrame(self.content_frame)
            budgeting_frame.pack(fill="both", expand=True)

        else:
            label = ctk.CTkLabel(
                self.content_frame, text=f"You are now on the {page_name} page",
                text_color="black", font=("Arial", 32)
            )
            label.pack(expand=True)


if __name__ == "__main__":
    app = Navigation()
    app.mainloop()