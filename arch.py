import tkinter as tk
from tkinter import messagebox
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

class FlatDesignerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Flat Designer")
        
        self.room_names = ["Bedroom", "Living Room", "Kitchen", "Bathroom", "Toilet", "Balcony"]
        self.entries = []

        self.create_input_fields()
        self.create_generate_button()

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
        generate_button = tk.Button(self.root, text="Generate PDF Designs", command=self.generate_designs)
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

        for _ in range(3):  # Generate 3 options
            design = {}
            available_spaces = [(0, 0, flat_width, flat_height)]

            for room_name, (area, min_dim) in room_data.items():
                max_dim = area / min_dim
                room_width = min_dim
                room_height = max_dim

                # Randomly pick a space and place the room
                for _ in range(100):  # Attempt 100 times to place the room
                    space = random.choice(available_spaces)
                    x1, y1, x2, y2 = space

                    if x2 - x1 >= room_width and y2 - y1 >= room_height:
                        # Place the room in this space
                        x_offset = x1
                        y_offset = y1

                        design[room_name] = (x_offset, y_offset, room_width, room_height)
                        available_spaces.remove(space)

                        # Update available spaces
                        available_spaces.append((x_offset + room_width, y_offset, x2, y2))
                        available_spaces.append((x1, y_offset + room_height, x2, y2))
                        break
                else:
                    # If unable to place room after multiple attempts, skip
                    continue

            options.append(design)

        return options

    def display_options(self, options):
        fig, axs = plt.subplots(1, len(options), figsize=(15, 5))
        if len(options) == 1:
            axs = [axs]

        for i, option in enumerate(options):
            ax = axs[i]
            ax.set_xlim(0, 20)
            ax.set_ylim(0, 15)
            ax.set_aspect('equal')
            ax.set_title(f"Option {i + 1}")
            
            for room_name, (x, y, w, h) in option.items():
                rect = patches.Rectangle((x, y), w, h, linewidth=1, edgecolor='r', facecolor='none')
                ax.add_patch(rect)
                ax.text(x + 0.5, y + 0.5, room_name, fontsize=8, ha='left')

            ax.set_xlabel("Width (m)")
            ax.set_ylabel("Height (m)")
            ax.grid(True)

        plt.tight_layout()
        plt.show()

        save_button = tk.Button(self.root, text="Save as PDF", command=lambda: self.save_as_pdf(options))
        save_button.grid(row=len(self.room_names) + 1, column=0, columnspan=3, pady=20)

        plt.tight_layout()
        plt.show()

        save_button = tk.Button(self.root, text="Save as PDF", command=lambda: self.save_as_pdf(options))
        save_button.grid(row=len(self.room_names) + 1, column=0, columnspan=3, pady=20)

    def save_as_pdf(self, options):
        save_dir = "pdf_designs"  # Directory to save PDF files
        os.makedirs(save_dir, exist_ok=True)

        for i, option in enumerate(options):
            fig, ax = plt.subplots(figsize=(10, 7))
            ax.set_xlim(0, 20)
            ax.set_ylim(0, 15)
            ax.set_aspect('equal')
            ax.set_title(f"Design Option {i + 1}")

            for room_name, (x, y, w, h) in option.items():
                rect = patches.Rectangle((x, y), w, h, linewidth=1, edgecolor='r', facecolor='none')
                ax.add_patch(rect)
                ax.text(x + 0.5, y + 0.5, room_name, fontsize=8, ha='left')

            ax.set_xlabel("Width (m)")
            ax.set_ylabel("Height (m)")
            ax.grid(True)

            filename = os.path.join(save_dir, f"flat_design_option_{i + 1}.pdf")
            plt.savefig(filename)
            plt.close()

        messagebox.showinfo("Success", "PDF files saved successfully.")

if __name__ == "__main__":
    root = tk.Tk()
    app = FlatDesignerApp(root)
    root.mainloop()
