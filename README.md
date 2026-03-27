# png-to-webp-windows

## Project intro

This is a simple **PNG → WebP** converter that can shrink something like a **2 MB PNG down to ~70 KB** (sometimes even smaller), while keeping the picture looking almost the same.

**Repository:** [github.com/DNZYDeniz/png-to-webp-windows](https://github.com/DNZYDeniz/png-to-webp-windows)

It’s built for a **very simple workflow** — no complicated setup: drop PNGs in **`input`**, run the tool, and pick up WebPs from **`converted`**.

**Two ways to use it**

- **Classic batch / CMD** — Double-click **`convert_png_to_webp.bat`**. You get a plain command window and the same fast, lightweight path as always (no GUI; no extra installs if **`cwebp`** is already in the project).
- **Optional desktop GUI** — Run **`run_gui.bat`** for a cleaner, rounded interface (Python + CustomTkinter). Same **Google `cwebp`** encoder underneath. **Target size and quality are easier to adjust** in the GUI (KB per file, or fixed quality **`-q`**), without editing environment variables.

Everything is **lightweight**, **fast**, and **meant for people who want smaller images** without wrestling with heavy tools. Processing stays **on your machine**.

**Highlights**

- Simple **`.bat`** workflow (GUI not required)  
- Optional **GUI** for quicker size / quality tweaks  
- Fast conversion, strong size reduction, minimal visible quality loss  

---

## What it does

Batch-convert every **PNG** in the **`input`** folder to **WebP** using Google’s official **`cwebp`** encoder. Output files go to the **`converted`** folder; originals in **`input`** are **not** deleted.

Default mode targets about **75 KB per image**. You can switch to **fixed quality** (`-q`) if you prefer.

## Do I need to install anything?

| How you run it | Extra installs |
|----------------|----------------|
| **`convert_png_to_webp.bat`** | **None**, if **`tools\bin\cwebp.exe`** is already in your copy of the project. No Python, no Node. |
| **`run_gui.bat`** | **Python 3.8+** (64-bit, from [python.org](https://www.python.org/downloads/), with **“Add to PATH”**). On first launch the GUI may run **`pip install customtkinter`** — **internet** helps; you can also run `pip install customtkinter` yourself first. Standard **tkinter** comes with the usual Windows Python installer. |

**Will it work on every PC?** Only on **Windows** PCs where **`cwebp.exe`** is present at **`tools\bin\cwebp.exe`**. If someone gets the repo **without** that executable (for example a source-only zip), they must add it once — steps below. The precompiled Google build is **x64**; use an **x64** Windows and matching **`cwebp`** for best results.

## Requirements

- **64-bit Windows** (as assumed by Google’s Windows **`cwebp`** bundle below)
- **`cwebp.exe`** at **`tools\bin\cwebp.exe`** (copy from Google’s ZIP if your project folder doesn’t include it yet)

### Desktop GUI (optional, `run_gui.bat`)

- **Python 3.8+** on `PATH` (`py` or `python`)
- **`customtkinter`** — installed on first successful GUI run via pip, or manually: `pip install customtkinter`

### If `cwebp` is missing or batch says “cwebp not found”

1. Download the **Windows x64** precompiled ZIP from Google:  
   [libwebp for Windows (precompiled)](https://developers.google.com/speed/webp/docs/precompiled)  
   Example direct link (version may update on their site):  
   `https://storage.googleapis.com/downloads.webmproject.org/releases/webp/libwebp-1.6.0-windows-x64.zip`
2. From the ZIP, copy **`bin\cwebp.exe`** → **`tools\bin\cwebp.exe`** (create folders if needed).
3. Run **`convert_png_to_webp.bat`** or **`run_gui.bat`** again.

## Quick start (no GUI — Command Prompt)

1. Put **`.png`** files in **`input`** (the script creates the folder if needed).
2. Double-click **`convert_png_to_webp.bat`** (plain Command Prompt window — no GUI).
3. Open **`converted`** for your **`.webp`** files.

From **cmd.exe** in the project folder:

```bat
convert_png_to_webp.bat
```

## Desktop GUI (CustomTkinter)

1. Double-click **`run_gui.bat`**.
2. Choose **PNG folder** and **output folder** (defaults: `input` and `converted`).
3. Set **target KB per file** or enable **fixed quality (-q)**, then **Start conversion**.
4. First run may install **`customtkinter`** via pip.

Everything runs **locally**; the GUI does not upload files.

## Configuration (optional — batch only)

Set environment variables **before** running **`convert_png_to_webp.bat`**.

### Target size mode (default)

```bat
set WEBP_TARGET_KB=60
convert_png_to_webp.bat
```

Examples: `55` (smaller), `75` (default if unset), `95` (larger).

### Fixed quality mode

```bat
set WEBP_USE_QUALITY=1
set WEBP_QUALITY=78
convert_png_to_webp.bat
```

## Technical notes

- Reads **`input\*.png`** only (not subfolders).
- **`cwebp`**: **`-m 6`**, **`-mt`**, **`-sharp_yuv`**, **`-alpha_q 100`**, **`-metadata none`**.

## Repository layout

| Path | Purpose |
|------|--------|
| `input/` | Put **`.png`** files here (batch default paths) |
| `convert_png_to_webp.bat` | **Batch converter** — plain CMD window (no GUI) |
| `run_gui.bat` / `gui/png_to_webp_gui.py` | **Desktop GUI** (Python + CustomTkinter + `cwebp`) |
| `tools\bin\cwebp.exe` | Google WebP encoder |
| `third-party\libwebp\COPYING` | libwebp license |
| `converted/` | Output **`.webp`** files |

## Third-party software

**`cwebp`** comes from **[libwebp](https://github.com/webmproject/libwebp)**; see **`third-party/libwebp/COPYING`**. It is **not** under this project’s MIT license.

## License

Project originals are **MIT** — see **`LICENSE`**. The **`cwebp`** binary follows **libwebp** terms in **`third-party/libwebp/COPYING`**.
