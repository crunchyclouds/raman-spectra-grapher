import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
import pandas as pd
import pathlib
import numpy as np


# Main function for the graphing of Raman spectra data
def plot_raman_spectra(path):
    # Identify if the path is a file or a directory
    if pathlib.Path(path).is_dir():
        files = [file for file in pathlib.Path(path).glob("*.csv")] + \
                [file for file in pathlib.Path(path).glob("*.xlsx")]
    else:
        files = [path]

    # Correcting matplotlib presets
    plt.rcParams.update({'font.size': 18})

    # Looping through all files
    for file in files:
        if file.suffix == '.csv':
            df = pd.read_csv(file, header=105)
        elif file.suffix == '.xlsx':
            df = pd.read_excel(file, header=105)

        # Prepare y-axis and x-axis data
        y_axis = df['Dark Subtracted #1'] - df['RelativeIntensityCorrection_Ratio #1']
        x_axis = df['Raman Shift']

        # Create a larger plot
        plt.figure(figsize=(12, 6))  # Set figure size
        plt.ylim(0, 20000)
        plt.plot(x_axis, y_axis, label=str(pathlib.Path(file).stem))
        plt.ylabel(r"Intensity (a.u.)")
        plt.xlabel("Raman Shift (cm^-1)")
        plt.legend(loc='lower right')
        plt.show()


def identify_peaks(path):
    # Load the data from the selected file
    if pathlib.Path(path).suffix == '.csv':
        df = pd.read_csv(path, header=105)
    elif pathlib.Path(path).suffix == '.xlsx':
        df = pd.read_excel(path, header=105)

    # Prepare y-axis and x-axis data
    y_axis = df['Dark Subtracted #1'] - df['RelativeIntensityCorrection_Ratio #1']
    x_axis = df['Raman Shift']

    # Identify major peaks using a simple threshold method (customize as needed)
    threshold = np.mean(y_axis) + 2 * np.std(y_axis)  # Example threshold for peak detection
    peaks = x_axis[y_axis > threshold]

    # Display peaks
    if len(peaks) > 0:
        peak_info = "Major Peaks:\n" + "\n".join([f"{peak:.2f} cm^-1" for peak in peaks])
    else:
        peak_info = "No major peaks identified above the threshold."

    messagebox.showinfo("Peak Identification", peak_info)


# Create a tkinter window
class RamanGrapherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Raman Spectroscopy Grapher")
        self.root.geometry("800x400")  # Set a larger window size
        self.root.configure(bg='#f5f5dc')  # Set background color to off-white tan

        # Set up the main frame
        frame = tk.Frame(root, bg='#f5f5dc', padx=10, pady=10)
        frame.pack(padx=20, pady=20)

        # Title Label
        self.title_label = tk.Label(frame, text="Raman Spectra Grapher and Analysis",
                                    font=("Helvetica", 20, 'bold'), bg='#f5f5dc', fg='darkblue')
        self.title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))

        # Instructions Label
        self.label = tk.Label(frame, text="Select an option:",
                              font=("Helvetica", 16), bg='#f5f5dc', fg='darkblue')
        self.label.grid(row=1, column=0, columnspan=2, pady=5)

        # Option selection for folder or file
        self.option_var = tk.StringVar(value="folder")

        # Radio buttons for folder and file selection
        self.folder_radio = tk.Radiobutton(frame, text="Select Folder", variable=self.option_var,
                                           value="folder", bg='#f5f5dc', fg='darkblue', font=("Helvetica", 14))
        self.folder_radio.grid(row=2, column=0, sticky='e', padx=(0, 5))

        self.file_radio = tk.Radiobutton(frame, text="Select Single File", variable=self.option_var,
                                         value="file", bg='#f5f5dc', fg='darkblue', font=("Helvetica", 14))
        self.file_radio.grid(row=2, column=1, sticky='w', padx=(5, 0))

        # Folder/File path display
        self.path_var = tk.StringVar()
        self.path_entry = tk.Entry(frame, textvariable=self.path_var, width=40, state='readonly',
                                   font=("Helvetica", 12), bg='white')
        self.path_entry.grid(row=3, column=0, padx=5, pady=(10, 0), columnspan=2)

        # Browse button
        self.browse_button = tk.Button(frame, text="Browse", command=self.select_path, bg='sky blue',
                                       font=("Helvetica", 14), width=15)
        self.browse_button.grid(row=4, column=0, padx=5, pady=(10, 0), columnspan=2)

        # Action buttons side by side
        self.plot_button = tk.Button(frame, text="Plot Raman Spectra", command=self.plot_spectra, bg='sky blue',
                                     font=("Helvetica", 14), width=20)
        self.plot_button.grid(row=5, column=0, padx=5, pady=(10, 0), sticky='w')

        self.peak_button = tk.Button(frame, text="Identify Peaks", command=self.identify_peaks, bg='sky blue',
                                     font=("Helvetica", 14), width=20)
        self.peak_button.grid(row=5, column=1, padx=5, pady=(10, 0), sticky='w')

        self.instructions_button = tk.Button(frame, text="Instructions", command=self.show_instructions, bg='sky blue',
                                             font=("Helvetica", 14), width=20)
        self.instructions_button.grid(row=6, column=0, columnspan=2, pady=(10, 5))

    def select_path(self):
        # Determine whether to ask for a folder or a single file based on user selection
        if self.option_var.get() == "folder":
            path = filedialog.askdirectory()  # Ask for a directory
        else:
            path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv"), ("Excel Files", "*.xlsx")])

        if path:  # Only set path_var if a path is selected
            self.path_var.set(path)

    def plot_spectra(self):
        # Call the grapher function with the selected path
        path = self.path_var.get()
        if path:
            try:
                plot_raman_spectra(path)
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while plotting: {e}")
        else:
            messagebox.showwarning("Warning", "Please select a folder or file first.")

    def identify_peaks(self):
        # Identify peaks for a single selected file
        path = self.path_var.get()
        if path:
            try:
                identify_peaks(path)
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while identifying peaks: {e}")
        else:
            messagebox.showwarning("Warning", "Please select a file first.")

    def show_instructions(self):
        # Show instructions in a message box
        instructions = ("1. Select a folder containing CSV files or a single CSV/XLSX file.\n"
                        "2. Click 'Plot Raman Spectra' to generate the plots.\n"
                        "3. Click 'Identify Peaks' to find major peaks in the selected file.\n"
                        "4. Ensure the data is formatted correctly for analysis.")
        messagebox.showinfo("Instructions", instructions)


# Run the tkinter application
if __name__ == "__main__":
    root = tk.Tk()
    app = RamanGrapherApp(root)
    root.mainloop()
