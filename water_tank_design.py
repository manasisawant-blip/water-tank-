import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import math
import argparse
import json
from pathlib import Path
import random
import os
from datetime import datetime

class WaterTankDesigner:
    def __init__(self, root):
        self.root = root
        self.root.title("Water Tank Design Calculator")
        self.root.geometry("700x800")
        
        # Tank types
        self.tank_types = {
            "Domestic Tank": {"quantity": 1, "color": "lightblue"},
            "Flushing Tank": {"quantity": 1, "color": "lightgreen"},
            "Fire Tank 1": {"quantity": 1, "color": "lightcoral"},
            "Fire Tank 2": {"quantity": 1, "color": "lightsalmon"}
        }
        
        self.tank_data = {}
        self.design_options = {}
        self.current_option = 0
        self.create_widgets()
    
    def create_widgets(self):
        # Title
        title = tk.Label(self.root, text="Water Tank Design Calculator", 
                        font=("Arial", 16, "bold"))
        title.pack(pady=10)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create frames for each tank type
        self.entries = {}
        for tank_name in self.tank_types.keys():
            frame = ttk.Frame(self.notebook)
            self.notebook.add(frame, text=tank_name)
            self.create_tank_input_frame(frame, tank_name)
        
        # Buttons frame
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=15)
        
        calculate_btn = tk.Button(button_frame, text="Calculate & Visualize", 
                                  command=self.calculate_tanks, 
                                  bg="green", fg="white", font=("Arial", 10, "bold"))
        calculate_btn.pack(side="left", padx=5)
        
        reset_btn = tk.Button(button_frame, text="Reset", 
                             command=self.reset_form,
                             bg="orange", fg="white", font=("Arial", 10, "bold"))
        reset_btn.pack(side="left", padx=5)
    
    def create_tank_input_frame(self, parent, tank_name):
        # Main container
        main_frame = tk.Frame(parent)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Tank name label
        name_label = tk.Label(main_frame, text=f"{tank_name} Specifications", 
                            font=("Arial", 12, "bold"))
        name_label.pack(pady=10)
        
        # Depth input
        depth_frame = tk.Frame(main_frame)
        depth_frame.pack(fill="x", pady=10)
        tk.Label(depth_frame, text="Depth (meters):", font=("Arial", 10), width=20, anchor="w").pack(side="left")
        depth_entry = tk.Entry(depth_frame, font=("Arial", 10), width=15)
        depth_entry.pack(side="left", padx=10)
        
        # Volume input
        volume_frame = tk.Frame(main_frame)
        volume_frame.pack(fill="x", pady=10)
        tk.Label(volume_frame, text="Volume (cubic meters):", font=("Arial", 10), width=20, anchor="w").pack(side="left")
        volume_entry = tk.Entry(volume_frame, font=("Arial", 10), width=15)
        volume_entry.pack(side="left", padx=10)
        
        # Info frame
        info_frame = tk.LabelFrame(main_frame, text="Calculated Dimensions", font=("Arial", 10, "bold"))
        info_frame.pack(fill="x", pady=15)
        
        info_label = tk.Label(info_frame, text="", font=("Arial", 9), justify="left")
        info_label.pack(padx=10, pady=10)
        
        self.entries[tank_name] = {
            "depth": depth_entry,
            "volume": volume_entry,
            "info_label": info_label
        }
    
    def calculate_tanks(self):
        try:
            self.tank_data = {}
            
            for tank_name, entry_dict in self.entries.items():
                depth_str = entry_dict["depth"].get().strip()
                volume_str = entry_dict["volume"].get().strip()
                
                # Validate input is not empty
                if not depth_str or not volume_str:
                    raise ValueError(f"{tank_name}: Both Depth and Volume fields must be filled")
                
                # Convert to float with error handling
                try:
                    depth = float(depth_str)
                    volume = float(volume_str)
                except ValueError:
                    raise ValueError(f"{tank_name}: Please enter valid numbers (not text)")
                
                if depth <= 0 or volume <= 0:
                    raise ValueError(f"{tank_name}: Depth and Volume must be positive values")
                
                # Calculate base area from volume
                # Volume = Base Area × Depth
                base_area = volume / depth
                
                # Assuming square tank: length = width = sqrt(base_area)
                side_length = math.sqrt(base_area)
                
                # Alternative: rectangular tank with aspect ratio 2:1
                length = math.sqrt(base_area * 2)
                width = base_area / length
                
                self.tank_data[tank_name] = {
                    "depth": depth,
                    "volume": volume,
                    "base_area": base_area,
                    "length": length,
                    "width": width,
                    "side_length": side_length
                }
                
                # Update info label
                info_text = f"Square Tank: {side_length:.2f}m × {side_length:.2f}m × {depth:.2f}m\n"
                info_text += f"Rectangular Tank: {length:.2f}m × {width:.2f}m × {depth:.2f}m\n"
                info_text += f"Base Area: {base_area:.2f} m²\n"
                info_text += f"Volume: {volume:.2f} m³"
                
                entry_dict["info_label"].config(text=info_text)
            
            # Generate design options
            self.generate_design_options()
            # Display visualization
            self.display_design_options()
            
        except ValueError as e:
            messagebox.showerror("Input Error", f"Please enter valid numeric values. Error: {str(e)}")
    
    def display_visualization(self):
        """Display tank visualization in a new window using tkinter"""
        viz_window = tk.Toplevel(self.root)
        viz_window.title("Tank Visualizations")
        viz_window.geometry("900x700")
        
        tank_names = list(self.tank_data.keys())
        n_tanks = len(tank_names)
        
        # Create canvas for each tank
        for idx, tank_name in enumerate(tank_names):
            data = self.tank_data[tank_name]
            
            # Frame for this tank
            frame = tk.LabelFrame(viz_window, text=tank_name, font=("Arial", 10, "bold"))
            frame.grid(row=idx, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
            
            # Top view canvas
            canvas_top = tk.Canvas(frame, width=200, height=200, bg="white", relief="sunken", border=2)
            canvas_top.pack(side="left", padx=10, pady=10)
            canvas_top.create_text(100, 10, text="Top View", font=("Arial", 10, "bold"))
            self.draw_top_view_canvas(canvas_top, tank_name, data)
            
            # Side view canvas
            canvas_side = tk.Canvas(frame, width=200, height=200, bg="white", relief="sunken", border=2)
            canvas_side.pack(side="left", padx=10, pady=10)
            canvas_side.create_text(100, 10, text="Side View", font=("Arial", 10, "bold"))
            self.draw_side_view_canvas(canvas_side, tank_name, data)
    
    def draw_top_view_canvas(self, canvas, tank_name, data):
        """Draw top view on tkinter canvas"""
        length = data["length"]
        width = data["width"]
        
        # Scale for display (fit in 180x180 area)
        max_dim = max(length, width)
        scale = 160 / max_dim if max_dim > 0 else 1
        
        x1, y1 = 20, 40
        x2, y2 = x1 + length * scale, y1 + width * scale
        
        # Draw tank outline
        color = self.tank_types[tank_name]["color"]
        canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black", width=2)
        
        # Draw dimensions
        canvas.create_text((x1 + x2) / 2, y2 + 15, text=f"{length:.1f}m", font=("Arial", 8))
        canvas.create_text(x1 - 15, (y1 + y2) / 2, text=f"{width:.1f}m", font=("Arial", 8))
    
    def draw_side_view_canvas(self, canvas, tank_name, data):
        """Draw side view on tkinter canvas"""
        length = data["length"]
        depth = data["depth"]
        
        # Scale for display
        max_dim = max(length, depth)
        scale = 160 / max_dim if max_dim > 0 else 1
        
        x1, y1 = 20, 40
        x2, y2 = x1 + length * scale, y1 + depth * scale
        
        # Draw tank outline
        color = self.tank_types[tank_name]["color"]
        canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black", width=2)
        
        # Draw water level (80% full)
        water_level = y1 + (y2 - y1) * 0.8
        canvas.create_rectangle(x1, water_level, x2, y2, fill="lightblue", outline="blue", width=1)
        canvas.create_text((x1 + x2) / 2, water_level - 5, text="80%", font=("Arial", 7), fill="blue")
        
        # Draw dimensions
        canvas.create_text((x1 + x2) / 2, y2 + 15, text=f"{length:.1f}m", font=("Arial", 8))
        canvas.create_text(x1 - 15, (y1 + y2) / 2, text=f"{depth:.1f}m", font=("Arial", 8))
    
    def generate_design_options(self):
        """Generate 3 different design options for each tank"""
        self.design_options = {}
        
        for tank_name, data in self.tank_data.items():
            options = []
            base_area = data["base_area"]
            depth = data["depth"]
            
            # Option 1: Square Tank
            side = math.sqrt(base_area)
            options.append({
                "name": "Square Tank",
                "length": side,
                "width": side,
                "depth": depth,
                "aspect_ratio": "1:1"
            })
            
            # Option 2: Rectangular Tank (2:1)
            length = math.sqrt(base_area * 2)
            width = base_area / length
            options.append({
                "name": "Rectangular Tank (2:1)",
                "length": length,
                "width": width,
                "depth": depth,
                "aspect_ratio": "2:1"
            })
            
            # Option 3: Rectangular Tank (3:1)
            length = math.sqrt(base_area * 3)
            width = base_area / length
            options.append({
                "name": "Rectangular Tank (3:1)",
                "length": length,
                "width": width,
                "depth": depth,
                "aspect_ratio": "3:1"
            })
            
            self.design_options[tank_name] = options
    
    def display_design_options(self):
        """Display all design options in a new window with scrolling"""
        options_window = tk.Toplevel(self.root)
        options_window.title("Tank Design Options")
        options_window.geometry("1200x1000")
        
        # Create a main frame with canvas and scrollbar
        canvas_frame = tk.Frame(options_window)
        canvas_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Create canvas with scrollbar
        canvas = tk.Canvas(canvas_frame, bg="white")
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Enable mousewheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        main_frame = scrollable_frame
        
        for tank_name, options in self.design_options.items():
            # Tank section
            tank_frame = tk.LabelFrame(main_frame, text=tank_name, font=("Arial", 12, "bold"), 
                                      bg=self.tank_types[tank_name]["color"], relief="raised", borderwidth=2)
            tank_frame.pack(fill="x", pady=15, padx=10)
            
            # Options row
            for idx, option in enumerate(options):
                option_frame = tk.Frame(tank_frame, bg="white", relief="sunken", borderwidth=1)
                option_frame.pack(side="left", padx=10, pady=10, expand=True, fill="both")
                
                # Option title
                title_label = tk.Label(option_frame, text=option["name"], 
                                      font=("Arial", 10, "bold"), bg="lightgray")
                title_label.pack(fill="x", padx=5, pady=5)
                
                # Canvas for design
                canvas_design = tk.Canvas(option_frame, width=250, height=200, bg="white", relief="ridge", border=1)
                canvas_design.pack(padx=10, pady=10)
                
                # Draw tank design
                self.draw_detailed_tank(canvas_design, option, tank_name)
                
                # Dimensions info
                info_frame = tk.Frame(option_frame, bg="lightyellow")
                info_frame.pack(fill="x", padx=5, pady=5)
                
                info_text = f"Length: {option['length']:.2f}m\n"
                info_text += f"Width: {option['width']:.2f}m\n"
                info_text += f"Depth: {option['depth']:.2f}m\n"
                info_text += f"Ratio: {option['aspect_ratio']}\n"
                info_text += f"Volume: {self.tank_data[tank_name]['volume']:.2f}m³"
                
                info_label = tk.Label(info_frame, text=info_text, font=("Arial", 9), justify="left", bg="lightyellow")
                info_label.pack(padx=5, pady=5)
                
                # Select button
                select_btn = tk.Button(option_frame, text="Select Design", 
                                      command=lambda o=option, t=tank_name: self.show_selected_design(t, o),
                                      bg="green", fg="white", font=("Arial", 9, "bold"))
                select_btn.pack(fill="x", padx=5, pady=5)
    
    def draw_detailed_tank(self, canvas, option, tank_name):
        """Draw detailed tank design on canvas"""
        length = option["length"]
        width = option["width"]
        depth = option["depth"]
        
        # Scale to fit canvas
        max_dim = max(length, width, depth)
        scale = 150 / max_dim if max_dim > 0 else 1
        
        # Drawing coordinates
        x_start = 25
        y_start = 30
        
        # Draw top view (showing length x width)
        l_scaled = length * scale
        w_scaled = width * scale
        
        # Main tank rectangle
        tank_color = self.tank_types[tank_name]["color"]
        canvas.create_rectangle(x_start, y_start, x_start + l_scaled, y_start + w_scaled,
                              fill=tank_color, outline="black", width=2)
        
        # Draw inlet (circle at top left)
        inlet_x = x_start + 10
        inlet_y = y_start + 10
        canvas.create_oval(inlet_x - 5, inlet_y - 5, inlet_x + 5, inlet_y + 5,
                         fill="blue", outline="darkblue", width=1)
        canvas.create_text(inlet_x - 15, inlet_y, text="Inlet", font=("Arial", 7))
        
        # Draw outlet (circle at bottom)
        outlet_x = x_start + l_scaled - 10
        outlet_y = y_start + w_scaled - 10
        canvas.create_oval(outlet_x - 5, outlet_y - 5, outlet_x + 5, outlet_y + 5,
                         fill="red", outline="darkred", width=1)
        canvas.create_text(outlet_x + 15, outlet_y, text="Outlet", font=("Arial", 7))
        
        # Draw overflow (circle at top right)
        overflow_x = x_start + l_scaled - 10
        overflow_y = y_start + 10
        canvas.create_oval(overflow_x - 5, overflow_y - 5, overflow_x + 5, overflow_y + 5,
                         fill="orange", outline="darkorange", width=1)
        canvas.create_text(overflow_x + 15, overflow_y, text="Overflow", font=("Arial", 7))
        
        # Add dimensions
        canvas.create_text(x_start + l_scaled / 2, y_start + w_scaled + 15,
                         text=f"{length:.1f}m", font=("Arial", 8, "bold"))
        canvas.create_text(x_start - 20, y_start + w_scaled / 2,
                         text=f"{width:.1f}m", font=("Arial", 8, "bold"))
        
        # Add depth indicator on side
        depth_x = x_start + l_scaled + 40
        depth_y_start = y_start
        depth_y_end = y_start + 50
        canvas.create_line(depth_x, depth_y_start, depth_x, depth_y_end, width=2, fill="gray")
        canvas.create_line(depth_x - 5, depth_y_start, depth_x + 5, depth_y_start, width=2, fill="gray")
        canvas.create_line(depth_x - 5, depth_y_end, depth_x + 5, depth_y_end, width=2, fill="gray")
        canvas.create_text(depth_x + 20, (depth_y_start + depth_y_end) / 2,
                         text=f"D:{depth:.1f}m", font=("Arial", 8, "bold"))
    
    def show_selected_design(self, tank_name, option):
        """Show detailed view of selected design"""
        design_window = tk.Toplevel(self.root)
        design_window.title(f"Selected Design - {tank_name}")
        design_window.geometry("700x600")
        
        # Title
        title_label = tk.Label(design_window, text=f"{tank_name} - {option['name']}", 
                              font=("Arial", 14, "bold"), bg=self.tank_types[tank_name]["color"])
        title_label.pack(fill="x", padx=5, pady=10)
        
        # Create large canvas
        canvas_frame = tk.Frame(design_window)
        canvas_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        canvas = tk.Canvas(canvas_frame, width=600, height=400, bg="white", relief="sunken", border=2)
        canvas.pack(fill="both", expand=True)
        
        # Draw isometric view
        self.draw_isometric_tank(canvas, option, tank_name)
        
        # Details panel
        details_frame = tk.LabelFrame(design_window, text="Tank Specifications", 
                                     font=("Arial", 11, "bold"))
        details_frame.pack(fill="x", padx=20, pady=10)
        
        details_text = f"""
Length (L): {option['length']:.2f} m
Width (W): {option['width']:.2f} m  
Depth (D): {option['depth']:.2f} m
Volume: {self.tank_data[tank_name]['volume']:.2f} m³
Base Area: {option['length'] * option['width']:.2f} m²
Surface Area: {2 * (option['length'] + option['width']) * option['depth']:.2f} m²
Aspect Ratio: {option['aspect_ratio']}
        """
        
        details_label = tk.Label(details_frame, text=details_text, font=("Arial", 10), 
                               justify="left", bg="lightyellow")
        details_label.pack(padx=10, pady=10)
        
        # Buttons frame
        button_frame = tk.Frame(design_window)
        button_frame.pack(pady=10)
        
        # Save DXF button
        save_dxf_btn = tk.Button(button_frame, text="Save as DXF", 
                                command=lambda: self.save_as_dxf(tank_name, option),
                                bg="blue", fg="white", font=("Arial", 10, "bold"))
        save_dxf_btn.pack(side="left", padx=5)
        
        # Close button
        close_btn = tk.Button(button_frame, text="Close", command=design_window.destroy,
                            bg="red", fg="white", font=("Arial", 10, "bold"))
        close_btn.pack(side="left", padx=5)
    
    def draw_isometric_tank(self, canvas, option, tank_name):
        """Draw isometric view of tank"""
        length = option["length"]
        width = option["width"]
        depth = option["depth"]
        
        # Scale
        max_dim = max(length, width, depth)
        scale = 100 / max_dim if max_dim > 0 else 1
        
        # Isometric angle constants
        x_center = 300
        y_center = 150
        
        l_iso = length * scale * 0.866
        w_iso = width * scale * 0.5
        d_iso = depth * scale
        
        tank_color = self.tank_types[tank_name]["color"]
        
        # Draw tank edges
        # Top edges
        canvas.create_line(x_center, y_center, x_center + l_iso, y_center - w_iso, 
                         width=2, fill="black")  # Front top
        canvas.create_line(x_center, y_center, x_center, y_center + d_iso, 
                         width=2, fill="black")  # Left top
        canvas.create_line(x_center + l_iso, y_center - w_iso, x_center + l_iso, y_center - w_iso + d_iso,
                         width=2, fill="black")  # Right top
        
        # Bottom edges
        canvas.create_line(x_center, y_center + d_iso, x_center + l_iso, y_center + d_iso - w_iso,
                         width=2, fill="black")  # Front bottom
        canvas.create_line(x_center + l_iso, y_center + d_iso - w_iso, x_center + l_iso, y_center - w_iso + d_iso,
                         width=2, fill="black")  # Right bottom
        
        # Fill tank faces with transparency effect
        points = [x_center, y_center, x_center + l_iso, y_center - w_iso, 
                 x_center + l_iso, y_center - w_iso + d_iso, x_center, y_center + d_iso]
        canvas.create_polygon(points, fill=tank_color, outline="black", width=2)
        
        # Add labels
        canvas.create_text(x_center + l_iso / 2, y_center - w_iso / 2 - 20, 
                         text=f"Length: {length:.1f}m", font=("Arial", 10, "bold"))
        canvas.create_text(x_center - 30, y_center + d_iso / 2, 
                         text=f"Depth: {depth:.1f}m", font=("Arial", 10, "bold"))
        canvas.create_text(x_center + l_iso - 30, y_center + d_iso / 2 - w_iso / 2, 
                         text=f"Width: {width:.1f}m", font=("Arial", 10, "bold"))
        
        # Add water level indicator
        water_depth = depth * 0.8
        water_points = [x_center, y_center + water_depth, x_center + l_iso, y_center - w_iso + water_depth,
                       x_center + l_iso, y_center - w_iso + water_depth, x_center, y_center + water_depth]
        canvas.create_polygon(water_points, fill="lightblue", outline="blue", width=1)
    
    def save_as_dxf(self, tank_name, option):
        """Save tank design as DXF file"""
        try:
            # Try to use ezdxf if available
            try:
                import ezdxf
            except ImportError:
                # If ezdxf not available, create a simple DXF format file
                self.save_dxf_simple(tank_name, option)
                return
            
            # Ask user where to save
            file_path = filedialog.asksaveasfilename(
                defaultextension=".dxf",
                filetypes=[("DXF files", "*.dxf"), ("All files", "*.*")],
                initialfile=f"{tank_name}_{option['name'].replace(' ', '_')}.dxf"
            )
            
            if not file_path:
                return
            
            # Create DXF file
            dwg = ezdxf.new('R2010')
            msp = dwg.modelspace()
            
            length = option['length']
            width = option['width']
            depth = option['depth']
            
            # Add title
            msp.add_text(f"{tank_name} - {option['name']}", dxfattribs={'height': 10})
            
            # Draw top view (plan)
            msp.add_lwpolyline([(0, 0), (length, 0), (length, width), (0, width), (0, 0)],
                             dxfattribs={'color': 1})
            
            # Add dimensions for top view
            msp.add_text(f"L: {length:.2f}m", dxfattribs={'height': 5, 'insert': (length/2, -2)})
            msp.add_text(f"W: {width:.2f}m", dxfattribs={'height': 5, 'insert': (-3, width/2)})
            
            # Draw side view (elevation) offset
            offset_y = width + 5
            msp.add_lwpolyline([(0, offset_y), (length, offset_y), (length, offset_y + depth), 
                              (0, offset_y + depth), (0, offset_y)],
                             dxfattribs={'color': 2})
            
            # Add dimensions for side view
            msp.add_text(f"L: {length:.2f}m", dxfattribs={'height': 5, 'insert': (length/2, offset_y - 2)})
            msp.add_text(f"D: {depth:.2f}m", dxfattribs={'height': 5, 'insert': (-3, offset_y + depth/2)})
            
            # Add specifications as text
            text_offset = offset_y + depth + 5
            specs = [
                f"Tank Name: {tank_name}",
                f"Design Type: {option['name']}",
                f"Length: {length:.2f} m",
                f"Width: {width:.2f} m",
                f"Depth: {depth:.2f} m",
                f"Volume: {self.tank_data[tank_name]['volume']:.2f} m³",
                f"Base Area: {length * width:.2f} m²",
                f"Surface Area: {2 * (length + width) * depth:.2f} m²",
                f"Aspect Ratio: {option['aspect_ratio']}",
                f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            ]
            
            for idx, spec in enumerate(specs):
                msp.add_text(spec, dxfattribs={'height': 3, 'insert': (0, text_offset + idx * 1.5)})
            
            # Save the DXF file
            dwg.saveas(file_path)
            messagebox.showinfo("Success", f"DXF file saved successfully!\n\n{file_path}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save DXF file: {str(e)}")
    
    def save_dxf_simple(self, tank_name, option):
        """Save tank design as simple DXF format (without ezdxf library)"""
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".dxf",
                filetypes=[("DXF files", "*.dxf"), ("All files", "*.*")],
                initialfile=f"{tank_name}_{option['name'].replace(' ', '_')}.dxf"
            )
            
            if not file_path:
                return
            
            length = option['length']
            width = option['width']
            depth = option['depth']
            
            # Create simple DXF content
            dxf_content = """999
AutoCAD DXF file
0
SECTION
2
HEADER
9
$ACADVER
1
AC1015
0
ENDSEC
0
SECTION
2
ENTITIES
0
TEXT
8
0
10
0
20
0
40
10
1
"""
            dxf_content += f"{tank_name} - {option['name']}\n0\nTEXT\n8\n0\n10\n0\n20\n-15\n40\n5\n1\n"
            dxf_content += f"Length: {length:.2f}m, Width: {width:.2f}m, Depth: {depth:.2f}m\n0\nTEXT\n8\n0\n10\n0\n20\n-25\n40\n5\n1\n"
            dxf_content += f"Volume: {self.tank_data[tank_name]['volume']:.2f} m³\n0\nTEXT\n8\n0\n10\n0\n20\n-35\n40\n5\n1\n"
            dxf_content += f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n0\nENDSEC\n0\nEOF\n"
            
            # Write to file
            with open(file_path, 'w') as f:
                f.write(dxf_content)
            
            messagebox.showinfo("Success", f"DXF file saved successfully!\n\n{file_path}\n\nNote: Basic DXF format. Install 'ezdxf' for enhanced drawings.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save DXF file: {str(e)}")
    
    def reset_form(self):
        """Clear all input fields"""
        for tank_name, entry_dict in self.entries.items():
            entry_dict["depth"].delete(0, tk.END)
            entry_dict["volume"].delete(0, tk.END)
            entry_dict["info_label"].config(text="")
        messagebox.showinfo("Reset", "All fields cleared!")


def main():
    root = tk.Tk()
    app = WaterTankDesigner(root)
    root.mainloop()


def headless_export(output_dir, input_data=None):
    """Generate DXF files for provided tank inputs without launching the GUI.

    input_data should be a dict mapping tank names to {"depth": float, "volume": float}.
    If not provided, sensible defaults will be used.
    """
    outdir = Path(output_dir)
    outdir.mkdir(parents=True, exist_ok=True)

    # default sample inputs
    defaults = {
        "Domestic Tank": {"depth": 2.5, "volume": 10.0},
        "Flushing Tank": {"depth": 1.5, "volume": 5.0},
        "Fire Tank 1": {"depth": 3.0, "volume": 50.0},
        "Fire Tank 2": {"depth": 4.0, "volume": 100.0}
    }

    data = input_data or defaults

    for tank_name, params in data.items():
        try:
            depth = float(params["depth"])
            volume = float(params["volume"])
        except Exception:
            print(f"Skipping {tank_name}: invalid parameters: {params}")
            continue

        if depth <= 0 or volume <= 0:
            print(f"Skipping {tank_name}: non-positive values")
            continue

        base_area = volume / depth

        # produce same three options as GUI
        options = []
        side = math.sqrt(base_area)
        options.append({"name": "Square Tank", "length": side, "width": side, "depth": depth, "aspect_ratio": "1:1"})

        length = math.sqrt(base_area * 2)
        width = base_area / length
        options.append({"name": "Rectangular Tank (2:1)", "length": length, "width": width, "depth": depth, "aspect_ratio": "2:1"})

        length = math.sqrt(base_area * 3)
        width = base_area / length
        options.append({"name": "Rectangular Tank (3:1)", "length": length, "width": width, "depth": depth, "aspect_ratio": "3:1"})

        for option in options:
            fname = f"{tank_name}_{option['name'].replace(' ', '_')}.dxf"
            outpath = outdir / fname

            # Try ezdxf first
            try:
                import ezdxf
                dwg = ezdxf.new('R2010')
                msp = dwg.modelspace()

                L = option['length']
                W = option['width']
                D = option['depth']

                msp.add_text(f"{tank_name} - {option['name']}", dxfattribs={'height': 10})
                msp.add_lwpolyline([(0, 0), (L, 0), (L, W), (0, W), (0, 0)], dxfattribs={'color': 1})
                offset_y = W + 5
                msp.add_lwpolyline([(0, offset_y), (L, offset_y), (L, offset_y + D), (0, offset_y + D), (0, offset_y)], dxfattribs={'color': 2})

                specs = [
                    f"Tank Name: {tank_name}",
                    f"Design Type: {option['name']}",
                    f"Length: {L:.2f} m",
                    f"Width: {W:.2f} m",
                    f"Depth: {D:.2f} m",
                    f"Volume: {volume:.2f} m³",
                    f"Base Area: {L * W:.2f} m²",
                    f"Surface Area: {2 * (L + W) * D:.2f} m²",
                    f"Aspect Ratio: {option['aspect_ratio']}",
                ]

                text_offset = offset_y + D + 5
                for idx, spec in enumerate(specs):
                    msp.add_text(spec, dxfattribs={'height': 3, 'insert': (0, text_offset + idx * 1.5)})

                dwg.saveas(str(outpath))
                print(f"Wrote DXF: {outpath}")

            except Exception:
                # fallback simple DXF
                try:
                    L = option['length']
                    W = option['width']
                    D = option['depth']
                    dxf_content = """999
AutoCAD DXF file
0
SECTION
2
HEADER
9
$ACADVER
1
AC1015
0
ENDSEC
0
SECTION
2
ENTITIES
0
TEXT
8
0
10
0
20
0
40
10
1
"""
                    dxf_content += f"{tank_name} - {option['name']}\n0\nTEXT\n8\n0\n10\n0\n20\n-15\n40\n5\n1\n"
                    dxf_content += f"Length: {L:.2f}m, Width: {W:.2f}m, Depth: {D:.2f}m\n0\nTEXT\n8\n0\n10\n0\n20\n-25\n40\n5\n1\n"
                    dxf_content += f"Volume: {volume:.2f} m³\n0\nTEXT\n8\n0\n10\n0\n20\n-35\n40\n5\n1\n"
                    dxf_content += f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n0\nENDSEC\n0\nEOF\n"
                    with open(outpath, 'w') as f:
                        f.write(dxf_content)
                    print(f"Wrote simple DXF: {outpath}")
                except Exception as e:
                    print(f"Failed to write DXF for {tank_name} {option['name']}: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Water Tank Designer (GUI or headless DXF export)")
    parser.add_argument("--export-dxf", dest="export_dxf", help="Directory to write DXF files (headless mode)")
    parser.add_argument("--input-json", dest="input_json", help="Optional JSON file with tank inputs")
    args = parser.parse_args()

    if args.export_dxf:
        inputs = None
        if args.input_json:
            try:
                with open(args.input_json, 'r') as fh:
                    inputs = json.load(fh)
            except Exception as e:
                print(f"Failed to load input JSON {args.input_json}: {e}")
                raise
        headless_export(args.export_dxf, inputs)
    else:
        main()
