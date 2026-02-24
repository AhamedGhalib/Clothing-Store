import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import datetime

class ClothingStoreApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GRAAF Clothing Management System")
        self.root.geometry("1300x800")
        
        self.db = self.connect_db()
        if not self.db:
            messagebox.showerror("Connection Error", "Could not connect to MySQL database.")
            self.root.destroy()
            return
        self.cursor = self.db.cursor()

        # --- GLOBAL STYLING ---
        self.style = ttk.Style()
        self.style.theme_use("clam") 
        self.style.configure("Treeview.Heading", font=("Arial", 10, "bold"), background="#ecf0f1", relief="flat")
        self.style.configure("Treeview", rowheight=25, font=("Arial", 10), borderwidth=0)

        self.setup_sidebar()
        self.content_frame = tk.Frame(self.root, bg="white")
        self.content_frame.pack(side="right", fill="both", expand=True)
        self.show_inventory() 

    def connect_db(self):
        try:
            return mysql.connector.connect(
                host="localhost", user="root", password="ace242633",
                database="clothing_store", auth_plugin="mysql_native_password"
            )
        except mysql.connector.Error as err:
            return None

    def setup_sidebar(self):
        sidebar = tk.Frame(self.root, bg="#2c3e50", width=250)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        tk.Label(sidebar, text="GRAAF MENU", font=("Arial", 16, "bold"), bg="#2c3e50", fg="white", pady=30).pack()
        btns = [("Billing", self.show_billing), ("Inventory", self.show_inventory), 
                ("Sales Report", self.show_profit), ("Exit", self.root.quit)]
        for text, cmd in btns:
            tk.Button(sidebar, text=text, command=cmd, font=("Arial", 12), bg="#34495e", 
                      fg="white", bd=0, pady=15).pack(fill="x", padx=10, pady=5)

    def clear_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    # --- INVENTORY SECTION ---
    def show_inventory(self):
        self.clear_frame()
        tk.Label(self.content_frame, text="Inventory Management", font=("Arial", 18, "bold"), bg="white").pack(pady=10)
        top_ctrl = tk.Frame(self.content_frame, bg="white")
        top_ctrl.pack(fill="x", padx=20, pady=5)
        
        btn_frame = tk.Frame(top_ctrl, bg="white")
        btn_frame.pack(side="left")
        tk.Button(btn_frame, text="+ Add Stock", command=self.add_stock_window, bg="#27ae60", fg="white").pack(side="left", padx=2)
        tk.Button(btn_frame, text="Update Stock", command=self.update_stock_window, bg="#f39c12", fg="white").pack(side="left", padx=2)
        tk.Button(btn_frame, text="Delete Selected", command=self.delete_stock, bg="#e74c3c", fg="white").pack(side="left", padx=2)
        
        table_border_frame = tk.Frame(self.content_frame, bg="white", highlightthickness=1, highlightbackground="#bdc3c7")
        table_border_frame.pack(fill="both", expand=True, padx=20, pady=10)
        self.tree = ttk.Treeview(table_border_frame, columns=("ID", "Brand", "Category", "Size", "Price", "Stock"), show="headings")
        for col in ("ID", "Brand", "Category", "Size", "Price", "Stock"):
            self.tree.heading(col, text=col); self.tree.column(col, width=100, anchor="center")
        self.tree.pack(fill="both", expand=True)
        
        self.cursor.execute("SELECT id, brand, category, size, sell_price, stock_quantity FROM inventory")
        for row in self.cursor.fetchall():
            f_row = list(row); f_row[4] = f"₹{float(row[4]):,.2f}"; self.tree.insert("", "end", values=f_row)

    def add_stock_window(self):
        win = tk.Toplevel(self.root); win.title("Add New Stock"); win.geometry("500x350")
        form_frame = tk.Frame(win, padx=20, pady=20)
        form_frame.pack(fill="both", expand=True)
        categories = ["Shirt", "T-Shirts", "Pants", "Jeans", "Shoes"]
        sizes = ["S", "M", "L", "XL"]
        ents = {}
        
        tk.Label(form_frame, text="Brand:").grid(row=0, column=0, sticky="w", pady=5)
        ents["Brand"] = tk.Entry(form_frame); ents["Brand"].grid(row=0, column=1, padx=10, pady=5)
        tk.Label(form_frame, text="Category:").grid(row=0, column=2, sticky="w", pady=5)
        ents["Category"] = ttk.Combobox(form_frame, values=categories, state="readonly"); ents["Category"].grid(row=0, column=3, padx=10, pady=5)
        tk.Label(form_frame, text="Cost Price:").grid(row=1, column=0, sticky="w", pady=5)
        ents["Cost"] = tk.Entry(form_frame); ents["Cost"].grid(row=1, column=1, padx=10, pady=5)
        tk.Label(form_frame, text="Quantity:").grid(row=1, column=2, sticky="w", pady=5)
        ents["Stock"] = tk.Entry(form_frame); ents["Stock"].grid(row=1, column=3, padx=10, pady=5)
        tk.Label(form_frame, text="Sell Price:").grid(row=2, column=0, sticky="w", pady=5)
        ents["Price"] = tk.Entry(form_frame); ents["Price"].grid(row=2, column=1, padx=10, pady=5)
        tk.Label(form_frame, text="Size:").grid(row=2, column=2, sticky="w", pady=5)
        ents["Size"] = ttk.Combobox(form_frame, values=sizes, state="readonly"); ents["Size"].grid(row=2, column=3, padx=10, pady=5)

        def save():
            try:
                d = (ents["Brand"].get(), ents["Category"].get(), ents["Size"].get(), ents["Cost"].get(), ents["Price"].get(), ents["Stock"].get())
                self.cursor.execute("INSERT INTO inventory (brand,category,size,cost_price,sell_price,stock_quantity) VALUES (%s,%s,%s,%s,%s,%s)", d)
                self.db.commit(); win.destroy(); self.show_inventory()
            except Exception as e: messagebox.showerror("Error", str(e))
        tk.Button(win, text="SAVE STOCK", command=save, bg="#27ae60", fg="white", font=("Arial", 10, "bold"), pady=10, padx=40).pack(pady=20)

    def update_stock_window(self):
        sel = self.tree.selection()
        if not sel: return
        item = self.tree.item(sel)['values']
        win = tk.Toplevel(self.root); win.geometry("250x200")
        tk.Label(win, text="New Price:").pack()
        p_ent = tk.Entry(win); p_ent.insert(0, item[4].replace("₹", "").replace(",", "")); p_ent.pack()
        tk.Label(win, text="New Stock:").pack()
        s_ent = tk.Entry(win); s_ent.insert(0, item[5]); s_ent.pack()
        def update():
            self.cursor.execute("UPDATE inventory SET sell_price=%s, stock_quantity=%s WHERE id=%s", (p_ent.get(), s_ent.get(), item[0]))
            self.db.commit(); win.destroy(); self.show_inventory()
        tk.Button(win, text="Update", command=update, bg="#f39c12", fg="white").pack(pady=10)

    def delete_stock(self):
        sel = self.tree.selection()
        if not sel: return
        if messagebox.askyesno("Confirm", "Delete this item?"):
            self.cursor.execute("DELETE FROM inventory WHERE id = %s", (self.tree.item(sel)['values'][0],))
            self.db.commit(); self.show_inventory()

    # --- BILLING SECTION ---
    def show_billing(self):
        self.clear_frame()
        self.cart = []; self.grand_total = 0; self.total_qty = 0
        tk.Label(self.content_frame, text="Billing Dashboard", font=("Arial", 18, "bold"), bg="white").pack(pady=10)

        # Input Controls
        input_ctrl = tk.Frame(self.content_frame, bg="white")
        input_ctrl.pack(fill="x", padx=20, pady=10)
        self.cursor.execute("SELECT id, brand, category, size FROM inventory")
        opts = [f"{r[0]}: {r[1]} {r[2]} ({r[3]})" for r in self.cursor.fetchall()]
        self.drop = ttk.Combobox(input_ctrl, values=opts, font=("Arial", 12), width=45, state="readonly"); self.drop.pack(side="left", padx=5)
        self.qty_ent = tk.Entry(input_ctrl, font=("Arial", 12), width=10, justify="center"); self.qty_ent.insert(0, "1"); self.qty_ent.pack(side="left", padx=5)
        tk.Button(input_ctrl, text="ADD TO CART", command=self.add_to_cart, bg="#3498db", fg="white", font=("Arial", 10, "bold"), padx=15, pady=5).pack(side="left")

        # Main Split
        main_billing_split = tk.Frame(self.content_frame, bg="white")
        main_billing_split.pack(fill="both", expand=True, padx=20, pady=10)

        # 1. Cart Table (Left)
        table_panel = tk.Frame(main_billing_split, bg="white", highlightthickness=1, highlightbackground="#bdc3c7")
        table_panel.pack(side="left", fill="both", expand=True)
        self.bill_tree = ttk.Treeview(table_panel, columns=("Item", "Qty", "Total"), show="headings")
        for col in ("Item", "Qty", "Total"): 
            self.bill_tree.heading(col, text=col); self.bill_tree.column(col, anchor="center", stretch=True) 
        self.bill_tree.pack(fill="both", expand=True)

        # 2. Summary Panel (Right)
        summary_panel = tk.Frame(main_billing_split, bg="#f8f9fa", width=325, padx=20, pady=25)
        summary_panel.pack(side="right", fill="y"); summary_panel.pack_propagate(False)

        tk.Label(summary_panel, text="ORDER SUMMARY", font=("Arial", 14, "bold"), bg="#f8f9fa", pady=20).pack()
        self.lbl_qty = tk.Label(summary_panel, text="Total Items: 0", font=("Arial", 12), bg="#f8f9fa", pady=10)
        self.lbl_qty.pack()
        self.lbl_total = tk.Label(summary_panel, text="Grand Total:\n₹0.00", font=("Arial", 22, "bold"), fg="green", bg="#f8f9fa", justify="center", pady=20)
        self.lbl_total.pack()
        
        # Checkout and Print Buttons
        tk.Button(summary_panel, text="CONFIRM & PAY", command=self.checkout, bg="#27ae60", fg="white", font=("Arial", 12, "bold"), pady=15).pack(fill="x", pady=5)
        tk.Button(summary_panel, text="🖨️ PRINT RECEIPT", command=self.process_and_print_bill, bg="#34495e", fg="white", font=("Arial", 12, "bold"), pady=15).pack(fill="x", pady=5)

    def add_to_cart(self):
        try:
            p_id = int(self.drop.get().split(":")[0]); qty = int(self.qty_ent.get())
            self.cursor.execute("SELECT brand, category, stock_quantity, cost_price, sell_price FROM inventory WHERE id=%s", (p_id,))
            res = self.cursor.fetchone()
            if res and int(res[2]) >= qty:
                total = float(res[4]) * qty
                self.cart.append({'id': p_id, 'brand': res[0], 'cat': res[1], 'qty': qty, 'total': total, 'profit': (float(res[4])-float(res[3]))*qty})
                self.bill_tree.insert("", "end", values=(f"{res[0]} {res[1]}", qty, f"₹{total:,.2f}"))
                self.grand_total += total; self.total_qty += qty
                self.lbl_total.config(text=f"Grand Total:\n₹{self.grand_total:,.2f}")
                self.lbl_qty.config(text=f"Total Items: {self.total_qty}")
            else: messagebox.showwarning("Stock", "Not enough stock!")
        except: pass

    def checkout(self):
        if not self.cart: return
        try:
            for item in self.cart:
                self.cursor.execute("UPDATE inventory SET stock_quantity = stock_quantity - %s WHERE id = %s", (item['qty'], item['id']))
                self.cursor.execute("INSERT INTO sales (product_id, brand, category, quantity, total_price, profit) VALUES (%s,%s,%s,%s,%s,%s)", 
                                    (item['id'], item['brand'], item['cat'], item['qty'], item['total'], item['profit']))
            self.db.commit(); messagebox.showinfo("Success", "Paid!"); self.show_billing()
        except Exception as e: self.db.rollback(); messagebox.showerror("Error", str(e))

    def process_and_print_bill(self):
        if not self.cart: return
        try:
            for item in self.cart:
                self.cursor.execute("UPDATE inventory SET stock_quantity = stock_quantity - %s WHERE id = %s", (item['qty'], item['id']))
                self.cursor.execute("INSERT INTO sales (product_id, brand, category, quantity, total_price, profit) VALUES (%s,%s,%s,%s,%s,%s)", 
                                    (item['id'], item['brand'], item['cat'], item['qty'], item['total'], item['profit']))
            self.db.commit()
            
            bill_win = tk.Toplevel(self.root); bill_win.title("GRAAF Receipt"); bill_win.geometry("380x600")
            txt = tk.Text(bill_win, font=("Courier", 10), padx=10, pady=10); txt.pack(fill="both", expand=True)
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            header = f"{'GRAAF CLOTHING':^40}\n{'Style & Comfort':^40}\n" + "="*40 + f"\nDate: {now}\n" + "="*40 + f"\n{'Item':<20} {'Qty':<5} {'Total':>12}\n" + "-"*40 + "\n"
            body = "".join([f"{f'{i['brand']} {i['cat']}'[:19]:<20} {i['qty']:<5} {f'₹{i['total']:,.2f}':>12}\n" for i in self.cart])
            footer = "-"*40 + f"\n{'TOTAL ITEMS:':<20} {self.total_qty:<5}\n{'GRAND TOTAL:':<20} {f'₹{self.grand_total:,.2f}':>18}\n" + "="*40 + f"\n{'THANK YOU FOR SHOPPING!':^40}\n"
            txt.insert("1.0", header + body + footer); txt.config(state="disabled")
            self.show_billing()
        except Exception as e: self.db.rollback(); messagebox.showerror("Error", str(e))

    # --- SALES REPORT SECTION ---
    def show_profit(self):
        self.clear_frame()
        tk.Label(self.content_frame, text="Sales Report Dashboard", font=("Arial", 18, "bold"), bg="white").pack(pady=10)
        main_split = tk.Frame(self.content_frame, bg="white")
        main_split.pack(fill="both", expand=True, padx=20, pady=10)
        
        stats_panel = tk.Frame(main_split, bg="#f1f2f6", padx=20, pady=20, width=300); stats_panel.pack(side="left", fill="both"); stats_panel.pack_propagate(False)
        self.cursor.execute("SELECT SUM(total_price), SUM(profit), COUNT(sale_id) FROM sales")
        summary = self.cursor.fetchone()
        rev, prof, count = float(summary[0] or 0), float(summary[1] or 0), summary[2] or 0

        tk.Label(stats_panel, text="BUSINESS SUMMARY", font=("Arial", 12, "bold"), bg="#f1f2f6").pack(pady=10)
        tk.Label(stats_panel, text=f"Total Revenue\n₹{rev:,.2f}", font=("Arial", 14, "bold"), fg="#2980b9", bg="#f1f2f6").pack(pady=10)
        tk.Label(stats_panel, text=f"Total Profit\n₹{prof:,.2f}", font=("Arial", 14, "bold"), fg="#27ae60", bg="#f1f2f6").pack(pady=10)
        tk.Label(stats_panel, text=f"Orders: {count}", font=("Arial", 10), bg="#f1f2f6").pack(pady=20)

        table_panel = tk.Frame(main_split, bg="white", highlightthickness=1, highlightbackground="#bdc3c7"); table_panel.pack(side="right", fill="both", expand=True)
        tree = ttk.Treeview(table_panel, columns=("Date", "Item", "Total"), show="headings")
        for col in ("Date", "Item", "Total"): tree.heading(col, text=col); tree.column(col, anchor="center")
        tree.pack(fill="both", expand=True)
        self.cursor.execute("SELECT sale_date, brand, category, total_price FROM sales ORDER BY sale_date DESC")
        for s in self.cursor.fetchall(): tree.insert("", "end", values=(s[0].strftime("%m-%d %H:%M"), f"{s[1]} {s[2]}", f"₹{float(s[3]):,.2f}"))

if __name__ == "__main__":
    root = tk.Tk(); app = ClothingStoreApp(root); root.mainloop()