import argparse
import os
import subprocess
from tkinter import Tk, Label, Entry, Button, filedialog, StringVar, messagebox, Frame
from core.extract_links import get_m3u8_links
from core.download_video import download_video as download_m3u8

# ===== CLI =====
def cli_mode(url: str, output: str):
    print("Extracting video links…")
    links = get_m3u8_links(url)
    if not links:
        print("No video links found.")
        return
    print("Found links:")
    for i, link in enumerate(links):
        print(f"{i+1}: {link}")

    choice = 0
    if len(links) > 1:
        choice = int(input(f"Select link to download (1-{len(links)}): ")) - 1

    selected_url = links[choice]
    print(f"Downloading {selected_url} …")
    download_m3u8(selected_url, output)
    print(f"Download complete! File saved to {os.path.abspath(output)}")


# ===== GUI =====
def gui_mode():
    def browse_folder():
        folder_path.set(filedialog.askdirectory())

    def open_folder():
        path = folder_path.get()
        if os.name == 'nt':
            os.startfile(path)
        elif os.name == 'posix':
            subprocess.run(['open', path] if os.uname().sysname == 'Darwin' else ['xdg-open', path])

    def start_download():
        status_var.set("Extracting links...")
        root.update_idletasks()

        url = url_var.get()
        folder = folder_path.get()
        fname = file_name.get()

        if not url or not folder or not fname:
            messagebox.showerror("Error", "URL, folder, and filename must be set.")
            status_var.set("Idle")
            return

        links = get_m3u8_links(url)
        if not links:
            messagebox.showerror("Error", "No video links found.")
            status_var.set("Idle")
            return

        output_path = os.path.join(folder, fname)
        status_var.set("Downloading video...")
        root.update_idletasks()
        download_m3u8(links[0], output_path)

        status_var.set("Download complete!")
        messagebox.showinfo("Done", f"Video saved to:\n{output_path}")
        status_var.set("Idle")
        open_folder_btn.config(state="normal")

    root = Tk()
    root.title("Amazon Video Downloader")
    root.eval('tk::PlaceWindow . center')

    # --- Page URL ---
    url_frame = Frame(root)
    url_frame.grid(row=0, column=0, columnspan=3)
    Label(url_frame, text="Page URL:").pack(side="left")
    url_var = StringVar()
    Entry(url_frame, textvariable=url_var, width=50).pack(side="left")

    # --- Save Folder ---
    folder_frame = Frame(root)
    folder_frame.grid(row=1, column=0, columnspan=3)
    Label(folder_frame, text="Save Folder:").pack(side="left")
    folder_path = StringVar()
    Entry(folder_frame, textvariable=folder_path, width=40).pack(side="left")
    Button(folder_frame, text="Browse", command=browse_folder).pack(side="left")

    # --- File Name ---
    fname_frame = Frame(root)
    fname_frame.grid(row=2, column=0, columnspan=3)
    Label(fname_frame, text="File Name:").pack(side="left")
    file_name = StringVar()
    Entry(fname_frame, textvariable=file_name, width=50).pack(side="left")

    # --- Status ---
    status_var = StringVar(value="Idle")
    Label(root, textvariable=status_var, fg="blue").grid(row=3, column=0, columnspan=3)

    # --- Buttons ---
    Button(root, text="Download", command=start_download, width=20).grid(row=4, column=1)
    open_folder_btn = Button(root, text="Open Folder", command=open_folder, state="disabled", width=20)
    open_folder_btn.grid(row=5, column=1)

    # --- Center columns ---
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_columnconfigure(2, weight=1)

    root.mainloop()

# ===== Entry Point =====
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Amazon m3u8 video downloader")
    parser.add_argument("--url", help="Page URL to extract video from")
    parser.add_argument("--output", help="Output video file path")
    parser.add_argument("--gui", action="store_true", help="Run GUI mode")
    args = parser.parse_args()

    if args.gui:
        gui_mode()
    elif args.url and args.output:
        cli_mode(args.url, args.output)
    else:
        print("Provide either --gui or both --url and --output")
