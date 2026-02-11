import math
import ezdxf
from ezdxf import units
import matplotlib.pyplot as plt


def get_positive_float(prompt):
    while True:
        try:
            v = float(input(prompt))
            if v <= 0:
                print("Value must be positive. Try again.")
                continue
            return v
        except ValueError:
            print("Please enter a numeric value.")


def main():
    print("Interactive compartment DXF generator")
    n = int(get_positive_float("Number of compartments: "))

    compartments = []
    for i in range(1, n + 1):
        name = input(f"Name of compartment {i}: ").strip() or f"Compartment_{i}"
        volume = get_positive_float(f"Volume of '{name}' (cubic meters): ")
        depth = get_positive_float(f"Depth/height of '{name}' (meters): ")
        area = volume / depth
        compartments.append({
            "name": name,
            "volume": volume,
            "depth": depth,
            "area": area,
        })

    # Compute drawing layout
    # We'll draw each compartment as a square of area 'area' (plan view), so side = sqrt(area)
    padding = 1.0  # meters between compartments
    side_lengths = [math.sqrt(c["area"]) for c in compartments]
    
    # Arrange compartments into rows so drawing width isn't excessive
    max_row_width = 10.0  # meters target width per row (tunable)
    rows = []  # list of rows, each row is list of (compartment, side)
    current_row = []
    current_width = padding
    for c, side in zip(compartments, side_lengths):
        needed = side + padding
        if current_row and (current_width + needed) > max_row_width:
            rows.append(current_row)
            current_row = []
            current_width = padding
        current_row.append((c, side))
        current_width += needed
    if current_row:
        rows.append(current_row)

    # Create DXF
    doc = ezdxf.new(dxfversion="R2010")
    doc.units = units.M
    msp = doc.modelspace()

    x = padding
    y = padding
    text_height = 0.25

    # Track overall drawing extents for PNG preview
    drawn_rects = []  # tuples: (x1,y1,x2,y2,label)

    for row in rows:
        x = padding
        row_height = 0
        for c, side in row:
        # rectangle corners
        x1 = x
        y1 = y
        x2 = x + side
        y2 = y + side

        # draw rectangle as lightweight polyline (closed)
        msp.add_lwpolyline([(x1, y1), (x2, y1), (x2, y2), (x1, y2)], close=True)

        # add label: name and area
        label = f"{c['name']}\nArea: {c['area']:.3f} m^2\nVol: {c['volume']:.3f} m^3\nDepth: {c['depth']:.3f} m"
        # ezdxf doesn't support multi-line text in add_text, so split lines
        lines = label.split("\n")
        for idx, line in enumerate(lines):
            msp.add_text(line, dxfattribs={"height": text_height}).set_pos((x1 + 0.05, y2 - (idx + 1) * (text_height + 0.02)), align="LEFT")

            drawn_rects.append((x1, y1, x2, y2, c['name']))
            x = x2 + padding
            row_height = max(row_height, side)
        y += row_height + padding

    filename = input("Filename to save DXF (default: compartments.dxf): ").strip() or "compartments.dxf"
    doc.saveas(filename)
    print(f"Saved DXF to {filename}")

    # Create PNG preview using matplotlib
    try:
        # compute extents
        if drawn_rects:
            min_x = min(r[0] for r in drawn_rects) - padding
            min_y = min(r[1] for r in drawn_rects) - padding
            max_x = max(r[2] for r in drawn_rects) + padding
            max_y = max(r[3] for r in drawn_rects) + padding
        else:
            min_x = min_y = 0
            max_x = max_y = 1

        fig_w = max(1.0, max_x - min_x)
        fig_h = max(1.0, max_y - min_y)

        fig = plt.figure(figsize=(fig_w, fig_h))
        ax = fig.add_subplot(111)
        for x1, y1, x2, y2, label in drawn_rects:
            rect_w = x2 - x1
            rect_h = y2 - y1
            ax.add_patch(plt.Rectangle((x1, y1), rect_w, rect_h, fill=False, edgecolor='black'))
            ax.text(x1 + 0.05, y2 - 0.05, label, fontsize=8, verticalalignment='top')

        ax.set_xlim(min_x, max_x)
        ax.set_ylim(min_y, max_y)
        ax.set_aspect('equal')
        ax.invert_yaxis()
        ax.axis('off')

        png_name = filename.rsplit('.', 1)[0] + '.png'
        fig.savefig(png_name, bbox_inches='tight', dpi=150)
        plt.close(fig)
        print(f"Saved PNG preview to {png_name}")
    except Exception as e:
        print(f"PNG preview failed: {e}")


if __name__ == "__main__":
    main()
