import tkinter as tk
from tkinter import simpledialog, filedialog, Toplevel
from fillpdf import fillpdfs
import requests

# Function to create Tkinter entries from PDF form fields and save them back to the PDF
def create_and_save_entries_from_pdf(win):
   # Ask the user if they want to download the PDF from a URL
   download_pdf = simpledialog.askstring("Download PDF", "Enter the URL of the PDF to download, or leave blank to select a local file:")
   if download_pdf:
       # Download the PDF from the provided URL
       response = requests.get(download_pdf)
       with open('downloaded_pdf.pdf', 'wb') as f:
           f.write(response.content)
       pdf_path = 'downloaded_pdf.pdf'
   else:
       # Ask the user for the PDF file path
       pdf_path = filedialog.askopenfilename(title="Select PDF file", filetypes=[("PDF files", "*.pdf")])
   if not pdf_path:  # If the user cancels the selection, exit the function
       return
   # Get the form fields from the PDF
   form_fields = fillpdfs.get_form_fields(pdf_path)
   # Create the main window
   root = Toplevel(win)
   root.transient(win)
   root.title("PDF Form Fields")
   x = 500
   y = 500
   root.geometry("+%d+%d" %(x,y))
   # Dictionary to hold the entry widgets and their corresponding keys
   entries = {}
   # Iterate over the form fields and create a Tkinter entry for each
   for index, (key, value) in enumerate(form_fields.items()):
       # Create a label for the entry
       label = tk.Label(root, text=key)
       label.grid(row=index, column=0, sticky="e")
       # Create an entry widget
       entry = tk.Entry(root)
       entry.grid(row=index, column=1)
       entry.insert(0, value)  # Insert the default value if needed
       # Store the entry in the dictionary
       entries[key] = entry
   # Function to save the entries back to the PDF
   def save_entries_to_pdf():
       # Ask the user for the output PDF file path using askstring
       output_pdf_path = simpledialog.askstring("Output PDF", "Enter the output PDF file name:")
       if not output_pdf_path:  # If the user cancels or enters nothing, exit the function
           return
       # Add '.pdf' extension if not present
       if not output_pdf_path.lower().endswith('.pdf'):
           output_pdf_path += '.pdf'
       # Create a dictionary to store the updated form fields
       updated_form_fields = {}
       for key, entry in entries.items():
           updated_form_fields[key] = entry.get()
       # Write the updated form fields back to the PDF
       fillpdfs.write_fillable_pdf(pdf_path, output_pdf_path, updated_form_fields)
       print(f"PDF saved to {output_pdf_path}")
   # Button to save all entry values back to the PDF
   save_button = tk.Button(root, text="Save to PDF", command=save_entries_to_pdf)
   save_button.grid(row=len(form_fields)+1, column=0, columnspan=2)
   # Run the main loop
   root.mainloop()

