import mysql.connector

def connect_db():
    try:
        connect=mysql.connector.connect(
            host="localhost",
            user="root",
            password="ace242633",
            database="clothing_store"
        )
        return connect
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

db = connect_db()
cursor =  db.cursor()
print("Successfully connected to the Inventory Database!")

# View Inventory
def view_inventory():
    print("\n"+"="*80)
    print(" "*30 +"INVENTORY")
    print("="*80)

    cursor.execute("SELECT * from inventory")
    for row in cursor.fetchall():
        print(f"\n {row[0]} | {row[1]} | {row[2]} | {row[3]} || Cost: ₹{row[4]} | Price: ₹{row[5]} | Stock: {row[6]}")
    print("="*80)

# Add a Stock          
def add_inventory():
    while True:
        print("\n"+"="*80)
        print(" "*30 +"ADD STOCK")
        print("="*80)

        categories={
            1: "Shirt",
            2: "T-Shirts",
            3: "Pants",
            4: "Jeans",
            5: "Shoes"
        }
        
        size_categories={
            1: "S",
            2: "M",
            3: "L",
            4: "XL"
        }

        brand=input("Enter Brand Name: ")

        while True:
                print("\nSelect a Category: ")
                for key, value in categories.items():
                    print(f"{key}. {value}")

                try:
                    choice = int(input("Enter choice (1-5): "))
                    if choice in categories:
                        category = categories[choice]
                        break
                    else:
                        print("Invalid option. Please choose a number from the list. !!!")
                except ValueError:
                    print(" Invalid input. Please enter a number. !!!")
        
        while True:
                print("\nSelect Size: ")
                for key, value in size_categories.items():
                    print(f"{key}. {value}")

                try:
                    choice = int(input("Enter choice (1-5): "))
                    if choice in size_categories:
                        size = size_categories[choice]
                        break
                    else:
                        print("Invalid option. Please choose a number from the list. !!!")
                except ValueError:
                    print(" Invalid input. Please enter a number. !!!")
        try:
            cost= int(input("Enter Cost Price: "))
            sell= int(input("Enter Selling Price: "))
        except ValueError:
            print("""\n Error!!!
                \n Price must be a number!!! """)
            return
        
        try:
            stock= int(input("Enter Initial Stock: "))
        except ValueError:
            print("""\n Error!!!
                \n Stock must be a number!!!""")
            return

    
        try:
            query = """insert into inventory (brand,category,size,cost_price,sell_price,stock_quantity)
            values(%s,%s,%s,%s,%s,%s)"""
            data = (brand,category,size,cost,sell,stock)
            cursor.execute(query,data)
            db.commit()
            print(f"\nSuccessfully added {brand} to Inventory!!!")
            print("="*80)
            
            view_inventory()

        except mysql.connector.Error as err:
            print(f"Databse Error: {err}")
        
        
        
        again = input("\nAdd another stock? (y/n): ").lower()
        if again != 'y':
            print("Returning to menu...")
            break

# Update a stock 
def update_inventory():
    view_inventory()
    
    while True:
        print("\n"+"="*80)
        print(" "*30 + "Update Stock")
        print("="*80)

        cursor.execute("SELECT id FROM inventory")
        valid_ids = [row[0] for row in cursor.fetchall()]

        try:
            product_id=int(input("\nSelect product to update: "))
            if product_id in valid_ids:

                change = int(input("\nEnter quantity change (use negative numbers for sales, e.g., -5): "))
            
                cursor.execute("SELECT brand,category,size,stock_quantity FROM inventory WHERE id = %s", (product_id,))
                result = cursor.fetchone()
            
                if result:
                    brand, category, size,stock_quantity = result
                    stock=int(stock_quantity)
                    query = "update inventory set stock_quantity= stock_quantity+%s where id= %s"
                    cursor.execute(query,(change,product_id))
                    db.commit()

                    print(f"\n[Success] Updated {brand},{category} (Size: {size}).")
                    print(f"New stock : {stock + change}")
                    
                print("="*80)
            
            else:
                print(f"\nNo item found with ID {product_id}!!!")

        except ValueError:
            print("Invalid input! Please enter a number for the ID.")
        except mysql.connector.Error as err:
            print(f"Databse Error: {err}")
        
        again = input("\nUpdate another stock? (y/n): ").lower()
        if again != 'y':
            print("Returning to menu...")
            break

# Delete a stock
def del_inventory():

    view_inventory()
    while True:
        print("\n"+"="*80)
        print(" "*30 + "REMOVE STOCK")
        print("="*80)

        product_id=int(input("Select stock to delete: "))

        try:

            cursor.execute("SELECT brand,category, size FROM inventory WHERE id = %s", (product_id,))
            result = cursor.fetchone()

            if result:
                brand, category, size = result
                query = "delete from inventory where id= %s"
                cursor.execute(query,(product_id,))
                db.commit()

            if cursor.rowcount > 0:
                print(f"\n[Success] Deleted {brand},{category} (Size:{size}) !!!")
            else:
                print(f"\nNo item found with ID {product_id}!!!")
            print("="*80)

        except ValueError:
            print("Invalid input! Please enter a number for the ID.")
        except mysql.connector.Error as err:
            print(f"Databse Error: {err}")
        view_inventory()

        again = input("\nDelete another stock? (y/n): ").lower()
        if again != 'y':
            print("Returning to menu...")
            break

# Inventory view for billing            
def product_list():
    print("\n"+"="*80)
    print(f"{'INVENTORY':^80}")
    print("="*80)


    cursor.execute("SELECT * from inventory")
    for row in cursor.fetchall():
        print(f"\n ID: {row[0]} | Name: {row[1]} | {row[2]} | Size: {row[3]} | Price: ₹{row[5]} | Stock: {row[6]}")
    print("="*80)

# Billing
def billing():
    print("\n" + "="*80)
    print(f"{'NEW BILL':^80}")
    print("="*80)

    cart = []
    grand_total = 0

    while True:

        product_list()

        cursor.execute("SELECT id FROM inventory")
        valid_ids = [row[0] for row in cursor.fetchall()]

        try:
            product_id = int(input("Enter Product ID being sold (or '0' to Exit): "))

            if product_id==0:
                break
            
            #check product id
            if product_id in valid_ids:
                qty = int(input("Enter Quantity: "))
                
                if qty <= 0:
                    print("!!! Error: Quantity must be positive.")
                    continue

                cursor.execute("SELECT brand, category, size,stock_quantity,cost_price,sell_price FROM inventory WHERE id = %s", (product_id,))
                result = cursor.fetchone()
                
                if result:
                    brand, category, size, stock_quantity,cost_price, price = result
                    cost=float(cost_price)
                    rate=float(price)

                    #Update inventory
                    if int(stock_quantity) >= qty:
                        update_query = "update inventory set stock_quantity= stock_quantity-%s where id= %s"
                        cursor.execute(update_query,(qty,product_id))

                        total_sales = rate * qty
                        total_cost = cost * qty
                        profit = total_sales - total_cost

                        grand_total += total_sales

                        #Sales Insert
                        sales_query = "INSERT INTO sales (product_id, brand,category, quantity, total_price,profit) VALUES (%s, %s, %s, %s, %s, %s)"
                        cursor.execute(sales_query, (product_id, brand,category, qty, total_sales, profit))
                        db.commit()

                        product_name = f"{brand} {category}"
                        cart.append([product_name, size, qty, rate, total_sales])

                        print(f"--> Added {qty} x {product_name} to cart.")
                        print(f"--> Grand Total: ₹{total_sales:.2f} | Profit: ₹{profit:.2f}")

                    else:
                        print(f"\n!!! INVALID QUANTITY !!!")
                        print(f"You only have {stock_quantity} in stock. Cannot sell {qty}.")
            else:
                print(f"\n Error!!!")
                print(f"\n No item found with ID {product_id}.")

        except ValueError:
            print("Invalid input! Please enter a number for the ID and qty.")
        except mysql.connector.Error as err:
            print(f"Databse Error: {err}")

    if cart:
        print("\n\n")
        print("="*50)
        print(f"{'RECEIPT':^50}")
        print("="*50)
        print(f"{'Item':<20} {'Size':<6} {'Qty':<5} {'Price':<10} {'Total':<10}")
        print("-" * 50)

        for item in cart:
            # [Name, Size, Qty, Price, Total]
            print(f"{item[0]:<20} {item[1]:<6} {item[2]:<5} ${item[3]:<9.2f} ${item[4]:<9.2f}")

        print("-" * 50)
        print(f"{'GRAND TOTAL:':<40} ${grand_total:.2f}")
        print("="*50)
        print("Thank you for shopping!\n")
    else:
        print("\nNo items purchased. Returning to menu...")

# Profit Report
def view_profit():
    print("\n\n")
    print("="*50)
    print(f"{'PROFIT REPORT':^50}")
    print("="*50)

    try:
        cursor.execute("SELECT SUM(total_price), SUM(profit) FROM sales")
        result = cursor.fetchone()

        if result and result[0] is not None:
            total_revenue = float(result[0])
            total_profit = float(result[1])

            print(f" TOTAL SALES REVENUE:  ₹{total_revenue:,.2f}")
            print(f" TOTAL NET PROFIT:     ₹{total_profit:,.2f}")
            
            #Profit Margin
            if total_revenue > 0:
                margin = (total_profit / total_revenue) * 100
                print("="*50)
                print(f" PROFIT MARGIN:        {margin:.1f}%")
        else:
            print(" No sales data found.")

    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
    
    print("="*50)
    input("\nPress Enter to go back...")

# Inventory Menu
def inventory():
    while True:
        print("\n"+"="*50)
        print(f"{'GRAAF CLOTHING INVENTORY':^50}")
        print("="*50)
        print("""
    1. View Inventory
    2. Add Stock
    3. Update Stock
    4. Delete Stock 
    5. Back to Main menu
        """)
        print("="*50)

        choice = input("Enter choice: ")

        if choice == "1":
            view_inventory()
        elif choice == "2":
            add_inventory()
        elif choice == "3":
            update_inventory()
        elif choice == "4":
            del_inventory()
        elif choice == "5":    
            break   
        else:
            print("Select an Option !!!")
        return

# Main Menu
while True:
    print("\n"+"="*50)
    print(f"{'WELCOME TO GRAAF CLOTHING':^50}")
    print("="*50)
    print("""
        1. Generate Bill
        2. Inventory
        3. Profit Report
        4. Exit
            """)
    print("="*50)

    choice = input("Enter choice: ")
    
    if choice == "1":
        billing()
    elif choice == "2":
        inventory()
    elif choice == "3":
        view_profit()
    elif choice == "4":
        print("Exiting Program.....")
        break   
    else:
        print("Select an Option !!!")


cursor.close()
db.close()