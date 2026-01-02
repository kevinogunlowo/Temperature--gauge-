import tkinter as tk
import math

# ----- Constants -----
# Temperature values
MIN_VALUE = 0
MAX_VALUE = 100
NORMAL_MIN = 20
NORMAL_MAX = 30

# Layout & scaling
GAUGE_VERTICAL_OFFSET = 0.65     # Vertical placement (as fraction of window height)
GAUGE_SIZE_RATIO = 3             # Determines gauge size relative to window

# Gauge design
TICK_INTERVAL = 20               # Temperature tick interval
TICK_LENGTH = 10                 # Tick mark length
LABEL_OFFSET = 15                # Distance between tick and label
NEEDLE_MARGIN = 25               # Gap between needle tip and gauge edge
VALUE_TEXT_OFFSET = 40           # Distance between gauge center and numeric display
SHADOW_OFFSET = 4                # Distance for gauge shadow offset
ARC_WIDTH = 6                    # Width of main gauge arc
CENTER_CIRCLE_RADIUS = 8         # Radius of needle pivot circle
SHADOW_THICKNESS = 8             # Thickness of gauge shadow

# Layout spacing
PADDING_SMALL = 3
PADDING_MEDIUM = 8
PADDING_LARGE = 10

# Fonts
FONT_MAIN = ("Helvetica", 12, "bold")
FONT_LABEL = ("Helvetica", 10)
FONT_INFO = ("Helvetica", 9)
FONT_DISPLAY = ("Helvetica", 16, "bold")

# Colors
COLOR_BACKGROUND = "#f5f7fa"
COLOR_GAUGE_OUTLINE = "#444"
COLOR_TICK = "#333"
COLOR_TEXT = "#222"
COLOR_SHADOW = "#ddd"
COLOR_NORMAL_TEXT = "#666"
COLOR_BUTTON_BG = "#0077b6"
COLOR_BUTTON_ACTIVE = "#023e8a"
COLOR_NEEDLE_COLD = "#0077b6"
COLOR_NEEDLE_NORMAL = "#2d6a4f"
COLOR_NEEDLE_HOT = "#d90429"


class GaugeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Responsive Temperature Gauge")
        self.value = 25  # Starting temperature
        self.root.configure(bg=COLOR_BACKGROUND)

        # Canvas setup
        self.canvas = tk.Canvas(root, bg=COLOR_BACKGROUND, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True, pady=(PADDING_LARGE, 0))

        # Input label
        tk.Label(
            root, text="Enter Temperature (°C):",
            font=FONT_LABEL, bg=COLOR_BACKGROUND
        ).pack(pady=(PADDING_LARGE, PADDING_SMALL))

        # Entry box
        self.entry = tk.Entry(root, width=10, justify="center", font=("Helvetica", 11))
        self.entry.pack(pady=PADDING_SMALL)

        # Button
        tk.Button(
            root, text="Update Gauge", font=FONT_LABEL,
            bg=COLOR_BUTTON_BG, fg="white",
            activebackground=COLOR_BUTTON_ACTIVE, activeforeground="white",
            relief="flat", padx=PADDING_MEDIUM, pady=PADDING_SMALL,
            command=self.update_value
        ).pack(pady=PADDING_SMALL)

        # Info label
        self.info = tk.Label(
            root,
            text=f"Low: {MIN_VALUE}°C | Normal: {NORMAL_MIN}-{NORMAL_MAX}°C | High: {MAX_VALUE}°C",
            fg=COLOR_NORMAL_TEXT, bg=COLOR_BACKGROUND, font=FONT_INFO
        )
        self.info.pack(pady=PADDING_MEDIUM)

        # Bind resize event
        self.canvas.bind("<Configure>", self.on_resize)
        self.draw_gauge()

    def on_resize(self, event):
        """Triggered when window is resized to redraw the gauge dynamically."""
        self.draw_gauge()

    def draw_gauge(self):
        """Draw the temperature gauge based on current size and value."""
        self.canvas.delete("all")

        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        center_x = width / 2
        center_y = height * GAUGE_VERTICAL_OFFSET
        radius = min(width, height) / GAUGE_SIZE_RATIO

        # Background shadow
        self.canvas.create_oval(
            center_x - radius + SHADOW_OFFSET,
            center_y - radius + SHADOW_OFFSET,
            center_x + radius + SHADOW_OFFSET,
            center_y + radius + SHADOW_OFFSET,
            outline=COLOR_SHADOW, width=SHADOW_THICKNESS
        )

        # Main gauge arc
        self.canvas.create_arc(
            center_x - radius, center_y - radius,
            center_x + radius, center_y + radius,
            start=180, extent=180, style="arc", width=ARC_WIDTH,
            outline=COLOR_GAUGE_OUTLINE
        )

        # Tick marks & labels
        for val in range(MIN_VALUE, MAX_VALUE + 1, TICK_INTERVAL):
            angle = 180 + (val - MIN_VALUE) * 180 / (MAX_VALUE - MIN_VALUE)
            rad = math.radians(angle)

            x1 = center_x + (radius - TICK_LENGTH) * math.cos(rad)
            y1 = center_y + (radius - TICK_LENGTH) * math.sin(rad)
            x2 = center_x + radius * math.cos(rad)
            y2 = center_y + radius * math.sin(rad)
            self.canvas.create_line(x1, y1, x2, y2, fill=COLOR_TICK, width=2)

            self.canvas.create_text(
                x1 - LABEL_OFFSET * math.cos(rad),
                y1 - LABEL_OFFSET * math.sin(rad),
                text=str(val), font=FONT_LABEL, fill=COLOR_TEXT
            )

        # Compute needle position
        pointer_angle = 180 + (self.value - MIN_VALUE) * 180 / (MAX_VALUE - MIN_VALUE)
        rad = math.radians(pointer_angle)
        pointer_x = center_x + (radius - NEEDLE_MARGIN) * math.cos(rad)
        pointer_y = center_y + (radius - NEEDLE_MARGIN) * math.sin(rad)

        # Needle color based on range
        if self.value < NORMAL_MIN:
            color = COLOR_NEEDLE_COLD
        elif self.value > NORMAL_MAX:
            color = COLOR_NEEDLE_HOT
        else:
            color = COLOR_NEEDLE_NORMAL

        # Draw needle and pivot circle
        self.canvas.create_line(center_x, center_y, pointer_x, pointer_y, width=5, fill=color, capstyle=tk.ROUND)
        self.canvas.create_oval(
            center_x - CENTER_CIRCLE_RADIUS, center_y - CENTER_CIRCLE_RADIUS,
            center_x + CENTER_CIRCLE_RADIUS, center_y + CENTER_CIRCLE_RADIUS,
            fill="#111", outline=""
        )

        # Draw numeric display
        self.canvas.create_text(
            center_x, center_y + VALUE_TEXT_OFFSET,
            text=f"{self.value:.1f} °C", font=FONT_DISPLAY, fill=color
        )

    def update_value(self):
        """Handles user input and updates the gauge safely."""
        try:
            val = float(self.entry.get())
            if val < MIN_VALUE or val > MAX_VALUE:
                raise ValueError
            self.value = val
            self.draw_gauge()
        except ValueError:
            self.canvas.delete("all")
            width = self.canvas.winfo_width()
            height = self.canvas.winfo_height()
            self.canvas.create_text(
                width / 2, height / 2,
                text="Enter a number between 0–100!",
                fill=COLOR_NEEDLE_HOT, font=FONT_MAIN
            )


# ----- Run the App -----
if __name__ == "__main__":
    root = tk.Tk() #instantiate the Tkinter window
    root.geometry("520x430") #set the window size
    app = GaugeApp(root) #create an instance of the GaugeApp class
    root.mainloop() #start the Tkinter event loop
