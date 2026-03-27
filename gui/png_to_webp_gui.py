#!/usr/bin/env python3
"""Desktop GUI: convert PNGs to WebP using the bundled cwebp encoder (Google libwebp)."""
from __future__ import annotations

import subprocess
import sys
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox

ROOT = Path(__file__).resolve().parent.parent
CWEBP = ROOT / "tools" / "bin" / "cwebp.exe"
DEFAULT_IN = ROOT / "input"
DEFAULT_OUT = ROOT / "converted"

# Premium dark palette
APP_BG = "#070709"
SURFACE = "#101015"
SURFACE_ELEVATED = "#16161f"
ENTRY_BG = "#eef0f5"
ENTRY_TEXT = "#121218"
ENTRY_BORDER = "#c5cad6"
ACCENT = "#c9223d"
ACCENT_HOVER = "#e63252"
MUTED = "#8b8b9a"
TEXT = "#f4f4f8"

R_LARGE = 22
R_CTL = 14
R_BTN = 16


def _ensure_customtkinter():
    try:
        import customtkinter as ctk  # type: ignore

        return ctk
    except ImportError:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "customtkinter"],
            cwd=str(ROOT),
        )
        import customtkinter as ctk  # type: ignore

        return ctk


def human_kb(n: int) -> str:
    if n < 1024:
        return f"{n} B"
    return f"{n / 1024:.1f} KB"


class App:
    def __init__(self, ctk) -> None:
        self._ctk = ctk
        self.root = ctk.CTk()
        self.root.title("png-to-webp-windows")
        self.root.geometry("720x600")
        self.root.minsize(560, 480)
        self.root.configure(fg_color=APP_BG)

        self.in_dir = tk.StringVar(value=str(DEFAULT_IN))
        self.out_dir = tk.StringVar(value=str(DEFAULT_OUT))
        self.target_kb = tk.StringVar(value="75")
        self.use_quality = tk.BooleanVar(value=False)
        self.quality = tk.StringVar(value="78")
        self._busy = False

        ctk.set_appearance_mode("dark")
        self._build()

    def _build(self) -> None:
        ctk = self._ctk

        shell = ctk.CTkFrame(self.root, fg_color=SURFACE, corner_radius=R_LARGE, border_width=1, border_color="#25252e")
        shell.pack(fill="both", expand=True, padx=20, pady=20)

        inner = ctk.CTkFrame(shell, fg_color="transparent")
        inner.pack(fill="both", expand=True, padx=22, pady=22)

        head = ctk.CTkLabel(
            inner,
            text="PNG → WebP",
            font=ctk.CTkFont(family="Segoe UI", size=26, weight="bold"),
            text_color=TEXT,
        )
        head.pack(anchor="w")

        sub = ctk.CTkLabel(
            inner,
            text="Local conversion with cwebp — nothing leaves your machine.",
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            text_color=MUTED,
        )
        sub.pack(anchor="w", pady=(4, 18))

        card = ctk.CTkFrame(inner, fg_color=SURFACE_ELEVATED, corner_radius=R_LARGE, border_width=1, border_color="#202028")
        card.pack(fill="x", pady=(0, 14))

        cp = ctk.CTkFrame(card, fg_color="transparent")
        cp.pack(fill="x", padx=18, pady=18)

        self._path_row(cp, "PNG folder", self.in_dir, self._pick_in, 0)
        self._path_row(cp, "Output folder", self.out_dir, self._pick_out, 1)

        opts = ctk.CTkFrame(inner, fg_color=SURFACE_ELEVATED, corner_radius=R_LARGE, border_width=1, border_color="#202028")
        opts.pack(fill="x", pady=(0, 14))

        op = ctk.CTkFrame(opts, fg_color="transparent")
        op.pack(fill="x", padx=18, pady=16)

        ctk.CTkLabel(
            op, text="Target size (KB / file)", font=ctk.CTkFont(size=13, weight="bold"), text_color=TEXT
        ).pack(side="left")
        self._mini_entry(op, self.target_kb, 72).pack(side="left", padx=(10, 24))

        self.chk = ctk.CTkCheckBox(
            op,
            text="Fixed quality (-q)",
            variable=self.use_quality,
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=TEXT,
            fg_color=ACCENT,
            hover_color=ACCENT_HOVER,
            border_width=2,
            corner_radius=R_CTL,
        )
        self.chk.pack(side="left")

        ctk.CTkLabel(op, text="q", font=ctk.CTkFont(size=13, weight="bold"), text_color=MUTED).pack(
            side="left", padx=(16, 6)
        )
        self._mini_entry(op, self.quality, 56).pack(side="left")

        self.go_btn = ctk.CTkButton(
            inner,
            text="Start conversion",
            command=self._start,
            font=ctk.CTkFont(family="Segoe UI", size=15, weight="bold"),
            fg_color=ACCENT,
            hover_color=ACCENT_HOVER,
            height=48,
            corner_radius=R_BTN,
            border_width=0,
        )
        self.go_btn.pack(anchor="w", pady=(4, 12))

        self.prog = ctk.CTkProgressBar(
            inner,
            height=10,
            corner_radius=5,
            fg_color="#2a2a34",
            progress_color=ACCENT,
            border_width=0,
        )
        self.prog.pack(fill="x", pady=(0, 10))
        self.prog.set(0)

        ctk.CTkLabel(inner, text="Activity log", font=ctk.CTkFont(size=12, weight="bold"), text_color=MUTED).pack(anchor="w")

        self.log = ctk.CTkTextbox(
            inner,
            height=200,
            font=ctk.CTkFont(family="Consolas", size=12, weight="bold"),
            fg_color="#0e0e14",
            text_color=TEXT,
            border_width=1,
            border_color="#2a2a34",
            corner_radius=R_LARGE,
            scrollbar_button_color="#3d3d4a",
            scrollbar_button_hover_color="#505060",
        )
        self.log.pack(fill="both", expand=True, pady=(6, 0))

    def _path_row(self, parent, label: str, var: tk.StringVar, cmd, row: int) -> None:
        ctk = self._ctk
        row_f = ctk.CTkFrame(parent, fg_color="transparent")
        row_f.pack(fill="x", pady=(0, 12) if row == 0 else 0)

        ctk.CTkLabel(row_f, text=label, font=ctk.CTkFont(size=13, weight="bold"), text_color=TEXT, width=120, anchor="w").pack(
            side="left", padx=(0, 12)
        )

        ent = ctk.CTkEntry(
            row_f,
            textvariable=var,
            height=42,
            font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"),
            fg_color=ENTRY_BG,
            text_color=ENTRY_TEXT,
            border_color=ENTRY_BORDER,
            border_width=1,
            corner_radius=R_CTL,
        )
        ent.pack(side="left", fill="x", expand=True, padx=(0, 10))

        ctk.CTkButton(
            row_f,
            text="Browse",
            command=cmd,
            width=100,
            height=42,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=ACCENT,
            hover_color=ACCENT_HOVER,
            corner_radius=R_BTN,
        ).pack(side="left")

    def _mini_entry(self, parent, var: tk.StringVar, width: int):
        ctk = self._ctk
        return ctk.CTkEntry(
            parent,
            textvariable=var,
            width=width,
            height=38,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=ENTRY_BG,
            text_color=ENTRY_TEXT,
            border_color=ENTRY_BORDER,
            border_width=1,
            corner_radius=R_CTL,
        )

    def _log(self, s: str) -> None:
        self.log.insert("end", s + "\n")
        self.log.see("end")

    def _pick_in(self) -> None:
        d = filedialog.askdirectory(initialdir=self.in_dir.get() or str(ROOT))
        if d:
            self.in_dir.set(d)

    def _pick_out(self) -> None:
        d = filedialog.askdirectory(initialdir=self.out_dir.get() or str(ROOT))
        if d:
            self.out_dir.set(d)

    def _start(self) -> None:
        if self._busy:
            return
        if not CWEBP.is_file():
            messagebox.showerror("Missing encoder", f"cwebp not found at:\n{CWEBP}")
            return
        in_p = Path(self.in_dir.get().strip())
        out_p = Path(self.out_dir.get().strip())
        if not in_p.is_dir():
            messagebox.showerror("Folder", f"PNG folder not found:\n{in_p}")
            return
        try:
            target = int(self.target_kb.get().strip())
        except ValueError:
            messagebox.showerror("Invalid value", "Target size must be a number (KB).")
            return
        try:
            q = int(self.quality.get().strip())
        except ValueError:
            messagebox.showerror("Invalid value", "Quality (-q) must be a number.")
            return
        if target < 1 or target > 99999:
            messagebox.showerror("Invalid value", "Target KB should be in a sensible range.")
            return
        if q < 0 or q > 100:
            messagebox.showerror("Invalid value", "Quality must be between 0 and 100.")
            return

        pngs = sorted(in_p.glob("*.png"))
        if not pngs:
            messagebox.showinfo("No PNGs", f"No .png files in:\n{in_p}")
            return

        self._busy = True
        self.go_btn.configure(state="disabled")
        self.prog.set(0)
        n = len(pngs)
        self.log.delete("0.0", "end")

        def worker() -> None:
            out_p.mkdir(parents=True, exist_ok=True)
            use_q = self.use_quality.get()
            ok = 0
            fail = 0
            total_in = 0
            total_out = 0
            for i, src in enumerate(pngs):
                dst = out_p / (src.stem + ".webp")
                if use_q:
                    args = [
                        str(CWEBP),
                        "-q",
                        str(q),
                        "-m",
                        "6",
                        "-mt",
                        "-sharp_yuv",
                        "-alpha_q",
                        "100",
                        "-metadata",
                        "none",
                        str(src),
                        "-o",
                        str(dst),
                    ]
                else:
                    size_b = target * 1024
                    args = [
                        str(CWEBP),
                        "-size",
                        str(size_b),
                        "-m",
                        "6",
                        "-mt",
                        "-sharp_yuv",
                        "-alpha_q",
                        "100",
                        "-metadata",
                        "none",
                        str(src),
                        "-o",
                        str(dst),
                    ]
                try:
                    r = subprocess.run(args, capture_output=True, text=True, check=False)
                except OSError as e:
                    self.after(0, lambda m=str(e): self._log(f"ERROR {m}"))
                    fail += 1
                    self.after(0, lambda p=(i + 1) / n: self.prog.set(p))
                    continue
                if r.returncode != 0:
                    err = (r.stderr or r.stdout or "").strip()[:220]
                    self.after(0, lambda n_=src.name, err_=err: self._log(f"ERROR {n_}: {err_}"))
                    fail += 1
                else:
                    ok += 1
                    sz_in = src.stat().st_size
                    sz_out = dst.stat().st_size if dst.is_file() else 0
                    total_in += sz_in
                    total_out += sz_out
                    self.after(
                        0,
                        lambda n_=src.name, si=sz_in, so=sz_out: self._log(f"OK {n_}  ({human_kb(si)} → {human_kb(so)})"),
                    )
                self.after(0, lambda p=(i + 1) / n: self.prog.set(p))

            def done() -> None:
                self._busy = False
                self.go_btn.configure(state="normal")
                self._log(f"--- Finished. Success: {ok}  Failed: {fail} ---")
                if ok:
                    self._log(f"Total in: {human_kb(total_in)}  out: {human_kb(total_out)}")
                if fail:
                    messagebox.showwarning("Done", f"{fail} file(s) failed.")
                elif ok:
                    messagebox.showinfo("Done", f"Wrote {ok} WebP file(s) to:\n{out_p}")

            self.after(0, done)

        threading.Thread(target=worker, daemon=True).start()

    def after(self, ms, fn):
        return self.root.after(ms, fn)

    def mainloop(self) -> None:
        self.root.mainloop()


def main() -> int:
    if sys.platform == "win32":
        try:
            from ctypes import windll

            windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass
    ctk = _ensure_customtkinter()
    App(ctk).mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
