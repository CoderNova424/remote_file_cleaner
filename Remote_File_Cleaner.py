import base64
#| Import            | What it does                                                                                 |
#| ----------------- | -------------------------------------------------------------------------------------------- |
#| `base64`          | Converts data to/from **Base64** text, often used for encoding files or images               |
#| `io`              | Lets Python work with **data in memory as if it were a file**                                |
#| `os`              | Interacts with the **operating system** — files, folders, paths, environment variables, etc. |
#| `threading`       | Runs tasks in **separate threads**, useful for keeping a GUI responsive                      |
#| `socket`          | Provides **network communication** functionality                                             |
#| `secrets`         | Generates **secure random values**, such as tokens or random keys                            |
#| `time`            | Deals with **time, delays, and timestamps**                                                  |
#| `json`            | Reads and creates **JSON data**                                                              |
#| `zipfile`         | Creates and extracts **`.zip` files**                                                        |
#| `tempfile`        | Creates **temporary files and folders**                                                      |
#| `shutil`          | Copies, moves, and deletes **files/folders**                                                 |
#| `sys`             | Gives access to Python/system information, command-line arguments, etc.                      |
#| `subprocess`      | Runs **other programs/commands** from Python                                                 |
#| `tkinter`         | Python's built-in library for making **GUI windows**                                         |
#| `filedialog`      | Creates things like **"Choose a file"** dialogs                                              |
#| `messagebox`      | Creates popup messages such as **Yes/No, Error, Warning**                                    |
#| `ttk`             | Provides nicer-looking Tkinter widgets like buttons, tabs, progress bars, etc.               |
#| `PIL.Image`       | Opens, creates, and edits **images**                                                         |
#| `PIL.ImageDraw`   | Draws shapes/text onto images                                                                |
#| `PIL.ImageFilter` | Applies image effects such as **blur and sharpening**                                        |
#| `PIL.ImageTk`     | Allows PIL images to be displayed inside **Tkinter GUIs**                                    |




import io
import os
import threading
import socket
import secrets
import time
import json
import zipfile
import tempfile
import shutil
import sys
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from PIL import Image, ImageDraw, ImageFilter, ImageTk

try:
    from send2trash import send2trash
    TRASH_AVAILABLE = True
except ImportError:
    TRASH_AVAILABLE = False

try:
    RESAMPLE = Image.Resampling.BICUBIC
except AttributeError:  # older Pillow
    RESAMPLE = Image.BICUBIC

JUNK_EXTENSIONS = [".log", ".tmp", ".bak", ".cache", ".old", ".dmp", ".chk", ".gid", ".ds_store"]
COMMON_EXTENSIONS = [".log", ".tmp", ".bak", ".cache", ".old", ".dmp", ".chk", ".gid", ".ds_store"]
WIN_W, WIN_H = 900, 680

REMOTE_PORT = 45821
CODE_TTL_SECONDS = 600
BUFFER_SIZE = 64 * 1024

DISCOVERY_TIMEOUT = 0.18
TRANSFER_TIMEOUT = 30


APP_ICON_B64 = (
    "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"
)


TEXT_DARK = "#1d1d1f"
TEXT_MUTED = "#6e6e73"
ACCENT_BTN = "#0a84ff"
ACCENT_BTN_ACTIVE = "#0071e3"
DANGER_BTN = "#ff453a"
DANGER_BTN_ACTIVE = "#d70015"
GLASS_WHITE = (255, 255, 255, 155)
GLASS_BORDER = (255, 255, 255, 190)


def human_size(num_bytes):
    size = float(num_bytes)
    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"


# ---------------------------------------------------------------------------
# Glass background rendering
# ---------------------------------------------------------------------------
def _lerp(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))


def make_gradient_bg(width, height):
    """Small diagonal 3-stop gradient, upscaled smoothly (fast + no banding)."""
    
    stops = [(226, 233, 241), (242, 239, 246), (224, 237, 249)]
    sw = 80
    sh = max(1, int(sw * height / width))
    small = Image.new("RGB", (sw, sh))
    px = small.load()
    for y in range(sh):
        for x in range(sw):
            t = (x / sw + y / sh) / 2
            if t < 0.5:
                color = _lerp(stops[0], stops[1], t * 2)
            else:
                color = _lerp(stops[1], stops[2], (t - 0.5) * 2)
            px[x, y] = color
    return small.resize((width, height), RESAMPLE)


def add_frosted_panel(base_rgba, box, radius=22, blur=22,
                       tint=(255, 255, 255, 65), border=(255, 255, 255, 130),
                       shadow_alpha=55):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0

    shadow = Image.new("RGBA", base_rgba.size, (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle(
        [x0, y0 + 8, x1, y1 + 8], radius=radius, fill=(20, 15, 40, shadow_alpha))
    shadow = shadow.filter(ImageFilter.GaussianBlur(14))
    base_rgba.alpha_composite(shadow)

    crop = base_rgba.crop(box).convert("RGB").filter(ImageFilter.GaussianBlur(blur))
    panel = Image.alpha_composite(crop.convert("RGBA"), Image.new("RGBA", (w, h), tint))

    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, w - 1, h - 1], radius=radius, fill=255)
    base_rgba.paste(panel, box, mask)

    ImageDraw.Draw(base_rgba).rounded_rectangle(box, radius=radius, outline=border, width=2)
    return base_rgba


def avg_color(img_rgba, box, lighten=0.0):
    cropped = img_rgba.convert("RGB").crop(box)
    pixels = list(cropped.getdata())
    n = len(pixels)
    if n == 0:
        return "#ffffff"
    r = sum(p[0] for p in pixels) / n
    g = sum(p[1] for p in pixels) / n
    b = sum(p[2] for p in pixels) / n

    if lighten:
        r += (255 - r) * lighten
        g += (255 - g) * lighten
        b += (255 - b) * lighten
    return f"#{int(r):02x}{int(g):02x}{int(b):02x}"



def make_pairing_code():
    """Create a random six-digit session code; no IP address is encoded."""
    return f"{secrets.randbelow(1_000_000):06d}"


def recv_exact(sock, size):
    chunks = []
    remaining = size
    while remaining:
        chunk = sock.recv(min(BUFFER_SIZE, remaining))
        if not chunk:
            raise ConnectionError("Connection closed unexpectedly.")
        chunks.append(chunk)
        remaining -= len(chunk)
    return b"".join(chunks)


def send_json(sock, payload):
    data = json.dumps(payload).encode("utf-8")
    sock.sendall(len(data).to_bytes(4, "big"))
    sock.sendall(data)


def recv_json(sock):
    size = int.from_bytes(recv_exact(sock, 4), "big")
    if size > 4 * 1024 * 1024:
        raise ValueError("Invalid message size.")
    return json.loads(recv_exact(sock, size).decode("utf-8"))


def folder_stats(folder):
    count = 0
    total = 0
    for root, _dirs, files in os.walk(folder):
        for name in files:
            path = os.path.join(root, name)
            try:
                total += os.path.getsize(path)
                count += 1
            except OSError:
                pass
    return count, total


def zip_folder(folder):
    temp = tempfile.NamedTemporaryFile(prefix="junkcleaner_", suffix=".zip", delete=False)
    temp.close()
    archive = temp.name
    base = os.path.abspath(folder)
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _dirs, files in os.walk(base):
            for name in files:
                path = os.path.join(root, name)
                zf.write(path, os.path.relpath(path, base))
    return archive


class JunkCleanerApp:
    TOP_BOX = (20, 20, WIN_W - 20, 180)
    LIST_BOX = (20, 195, WIN_W - 20, 560)
    FOOTER_BOX = (20, 580, WIN_W - 20, 660)

    def __init__(self, root):
        self.root = root
        self.selected_folder = ""
        self.found_files = []
        self.ext_vars = {ext: tk.BooleanVar(value=True) for ext in JUNK_EXTENSIONS}
        self.custom_ext_var = tk.StringVar()
        self.trash_var = tk.BooleanVar(value=TRASH_AVAILABLE)
        self.remote_server = None
        self.remote_code = None
        self.remote_code_created = 0

        self._build_background()
        self._build_ui()

    def _build_background(self):
        bg = make_gradient_bg(WIN_W, WIN_H).convert("RGBA")
        add_frosted_panel(
            bg, self.TOP_BOX, radius=18, blur=18,
            tint=GLASS_WHITE, border=GLASS_BORDER, shadow_alpha=35
        )
        add_frosted_panel(
            bg, self.LIST_BOX, radius=18, blur=20,
            tint=(255, 255, 255, 145), border=GLASS_BORDER, shadow_alpha=35
        )
        add_frosted_panel(
            bg, self.FOOTER_BOX, radius=18, blur=18,
            tint=(255, 255, 255, 150), border=GLASS_BORDER, shadow_alpha=30
        )

        self.colors = {
            "top": avg_color(bg, self.TOP_BOX),
            "list": avg_color(bg, self.LIST_BOX),
            "footer": avg_color(bg, self.FOOTER_BOX),
            "chip": avg_color(bg, self.LIST_BOX, lighten=0.32),
            "chip_alt": avg_color(bg, self.LIST_BOX, lighten=0.18),
        }
        self._bg_image = ImageTk.PhotoImage(bg)

    def _build_ui(self):
        self.root.title("Junk File & Folder Cleaner")
        self.root.geometry(f"{WIN_W}x{WIN_H}")
        self.root.resizable(False, False)

        tk.Label(self.root, image=self._bg_image, bd=0).place(x=0, y=0, width=WIN_W, height=WIN_H)

        style = ttk.Style(self.root)
        style.theme_use("clam")

        style.configure("Treeview", background=self.colors["chip"], fieldbackground=self.colors["chip"],
                         foreground=TEXT_DARK, rowheight=30, borderwidth=0, font=("Segoe UI", 10))
        style.map("Treeview", background=[("selected", ACCENT_BTN)], foreground=[("selected", "white")])
        style.configure("Treeview.Heading", background=self.colors["list"], foreground=TEXT_MUTED,
                         borderwidth=0, font=("Segoe UI", 9, "bold"))
        style.map("Treeview.Heading", background=[("active", self.colors["list"])])

        style.configure("Vertical.TScrollbar", background=self.colors["list"],
                         troughcolor=self.colors["list"], arrowsize=12)

        style.configure("Top.TCheckbutton", background=self.colors["top"], foreground=TEXT_DARK,
                         font=("Segoe UI", 9))
        style.map("Top.TCheckbutton", background=[("active", self.colors["top"])])
        style.configure("Footer.TCheckbutton", background=self.colors["footer"], foreground=TEXT_MUTED,
                         font=("Segoe UI", 9))
        style.map("Footer.TCheckbutton", background=[("active", self.colors["footer"])])

        style.configure("Glass.Horizontal.TProgressbar", background=ACCENT_BTN,
                         troughcolor=self.colors["top"], borderwidth=0, thickness=6)

        # ---------------- Top glass panel ----------------
        tk.Label(self.root, text="🧹  Junk File & Folder Cleaner", font=("Segoe UI", 18, "bold"),
                 bg=self.colors["top"], fg=TEXT_DARK).place(x=40, y=28)

        self.scan_btn = tk.Button(self.root, text="📁  Select Folder & Scan", font=("Segoe UI", 10, "bold"),
                                   bg=ACCENT_BTN, fg="white", activebackground=ACCENT_BTN_ACTIVE,
                                   activeforeground="white", relief="flat", bd=0, cursor="hand2",
                                   highlightthickness=0,
                                   command=self.select_folder)
        self.scan_btn.place(x=700, y=28, width=160, height=42)

        self.remote_btn = tk.Button(
            self.root, text="🔗  Remote Clean", font=("Segoe UI", 10, "bold"),
            bg=self.colors["chip"], fg=TEXT_DARK, activebackground="#e8e8ed",
            relief="flat", bd=0, cursor="hand2", highlightthickness=0,
            command=self.open_remote_clean
        )
        self.remote_btn.place(x=560, y=28, width=125, height=42)

        ext_frame = tk.Frame(self.root, bg=self.colors["top"])
        ext_frame.place(x=40, y=80, width=820, height=26)
        tk.Label(ext_frame, text="Extensions:", bg=self.colors["top"], fg=TEXT_MUTED,
                 font=("Segoe UI", 9)).pack(side="left", padx=(0, 8))
        for ext, var in self.ext_vars.items():
            ttk.Checkbutton(ext_frame, text=ext, variable=var, style="Top.TCheckbutton").pack(side="left", padx=4)
        tk.Label(ext_frame, text="Custom (e.g. .cache,.old):", bg=self.colors["top"], fg=TEXT_MUTED,
                 font=("Segoe UI", 9)).pack(side="left", padx=(16, 6))
        tk.Entry(ext_frame, textvariable=self.custom_ext_var, width=18, bg=self.colors["chip"], fg=TEXT_DARK,
                 insertbackground=TEXT_DARK, relief="flat").pack(side="left", ipady=3)

        self.path_label = tk.Label(self.root, text="No folder selected", font=("Segoe UI", 9),
                                    bg=self.colors["top"], fg=TEXT_MUTED, anchor="w")
        self.path_label.place(x=40, y=130, width=800, height=20)

        self.progress = ttk.Progressbar(self.root, style="Glass.Horizontal.TProgressbar", mode="determinate")
        self.progress.place(x=40, y=158, width=820, height=6)

        # ---------------- List view glass panel ----------------
        self.tree_frame = tk.Frame(self.root, bg=self.colors["list"])
        self.tree_frame.place(x=40, y=210, width=820, height=330)

        self.result_hint = tk.Label(
            self.root, text="Scan results • select individual files or use Delete All",
            font=("Segoe UI", 8), bg=self.colors["list"], fg=TEXT_MUTED, anchor="w"
        )
        self.result_hint.place(x=40, y=192, width=500, height=16)

        self.tree = ttk.Treeview(self.tree_frame, columns=("name", "ext", "size", "path"), show="headings", style="Treeview")
        self.tree.heading("name", text="File Name")
        self.tree.heading("ext", text="Type")
        self.tree.heading("size", text="Size")
        self.tree.heading("path", text="Path")

        self.tree.column("name", width=200, anchor="w")
        self.tree.column("ext", width=80, anchor="center")
        self.tree.column("size", width=90, anchor="e")
        self.tree.column("path", width=450, anchor="w")

        scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview, style="Vertical.TScrollbar")
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.bind("<Delete>", lambda _e: self.delete_selected())
        self.tree.bind("<Double-1>", self.open_result_location)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # ---------------- Footer glass panel ----------------
        footer_frame = tk.Frame(self.root, bg=self.colors["footer"])
        footer_frame.place(x=40, y=590, width=820, height=60)

        self.summary_label = tk.Label(footer_frame, text="0 junk files found  •  0 B", font=("Segoe UI", 10, "bold"),
                                       bg=self.colors["footer"], fg=TEXT_DARK, anchor="w")
        self.summary_label.place(x=0, y=6, width=340, height=22)

        trash_state = "normal" if TRASH_AVAILABLE else "disabled"
        self.trash_check = ttk.Checkbutton(
            footer_frame, text="Move to Recycle Bin",
            variable=self.trash_var, style="Footer.TCheckbutton",
            state=trash_state
        )
        self.trash_check.place(x=0, y=32, width=260, height=22)
        if not TRASH_AVAILABLE:
            tk.Label(footer_frame, text="(install send2trash for this)", font=("Segoe UI", 8),
                     bg=self.colors["footer"], fg=TEXT_MUTED).place(x=0, y=50, width=260, height=16)

        self.delete_selected_btn = tk.Button(footer_frame, text="Delete Selected", font=("Segoe UI", 10, "bold"),
                                              bg=self.colors["chip"], fg=TEXT_DARK, relief="flat", bd=0,
                                              cursor="hand2", command=self.delete_selected)
        self.delete_selected_btn.place(x=520, y=8, width=140, height=40)

        self.delete_all_btn = tk.Button(footer_frame, text="Delete All", font=("Segoe UI", 10, "bold"),
                                         bg=DANGER_BTN, fg="white", activebackground=DANGER_BTN_ACTIVE,
                                         activeforeground="white", relief="flat", bd=0, cursor="hand2",
                                         command=self.delete_all)
        self.delete_all_btn.place(x=670, y=8, width=150, height=40)

        self._add_hover(self.scan_btn, ACCENT_BTN, ACCENT_BTN_ACTIVE)
        self._add_hover(self.remote_btn, self.colors["chip"], "#e8e8ed")
        self._add_hover(self.delete_selected_btn, self.colors["chip"], "#e8e8ed")
        self._add_hover(self.delete_all_btn, DANGER_BTN, DANGER_BTN_ACTIVE)

        self._set_delete_buttons_state("disabled")

    def _add_hover(self, widget, normal_bg, hover_bg):
        widget.bind("<Enter>", lambda _e: widget.config(bg=hover_bg))
        widget.bind("<Leave>", lambda _e: widget.config(bg=normal_bg))

    # ------------------------------------------------------------------
    # Behaviour
    # ------------------------------------------------------------------

    # ------------------------------------------------------------------
    # Remote Clean
    # ------------------------------------------------------------------
    def open_remote_clean(self):
        win = tk.Toplevel(self.root)
        win.title("Remote Clean")
        win.geometry("520x430")
        win.resizable(False, False)
        win.transient(self.root)
        win.grab_set()

        tk.Label(win, text="Remote Clean", font=("Segoe UI", 20, "bold"),
                 fg=TEXT_DARK).pack(pady=(24, 4))
        tk.Label(
            win,
            text="Transfer a folder using a temporary 6-digit pairing code.\n"
                 "The code does not contain or expose an IP address.",
            font=("Segoe UI", 10), fg=TEXT_MUTED, justify="center"
        ).pack(pady=(0, 20))

        host = tk.Frame(win)
        host.pack(fill="x", padx=30, pady=8)

        tk.Label(host, text="I want to:", font=("Segoe UI", 10, "bold"),
                 fg=TEXT_DARK).pack(anchor="w", pady=(0, 8))

        tk.Button(
            host, text="📤  Send a folder", font=("Segoe UI", 11, "bold"),
            bg=ACCENT_BTN, fg="white", activebackground=ACCENT_BTN_ACTIVE,
            relief="flat", bd=0, height=2,
            command=lambda: self.remote_send_dialog(win)
        ).pack(fill="x", pady=5)

        tk.Button(
            host, text="📥  Receive a folder", font=("Segoe UI", 11, "bold"),
            bg="#e8e8ed", fg=TEXT_DARK, activebackground="#d8d8dd",
            relief="flat", bd=0, height=2,
            command=lambda: self.remote_receive_dialog(win)
        ).pack(fill="x", pady=5)

        tk.Label(
            win,
            text="Both computers must be running this app and connected to the same local network.",
            font=("Segoe UI", 9), fg=TEXT_MUTED, wraplength=430, justify="center"
        ).pack(pady=22)

    def remote_send_dialog(self, parent):
        folder = filedialog.askdirectory(parent=parent, title="Choose folder to send")
        if not folder:
            return

        count, size = folder_stats(folder)
        code = make_pairing_code()

        win = tk.Toplevel(parent)
        win.title("Waiting for receiver")
        win.geometry("500x390")
        win.resizable(False, False)
        win.transient(parent)

        tk.Label(win, text="Share this code", font=("Segoe UI", 13),
                 fg=TEXT_MUTED).pack(pady=(25, 2))
        tk.Label(win, text=code, font=("Segoe UI", 38, "bold"),
                 fg=ACCENT_BTN).pack(pady=2)
        tk.Label(win, text=f"{count:,} files  •  {human_size(size)}",
                 font=("Segoe UI", 10), fg=TEXT_MUTED).pack(pady=2)
        status = tk.Label(win, text="Waiting for the other computer…",
                          font=("Segoe UI", 10, "bold"), fg=TEXT_DARK)
        status.pack(pady=20)

        self.remote_code = code
        self.remote_code_created = time.time()

        def server_worker():
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.remote_server = server
            try:
                server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                server.bind(("", REMOTE_PORT))
                server.listen(1)
                server.settimeout(1.0)

                # Pairing is a random session code, not an encoded IP.
                while time.time() - self.remote_code_created < CODE_TTL_SECONDS:
                    try:
                        conn, _addr = server.accept()
                    except socket.timeout:
                        continue

                    with conn:
                        try:
                            hello = recv_json(conn)
                            if hello.get("code") != code:
                                send_json(conn, {"ok": False, "error": "Invalid pairing code."})
                                continue

                            send_json(conn, {
                                "ok": True,
                                "folder_name": os.path.basename(os.path.abspath(folder)),
                                "files": count,
                                "size": size
                            })

                            approval = recv_json(conn)
                            if not approval.get("approved"):
                                self.root.after(0, lambda: status.config(text="Receiver declined the transfer."))
                                break

                            archive = zip_folder(folder)
                            try:
                                archive_size = os.path.getsize(archive)
                                send_json(conn, {"ready": True, "size": archive_size})
                                with open(archive, "rb") as f:
                                    while True:
                                        chunk = f.read(BUFFER_SIZE)
                                        if not chunk:
                                            break
                                        conn.sendall(chunk)
                                self.root.after(0, lambda: status.config(text="Transfer complete."))
                            finally:
                                try:
                                    os.remove(archive)
                                except OSError:
                                    pass
                            break
                        except Exception as exc:
                            self.root.after(0, lambda e=str(exc): status.config(text=f"Transfer error: {e}"))
                            break
            finally:
                try:
                    server.close()
                except OSError:
                    pass
                self.remote_server = None

        threading.Thread(target=server_worker, daemon=True).start()

        tk.Button(
            win, text="Cancel", command=lambda: win.destroy(),
            bg="#e8e8ed", fg=TEXT_DARK, relief="flat", bd=0
        ).pack(pady=15)

    def remote_receive_dialog(self, parent):
        win = tk.Toplevel(parent)
        win.title("Receive a folder")
        win.geometry("500x390")
        win.resizable(False, False)
        win.transient(parent)

        tk.Label(win, text="Enter pairing code", font=("Segoe UI", 15, "bold"),
                 fg=TEXT_DARK).pack(pady=(30, 12))

        code_var = tk.StringVar()
        entry = tk.Entry(
            win, textvariable=code_var, justify="center",
            font=("Segoe UI", 24, "bold"), width=8, relief="flat"
        )
        entry.pack(pady=5)
        entry.focus_set()

        status = tk.Label(win, text="The code expires after 10 minutes.",
                          font=("Segoe UI", 9), fg=TEXT_MUTED)
        status.pack(pady=12)

        def connect():
            code = code_var.get().strip()
            if not (code.isdigit() and len(code) == 6):
                status.config(text="Enter exactly 6 digits.")
                return

            # Discover the sender locally without putting an IP in the code.
            threading.Thread(
                target=self._remote_discover_and_receive,
                args=(code, win, status),
                daemon=True
            ).start()

        tk.Button(
            win, text="Connect", font=("Segoe UI", 11, "bold"),
            bg=ACCENT_BTN, fg="white", activebackground=ACCENT_BTN_ACTIVE,
            relief="flat", bd=0, command=connect
        ).pack(pady=10)

    def _remote_discover_and_receive(self, code, win, status):
        status.config(text="Looking for the sender on your local network…")

        # We deliberately do not encode an IP into the six-digit code.
        # The app tries local addresses on the current subnet.
        local = socket.gethostbyname(socket.gethostname())
        parts = local.split(".")
        if len(parts) != 4:
            self.root.after(0, lambda: status.config(text="Could not determine local network."))
            return

        prefix = ".".join(parts[:3])
        candidates = [f"{prefix}.{i}" for i in range(1, 255) if i != int(parts[3])]

        def try_host(host):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Keep discovery itself fast so a full subnet sweep finishes
            # quickly and the UI doesn't feel stuck.
            sock.settimeout(DISCOVERY_TIMEOUT)
            try:
                sock.connect((host, REMOTE_PORT))
                send_json(sock, {"code": code})
                info = recv_json(sock)
                if not info.get("ok"):
                    return False

                # We've now confirmed this is the right host. The rest of
                # the exchange (waiting for approval, zipping on the other
                # end, streaming the archive) legitimately takes longer
                # than the short discovery window above, so loosen the
                # timeout before doing anything else with this socket.
                sock.settimeout(TRANSFER_TIMEOUT)

                def ask():
                    approved = messagebox.askyesno(
                        "Allow Remote Folder?",
                        f"Another computer wants to send you:\n\n"
                        f"Folder: {info.get('folder_name', 'Unknown')}\n"
                        f"Files: {info.get('files', 0):,}\n"
                        f"Size: {human_size(info.get('size', 0))}\n\n"
                        f"Do you want to receive it?",
                        parent=win
                    )
                    try:
                        send_json(sock, {"approved": approved})
                        if not approved:
                            status.config(text="Transfer declined.")
                            sock.close()
                            return

                        status.config(text="Receiving folder…")
                        ready = recv_json(sock)
                        total = int(ready["size"])

                        target = filedialog.askdirectory(
                            parent=win, title="Choose where to save the received folder"
                        )
                        if not target:
                            send_json(sock, {"approved": False})
                            status.config(text="Transfer cancelled.")
                            sock.close()
                            return

                        # Once the user has picked a destination, the actual
                        # byte-for-byte download shouldn't be bound by a
                        # fixed timeout at all — large folders can take a
                        # while. Let this final phase block indefinitely.
                        sock.settimeout(None)

                        archive = tempfile.NamedTemporaryFile(
                            prefix="received_", suffix=".zip", delete=False
                        ).name
                        received = 0
                        with open(archive, "wb") as f:
                            while received < total:
                                chunk = sock.recv(min(BUFFER_SIZE, total - received))
                                if not chunk:
                                    raise ConnectionError("Sender disconnected.")
                                f.write(chunk)
                                received += len(chunk)

                        folder_name = info.get("folder_name") or "Received Folder"
                        # Normalize so the destination path is well-formed
                        # regardless of the separators the folder picker
                        # returned (Tkinter dialogs use forward slashes,
                        # even on Windows).
                        destination = os.path.normpath(os.path.join(target, folder_name))
                        os.makedirs(destination, exist_ok=True)

                        with zipfile.ZipFile(archive, "r") as zf:
                            # Prevent archive path traversal.
                            root = os.path.abspath(destination)
                            for member in zf.infolist():
                                member_path = os.path.abspath(os.path.join(destination, member.filename))
                                if not (member_path == root or member_path.startswith(root + os.sep)):
                                    raise ValueError("Unsafe path in received archive.")
                            zf.extractall(destination)

                        try:
                            os.remove(archive)
                        except OSError:
                            pass

                        status.config(text="Folder received successfully.")
                        messagebox.showinfo(
                            "Transfer complete",
                            f"Received {folder_name}.\n\nYou can now scan it for junk files.",
                            parent=win
                        )
                    except socket.timeout:
                        status.config(text="Connection timed out waiting for data — try again.")
                        messagebox.showerror(
                            "Transfer error",
                            "The connection timed out while waiting for data from the sender.",
                            parent=win
                        )
                    except Exception as exc:
                        status.config(text=f"Transfer error: {exc}")
                        messagebox.showerror("Transfer error", str(exc), parent=win)

                self.root.after(0, ask)
                return True
            except (OSError, ConnectionError, ValueError, json.JSONDecodeError):
                return False
            finally:
                if sock.fileno() != -1 and not sock._closed:
                    # Keep the socket open only when ask() will continue using it.
                    # In that case the closure is handled by the receiving callback.
                    pass

        # Limit concurrent connection attempts so the UI stays responsive.
        found = []
        workers = []
        lock = threading.Lock()

        def worker(host):
            if try_host(host):
                with lock:
                    found.append(host)

        for host in candidates:
            t = threading.Thread(target=worker, args=(host,), daemon=True)
            workers.append(t)
            t.start()

        deadline = time.time() + 8
        while time.time() < deadline and not found:
            time.sleep(0.05)

        if not found:
            self.root.after(
                0, lambda: status.config(
                    text="No matching sender found. Make sure both apps are on the same Wi-Fi."
                )
            )


    def open_result_location(self, _event=None):
        selected = self.tree.selection()
        if not selected:
            return
        path = self.tree.item(selected[0], "values")[3]
        try:
            if os.name == "nt":
                os.startfile(os.path.dirname(path))
            elif sys.platform == "darwin":
                subprocess.Popen(["open", os.path.dirname(path)])
            else:
                subprocess.Popen(["xdg-open", os.path.dirname(path)])
        except Exception:
            pass

    def _set_delete_buttons_state(self, state):
        self.delete_selected_btn.config(state=state)
        self.delete_all_btn.config(state=state)

    def _active_extensions(self):
        exts = {ext for ext, var in self.ext_vars.items() if var.get()}
        custom = self.custom_ext_var.get().strip()
        if custom:
            for part in custom.split(","):
                part = part.strip()
                if not part:
                    continue
                if not part.startswith("."):
                    part = "." + part
                exts.add(part.lower())
        return exts


    def select_all_extensions(self):
        for var in self.ext_vars.values():
            var.set(True)

    def clear_extensions(self):
        for var in self.ext_vars.values():
            var.set(False)

    def open_extension_manager(self):
        win = tk.Toplevel(self.root)
        win.title("Junk File Types")
        win.geometry("430x500")
        win.resizable(False, False)
        win.transient(self.root)

        tk.Label(
            win, text="Choose file types to clean",
            font=("Segoe UI", 16, "bold"), fg=TEXT_DARK
        ).pack(pady=(20, 4))

        tk.Label(
            win,
            text="Only checked extensions can appear in scan results.",
            font=("Segoe UI", 9), fg=TEXT_MUTED
        ).pack(pady=(0, 12))

        body = tk.Frame(win)
        body.pack(fill="both", expand=True, padx=28)

        canvas = tk.Canvas(body, highlightthickness=0)
        scrollbar = ttk.Scrollbar(body, orient="vertical", command=canvas.yview)
        inner = tk.Frame(canvas)

        inner.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=inner, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for ext in sorted(self.ext_vars):
            ttk.Checkbutton(
                inner, text=ext, variable=self.ext_vars[ext],
                style="Top.TCheckbutton"
            ).pack(anchor="w", pady=3)

        custom_frame = tk.Frame(win)
        custom_frame.pack(fill="x", padx=28, pady=12)

        tk.Label(
            custom_frame, text="Add extensions:",
            font=("Segoe UI", 9, "bold"), fg=TEXT_DARK
        ).pack(anchor="w")

        tk.Entry(
            custom_frame, textvariable=self.custom_ext_var,
            font=("Segoe UI", 10), relief="flat"
        ).pack(fill="x", pady=5)

        tk.Label(
            custom_frame,
            text="Example: .cache, .old, .whatever",
            font=("Segoe UI", 8), fg=TEXT_MUTED
        ).pack(anchor="w")

        tk.Button(
            win, text="Done", font=("Segoe UI", 10, "bold"),
            bg=ACCENT_BTN, fg="white", relief="flat", bd=0,
            command=win.destroy
        ).pack(pady=(0, 18), ipadx=25, ipady=5)

    def get_selected_extension_names(self):
        return sorted(self._active_extensions())

    def select_folder(self):
        folder = filedialog.askdirectory(title="Select folder to scan")
        if not folder:
            return
        # Normalize immediately so every downstream consumer (scan results,
        # deletion, "open location") works with OS-native separators. On
        # Windows, Tkinter's folder picker returns forward slashes, which
        # breaks send2trash's internal \\?\ long-path handling if left as-is.
        self.selected_folder = os.path.normpath(folder)
        self.path_label.config(text=self.selected_folder)
        self.scan_folder()

    def scan_folder(self):
        exts = self._active_extensions()
        if not exts:
            messagebox.showwarning("No extensions selected",
                                    "Pick at least one extension (or enter a custom one) to scan for.")
            return

        self.tree.delete(*self.tree.get_children())
        self.found_files = []
        self._set_delete_buttons_state("disabled")
        self.scan_btn.config(state="disabled", text="Scanning…")
        self.progress.config(mode="indeterminate")
        self.progress.start(12)

        thread = threading.Thread(target=self._scan_worker, args=(self.selected_folder, exts), daemon=True)
        thread.start()

    def _scan_worker(self, folder, exts):
        results = []
        try:
            for dirpath, _dirnames, filenames in os.walk(folder):
                for fname in filenames:
                    ext = os.path.splitext(fname)[1].lower()
                    if ext in exts:
                        full_path = os.path.join(dirpath, fname)
                        try:
                            size = os.path.getsize(full_path)
                        except OSError:
                            size = 0
                        results.append((fname, ext, size, full_path))
        except Exception as exc:
            self.root.after(0, lambda: messagebox.showerror("Scan error", str(exc)))

        self.root.after(0, lambda: self._scan_finished(results))

    def _scan_finished(self, results):
        self.progress.stop()
        self.progress.config(mode="determinate", value=0)
        self.scan_btn.config(state="normal", text="📁  Select Folder & Scan")

        self.found_files = results
        total_size = 0
        for fname, ext, size, full_path in results:
            self.tree.insert("", "end", values=(fname, ext, human_size(size), full_path))
            total_size += size

        self.summary_label.config(text=f"{len(results)} junk files found  •  {human_size(total_size)}")
        self._set_delete_buttons_state("normal" if results else "disabled")

        if not results:
            messagebox.showinfo("Scan complete", "No junk files found for the selected extensions.")

    def _delete_paths(self, paths):
        use_trash = TRASH_AVAILABLE
        deleted, failed = [], []
        for path in paths:
            try:
             
                norm_path = os.path.normpath(path)
                if use_trash:
                    send2trash(norm_path)
                else:
                    os.remove(norm_path)
                deleted.append(path)
            except Exception as exc:
                failed.append((path, str(exc)))
        return deleted, failed

    def delete_selected(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showinfo("Nothing selected", "Select one or more rows in the list first.")
            return

        paths = [self.tree.item(item, "values")[3] for item in selected_items]
        verb = "move to Recycle Bin" if TRASH_AVAILABLE else "delete"
        extensions = sorted({self.tree.item(item, "values")[1] for item in selected_items})
        ext_text = ", ".join(extensions)
        if not messagebox.askyesno(
            "Confirm delete",
            f"{verb.capitalize()} {len(paths)} file(s)?\n\n"
            f"Types: {ext_text}\n\n"
            "Files are sent to the Recycle Bin when send2trash is available."
        ):
            return

        deleted, failed = self._delete_paths(paths)
        for item in selected_items:
            values = self.tree.item(item, "values")
            if values[3] in deleted:
                self.tree.delete(item)

        self._after_delete(deleted, failed)

    def delete_all(self):
        if not self.found_files:
            return
        paths = [f[3] for f in self.found_files]
        verb = "move to Recycle Bin" if TRASH_AVAILABLE else "delete"
        extensions = sorted({f[1] for f in self.found_files})
        ext_text = ", ".join(extensions)
        if not messagebox.askyesno(
            "Confirm delete",
            f"{verb.capitalize()} ALL {len(paths)} junk file(s)?\n\n"
            f"Types: {ext_text}\n\n"
            "This only affects files found by the currently selected extensions."
        ):
            return

        deleted, failed = self._delete_paths(paths)
        self.tree.delete(*self.tree.get_children())
        self._after_delete(deleted, failed)

    def _after_delete(self, deleted, failed):
        self.found_files = [f for f in self.found_files if f[3] not in deleted]
        total_size = sum(f[2] for f in self.found_files)
        self.summary_label.config(text=f"{len(self.found_files)} junk files found  •  {human_size(total_size)}")
        self._set_delete_buttons_state("normal" if self.found_files else "disabled")

        msg = f"Deleted {len(deleted)} file(s)."
        if failed:
            msg += f"\n{len(failed)} failed:\n" + "\n".join(f"{p}: {e}" for p, e in failed[:5])
            messagebox.showwarning("Delete finished with errors", msg)
        else:
            messagebox.showinfo("Done", msg)


def main():
    root = tk.Tk()
    JunkCleanerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
