# app.py
'''
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from datetime import date, datetime, timedelta
import csv
import database as db
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from tkcalendar import DateEntry


# Define colors for categories for consistent styling in charts and the treeview
CATEGORY_COLORS = {
    "Food": "#ff9999", "Transport": "#66b3ff", "Bills": "#99ff99",
    "Shopping": "#ffcc99", "Health": "#c2c2f0", "Entertainment": "#ffb3e6",
    "Other": "#c9c9c9"
}

class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("💼 Personal Expense Tracker")
        self.root.geometry("1000x620")

        db.initialize_db()

        # Load theme from DB, default to 'light' if not set
        self.theme = tk.StringVar(value=db.load_setting('theme') or 'light')

        # --- FIX: Define icons BEFORE they are used in apply_theme ---
        try:
            self.light_icon = tk.PhotoImage(file="light_mode.png")
            self.dark_icon = tk.PhotoImage(file="dark_mode.png")
            self.use_icons = True
        except tk.TclError:
            # This will run if the image files are not found
            self.use_icons = False
            print("Warning: Theme icon images not found. Falling back to text button.")

        self.setup_styles()
        self.apply_theme() # Apply loaded theme on startup

        header = ttk.Frame(self.root, style="Header.TFrame")
        header.pack(fill="x", pady=(0, 10), ipady=5)
        ttk.Label(header, text="💼 Expense Tracker", font=("Segoe UI", 18, "bold"), style="Header.TLabel").pack(side="left", padx=20)
        
        # Using an image for the theme toggle button if available
        if self.use_icons:
            self.theme_button = ttk.Button(header, image=self.light_icon, command=self.toggle_theme, style="Header.TButton")
        else:
            # Fallback to a text button if icons failed to load
            self.theme_button = ttk.Button(header, text="Toggle Theme", command=self.toggle_theme)
        self.theme_button.pack(side="right", padx=20)


        input_frame = ttk.LabelFrame(self.root, text="➕ Add New Expense", padding=15)
        input_frame.pack(padx=20, pady=10, fill="x")

        action_frame = ttk.Frame(self.root)
        action_frame.pack(padx=20, pady=5, fill="x")

        display_frame = ttk.LabelFrame(self.root, text="📊 Expense History", padding=10)
        display_frame.pack(padx=20, pady=10, fill="both", expand=True)

        # --- Input Widgets ---
        ttk.Label(input_frame, text="📅 Date:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.date_entry = ttk.Entry(input_frame)
        self.date_entry.insert(0, date.today().strftime("%Y-%m-%d"))
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="📂 Category:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.category_entry = ttk.Combobox(input_frame, values=list(CATEGORY_COLORS.keys()), state="readonly")
        self.category_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(input_frame, text="💵 Amount:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.amount_entry = ttk.Entry(input_frame)
        self.amount_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="📝 Description:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.desc_entry = ttk.Entry(input_frame)
        self.desc_entry.grid(row=1, column=3, padx=5, pady=5)

        ttk.Label(input_frame, text="🎯 Monthly Target:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.monthly_target_entry = ttk.Entry(input_frame)
        self.monthly_target_entry.grid(row=3, column=1, padx=5, pady=5)
        self.monthly_target_entry.insert(0, db.load_setting("monthly_target") or "0")


        # --- Action Buttons ---
        ttk.Button(input_frame, text="Add Expense", command=self.add_expense).grid(row=2, column=0, pady=10)
        ttk.Button(input_frame, text="Delete Selected", command=self.delete_expense).grid(row=2, column=1, pady=10)
        ttk.Button(input_frame, text="🗑️ Delete All", command=self.delete_all_expenses).grid(row=2, column=3, pady=10)
        ttk.Button(input_frame, text="📈 View Statistics", command=self.view_stats).grid(row=2, column=2, pady=10)

        # --- Search and Data Actions ---
        ttk.Label(action_frame, text="🔍 Search Category:").pack(side="left", padx=5)
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(action_frame, textvariable=self.search_var)
        self.search_entry.pack(side="left", padx=5)
        self.search_entry.bind("<KeyRelease>", self.load_expenses)

        ttk.Button(input_frame, text="📤 Bulk Upload CSV", command=self.bulk_upload).grid(row=3, column=2, pady=10)
        self.total_label = ttk.Label(action_frame, text="💰 Total: ₹0.00", font=("Segoe UI", 10, "bold"))
        self.total_label.pack(side="right", padx=10)

        # --- Treeview Display ---
        self.tree = ttk.Treeview(display_frame, columns=("ID", "Date", "Category", "Amount", "Description"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Amount", text="Amount")
        self.tree.heading("Description", text="Description")
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Date", width=100, anchor="center")
        self.tree.column("Category", width=120, anchor="center")
        self.tree.column("Amount", width=100, anchor="e")
        self.tree.column("Description", width=350)
        self.tree.pack(fill="both", expand=True)

        self.load_expenses()

    def setup_styles(self):
        self.style = ttk.Style(self.root)
        self.style.theme_use("clam")

    def apply_theme(self):
        """Applies the selected theme to all widgets."""
        is_dark = self.theme.get() == 'dark'
        
        # Colors
        bg_color = "#2e2e2e" if is_dark else "#f7f9fc"
        fg_color = "white" if is_dark else "black"
        header_bg = "#3a3a3a" if is_dark else "#e1e1e1"
        tree_bg = "#3a3a3a" if is_dark else "white"
        tree_fg = "white" if is_dark else "black"
        tree_heading_bg = "#555555" if is_dark else "#4a90e2"

        self.root.configure(bg=bg_color)
        
        # Style configurations
        self.style.configure("TFrame", background=bg_color)
        self.style.configure("TLabel", background=bg_color, foreground=fg_color, font=("Segoe UI", 10))
        self.style.configure("Header.TFrame", background=header_bg)
        self.style.configure("Header.TLabel", background=header_bg, foreground=fg_color)
        self.style.configure("Header.TButton", background=header_bg)
        self.style.configure("TLabelFrame", background=bg_color, foreground=fg_color)
        self.style.configure("TLabelFrame.Label", background=bg_color, foreground=fg_color)
        self.style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6)
        
        # Treeview Style
        self.style.configure("Treeview", font=("Segoe UI", 10), rowheight=28, background=tree_bg, foreground=tree_fg, fieldbackground=tree_bg)
        self.style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"), background=tree_heading_bg, foreground="white")
        self.style.map('Treeview', background=[('selected', '#555555' if is_dark else '#4a90e2')])
        
        # Update theme toggle icon if icons are being used
        if self.use_icons:
            icon = self.dark_icon if is_dark else self.light_icon
            self.theme_button.configure(image=icon)

    def toggle_theme(self):
        """Toggles the theme and saves the setting."""
        if self.theme.get() == 'light':
            self.theme.set('dark')
        else:
            self.theme.set('light')
        
        self.apply_theme()
        db.save_setting('theme', self.theme.get())

    def load_expenses(self, event=None):
        search_term = self.search_var.get().lower()
        self.tree.delete(*self.tree.get_children())
        total = 0.0

        for expense in db.get_expenses():
            if search_term and search_term not in expense[2].lower():
                continue
            
            category = expense[2]
            self.tree.insert("", "end", values=expense, tags=(category,))
            total += float(expense[3])
        
        # Apply category colors
        for category, color in CATEGORY_COLORS.items():
            self.tree.tag_configure(category, background=color, foreground="black")

        self.total_label.config(text=f"💰 Total: ₹{total:.2f}")

    def add_expense(self):
        """Adds a single expense entry from the input fields."""
        date_val = self.date_entry.get()
        category = self.category_entry.get()
        amount = self.amount_entry.get()
        description = self.desc_entry.get()
        current_month = date.today().strftime('%Y-%m')
        total = db.get_month_total(current_month)
        target = float(self.monthly_target_entry.get() or 0)
        if total > target:
         messagebox.showwarning("⚠️ Target Exceeded", f"You have exceeded your monthly target of ₹{target:.2f}")


        if not all([date_val, category, amount]):
            messagebox.showerror("❌ Error", "Date, Category, and Amount are required.")
            return

        try:
            amount_float = float(amount)
        except ValueError:
            messagebox.showerror("❌ Error", "Amount must be numeric.")
            return

        db.add_expense(date_val, category, amount_float, description)
        db.save_setting("monthly_target", self.monthly_target_entry.get())
        messagebox.showinfo("✅ Success", "Expense added.")
        self.clear_entries()
        self.load_expenses()

    def delete_expense(self):
        """Deletes the selected expense from the treeview."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("⚠️ Error", "Select an expense to delete.")
            return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected expense?"):
            expense_id = self.tree.item(selected, "values")[0]
            db.delete_expense(expense_id)
            messagebox.showinfo("🗑️ Deleted", "Expense removed.")
            self.load_expenses()

    def delete_all_expenses(self):
        """Deletes all expense records after confirmation."""
        if messagebox.askyesno("Delete All", "Are you sure you want to delete ALL expenses? This action cannot be undone."):
            db.delete_all_expenses()
            messagebox.showinfo("🗑️ Deleted", "All expenses removed.")
            self.load_expenses()


    def clear_entries(self):
        """Clears the input fields after adding an expense."""
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, date.today().strftime("%Y-%m-%d"))
        self.category_entry.set("")
        self.amount_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)

    def bulk_upload(self):
        """Handles bulk CSV upload and refreshes the display correctly."""
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not file_path:
            return
        try:
            with open(file_path, newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                # Skip header if present
                header = next(reader)
                for row in reader:
                    # FIX: Unpack row correctly, ignoring the first ID column
                    if len(row) < 4: continue
                    _, date_val, category, amount, *desc = row
                    description = desc[0] if desc else ""
                    try:
                        db.add_expense(date_val, category, float(amount), description)
                    except ValueError:
                        print(f"Skipping row with invalid amount: {row}")
                        continue
            
            messagebox.showinfo("✅ Uploaded", "CSV data uploaded successfully.")
            self.search_var.set("")
            self.load_expenses()
        except Exception as e:
            messagebox.showerror("❌ Error", f"Failed to upload file:\n{e}")

    def view_stats(self):
        expenses = db.get_expenses()
        if not expenses:
            messagebox.showinfo("No Data", "No expenses to generate statistics for.")
            return

        #df = pd.DataFrame(expenses, columns=['ID', 'Date', 'Category', 'Amount', 'Description'])
        #df['Date'] = pd.to_datetime(df['Date'])

        stats_window = tk.Toplevel(self.root)
        stats_window.title("\U0001F4C8 Expense Statistics")
        stats_window.geometry("1000x700")

        option = tk.StringVar(value="Category")
        axis_frame = ttk.Frame(stats_window)
        axis_frame.pack(fill="x", pady=10)
        ttk.Label(axis_frame, text="Select Axis:").pack(side="left", padx=10)
        axis_menu = ttk.OptionMenu(axis_frame, option, "Category", "Category", "Date", "Month")
        axis_menu.pack(side="left")
        ttk.Label(axis_frame, text="From:").pack(side="left", padx=5)
        from_date = DateEntry(axis_frame, width=10, date_pattern='yyyy-mm-dd')
        from_date.pack(side="left")
        ttk.Label(axis_frame, text="To:").pack(side="left", padx=5)
        to_date = DateEntry(axis_frame, width=10, date_pattern='yyyy-mm-dd')
        to_date.pack(side="left")

        canvas_frame = ttk.Frame(stats_window)
        canvas_frame.pack(fill="both", expand=True)

        def plot_graph():
            df = pd.DataFrame(expenses, columns=['ID', 'Date', 'Category', 'Amount', 'Description'])
            df['Date'] = pd.to_datetime(df['Date'])
            
            # Fix for date range filtering
            start = pd.to_datetime(from_date.get_date()) # Use .get_date()
            # Set end date to the end of the day
            end = pd.to_datetime(to_date.get_date()) + timedelta(days=1) - timedelta(microseconds=1)
            
            filtered_df = df[(df['Date'] >= start) & (df['Date'] <= end)]
            if filtered_df.empty:
               messagebox.showinfo("No Data", "No expenses in selected range.")
               return

            df = filtered_df


            for widget in canvas_frame.winfo_children():
                widget.destroy()

            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

            if option.get() == "Category":
                data_group = df.groupby('Category')['Amount'].sum().sort_values(ascending=False)
                colors = [CATEGORY_COLORS.get(cat, "#c9c9c9") for cat in data_group.index]
                data_group.plot(kind='bar', ax=ax1, color=colors)
                ax1.set_title('Total Spending by Category')
                ax1.set_ylabel('Amount (INR)')
                ax1.tick_params(axis='x', rotation=45)
                ax2.pie(data_group, labels=data_group.index, autopct='%1.1f%%', startangle=140, colors=colors)
                ax2.set_title('Expense Distribution')
                ax2.axis('equal')
            elif option.get() == "Date":
                data_group = df.groupby(df['Date'].dt.date)['Amount'].sum()
                data_group.plot(kind='bar', ax=ax1, color="#4a90e2")
                ax1.set_title('Total Spending by Date')
                ax1.set_ylabel('Amount (INR)')
                ax1.tick_params(axis='x', rotation=45)
                ax2.plot(data_group.index, data_group.values, marker='o', linestyle='-', color="#4a90e2")
                ax2.set_title('Spending Over Time')
                ax2.set_xlabel('Date')
                ax2.set_ylabel('Amount')
            else:
                df['Month'] = df['Date'].dt.to_period('M')
                data_group = df.groupby('Month')['Amount'].sum()
                data_group.index = data_group.index.astype(str)
                data_group.plot(kind='bar', ax=ax1, color="#ffb347")
                ax1.set_title('Total Spending by Month')
                ax1.set_ylabel('Amount (INR)')
                ax1.tick_params(axis='x', rotation=45)
                ax2.plot(data_group.index, data_group.values, marker='o', linestyle='-', color="#ffb347")
                ax2.set_title('Monthly Expense Trend')
                ax2.set_xlabel('Month')
                ax2.set_ylabel('Amount')

            plt.tight_layout()
            canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        ttk.Button(axis_frame, text="Generate Graphs", command=plot_graph).pack(side="left", padx=10)
        plot_graph()


if __name__ == "__main__":
    root = tk.Tk()
    # Note: For the theme toggle icons to work, you need 'light_mode.png' and 'dark_mode.png'
    # in the same directory, or you can replace the image with text="Toggle Theme".
    app = ExpenseTrackerApp(root)
    root.mainloop()

'''
# app.py
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from datetime import date, datetime, timedelta # Ensure timedelta is imported
import csv
import database as db
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from tkcalendar import DateEntry

# Define colors for categories for consistent styling in charts and the treeview
CATEGORY_COLORS = {
    "Food": "#ff9999", "Transport": "#66b3ff", "Bills": "#99ff99",
    "Shopping": "#ffcc99", "Health": "#c2c2f0", "Entertainment": "#ffb3e6",
    "Other": "#c9c9c9"
}

class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("💼 Personal Expense Tracker")
        self.root.geometry("1000x620")

        db.initialize_db()

        # Load theme from DB, default to 'light' if not set
        self.theme = tk.StringVar(value=db.load_setting('theme') or 'light')

        # --- FIX: Define icons BEFORE they are used in apply_theme ---
        try:
            self.light_icon = tk.PhotoImage(file="light_mode.png")
            self.dark_icon = tk.PhotoImage(file="dark_mode.png")
            self.use_icons = True
        except tk.TclError:
            # This will run if the image files are not found
            self.use_icons = False
            print("Warning: Theme icon images not found. Falling back to text button.")

        self.setup_styles()
        self.apply_theme() # Apply loaded theme on startup

        header = ttk.Frame(self.root, style="Header.TFrame")
        header.pack(fill="x", pady=(0, 10), ipady=5)
        ttk.Label(header, text="💼 Expense Tracker", font=("Segoe UI", 18, "bold"), style="Header.TLabel").pack(side="left", padx=20)
        
        # Using an image for the theme toggle button if available
        if self.use_icons:
            self.theme_button = ttk.Button(header, image=self.light_icon, command=self.toggle_theme, style="Header.TButton")
        else:
            # Fallback to a text button if icons failed to load
            self.theme_button = ttk.Button(header, text="Toggle Theme", command=self.toggle_theme)
        self.theme_button.pack(side="right", padx=20)


        input_frame = ttk.LabelFrame(self.root, text="➕ Add New Expense", padding=15)
        input_frame.pack(padx=20, pady=10, fill="x")

        action_frame = ttk.Frame(self.root)
        action_frame.pack(padx=20, pady=5, fill="x")

        display_frame = ttk.LabelFrame(self.root, text="📊 Expense History", padding=10)
        display_frame.pack(padx=20, pady=10, fill="both", expand=True)

        # --- Input Widgets ---
        ttk.Label(input_frame, text="📅 Date:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.date_entry = ttk.Entry(input_frame)
        self.date_entry.insert(0, date.today().strftime("%Y-%m-%d"))
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="📂 Category:").grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.category_entry = ttk.Combobox(input_frame, values=list(CATEGORY_COLORS.keys()), state="readonly")
        self.category_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(input_frame, text="💵 Amount:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.amount_entry = ttk.Entry(input_frame)
        self.amount_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="📝 Description:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.desc_entry = ttk.Entry(input_frame)
        self.desc_entry.grid(row=1, column=3, padx=5, pady=5)

        ttk.Label(input_frame, text="🎯 Monthly Target:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.monthly_target_entry = ttk.Entry(input_frame)
        self.monthly_target_entry.grid(row=3, column=1, padx=5, pady=5)
        self.monthly_target_entry.insert(0, db.load_setting("monthly_target") or "0")


        # --- Action Buttons ---
        ttk.Button(input_frame, text="Add Expense", command=self.add_expense).grid(row=2, column=0, pady=10)
        ttk.Button(input_frame, text="Delete Selected", command=self.delete_expense).grid(row=2, column=1, pady=10)
        ttk.Button(input_frame, text="🗑️ Delete All", command=self.delete_all_expenses).grid(row=2, column=3, pady=10)
        ttk.Button(input_frame, text="📈 View Statistics", command=self.view_stats).grid(row=2, column=2, pady=10)

        # --- Search and Data Actions ---
        ttk.Label(action_frame, text="🔍 Search Category:").pack(side="left", padx=5)
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(action_frame, textvariable=self.search_var)
        self.search_entry.pack(side="left", padx=5)
        self.search_entry.bind("<KeyRelease>", self.load_expenses)

        ttk.Button(input_frame, text="📤 Bulk Upload CSV", command=self.bulk_upload).grid(row=3, column=2, pady=10)
        self.total_label = ttk.Label(action_frame, text="💰 Total: ₹0.00", font=("Segoe UI", 10, "bold"))
        self.total_label.pack(side="right", padx=10)

        # --- Treeview Display ---
        self.tree = ttk.Treeview(display_frame, columns=("ID", "Date", "Category", "Amount", "Description"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Amount", text="Amount")
        self.tree.heading("Description", text="Description")
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Date", width=100, anchor="center")
        self.tree.column("Category", width=120, anchor="center")
        self.tree.column("Amount", width=100, anchor="e")
        self.tree.column("Description", width=350)
        self.tree.pack(fill="both", expand=True)

        self.load_expenses()

    def setup_styles(self):
        self.style = ttk.Style(self.root)
        self.style.theme_use("clam")

    def apply_theme(self):
        """Applies the selected theme to all widgets."""
        is_dark = self.theme.get() == 'dark'
        
        # Colors
        bg_color = "#2e2e2e" if is_dark else "#f7f9fc"
        fg_color = "white" if is_dark else "black"
        header_bg = "#3a3a3a" if is_dark else "#e1e1e1"
        tree_bg = "#3a3a3a" if is_dark else "white"
        tree_fg = "white" if is_dark else "black"
        tree_heading_bg = "#555555" if is_dark else "#4a90e2"

        self.root.configure(bg=bg_color)
        
        # Style configurations
        self.style.configure("TFrame", background=bg_color)
        self.style.configure("TLabel", background=bg_color, foreground=fg_color, font=("Segoe UI", 10))
        self.style.configure("Header.TFrame", background=header_bg)
        self.style.configure("Header.TLabel", background=header_bg, foreground=fg_color)
        self.style.configure("Header.TButton", background=header_bg)
        self.style.configure("TLabelFrame", background=bg_color, foreground=fg_color)
        self.style.configure("TLabelFrame.Label", background=bg_color, foreground=fg_color)
        self.style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6)
        
        # Treeview Style
        self.style.configure("Treeview", font=("Segoe UI", 10), rowheight=28, background=tree_bg, foreground=tree_fg, fieldbackground=tree_bg)
        self.style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"), background=tree_heading_bg, foreground="white")
        self.style.map('Treeview', background=[('selected', '#555555' if is_dark else '#4a90e2')])
        
        # Update theme toggle icon if icons are being used
        if self.use_icons:
            icon = self.dark_icon if is_dark else self.light_icon
            self.theme_button.configure(image=icon)

    def toggle_theme(self):
        """Toggles the theme and saves the setting."""
        if self.theme.get() == 'light':
            self.theme.set('dark')
        else:
            self.theme.set('light')
        
        self.apply_theme()
        db.save_setting('theme', self.theme.get())

    def load_expenses(self, event=None):
        search_term = self.search_var.get().lower()
        self.tree.delete(*self.tree.get_children())
        total = 0.0

        for expense in db.get_expenses():
            if search_term and search_term not in expense[2].lower():
                continue
            
            category = expense[2]
            self.tree.insert("", "end", values=expense, tags=(category,))
            total += float(expense[3])
        
        # Apply category colors
        for category, color in CATEGORY_COLORS.items():
            self.tree.tag_configure(category, background=color, foreground="black")

        self.total_label.config(text=f"💰 Total: ₹{total:.2f}")

    def add_expense(self):
        """Adds a single expense entry from the input fields."""
        date_val = self.date_entry.get()
        category = self.category_entry.get()
        amount = self.amount_entry.get()
        description = self.desc_entry.get()
        current_month = date.today().strftime('%Y-%m')
        total = db.get_month_total(current_month)
        target = float(self.monthly_target_entry.get() or 0)
        if total > target:
            messagebox.showwarning("⚠️ Target Exceeded", f"You have exceeded your monthly target of ₹{target:.2f}")


        if not all([date_val, category, amount]):
            messagebox.showerror("❌ Error", "Date, Category, and Amount are required.")
            return

        try:
            amount_float = float(amount)
        except ValueError:
            messagebox.showerror("❌ Error", "Amount must be numeric.")
            return

        db.add_expense(date_val, category, amount_float, description)
        db.save_setting("monthly_target", self.monthly_target_entry.get())
        messagebox.showinfo("✅ Success", "Expense added.")
        self.clear_entries()
        self.load_expenses()

    def delete_expense(self):
        """Deletes the selected expense from the treeview."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("⚠️ Error", "Select an expense to delete.")
            return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected expense?"):
            expense_id = self.tree.item(selected, "values")[0]
            db.delete_expense(expense_id)
            messagebox.showinfo("🗑️ Deleted", "Expense removed.")
            self.load_expenses()

    def delete_all_expenses(self):
        """Deletes all expense records after confirmation."""
        if messagebox.askyesno("Delete All", "Are you sure you want to delete ALL expenses? This action cannot be undone."):
            db.delete_all_expenses()
            messagebox.showinfo("🗑️ Deleted", "All expenses removed.")
            self.load_expenses()


    def clear_entries(self):
        """Clears the input fields after adding an expense."""
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, date.today().strftime("%Y-%m-%d"))
        self.category_entry.set("")
        self.amount_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)

    def bulk_upload(self):
        """Handles bulk CSV upload and refreshes the display correctly."""
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not file_path:
            return
        try:
            with open(file_path, newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                # Skip header if present
                header = next(reader)
                for row in reader:
                    if len(row) < 4: continue
                    _, date_val, category, amount, *desc = row
                    description = desc[0] if desc else ""
                    try:
                        db.add_expense(date_val, category, float(amount), description)
                    except ValueError:
                        print(f"Skipping row with invalid amount: {row}")
                        continue
            
            messagebox.showinfo("✅ Uploaded", "CSV data uploaded successfully.")
            self.search_var.set("")
            self.load_expenses()
        except Exception as e:
            messagebox.showerror("❌ Error", f"Failed to upload file:\n{e}")

    def view_stats(self):
        expenses = db.get_expenses()
        if not expenses:
            messagebox.showinfo("No Data", "No expenses to generate statistics for.")
            return

        # Prepare DataFrame to determine min/max dates
        df_all = pd.DataFrame(expenses, columns=['ID', 'Date', 'Category', 'Amount', 'Description'])
        df_all['Date'] = pd.to_datetime(df_all['Date'])

        # Determine the earliest and latest dates from actual expenses
        # Provide sensible defaults if df_all is empty (though checked above)
        earliest_expense_date = df_all['Date'].min().date() if not df_all.empty else date.today().replace(day=1)
        latest_expense_date = df_all['Date'].max().date() if not df_all.empty else date.today()
        
        print(f"Data date range: {earliest_expense_date} to {latest_expense_date}")

        stats_window = tk.Toplevel(self.root)
        stats_window.title("📈 Expense Statistics")
        stats_window.geometry("1000x700")

        option = tk.StringVar(value="Category")
        axis_frame = ttk.Frame(stats_window)
        axis_frame.pack(fill="x", pady=10)
        ttk.Label(axis_frame, text="Select Axis:").pack(side="left", padx=10)
        axis_menu = ttk.OptionMenu(axis_frame, option, "Category", "Category", "Date", "Month")
        axis_menu.pack(side="left")
        
        ttk.Label(axis_frame, text="From:").pack(side="left", padx=5)
        # Initialize with the earliest expense date found
        from_date_cal = DateEntry(axis_frame, width=10, date_pattern='yyyy-mm-dd',
                                  setweektoday=False, initialdate=earliest_expense_date)
        from_date_cal.pack(side="left")
        
        ttk.Label(axis_frame, text="To:").pack(side="left", padx=5)
        # Initialize with the latest expense date found
        to_date_cal = DateEntry(axis_frame, width=10, date_pattern='yyyy-mm-dd',
                                setweektoday=False, initialdate=latest_expense_date)
        to_date_cal.pack(side="left")

        canvas_frame = ttk.Frame(stats_window)
        canvas_frame.pack(fill="both", expand=True)

        def plot_graph():
            df = df_all.copy() # Use the full DataFrame for filtering

            # Get dates from the calendar widgets
            start_date_selected = from_date_cal.get_date()
            end_date_selected = to_date_cal.get_date()

            # Validate date range
            if start_date_selected > end_date_selected:
                messagebox.showerror("Invalid Date Range", "Start date cannot be after end date.")
                return

            # FIXED: Proper date filtering - convert to datetime for comparison
            start_datetime = pd.to_datetime(start_date_selected)
            end_datetime = pd.to_datetime(end_date_selected) + pd.Timedelta(days=1) - pd.Timedelta(microseconds=1)
            
            print(f"Filtering from: {start_datetime} to: {end_datetime}") # Debugging print
            print(f"Date range in data: {df['Date'].min()} to {df['Date'].max()}")
            
            # Filter the dataframe
            filtered_df = df[(df['Date'] >= start_datetime) & (df['Date'] <= end_datetime)]
            
            print(f"Filtered data count: {len(filtered_df)} out of {len(df)} total records")

            if filtered_df.empty:
                # More helpful error message
                messagebox.showinfo("No Data", 
                    f"No expenses found between {start_date_selected} and {end_date_selected}.\n\n"
                    f"Your expense data covers: {earliest_expense_date} to {latest_expense_date}\n\n"
                    f"Please select a date range within your data range or use 'Reset to All Data'.")
                for widget in canvas_frame.winfo_children():
                    widget.destroy()
                return

            df = filtered_df # Use the filtered DataFrame for plotting

            for widget in canvas_frame.winfo_children():
                widget.destroy()

            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

            if option.get() == "Category":
                data_group = df.groupby('Category')['Amount'].sum().sort_values(ascending=False)
                colors = [CATEGORY_COLORS.get(cat, "#c9c9c9") for cat in data_group.index]
                data_group.plot(kind='bar', ax=ax1, color=colors)
                ax1.set_title('Total Spending by Category')
                ax1.set_ylabel('Amount (INR)')
                ax1.tick_params(axis='x', rotation=45)
                ax2.pie(data_group, labels=data_group.index, autopct='%1.1f%%', startangle=140, colors=colors)
                ax2.set_title('Expense Distribution')
                ax2.axis('equal')
            elif option.get() == "Date":
                data_group = df.groupby(df['Date'].dt.date)['Amount'].sum().sort_index()
                data_group.plot(kind='bar', ax=ax1, color="#4a90e2")
                ax1.set_title('Total Spending by Date')
                ax1.set_ylabel('Amount (INR)')
                ax1.tick_params(axis='x', rotation=45)
                ax2.plot(data_group.index, data_group.values, marker='o', linestyle='-', color="#4a90e2")
                ax2.set_title('Spending Over Time')
                ax2.set_xlabel('Date')
                ax2.set_ylabel('Amount')
                ax2.tick_params(axis='x', rotation=45)
            else: # Monthly view
                df['Month'] = df['Date'].dt.to_period('M')
                data_group = df.groupby('Month')['Amount'].sum().sort_index()
                data_group.index = data_group.index.astype(str)
                data_group.plot(kind='bar', ax=ax1, color="#ffb347")
                ax1.set_title('Total Spending by Month')
                ax1.set_ylabel('Amount (INR)')
                ax1.tick_params(axis='x', rotation=45)
                ax2.plot(data_group.index, data_group.values, marker='o', linestyle='-', color="#ffb347")
                ax2.set_title('Monthly Expense Trend')
                ax2.set_xlabel('Month')
                ax2.set_ylabel('Amount')
                ax2.tick_params(axis='x', rotation=45)

            plt.tight_layout()
            canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Add refresh button to regenerate graph with new date range
        ttk.Button(axis_frame, text="Generate Graphs", command=plot_graph).pack(side="left", padx=10)
        
        # Add a reset button to show all data
        def reset_dates():
            from_date_cal.set_date(earliest_expense_date)
            to_date_cal.set_date(latest_expense_date)
            plot_graph()
        
        ttk.Button(axis_frame, text="Reset to All Data", command=reset_dates).pack(side="left", padx=5)
        
        plot_graph() # Initial plot when the window opens


if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()