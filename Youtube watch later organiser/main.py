from tkinter import *
from tkinter import messagebox
import webbrowser
import requests
import json
from datetime import datetime
from PIL import Image, ImageTk
from googleapiclient.discovery import build
from urllib.parse import urlparse


api_key = "use-your-api-key" #go to googlepythonapiclient


def get_clipboard():
    try:
        # Retrieve content from clipboard
        clipboard_content = win.clipboard_get()
        # Display content in the text field
        url_input.delete(0, END)  # Clear existing content
        url_input.insert(0, clipboard_content)
    except Exception as e:
        # Handle exceptions (e.g., if the clipboard is empty or contains unsupported content)
        messagebox.showerror("Error", f"Could not retrieve clipboard content: {e}")


def extract_video_id(URL):
    # Parse the URL
    parsed_url = urlparse(URL)
    # Extract the path
    path = parsed_url.path
    # The video ID is the part after the '/'
    video_id = path.lstrip('/')
    return video_id


def get_youtube_video_details(api_key, video_id):
    youtube = build('youtube', 'v3', developerKey=api_key)

    # Make the API request
    request = youtube.videos().list(
        part="snippet",
        id=video_id
    )
    response = request.execute()
    print(response)

    if response['items']:
        video_title = response['items'][0]['snippet']['title']
        channel_name = response['items'][0]['snippet']['channelTitle']
        return video_title, channel_name
    else:
        return None  # Replace with your API key and the video ID


# Create an instance of tkinter frame
win = Tk()
win.geometry("800x500")
win.title("Watch Later")

win.attributes('-topmost', 1)

background_image = Image.open("TUBE.png")  # Replace with your image file
background_photo = ImageTk.PhotoImage(background_image)

# Create a Label widget to hold the background image
background_label = Label(win, image=background_photo)
background_label.place(relwidth=1, relheight=1)


# Define a callback function for opening URLs
def callback(link):
    webbrowser.open_new_tab(link)


# Function to display links from the JSON file
def display_link():
    try:
        with open("links.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found")
        return
    except json.JSONDecodeError:
        messagebox.showinfo(title="Error", message="Error reading JSON file")
        return

    for widget in display_frame.winfo_children():
        if int(widget.grid_info()["row"]) > 0:  # Skip header row (row 0)
            widget.destroy()

    row = 1
    for entry in data:
        if isinstance(entry, dict):
            # Channel name label
            channel_label = Label(display_frame, text=entry['channel'].title(), anchor="w", width=20, bg="white")
            channel_label.grid(row=row, column=0, padx=10, pady=5, sticky="w")

            # Description label
            about_label = Label(display_frame, text=entry['description'], anchor="w", width=30, bg="white")
            about_label.grid(row=row, column=1, padx=10, pady=5, sticky="w")

            # Date added label
            date_label = Label(display_frame, text=entry['date_added'], anchor="w", width=20, bg="white")
            date_label.grid(row=row, column=2, padx=10, pady=5, sticky="w")

            # Clickable URL
            url_link = entry['URL']
            link = Label(display_frame, image=img, cursor="hand2", bg="white")
            link.grid(row=row, column=3, padx=10, pady=5, sticky="w")
            link.bind("<Button-1>", lambda e, url=url_link: callback(url))

            # "Watched" button for deleting the channel
            watched_button = Button(display_frame, text="Watched", command=lambda e=url_link: delete_channel(e), bg="#d82524")
            watched_button.grid(row=row, column=4, padx=10, pady=5, sticky="w")

            row += 1  # Move to the next row


def add_watchlater():
    url = url_input.get()
    video_id = extract_video_id(url)
    title, channel= get_youtube_video_details(api_key, video_id)


    if not url:
        messagebox.showwarning("Input Error", "Please fill all fields!")
        return

    date_added = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    new_data = {
        "channel": channel,
        "description": title,
        "URL": url,
        "date_added": date_added
    }

    try:
        with open("links.json", "r") as file:
            # Reading the old data
            data = json.load(file)
    except FileNotFoundError:
        data = []

    # Append the new data to the list
    data.append(new_data)

    with open("links.json", "w") as file:
        json.dump(data, file, indent=4)

    url_input.delete(0, END)

    display_link()


def delete_channel(url):
    try:
        with open("links.json", "r") as file:
            data = json.load(file)

        # Filter out the channel with the specified URL
        data = [entry for entry in data if entry['URL'] != url]

        # Save the updated data to file
        with open("links.json", "w") as file:
            json.dump(data, file, indent=4)

        # Refresh the displayed data
        display_link()

    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found")


# Input Frame for labels and inputs
input_frame = Frame(win, bg="white")
input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="w")

# Display Frame for showing data
display_frame = Frame(win, bg="white")
display_frame.grid(row=1, column=0, padx=10, pady=10, sticky="w")

# Header for the display area
header_channel = Label(display_frame, text="Channel", font=("Helvetica", 12, "bold"), bg="white")
header_channel.grid(row=0, column=0, padx=10, pady=5, sticky="w")

header_description = Label(display_frame, text="Description", font=("Helvetica", 12, "bold"), bg="white")
header_description.grid(row=0, column=1, padx=10, pady=5, sticky="w")

header_date = Label(display_frame, text="Date Added", font=("Helvetica", 12, "bold"), bg="white")
header_date.grid(row=0, column=2, padx=10, pady=5, sticky="w")

header_link = Label(display_frame, text="Link", font=("Helvetica", 12, "bold"), bg="white")
header_link.grid(row=0, column=3, padx=10, pady=5, sticky="w")

header_action = Label(display_frame, text="Action", font=("Helvetica", 12, "bold"), bg="white")
header_action.grid(row=0, column=4, padx=10, pady=5, sticky="w")


url_input = Entry(input_frame, width=34)
url_input.grid(column=1, row=2)

fetch_button = Button(input_frame, text="Paste", width=8, command=get_clipboard)
fetch_button.grid(column=0, row=2, padx=5)

# Create Buttons inside input_frame
add_button = Button(input_frame, text="Add", width=8, command=add_watchlater, bg="#d82524")
add_button.grid(row=3, column=0, pady=5)

refresh_button = Button(input_frame, text="Refresh", width=28, command=display_link, bg="#d82524")
refresh_button.grid(row=3, column=1, pady=5)

win.mainloop()
