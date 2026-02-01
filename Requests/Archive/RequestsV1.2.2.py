##########################################################################################
#                                   !!DISCLAIMER!!                                       #
#                                                                                        #
#  This software is provided for EDUCATIONAL AND RESEARCH PURPOSES ONLY.                 #
#  The author does not condone, encourage, or support the use of this tool for:          #
#  - Brute-forcing passwords or unauthorized access to systems.                          #
#  - Performing Denial of Service (DoS) or Distributed Denial of Service (DDoS) attacks. #
#  - Any form of illegal cyber activity or disruption of services.                       #
#                                                                                        #
#  The user is 100% responsible for their actions. Always ensure you have explicit,      #
#  written permission before testing the security of any system or network.              #
#                                                                                        #
##########################################################################################

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import httpx
from urllib.parse import urljoin, urlencode
import time
import re
import random
import string

# Dictionary to store settings for each URL
url_configs = {}

# Simple generators for when presets are used
def generate_value(preset_key, min_len=6, max_len=16, include_numbers=True, include_capitals=True, include_symbols=False):
    if preset_key == "common_passwords":
        commons = ["123456", "password", "admin", "qwerty", "letmein", "welcome", "12345678", "abc123", "password1"]
        return random.choice(commons)
    
    if preset_key == "admin_variants":
        return random.choice(["admin", "administrator", "root", "admin123", "root123", "adm1n", "admin!"])
    
    if preset_key == "numbers_only":
        length = random.randint(max(1, min_len), min(20, max_len))
        return ''.join(random.choices(string.digits, k=length))
    
    if preset_key == "letters_only":
        chars = string.ascii_lowercase
        if include_capitals:
            chars += string.ascii_uppercase
        length = random.randint(max(4, min_len), min(20, max_len))
        return ''.join(random.choices(chars, k=length))
    
    # default / alphanum / strong
    chars = string.ascii_lowercase
    if include_capitals:
        chars += string.ascii_uppercase
    if include_numbers:
        chars += string.digits
    if include_symbols:
        chars += "!@#$%^&*()_+-=[]{}|"
    
    length = random.randint(max(6, min_len), min(24, max_len))
    val = ''.join(random.choices(chars, k=length))
    
    # enforce minimum requirements if requested
    if include_numbers and not any(c.isdigit() for c in val):
        pos = random.randint(0, length-1)
        val = val[:pos] + random.choice(string.digits) + val[pos+1:]
    if include_capitals and not any(c.isupper() for c in val):
        pos = random.randint(0, length-1)
        val = val[:pos] + random.choice(string.ascii_uppercase) + val[pos+1:]
    
    return val


def open_config_window(url_label):
    """Opens configuration window for a specific URL"""
    url_match = re.search(r'https?://[^\s\]]+', url_label)
    if not url_match:
        messagebox.showerror("Error", "Could not extract valid URL")
        return
    full_url = url_match.group(0)

    config_win = tk.Toplevel(root)
    config_win.title(f"Config for: {full_url[:55]}...")
    config_win.geometry("580x860")

    container = ttk.Frame(config_win, padding=18)
    container.pack(fill=tk.BOTH, expand=True)

    cfg = url_configs.get(full_url, {})

    # ── BOX 1 ── (usually parameter name / field name)
    ttk.Label(container, text="BOX 1 (Parameter name or values):", font=('Segoe UI', 10, 'bold')).pack(anchor=tk.W)
    box1_entry = ttk.Entry(container, width=55)
    box1_entry.pack(fill=tk.X, pady=(4, 4))
    box1_entry.insert(0, cfg.get("box1", "username"))

    f1 = ttk.Frame(container)
    f1.pack(fill=tk.X, pady=6)
    ttk.Label(f1, text="Preset for BOX 1:").pack(side=tk.LEFT, padx=(0,12))
    p1_var = tk.StringVar(value=cfg.get("p1", "N"))
    for opt in ["Y", "N", "F"]:
        ttk.Radiobutton(f1, text=opt, variable=p1_var, value=opt).pack(side=tk.LEFT, padx=10)

    ttk.Label(container, text="Or use text file for BOX 1 values:").pack(anchor=tk.W, pady=(10,2))
    box1_path_var = tk.StringVar(value=cfg.get("box1_path", ""))
    ttk.Entry(container, textvariable=box1_path_var, width=55).pack(fill=tk.X, pady=2)
    ttk.Button(container, text="Browse file for BOX 1", command=lambda: box1_path_var.set(
        filedialog.askopenfilename(title="Select BOX 1 values txt", filetypes=[("Text files","*.txt")])
    )).pack(anchor=tk.W, pady=4)

    ttk.Separator(container, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=12)

    # ── BOX 2 ── (values / passwords / list source)
    ttk.Label(container, text="BOX 2 (Values / Wordlist / Passwords):", font=('Segoe UI', 10, 'bold')).pack(anchor=tk.W)
    box2_entry = ttk.Entry(container, width=55)
    box2_entry.pack(fill=tk.X, pady=(4, 8))
    box2_entry.insert(0, cfg.get("box2", ""))

    f2 = ttk.Frame(container)
    f2.pack(fill=tk.X, pady=6)
    ttk.Label(f2, text="Preset for BOX 2:").pack(side=tk.LEFT, padx=(0,12))
    p2_var = tk.StringVar(value=cfg.get("p2", "N"))
    for opt in ["Y", "N", "F"]:
        ttk.Radiobutton(f2, text=opt, variable=p2_var, value=opt).pack(side=tk.LEFT, padx=10)

    ttk.Label(container, text="Or use wordlist file for BOX 2:").pack(anchor=tk.W, pady=(10,2))
    wordlist_path_var = tk.StringVar(value=cfg.get("wordlist_path", ""))
    ttk.Entry(container, textvariable=wordlist_path_var, width=55).pack(fill=tk.X, pady=2)
    ttk.Button(container, text="Browse wordlist", command=lambda: wordlist_path_var.set(
        filedialog.askopenfilename(title="Select wordlist txt", filetypes=[("Text files","*.txt")])
    )).pack(anchor=tk.W, pady=4)

    ttk.Separator(container, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=14)

    # ── Constraints (used when generating values with presets) ──
    ttk.Label(container, text="Generation constraints (when preset = Y/F):", font=('Segoe UI', 9, 'bold')).pack(anchor=tk.W, pady=(8,4))

    grid_frame = ttk.Frame(container)
    grid_frame.pack(fill=tk.X, pady=6)

    constraints = [
        ("Min Length", "min_len", cfg.get("min_len", "6")),
        ("Max Length", "max_len", cfg.get("max_len", "20")),
        ("Min Numbers", "min_numbers", cfg.get("min_numbers", "1")),
        ("Min Symbols", "min_symbols", cfg.get("min_symbols", "0"))
    ]

    constraint_vars = {}
    for i, (label, key, default) in enumerate(constraints):
        r, c = divmod(i, 2)
        ttk.Label(grid_frame, text=label + ":").grid(row=r, column=c*3, sticky=tk.W, padx=(0,4), pady=3)
        ent = ttk.Entry(grid_frame, width=6)
        ent.grid(row=r, column=c*3+1, padx=4, pady=3)
        ent.insert(0, default)
        constraint_vars[key] = ent

    # Character types
    char_frame = ttk.Frame(container)
    char_frame.pack(fill=tk.X, pady=8)
    num_var = tk.BooleanVar(value=cfg.get("numbers", True))
    cap_var = tk.BooleanVar(value=cfg.get("capitals", True))
    sym_var = tk.BooleanVar(value=cfg.get("symbols", False))
    tk.Checkbutton(char_frame, text="Numbers", variable=num_var).pack(side=tk.LEFT, padx=12)
    tk.Checkbutton(char_frame, text="Capitals", variable=cap_var).pack(side=tk.LEFT, padx=12)
    tk.Checkbutton(char_frame, text="Symbols", variable=sym_var).pack(side=tk.LEFT, padx=12)

    ttk.Separator(container, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=14)

    # ── Retry / flag condition ──
    ttk.Label(container, text="Flag / retry if response contains:").pack(anchor=tk.W)
    retry_text = ttk.Entry(container, width=55)
    retry_text.pack(fill=tk.X, pady=4)
    retry_text.insert(0, cfg.get("retry_text", "incorrect|failed|invalid|Try again"))

    # ── Save & Test ───────────────────────────────────────────────────
    def save_config():
        try:
            minl = int(constraint_vars["min_len"].get().strip() or "6")
            maxl = int(constraint_vars["max_len"].get().strip() or "20")
            if minl > maxl:
                minl, maxl = maxl, minl
        except:
            minl, maxl = 6, 20

        settings = {
            "box1": box1_entry.get().strip(),
            "p1": p1_var.get(),
            "box1_path": box1_path_var.get().strip(),
            "box2": box2_entry.get().strip(),
            "p2": p2_var.get(),
            "wordlist_path": wordlist_path_var.get().strip(),
            "min_len": minl,
            "max_len": maxl,
            "min_numbers": int(constraint_vars["min_numbers"].get().strip() or "0"),
            "min_symbols": int(constraint_vars["min_symbols"].get().strip() or "0"),
            "numbers": num_var.get(),
            "capitals": cap_var.get(),
            "symbols": sym_var.get(),
            "retry_text": retry_text.get().strip(),
        }

        if (settings["box1"] or settings["p1"] != "N" or settings["box1_path"] or
            settings["p2"] != "N" or settings["wordlist_path"]):
            url_configs[full_url] = settings
            messagebox.showinfo("Saved", "Configuration saved.")
        else:
            messagebox.showinfo("Saved", "No useful settings → not saved.")

    def start_fuzz_test():
        save_config()
        cfg_now = url_configs.get(full_url, {})
        if not cfg_now:
            messagebox.showwarning("Missing", "No configuration saved")
            return

        param = cfg_now.get("box1", "")
        p1_preset = cfg_now.get("p1", "N")
        box1_path = cfg_now.get("box1_path", "")
        p2_preset = cfg_now.get("p2", "N")
        wordlist_path = cfg_now.get("wordlist_path", "")
        min_len = cfg_now["min_len"]
        max_len = cfg_now["max_len"]
        use_num = cfg_now["numbers"]
        use_cap = cfg_now["capitals"]
        use_sym = cfg_now["symbols"]
        retry_if_contains = cfg_now["retry_text"].lower().split("|") if cfg_now.get("retry_text") else []

        # How many attempts
        ATTEMPT_COUNT = 40

        text_output.insert(tk.END, f"\nFuzzing {full_url}  →  {param}=...   ({ATTEMPT_COUNT} attempts)\n", "header")

        keys = []   # BOX 1 values (parameter names or fixed values)
        values = [] # BOX 2 values (payloads)

        # ── Load BOX 1 ───────────────────────────────────────
        if box1_path and p1_preset == "N":
            try:
                with open(box1_path, encoding="utf-8", errors="ignore") as f:
                    keys = [line.strip() for line in f if line.strip()]
                text_output.insert(tk.END, f"Loaded {len(keys)} keys/parameters from BOX 1 file\n")
            except Exception as e:
                text_output.insert(tk.END, f"BOX 1 file error: {e}\n", "error")
                keys = []
        else:
            if param:
                keys = [param]  # single value from entry
            else:
                text_output.insert(tk.END, "No BOX 1 value or file provided\n", "error")
                return

        # ── Load BOX 2 ───────────────────────────────────────
        if wordlist_path and p2_preset == "N":
            try:
                with open(wordlist_path, encoding="utf-8", errors="ignore") as f:
                    values = [line.strip() for line in f if line.strip()]
                text_output.insert(tk.END, f"Loaded {len(values)} values from wordlist\n")
            except Exception as e:
                text_output.insert(tk.END, f"Wordlist error: {e}\n", "error")
                values = []

        if not values:
            text_output.insert(tk.END, f"Generating values (preset: {p2_preset})\n")
            for _ in range(ATTEMPT_COUNT):
                val = generate_value(
                    p2_preset if p2_preset != "N" else "alphanum",
                    min_len, max_len, use_num, use_cap, use_sym
                )
                values.append(val)

        if not keys or not values:
            text_output.insert(tk.END, "Cannot fuzz — missing keys or values\n", "error")
            return

        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

        with httpx.Client(headers=headers, timeout=10.0, follow_redirects=True) as client:
            attempt = 0
            for key in keys:
                for value in values:
                    attempt += 1
                    if attempt > ATTEMPT_COUNT * 2:  # safety limit
                        break

                    try:
                        query = urlencode({key: value})
                        test_url = f"{full_url}?{query}" if "?" not in full_url else f"{full_url}&{query}"

                        r = client.get(test_url)
                        status = r.status_code
                        size = len(r.content) / 1024.0

                        line = f"[{attempt:2d}] {status:3d}  {size:5.1f} KB   {key}={value[:40]}"

                        flagged = any(kw.strip() in r.text.lower() for kw in retry_if_contains if kw.strip())

                        if status == 200:
                            if flagged:
                                text_output.insert(tk.END, line + "   [FLAGGED]\n", "ok")
                            else:
                                # SWAP FLAG FOR CORRECT + GOLD IMPACT
                                text_output.insert(tk.END, line + "   [CORRECT]\n", "gold")
                        elif status in (401, 403):
                            text_output.insert(tk.END, line + "  (auth?)\n", "error")
                        else:
                            text_output.insert(tk.END, line + "\n")

                        if flagged:
                            text_output.insert(tk.END, f"   → Retry condition matched: {r.text[:120]}...\n", "error")

                    except Exception as e:
                        text_output.insert(tk.END, f"[{attempt:2d}] ERROR  {key}={value[:30]}  ({str(e)})\n", "error")

                    text_output.see(tk.END)
                    root.update_idletasks()
                    time.sleep(0.35)

                if attempt >= ATTEMPT_COUNT * 2:
                    break

        text_output.insert(tk.END, "Fuzzing finished.\n\n", "header")


    btn_frame = ttk.Frame(container)
    btn_frame.pack(pady=20)

    ttk.Button(btn_frame, text="Save", command=save_config).pack(side=tk.LEFT, padx=12)
    ttk.Button(btn_frame, text="Test / Fuzz", command=start_fuzz_test).pack(side=tk.LEFT, padx=12)
    ttk.Button(btn_frame, text="Close", command=config_win.destroy).pack(side=tk.LEFT, padx=12)


def filter_only_ok():
    all_text = text_output.get("1.0", tk.END).splitlines()
    text_output.delete("1.0", tk.END)
    
    for line in all_text:
        if any(keyword in line for keyword in ["OK", "Starting", "Base:", "Fuzzing", "FLAGGED", "CORRECT"]):
            start_idx = text_output.index(tk.END)
            text_output.insert(tk.END, line + "\n")
            if "OK" in line:
                end_idx = text_output.index(f"{start_idx} lineend")
                text_output.tag_add("ok", start_idx, end_idx)
            if "CORRECT" in line:
                end_idx = text_output.index(f"{start_idx} lineend")
                text_output.tag_add("gold", start_idx, end_idx)


def on_line_click(event):
    idx = text_output.index(f"@{event.x},{event.y}")
    line_num = idx.split('.')[0]
    line_content = text_output.get(f"{line_num}.0", f"{line_num}.end")
    
    if "OK" in line_content:
        open_config_window(line_content)


def load_paths_from_file():
    file_path = filedialog.askopenfilename(
        title="Select txt file with paths",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    if not file_path:
        return []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except Exception as e:
        messagebox.showerror("File error", str(e))
        return []


def start_checking():
    base_url = entry_base.get().strip()
    if not base_url:
        messagebox.showwarning("Missing base URL", "Please enter a base URL")
        return
    
    paths = load_paths_from_file()
    if not paths:
        return
    
    if not base_url.endswith("/"):
        base_url += "/"
    
    text_output.delete("1.0", tk.END)
    text_output.insert(tk.END, f"Starting checks...\nBase: {base_url}\n\n", "header")
    
    headers = {"User-Agent": "Mozilla/5.0"}

    with httpx.Client(headers=headers, follow_redirects=True, timeout=10.0) as client:
        for i, path in enumerate(paths, 1):
            full_url = urljoin(base_url, path.lstrip("/"))
            try:
                r = client.get(full_url)
                status = r.status_code
                line = f"[{i:3d}] {status:3d} → {full_url}"
                
                if status == 200:
                    line += f"   OK   ({len(r.content)/1024:.1f} KB)"
                    text_output.insert(tk.END, line + "\n", "ok")
                else:
                    text_output.insert(tk.END, line + f"   {status}\n")
                    
            except Exception as e:
                text_output.insert(tk.END, f"ERROR → {full_url} ({e})\n", "error")
            
            text_output.see(tk.END)
            root.update()
            time.sleep(0.5)


# ────────────────────────────────────────────────
#                 GUI SETUP
# ────────────────────────────────────────────────

root = tk.Tk()
root.title("Requests V1.2")
root.geometry("1080x740")

frame_top = ttk.Frame(root, padding=12)
frame_top.pack(fill=tk.X)

ttk.Label(frame_top, text="Base URL:", font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=(0,8))
entry_base = ttk.Entry(frame_top, width=65, font=("Consolas", 11))
entry_base.insert(0, "https://example.com/")
entry_base.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=8)

ttk.Button(frame_top, text="Run Check", command=start_checking).pack(side=tk.LEFT, padx=8)
ttk.Button(frame_top, text="Filter Only OK", command=filter_only_ok).pack(side=tk.LEFT, padx=8)

text_output = scrolledtext.ScrolledText(
    root, wrap=tk.WORD, font=("Consolas", 10), bg="#fdfdfd", cursor="hand2"
)
text_output.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Tags
text_output.tag_config("ok",     foreground="#006400", underline=True)
text_output.tag_config("error",  foreground="#8B0000")
text_output.tag_config("header", foreground="#1E90FF", font=("Consolas", 11, "bold"))

# Correct Status Tag: Gold, Bold, Impact
text_output.tag_config("gold",   foreground="#D4AF37", font=("Impact", 11, "bold"))

text_output.tag_bind("ok", "<Button-1>", on_line_click)

root.mainloop()