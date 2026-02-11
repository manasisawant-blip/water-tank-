import tkinter as tk
from tkinter import messagebox
import random

class FlatDesignerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flat Designer")
        
        self.room_names = ["Bedroom", "Living Room", "Kitchen", "Bathroom", "Toilet", "Balcony"]
        self.entries = []

        self.create_input_fields()
        self.create_generate_button()
        self.canvas = None

    def create_input_fields(self):
        for i, room in enumerate(self.room_names):
            label = tk.Label(self.root, text=f"{room} Area (sqm) and Min. Dimension (m):")
            label.grid(row=i, column=0, padx=10, pady=5)

            area_entry = tk.Entry(self.root)
            area_entry.grid(row=i, column=1, padx=10, pady=5)

            min_dim_entry = tk.Entry(self.root)
            min_dim_entry.grid(row=i, column=2, padx=10, pady=5)

            self.entries.append((area_entry, min_dim_entry))

    def create_generate_button(self):
        generate_button = tk.Button(self.root, text="Generate Designs", command=self.generate_designs)
        generate_button.grid(row=len(self.room_names), column=0, columnspan=3, pady=20)

    def generate_designs(self):
        room_data = {}
        try:
            for room, (area_entry, min_dim_entry) in zip(self.room_names, self.entries):
                area = float(area_entry.get())
                min_dim = float(min_dim_entry.get())
                room_data[room] = (area, min_dim)

            options = self.generate_design_options(room_data)
            self.display_options(options)
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numeric values for area and dimensions.")

    def generate_design_options(self, room_data):
        options = []
        flat_width = 20  # Arbitrary flat width in meters
        flat_height = 15  # Arbitrary flat height in meters
        scale = 10  # Scaling factor for visualization

        for _ in range(3):  # Generate 3 options
            design = {}
            available_spaces = [(0, 0, flat_width * scale, flat_height * scale)]

            for room_name, (area, min_dim) in room_data.items():
                max_dim = area / min_dim
                room_width = min_dim
                room_height = max_dim

                # Randomly pick a space and place the room
                for _ in range(100):  # Attempt 100 times to place the room
                    space = random.choice(available_spaces)
                    x1, y1, x2, y2 = space

                    if x2 - x1 >= room_width * scale and y2 - y1 >= room_height * scale:
                        # Place the room in this space
                        x_offset = x1
                        y_offset = y1

                        design[room_name] = (x_offset, y_offset, room_width * scale, room_height * scale)
                        available_spaces.remove(space)

                        # Update available spaces
                        available_spaces.append((x_offset + room_width * scale, y_offset, x2, y2))
                        available_spaces.append((x1, y_offset + room_height * scale, x2, y2))
                        break
                else:
                    # If unable to place room after multiple attempts, skip
                    continue

            options.append(design)

        return options

    def display_options(self, options):
        if self.canvas:
            self.canvas.destroy()  # Clear previous canvas
        self.canvas = tk.Canvas(self.root, width=800, height=600, bg="white")
        self.canvas.grid(row=len(self.room_names) + 1, column=0, columnspan=3, pady=20)

        for i, option in enumerate(options):
            x_offset = i * 260 + 20
            self.canvas.create_text(x_offset + 100, 20, text=f"Option {i + 1}", font=("Arial", 14, "bold"))

            for room_name, (x, y, w, h) in option.items():
                # Draw the room
                self.canvas.create_rectangle(x_offset + x, y + 50, x_offset + x + w, y + 50 + h, outline="black")
                self.canvas.create_text(x_offset + x + w / 2, y + 50 + h / 2, text=room_name, font=("Arial", 8))

if __name__ == "__main__":
    root = tk.Tk()
    app = FlatDesignerApp(root)
    root.mainloop()
