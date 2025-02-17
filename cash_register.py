import tkinter as tk
from tkinter.simpledialog import askstring, askfloat
from tkinter import messagebox  # For displaying message box


class CashRegisterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dynamic Blocks")
        self.blocks = {}  # Will store block name as key and a dictionary for price, quantity, and click count
        self.total_sum = 0  # This will store the overall total sum
        self.page = 0  # Current page number
        self.items_per_page = 5  # Maximum products per page
        self.create_ui()

    def create_ui(self):
        self.frame = tk.Frame(self.root, bg="#FAEBD7")  # Background color set to yellow sand
        self.frame.pack(padx=10, pady=10)

        root.configure(bg="#FAEBD7")
        # Button to add a new block (product)
        self.add_button = tk.Button(self.root, text="Add Product", command=self.add_new_block, font=("Arial", 10))
        self.add_button.pack(pady=5)

        # Button to calculate total sum
        self.pay_button = tk.Button(self.root, text="Pay", command=self.pay, font=("Arial", 10))
        self.pay_button.pack(pady=5)

        # Label to display mid-receipt value
        self.mid_receipt_label = tk.Label(self.root, text="Mid-Receipt: €0.00", font=("Arial", 10))
        self.mid_receipt_label.pack(pady=5)

        # Frame to hold total sum, export button, and pagination buttons
        total_frame = tk.Frame(self.root)
        total_frame.pack(pady=5)

        # Button to export product data
        self.export_button = tk.Button(total_frame, text="Export", command=self.export_data, font=("Arial", 10))
        self.export_button.pack(side=tk.LEFT)

        # Label to display total sum
        self.total_label = tk.Label(total_frame, text="Total: €0.00", font=("Arial", 10))
        self.total_label.pack(side=tk.LEFT, padx=10)

        # Navigation buttons (Next/Previous)
        self.prev_button = tk.Button(total_frame, text="<", command=self.previous_page, font=("Arial", 10),
                                     state=tk.DISABLED)
        self.prev_button.pack(side=tk.LEFT, padx=10)

        self.next_button = tk.Button(total_frame, text=">", command=self.next_page, font=("Arial", 10),
                                     state=tk.DISABLED)
        self.next_button.pack(side=tk.LEFT)

    def create_block(self, block_name, price):
        # Create frame for each block (product)
        block_frame = tk.Frame(self.frame, bg="#FAEBD7")
        block_frame.pack(pady=5)

        # Default quantity is 0, so no need to ask for it
        quantity = 0
        new_increments = 0  # Start with 0 new increments

        # Create block button with quantity and price information
        block_button = tk.Button(block_frame, text=f"{block_name}: {quantity} ({new_increments})", width=20, height=3,
                                 font=("Arial", 12),
                                 bg="green", fg="white",
                                 command=lambda name=block_name: self.increment_click(name, block_button))
        block_button.pack(side=tk.LEFT)

        # Create decrement button to reduce quantity
        decrement_button = tk.Button(block_frame, text="-", width=3, height=3, font=("Arial", 12),
                                     bg="red", fg="white",
                                     command=lambda name=block_name: self.decrement_click(name, block_button))
        decrement_button.pack(side=tk.LEFT)

        # Save the block's data so we can update it later
        self.blocks[block_name] = {
            "quantity": quantity,
            "price": price,
            "new_increments": new_increments,  # Track the number of new increments
            "button": block_button,
            "frame": block_frame  # Store the frame for pagination control
        }

        # Update pagination
        self.update_pagination()

    def update_block_button_text(self, block_name):
        block_data = self.blocks[block_name]
        block_button = block_data["button"]
        # Show both total quantity and new increments
        block_button.config(text=f"{block_name}: {block_data['quantity']} ({block_data['new_increments']})")

    def increment_click(self, block_name, block_button):
        # Increment the total quantity and new increments count for the block
        self.blocks[block_name]["new_increments"] += 1
        self.update_block_button_text(block_name)
        self.update_mid_receipt_value()

    def decrement_click(self, block_name, block_button):
        # Decrement the total quantity (but don't decrement the new increments)
        if self.blocks[block_name]["new_increments"] > 0:
            self.blocks[block_name]["new_increments"] -= 1
        self.update_block_button_text(block_name)
        self.update_mid_receipt_value()

    def add_new_block(self):
        # Prompt the user to enter a name for the new block (product)
        block_name = askstring("Product name", "Enter a product name:")
        if block_name:  # Only proceed if the user entered a name
            # Prompt the user to enter the price for the product
            price = askfloat("Product price", f"Enter the price for {block_name}:")
            if price is not None:  # Only proceed if the user entered a valid price
                self.create_block(block_name, price)

    def pay(self):
        # Calculate the mid-receipt value based on the new increments
        mid_receipt_value = 0
        for block in self.blocks:
            block_data = self.blocks[block]
            block_data["quantity"] += block_data["new_increments"]
            mid_receipt_value += block_data["new_increments"] * block_data["price"]
            # After calculating the value, reset new_increments
            block_data["new_increments"] = 0
            self.update_block_button_text(block)
        # Add the mid-receipt value to the total sum
        self.total_sum += mid_receipt_value

        # Update the total sum label
        self.total_label.config(text=f"Total: €{self.total_sum:.2f}")

        # Reset mid-receipt value display
        self.update_mid_receipt_value()

    def update_mid_receipt_value(self):
        # Calculate the mid-receipt value based on the new increments
        mid_receipt_value = 0
        for block in self.blocks:
            block_data = self.blocks[block]
            mid_receipt_value += block_data["new_increments"] * block_data["price"]

        # Update the mid-receipt label
        self.mid_receipt_label.config(text=f"Mid-Receipt: €{mid_receipt_value:.2f}")

    def update_pagination(self):
        # Calculate the current page start and end indexes
        start_index = self.page * self.items_per_page
        end_index = start_index + self.items_per_page

        # Hide all products
        for block_data in self.blocks.values():
            block_data["frame"].pack_forget()

        # Show products for the current page
        product_names = list(self.blocks.keys())
        for i in range(start_index, min(end_index, len(product_names))):
            block_name = product_names[i]
            block_data = self.blocks[block_name]
            block_data["frame"].pack(pady=5)

        # Enable/Disable page navigation buttons based on the number of products
        if self.page > 0:
            self.prev_button.config(state=tk.NORMAL)
        else:
            self.prev_button.config(state=tk.DISABLED)

        if end_index < len(self.blocks):
            self.next_button.config(state=tk.NORMAL)
        else:
            self.next_button.config(state=tk.DISABLED)

    def next_page(self):
        # Increment the page number and update the pagination
        self.page += 1
        self.update_pagination()

    def previous_page(self):
        # Decrement the page number and update the pagination
        self.page -= 1
        self.update_pagination()

    def export_data(self):
        """Export product details (name, quantity, price) to a text file."""
        exported_data = ""
        total_price = 0
        # Loop through the blocks and gather the information
        for block_name, block_data in self.blocks.items():
            quantity = block_data["quantity"] + block_data["new_increments"]
            price = block_data["price"]
            total = quantity * price
            exported_data += f"{block_name}: {quantity}, Total: €{total:.2f}\n"
            total_price += total

        # Add the overall total at the bottom
        exported_data += f"\nOverall Total: €{total_price:.2f}"

        # Ask user for the file name
        file_name = askstring("Export Filename", "Enter filename (e.g., receipt.txt):")
        if file_name:
            # Write to the specified file
            with open(file_name, "w") as file:
                file.write(exported_data)

            # Notify the user that the export was successful
            messagebox.showinfo("Export Successful", f"Data has been exported to {file_name}")


if __name__ == "__main__":
    root = tk.Tk()
    app = CashRegisterApp(root)
    root.mainloop()
