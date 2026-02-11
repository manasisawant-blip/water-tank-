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


def get_positive_int(prompt):
    while True:
        try:
            v = int(input(prompt))
            if v <= 0:
                print("Value must be a positive integer. Try again.")
                continue
            return v
        except ValueError:
            print("Please enter an integer.")


def get_nonempty(prompt, default=None):
    v = input(prompt).strip()
    if v:
        return v
    return default


def main():
    print("Interactive compartment DXF generator")
    n = get_positive_int("Number of compartments: ")

    # Global inputs
    depth = get_positive_float("Global Depth/height for all compartments (m): ")
    # choose fixed dimension
    while True:
        fixed_choice = input("Which dimension is fixed for the assembly? Enter 'Width' or 'Length': ").strip().lower()
        if fixed_choice in ("width", "length"):
            break
        print("Please enter 'Width' or 'Length'.")
    fixed_value = get_positive_float(f"Fixed {fixed_choice.title()} value (meters): ")

    compartments = []
    for i in range(1, n + 1):
        name = input(f"Name of compartment {i}: ").strip() or f"Compartment_{i}"
        volume = get_positive_float(f"Volume of '{name}' (cubic meters): ")
        # compute variable dimension: variable = volume / (depth * fixed)
        variable = volume / (depth * fixed_value)
        compartments.append({
            "name": name,
            "volume": volume,
            "depth": depth,
            "fixed_choice": fixed_choice,
            "fixed_value": fixed_value,
            "variable": variable,
        })

    # Compute drawing layout for serial (linear) arrangement
    padding = 0.0  # zero padding between compartments as requested

    # Determine orientation and rectangle sizes
    rects = []  # list of (x1,y1,x2,y2,label, fixed, variable)
    x = 0.0
    y = 0.0
    if compartments and compartments[0]["fixed_choice"] == "width":
        # fixed width => fixed Y size = fixed_value, variable X size varies; stack along X
        for c in compartments:
            w = c["variable"]  # X length
            h = c["fixed_value"]  # Y (width) constant
            x1 = x
            y1 = 0.0
            x2 = x1 + w
            y2 = y1 + h
            rects.append((x1, y1, x2, y2, c["name"], w, h))
            x = x2 + padding
    else:
        # fixed length => fixed X size = fixed_value, variable Y size varies; stack along Y
        for c in compartments:
            w = c["fixed_value"]  # X constant
            h = c["variable"]  # Y length
            x1 = 0.0
            y1 = y
            x2 = x1 + w
            y2 = y1 + h
            rects.append((x1, y1, x2, y2, c["name"], w, h))
            y = y2 + padding

    # Create DXF
    doc = ezdxf.new(dxfversion="R2010")
    doc.units = units.M
    msp = doc.modelspace()

    text_height = 0.25

    # Track drawing extents
    drawn_rects = []
    for (x1, y1, x2, y2, label, w, h) in rects:
        # draw rectangle
        msp.add_lwpolyline([(x1, y1), (x2, y1), (x2, y2), (x1, y2)], close=True)

        # add labels (name, vol, dims). Place inside if space allows, else outside.
        center_x = (x1 + x2) / 2.0
        center_y = (y1 + y2) / 2.0
        vol = next(c['volume'] for c in compartments if c['name'] == label)
        lines = [f"{label}", f"Vol: {vol:.3f} m^3", f"W: {w:.3f} m", f"H: {h:.3f} m"]
        # determine text height scaled to rect
        th = min(text_height, max(0.08, min(w, h) / 8.0))
        # try to place lines starting near top inside rectangle
        top_y = y2 - 0.05
        for idx, line in enumerate(lines):
            t = msp.add_text(line, dxfattribs={"height": th})
            insert_x = x1 + 0.05
            insert_y = top_y - idx * (th + 0.02)
            # if text would be outside bottom, shift to below rectangle
            if insert_y - th < y1 - 0.01:
                insert_y = y1 - (idx + 1) * (th + 0.02)
            t.dxf.insert = (insert_x, insert_y)

        drawn_rects.append((x1, y1, x2, y2, label))

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

        # Add a small margin for preview (visual only)
        margin_x = max(0.1, (max_x - min_x) * 0.02)
        margin_y = max(0.1, (max_y - min_y) * 0.02)

        width = max_x - min_x + 2 * margin_x
        height = max_y - min_y + 2 * margin_y

        # Choose figure size in inches (max cap) while keeping aspect ratio
        max_fig_w = 12.0
        fig_w = min(max_fig_w, max(4.0, width))
        fig_h = max(3.0, fig_w * (height / max(width, 1e-6)))

        fig = plt.figure(figsize=(fig_w, fig_h))
        ax = fig.add_subplot(111)
        for x1, y1, x2, y2, label in drawn_rects:
            rect_w = x2 - x1
            rect_h = y2 - y1
            ax.add_patch(plt.Rectangle((x1, y1), rect_w, rect_h, fill=False, edgecolor='black', linewidth=1))
            # place multi-line text inside if fits
            cx = x1 + 0.05
            cy = y2 - 0.05
            vol = next((c['volume'] for c in compartments if c['name'] == label), None)
            lines = [label, f"Vol: {vol:.3f} m^3" if vol is not None else "", f"{rect_w:.3f} x {rect_h:.3f} m"]
            for i, ln in enumerate(lines):
                ax.text(cx, cy - i * 0.12, ln, fontsize=8, verticalalignment='top', horizontalalignment='left')

        ax.set_xlim(min_x - margin_x, max_x + margin_x)
        ax.set_ylim(min_y - margin_y, max_y + margin_y)
        ax.set_aspect('equal')
        # keep normal axis orientation (no invert) so Y increases upwards
        ax.axis('off')

        png_name = filename.rsplit('.', 1)[0] + '.png'
        fig.savefig(png_name, bbox_inches='tight', dpi=150)
        plt.close(fig)
        print(f"Saved PNG preview to {png_name}")
    except Exception as e:
        print(f"PNG preview failed: {e}")


if __name__ == "__main__":
    main()
