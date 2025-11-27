"""Main file"""

# pylint: disable=W0621, C0103

# | IMPORT
import json
import os
import tkinter as tk

from tkinter import filedialog

import chardet
import pandas as pd


# | FUNCTIONS


def detect_encoding(file_path: str) -> str | None:
    """Detect file encodiung

    Args:
        file_path (str): file path

    Returns:
        str | None: file encoding
    """
    with open(file_path, "rb") as file:
        detector = chardet.universaldetector.UniversalDetector()
        for line in file:
            detector.feed(line)
            if detector.done:
                break
        detector.close()
    return detector.result["encoding"]


def get_file_path() -> str:
    """Get file path from file select windows

    Returns:
        str: file path
    """
    file_path = filedialog.askopenfilename(
        initialdir=os.path.abspath(__file__),
        title="Select a File",
        filetypes=[("JSON", "*.json"), ("JSON in TXT", "*.txt"), ("Other", "*")],
    )

    return file_path


# | MAIN

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    file_path = get_file_path()
    file_name = os.path.splitext(os.path.split(file_path)[1])[0]

    if not file_path:
        tk.messagebox.showwarning(  # type: ignore
            title="No file select!", message="No file select!\nExiting..."
        )
        root.destroy()
        import sys

        sys.exit()

    encoding = detect_encoding(file_path)
    encoding = "utf-8" if encoding is None else encoding

    with open(file_path, "rt", encoding=encoding) as f:
        try:
            json_data = json.load(f)
            if not isinstance(json_data, list):
                json_data = [json_data.copy()]
        except json.decoder.JSONDecodeError as e:
            f.seek(0)
            json_raw_string = f.read()
            json_raw_string = json_raw_string.replace("﻿", ",")
            json_raw_string = json_raw_string.replace(chr(0x00), "")
            if json_raw_string[0] != "[" or json_raw_string[-1] != "]":
                json_raw_string = f"[{json_raw_string.lstrip('[').rstrip(']')}]"

            json_data = json.loads(json_raw_string)

    df = pd.DataFrame(json_data)
    df.to_excel(f"{file_name}.xlsx", index=False)
    tk.messagebox.showinfo(  # type: ignore
        title="The file has been converted!",
        message="The file has been converted!\nClosing...",
    )
