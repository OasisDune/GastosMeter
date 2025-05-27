import customtkinter as ctk
import tkinter.messagebox

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class OverviewPage(ctk.CTkFrame):
    def __init__(self, master, get_balance, set_balance, get_total_expenses, transactions, envelopes):
        super().__init__(master, fg_color="#11161e")
        self.get_balance = get_balance
        self.set_balance = set_balance
        self.get_total_expenses = get_total_expenses
        self.transactions = transactions
        self.envelopes = envelopes

        # Summary Section
        summary_frame = ctk.CTkFrame(self, fg_color="#2a2d2e", corner_radius=10)
        summary_frame.pack(fill="x", padx=(60, 20), pady=10)

        self.total_balance_label = ctk.CTkLabel(summary_frame, text="Total Balance: ₱0.00", font=("Arial", 14, "bold"))
        self.total_balance_label.grid(row=0, column=0, padx=10, pady=5)

        self.total_expenses_label = ctk.CTkLabel(summary_frame, text="Total Expenses: ₱0.00", font=("Arial", 14, "bold"))
        self.total_expenses_label.grid(row=0, column=1, padx=10, pady=5)

        self.remaining_budget_label = ctk.CTkLabel(summary_frame, text="Remaining Budget: ₱0.00", font=("Arial", 14, "bold"))
        self.remaining_budget_label.grid(row=0, column=2, padx=10, pady=5)

        self.top_spending_label = ctk.CTkLabel(summary_frame, text="Top Spending: None", font=("Arial", 14, "bold"))
        self.top_spending_label.grid(row=0, column=3, padx=10, pady=5)

        header = ctk.CTkFrame(self, fg_color="#23c36b", height=210)
        header.pack(fill="x", side="top")

        wallet_frame = ctk.CTkFrame(self, width=300, height=150, fg_color="#19212C")
        wallet_frame.place(relx=0.5, rely=0.2, anchor="n")

        ctk.CTkLabel(wallet_frame, text="Wallet", font=("Arial", 15), text_color="white").place(relx=0.1, rely=0.1)

        self.balance_label = ctk.CTkLabel(
            wallet_frame,
            text=f"₱{self.get_balance():,.2f}",
            font=("Arial", 14, "bold"),
            text_color="white"
        )
        self.balance_label.place(relx=0.5, rely=0.5, anchor="center")

        edit_balance_btn = ctk.CTkButton(
            wallet_frame,
            text="Edit Balance",
            fg_color="#355e46",
            hover_color="#3d6e50",
            font=("Arial", 12, "bold"),
            command=self.open_edit_balance_dialog
        )
        edit_balance_btn.place(relx=0.5, rely=0.8, anchor="center")

        self.warning_label = ctk.CTkLabel(wallet_frame, text="", font=("Arial", 13, "bold"), text_color="red")
        self.warning_label.place(relx=0.5, rely=0.7, anchor="center")

        content_frame = ctk.CTkFrame(self, fg_color="#19212C")
        content_frame.pack(expand=True, fill="both", pady=(170, 70), padx=50)
        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_columnconfigure((0, 1, 2), weight=1)

        # Transaction History
        transaction_frame = ctk.CTkFrame(content_frame, fg_color="#ffc700", corner_radius=5)
        transaction_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(transaction_frame, text="Transaction History", font=("Arial", 16, "bold"),
                     text_color="white").pack(pady=10)
        # Column titles for transaction history
        tx_header = ctk.CTkFrame(transaction_frame, fg_color="transparent")
        tx_header.pack(fill="x", padx=5)
        ctk.CTkLabel(tx_header, text="Date", font=("Arial", 13, "bold"), width=90, anchor="w").grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(tx_header, text="Envelope", font=("Arial", 13, "bold"), width=90, anchor="w").grid(row=0, column=1, sticky="w")
        ctk.CTkLabel(tx_header, text="Details", font=("Arial", 13, "bold"), width=120, anchor="w").grid(row=0, column=2, sticky="w")
        ctk.CTkLabel(tx_header, text="Amount", font=("Arial", 13, "bold"), width=80, anchor="w").grid(row=0, column=3, sticky="w")

        self.tx_history_frame = ctk.CTkScrollableFrame(transaction_frame, height=200)
        self.tx_history_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Envelope List
        envelope_list_box = ctk.CTkFrame(content_frame, fg_color="#ffa652", corner_radius=5)
        envelope_list_box.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(envelope_list_box, text="Envelope List", font=("Arial", 16, "bold"),
                     text_color="white").pack(pady=(7, 5))
        # Column titles for envelope list
        env_header = ctk.CTkFrame(envelope_list_box, fg_color="transparent")
        env_header.pack(fill="x", padx=5)
        ctk.CTkLabel(env_header, text="Envelope", font=("Arial", 13, "bold"), width=120, anchor="w").grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(env_header, text="Amount", font=("Arial", 13, "bold"), width=80, anchor="w").grid(row=0, column=1, sticky="w")

        self.envelope_list_frame = ctk.CTkScrollableFrame(envelope_list_box, height=200)
        self.envelope_list_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.update_overview()

    def open_edit_balance_dialog(self):
        dialog = ctk.CTkToplevel(self)
        dialog.title("Edit Balance")
        dialog.geometry("300x150")
        dialog.grab_set()

        ctk.CTkLabel(dialog, text="New Balance (₱):", font=("Arial", 14)).pack(pady=(20, 5))
        balance_entry = ctk.CTkEntry(dialog, width=200)
        balance_entry.insert(0, str(self.get_balance()))
        balance_entry.pack(pady=5)

        def save_balance():
            try:
                new_balance = float(balance_entry.get())
                self.set_balance(new_balance)
                self.update_overview()
                dialog.destroy()
            except ValueError:
                tkinter.messagebox.showerror("Error", "Please enter a valid number.")

        save_btn = ctk.CTkButton(dialog, text="Save", fg_color="#23c36b", font=("Arial", 14, "bold"), command=save_balance)
        save_btn.pack(pady=20)

    def update_overview(self):
        total_balance = sum(self.envelopes.values())
        total_expenses = self.get_total_expenses()
        remaining_budget = total_balance - total_expenses
        top_spending = None
        if self.envelopes:
            top_spending = max(self.envelopes, key=lambda k: self.envelopes[k])
        self.total_balance_label.configure(text=f"Total Balance: ₱{total_balance:,.2f}")
        self.total_expenses_label.configure(text=f"Total Expenses: ₱{total_expenses:,.2f}")
        self.remaining_budget_label.configure(text=f"Remaining Budget: ₱{remaining_budget:,.2f}")
        self.top_spending_label.configure(text=f"Top Spending: {top_spending if top_spending else 'None'}")

        balance = self.get_balance()
        expenses = self.get_total_expenses()
        self.balance_label.configure(text=f"₱{balance:,.2f}")
        if expenses > balance:
            self.warning_label.configure(text="Warning: You are over budget!")
        else:
            self.warning_label.configure(text="")

        # Update transaction history
        for widget in self.tx_history_frame.winfo_children():
            widget.destroy()
        if not self.transactions:
            ctk.CTkLabel(self.tx_history_frame, text="No transactions yet.", text_color="gray").pack()
        else:
            for tx in self.transactions[::-1]:
                row = ctk.CTkFrame(self.tx_history_frame, fg_color="transparent")
                row.pack(fill="x", padx=0, pady=1)
                ctk.CTkLabel(row, text=tx.get('date', ''), width=90, anchor="w", font=("Arial", 13)).grid(row=0, column=0, sticky="w")
                ctk.CTkLabel(row, text=tx['envelope'], width=90, anchor="w", font=("Arial", 13)).grid(row=0, column=1, sticky="w")
                ctk.CTkLabel(row, text=tx['details'], width=120, anchor="w", font=("Arial", 13)).grid(row=0, column=2, sticky="w")
                ctk.CTkLabel(row, text=f"₱{tx['amount']:,.2f}", width=80, anchor="w", font=("Arial", 13)).grid(row=0, column=3, sticky="w")

        # Update envelope list
        for widget in self.envelope_list_frame.winfo_children():
            widget.destroy()
        if not self.envelopes:
            ctk.CTkLabel(self.envelope_list_frame, text="No envelopes yet.", text_color="gray").pack()
        else:
            for name, amount in self.envelopes.items():
                row = ctk.CTkFrame(self.envelope_list_frame, fg_color="transparent")
                row.pack(fill="x", padx=0, pady=2)
                ctk.CTkLabel(row, text=name, width=120, anchor="w", font=("Arial", 14)).grid(row=0, column=0, sticky="w")
                ctk.CTkLabel(row, text=f"₱{amount:,.2f}", width=80, anchor="w", font=("Arial", 14)).grid(row=0, column=1, sticky="w")


# ... (rest of the code remains unchanged, including ProfilePage, EnvelopeBudgetingFrame, and Navigation)


class ProfilePage(ctk.CTkFrame):
    def __init__(self, master, user_data=None):
        super().__init__(master, fg_color="#181c1b")
        if user_data is None:
            user_data = {
                "name": "Alex",
                "email": "alex@email.com",
                "joined": "2024-01-01",
                "password": "password123",
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
                self.user_data["password"] = new_password
            self.name_label.configure(text=self.user_data["name"])
            self.email_label.configure(text=self.user_data["email"])
            dialog.destroy()

        save_btn = ctk.CTkButton(dialog, text="Save", fg_color="#23c36b", font=("Arial", 14, "bold"), command=save)
        save_btn.pack(pady=30)



class EnvelopeBudgetingFrame(ctk.CTkFrame):
    def __init__(self, parent, envelopes, transactions, update_overview_callback):
        super().__init__(parent)
        self.envelopes = envelopes
        self.transactions = transactions
        self.update_overview_callback = update_overview_callback

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

        # Envelope list column headers
        env_header = ctk.CTkFrame(frame_left, fg_color="transparent")
        env_header.pack(fill="x", padx=5)
        ctk.CTkLabel(env_header, text="Envelope", font=("Arial", 13, "bold"), width=120, anchor="w").grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(env_header, text="Amount", font=("Arial", 13, "bold"), width=80, anchor="w").grid(row=0, column=1, sticky="w")

        self.envelope_list_frame = ctk.CTkScrollableFrame(frame_left, height=200)
        self.envelope_list_frame.pack(fill="both", expand=True, padx=0, pady=(0, 10))

        frame_right = ctk.CTkFrame(self)
        frame_right.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        title2 = ctk.CTkLabel(frame_right, text="Add Transaction", font=("Arial", 20, "bold"))
        title2.pack(pady=10)

        self.envelope_var = ctk.StringVar()
        self.envelope_dropdown = ctk.CTkOptionMenu(frame_right, variable=self.envelope_var, values=list(self.envelopes.keys()))
        self.envelope_dropdown.pack(pady=5)

        ctk.CTkLabel(frame_right, text="Date (YYYY-MM-DD):", font=("Arial", 14)).pack(pady=(5, 0))
        self.transaction_date_entry = ctk.CTkEntry(frame_right, placeholder_text="YYYY-MM-DD")
        self.transaction_date_entry.pack(pady=5)

        self.transaction_details_entry = ctk.CTkEntry(frame_right, placeholder_text="Transaction Details")
        self.transaction_details_entry.pack(pady=5)

        self.transaction_amount_entry = ctk.CTkEntry(frame_right, placeholder_text="Amount (₱)")
        self.transaction_amount_entry.pack(pady=5)

        add_expense_btn = ctk.CTkButton(frame_right, text="Add Expense", command=self.add_expense)
        add_expense_btn.pack(pady=10)

        transaction_history_label = ctk.CTkLabel(frame_right, text="Transaction History", font=("Arial", 16, "bold"))
        transaction_history_label.pack(pady=(15, 2))

        # Transaction history column headers
        tx_header = ctk.CTkFrame(frame_right, fg_color="transparent")
        tx_header.pack(fill="x", padx=5)
        ctk.CTkLabel(tx_header, text="Date", font=("Arial", 13, "bold"), width=90, anchor="w").grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(tx_header, text="Envelope", font=("Arial", 13, "bold"), width=90, anchor="w").grid(row=0, column=1, sticky="w")
        ctk.CTkLabel(tx_header, text="Details", font=("Arial", 13, "bold"), width=120, anchor="w").grid(row=0, column=2, sticky="w")
        ctk.CTkLabel(tx_header, text="Amount", font=("Arial", 13, "bold"), width=80, anchor="w").grid(row=0, column=3, sticky="w")

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
                self.update_overview_callback()
            except ValueError:
                tkinter.messagebox.showerror("Error", "Amount must be a number.")
        else:
            tkinter.messagebox.showerror("Error", "Please fill in all fields.")

    def update_envelope_menu(self):
        self.envelope_dropdown.configure(values=list(self.envelopes.keys()))

    def add_expense(self):
        selected_envelope = self.envelope_var.get()
        date = self.transaction_date_entry.get()
        details = self.transaction_details_entry.get()
        amount = self.transaction_amount_entry.get()
        if selected_envelope and date and details and amount:
            try:
                amount = float(amount)
                if self.envelopes[selected_envelope] >= amount:
                    self.envelopes[selected_envelope] -= amount
                    self.transactions.append({
                        "envelope": selected_envelope,
                        "date": date,
                        "details": details,
                        "amount": amount
                    })
                    tkinter.messagebox.showinfo(
                        "Expense Added",
                        f"₱{amount:.2f} deducted from '{selected_envelope}'. Remaining: ₱{self.envelopes[selected_envelope]:.2f}"
                    )
                    self.transaction_date_entry.delete(0, ctk.END)
                    self.transaction_details_entry.delete(0, ctk.END)
                    self.transaction_amount_entry.delete(0, ctk.END)
                    self.update_envelope_list()
                    self.update_transaction_history()
                    self.update_total_expenses()
                    self.update_overview_callback()
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
                row = ctk.CTkFrame(self.envelope_list_frame, fg_color="transparent")
                row.pack(fill="x", padx=0, pady=2)
                ctk.CTkLabel(row, text=name, width=120, anchor="w", font=("Arial", 14)).grid(row=0, column=0, sticky="w")
                ctk.CTkLabel(row, text=f"₱{amount:,.2f}", width=80, anchor="w", font=("Arial", 14)).grid(row=0, column=1, sticky="w")
        self.update_envelope_menu()

    def update_transaction_history(self):
        for widget in self.transaction_history_frame.winfo_children():
            widget.destroy()
        if not self.transactions:
            ctk.CTkLabel(self.transaction_history_frame, text="No transactions yet.", text_color="gray").pack()
        else:
            for tx in self.transactions[::-1]:
                row = ctk.CTkFrame(self.transaction_history_frame, fg_color="transparent")
                row.pack(fill="x", padx=0, pady=1)
                ctk.CTkLabel(row, text=tx.get('date', ''), width=90, anchor="w", font=("Arial", 13)).grid(row=0, column=0, sticky="w")
                ctk.CTkLabel(row, text=tx['envelope'], width=90, anchor="w", font=("Arial", 13)).grid(row=0, column=1, sticky="w")
                ctk.CTkLabel(row, text=tx['details'], width=120, anchor="w", font=("Arial", 13)).grid(row=0, column=2, sticky="w")
                ctk.CTkLabel(row, text=f"₱{tx['amount']:,.2f}", width=80, anchor="w", font=("Arial", 13)).grid(row=0, column=3, sticky="w")
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

        self.balance = 0.0
        self.user_data = {
            "name": "Alex",
            "email": "alex@email.com",
            "joined": "2024-01-01",
            "password": "password123"
        }
        self.envelopes = {}
        self.transactions = []
        self.overview_page = None

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


    def reset_data(self):
        self.envelopes.clear()
        self.transactions.clear()
        self.set_balance(0.0)
        tkinter.messagebox.showinfo("Reset Data", "All data has been reset.")
        self.update_overview()

    def get_balance(self):
        return self.balance

    def set_balance(self, value):
        self.balance = value
        if self.overview_page:
            self.overview_page.update_overview()

    def get_total_expenses(self):
        return sum(tx['amount'] for tx in self.transactions)

    def update_overview(self):
        if self.overview_page:
            self.overview_page.update_overview()

    def navigate_to(self, page_name):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        if page_name == "Overview":
            self.overview_page = OverviewPage(
                self.content_frame,
                get_balance=self.get_balance,
                set_balance=self.set_balance,
                get_total_expenses=self.get_total_expenses,
                transactions=self.transactions,
                envelopes=self.envelopes
            )
            self.overview_page.pack(fill="both", expand=True)

        elif page_name == "Profile":
            profile_page = ProfilePage(self.content_frame, user_data=self.user_data)
            profile_page.pack(fill="both", expand=True)

        elif page_name == "Edit Info":
            budgeting_frame = EnvelopeBudgetingFrame(
                self.content_frame,
                envelopes=self.envelopes,
                transactions=self.transactions,
                update_overview_callback=self.update_overview
            )
            budgeting_frame.pack(fill="both", expand=True)



        # Update the SettingsPage instantiation in the Navigation class

        # Update the SettingsPage instantiation in the Navigation class



        else:
            label = ctk.CTkLabel(
                self.content_frame, text=f"You are now on the {page_name} page",
                text_color="black", font=("Arial", 32)
            )
            label.pack(expand=True)


if __name__ == "__main__":
    app = Navigation()
    app.mainloop()