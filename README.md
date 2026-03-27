# png-to-webp-windows

Batch-convert every **PNG** in the **`input`** folder to **WebP** using Google’s official **`cwebp`** encoder. Output files are written to the **`converted`** folder; original PNGs in **`input`** are **not** deleted.

Default mode targets a **compact file size per image** (~75 KB by default), which works well for mobile apps and thumbnails. You can switch to a **fixed quality** mode if you prefer.

## Requirements

- **Windows**
- **`cwebp.exe`** at `tools\bin\cwebp.exe`

If the script reports that `cwebp` is missing:

1. Download the official Windows x64 archive from Google:  
   [libwebp for Windows (precompiled)](https://developers.google.com/speed/webp/docs/precompiled)  
   Direct link (check the site for newer versions):  
   `https://storage.googleapis.com/downloads.webmproject.org/releases/webp/libwebp-1.6.0-windows-x64.zip`
2. From the ZIP, copy **`bin\cwebp.exe`** to **`tools\bin\cwebp.exe`** (create the folders if needed).

## Quick start

1. Clone or copy this repository to your PC.
2. Put all **`.png`** files in the **`input`** folder (create it if needed — the script creates it when missing).
3. Double-click **`convert_png_to_webp.bat`** at the project root (or run it from Command Prompt).
4. Open the **`converted`** folder — you’ll find **`.webp`** files with the same base names as the PNGs.

## Configuration (optional)

### Target size mode (default)

The encoder tries to hit roughly this size **per file** (in kilobytes). **Lower = smaller files**, more compression artifacts possible.

**Command Prompt** (before running the batch file):

```bat
set WEBP_TARGET_KB=60
convert_png_to_webp.bat
```

**Examples**

- `WEBP_TARGET_KB=55` — smaller (~50–60 KB range depending on image)
- `WEBP_TARGET_KB=75` — **default** if unset
- `WEBP_TARGET_KB=95` — larger, usually cleaner

### Fixed quality mode

Use a constant **`-q`** value instead of `-size`:

```bat
set WEBP_USE_QUALITY=1
set WEBP_QUALITY=78
convert_png_to_webp.bat
```

## Technical notes

- Reads **`input\*.png`** only (not subfolders). To convert nested sets, flatten copies into **`input`** or run from a tool that supports recursion.
- Uses **`cwebp`** with **method `-m 6`**, **`-mt`** (multithreading), **`-sharp_yuv`**, **`-alpha_q 100`**, and **`-metadata none`** (strips metadata for smaller output).
- **Target size** (`-size`) is approximate; results vary with image content and dimensions.

## Repository layout

| Path | Purpose |
|------|--------|
| `input/` | **Put your `.png` files here** before running the script |
| `convert_png_to_webp.bat` | Run this from the project root |
| `tools\bin\cwebp.exe` | Google WebP encoder (bundled; see libwebp license) |
| `third-party\libwebp\COPYING` | License text for **`cwebp`** / libwebp |
| `converted/` | Output **`.webp`** files (created automatically) |

## Third-party software

**`tools\bin\cwebp.exe`** is the **`cwebp`** utility from Google’s **[libwebp](https://github.com/webmproject/libwebp)** release bundle (e.g. the [precompiled Windows x64 ZIP](https://developers.google.com/speed/webp/docs/precompiled)). It is **not** covered by this repository’s **MIT** license; redistribution of the binary must follow libwebp’s terms. See **`third-party/libwebp/COPYING`**.

## License

This project’s **original materials** (batch script, documentation, etc.) are licensed under the **MIT License** — see **`LICENSE`**.

The **`cwebp`** binary remains under the **libwebp** license in **`third-party/libwebp/COPYING`**.
