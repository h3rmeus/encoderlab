import tkinter as tk
from tkinter import scrolledtext, messagebox
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from encoder_engine import ALGORITHMS, CATEGORIES, encode, decode

BG      = "#0f111a"
PANEL   = "#161b27"
SURFACE = "#1e2330"
BORDER  = "#2a3040"
ACCENT  = "#4f9eff"
GREEN   = "#3ddc84"
RED     = "#ff5f5f"
TEXT    = "#e2e8f0"
MUTED   = "#6b7a99"

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("EncoderLab")
        self.geometry("1100x780")
        self.minsize(880, 580)
        self.configure(bg=BG)
        self._cur = list(ALGORITHMS.keys())[0]
        self._build()

    def _btn(self, parent, text, bg, cmd, **kw):
        return tk.Button(parent, text=text, bg=bg, fg=TEXT,
                         activebackground=bg, activeforeground=TEXT,
                         font=("Consolas", 10, "bold"), relief="flat",
                         bd=0, cursor="hand2", command=cmd, **kw)

    def _area(self, parent):
        t = scrolledtext.ScrolledText(
            parent, bg=SURFACE, fg=TEXT, insertbackground=TEXT,
            font=("Consolas", 10), relief="flat", bd=0,
            padx=10, pady=8, wrap="word",
            selectbackground=ACCENT, selectforeground="#000"
        )
        return t

    def _build(self):
        hdr = tk.Frame(self, bg=PANEL, height=52)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        tk.Label(hdr, text="⬡  EncoderLab", bg=PANEL, fg=ACCENT,
                 font=("Consolas", 17, "bold")).pack(side="left", padx=20, pady=10)
        tk.Label(hdr, text="18 encoding and cipher algorithms", bg=PANEL, fg=MUTED,
                 font=("Consolas", 10)).pack(side="left")

        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True, padx=14, pady=10)

        self._build_left(body)
        self._build_right(body)

        sb = tk.Frame(self, bg=PANEL, height=26)
        sb.pack(fill="x", side="bottom")
        sb.pack_propagate(False)
        self._status = tk.StringVar(value="Ready")
        tk.Label(sb, textvariable=self._status, bg=PANEL, fg=MUTED,
                 font=("Consolas", 9)).pack(side="left", padx=14)

    def _build_left(self, parent):
        lf = tk.Frame(parent, bg=PANEL, width=240)
        lf.pack(side="left", fill="y", padx=(0, 12))
        lf.pack_propagate(False)

        tk.Label(lf, text="ALGORITHM", bg=PANEL, fg=ACCENT,
                 font=("Consolas", 10, "bold")).pack(anchor="w", padx=14, pady=(14, 4))

        self._lb = tk.Listbox(lf, bg=SURFACE, fg=TEXT,
                              selectbackground=ACCENT, selectforeground="#000",
                              font=("Consolas", 9), bd=0, highlightthickness=0,
                              activestyle="none", relief="flat")
        self._lb.pack(fill="both", expand=True, padx=10, pady=(0, 6))
        self._lb.bind("<<ListboxSelect>>", self._on_select)

        self._lbmap = {}
        idx = 0
        for cat, algos in CATEGORIES.items():
            self._lb.insert("end", f"  {cat}")
            self._lb.itemconfig(idx, fg=MUTED, selectbackground=PANEL,
                                selectforeground=MUTED)
            self._lbmap[idx] = None
            idx += 1
            for a in algos:
                self._lb.insert("end", f"    {a}")
                self._lbmap[idx] = a
                idx += 1

        self._lb.selection_set(1)

        tk.Frame(lf, bg=BORDER, height=1).pack(fill="x", padx=10)
        tk.Label(lf, text="DESCRIPTION", bg=PANEL, fg=MUTED,
                 font=("Consolas", 8, "bold")).pack(anchor="w", padx=14, pady=(8, 2))
        self._desc = tk.Label(lf, text="", bg=PANEL, fg=MUTED,
                              font=("Consolas", 8), wraplength=214, justify="left")
        self._desc.pack(anchor="w", padx=14, pady=(0, 12))
        self._refresh_desc()

    def _build_right(self, parent):
        rf = tk.Frame(parent, bg=BG)
        rf.pack(side="left", fill="both", expand=True)
        rf.columnconfigure(0, weight=1)
        rf.rowconfigure(1, weight=1)
        rf.rowconfigure(4, weight=1)

        tk.Label(rf, text="INPUT TEXT", bg=BG, fg=TEXT,
                 font=("Consolas", 9, "bold")).grid(row=0, column=0, sticky="w", pady=(0, 3))
        self._inp = self._area(rf)
        self._inp.grid(row=1, column=0, sticky="nsew", pady=(0, 8))

        btns = tk.Frame(rf, bg=BG)
        btns.grid(row=2, column=0, sticky="ew", pady=4)
        self._btn(btns, "  ⬡  ENCODE  ", ACCENT, self._do_enc).pack(
            side="left", ipady=5, ipadx=6, padx=(0, 8))
        self._btn(btns, "  ⬡  DECODE  ", "#2d6a4f", self._do_dec).pack(
            side="left", ipady=5, ipadx=6, padx=(0, 8))
        self._btn(btns, "  ↕  Swap  ", SURFACE, self._swap).pack(
            side="left", ipady=5, padx=(0, 8))
        self._btn(btns, "  ✕  Clear  ", "#5a1f1f", self._clear).pack(
            side="left", ipady=5)
        self._btn(btns, "  ⎘  Copy result  ", SURFACE, self._copy).pack(
            side="right", ipady=5)

        tk.Label(rf, text="RESULT", bg=BG, fg=TEXT,
                 font=("Consolas", 9, "bold")).grid(row=3, column=0, sticky="w", pady=(0, 3))
        self._out = self._area(rf)
        self._out.grid(row=4, column=0, sticky="nsew")
        self._out.bind("<Key>", lambda e: "break")

        rf.rowconfigure(1, weight=1)
        rf.rowconfigure(4, weight=1)

    def _on_select(self, _=None):
        sel = self._lb.curselection()
        if not sel:
            return
        name = self._lbmap.get(sel[0])
        if name:
            self._cur = name
            self._refresh_desc()

    def _refresh_desc(self):
        self._desc.config(text=ALGORITHMS[self._cur]['desc'])

    def _set_out(self, text, color=TEXT):
        self._out.config(state="normal", fg=color)
        self._out.delete("1.0", "end")
        self._out.insert("end", text)
        self._out.config(state="disabled")

    def _do_enc(self):
        t = self._inp.get("1.0", "end-1c")
        if not t.strip():
            messagebox.showwarning("Empty", "Please enter some text.")
            return
        try:
            self._set_out(encode(self._cur, t), ACCENT)
            self._status.set(f"✓  Encoded: {self._cur}")
        except Exception as e:
            self._set_out(str(e), RED)
            self._status.set("Encoding error")

    def _do_dec(self):
        t = self._inp.get("1.0", "end-1c")
        if not t.strip():
            messagebox.showwarning("Empty", "Please enter encoded text.")
            return
        try:
            self._set_out(decode(self._cur, t), GREEN)
            self._status.set(f"✓  Decoded: {self._cur}")
        except Exception as e:
            self._set_out(str(e), RED)
            self._status.set("Decoding error")

    def _swap(self):
        a = self._inp.get("1.0", "end-1c")
        b = self._out.get("1.0", "end-1c")
        self._inp.delete("1.0", "end")
        self._inp.insert("end", b)
        self._set_out(a)

    def _clear(self):
        self._inp.delete("1.0", "end")
        self._set_out("")
        self._status.set("Cleared")

    def _copy(self):
        text = self._out.get("1.0", "end-1c")
        if text:
            self.clipboard_clear()
            self.clipboard_append(text)
            self._status.set("Copied to clipboard")

if __name__ == "__main__":
    App().mainloop()
