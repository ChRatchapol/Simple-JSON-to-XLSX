import pandas as pd
import json
import tkinter as tk
import os

from tkinter import filedialog


def get_file_path():
    file_path = filedialog.askopenfilename(
        initialdir=os.path.abspath(__file__),
        title="Select a File",
        filetypes=[("JSON", "*.json")],
    )

    return file_path


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    file_path = get_file_path()
    file_name = os.path.splitext(os.path.split(file_path)[1])[0]

    if not file_path:
        tk.messagebox.showwarning(
            title="No file select!", message="No file select!\nExiting..."
        )
        root.destroy()
        import sys

        sys.exit()

    with open(file_path, "rt", encoding="utf-8") as f:
        json_data = json.load(f)

    df = pd.DataFrame(json_data)
    df.to_excel(f"{file_name}.xlsx", index=False)
    tk.messagebox.showinfo(
        title="The file has been converted!",
        message="The file has been converted!\nClosing...",
    )
