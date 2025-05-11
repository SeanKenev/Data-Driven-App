import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import urllib.request
import json

# Fetch data from the Pokémon API using urllib with headers
def fetch_pokemon_data(pokemon_name):
    try:
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        )
        with urllib.request.urlopen(request) as response:
            data = response.read()
        return json.loads(data)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            messagebox.showerror("Error", "Pokémon not found. Please try again.")
        else:
            messagebox.showerror("Error", f"HTTP Error: {e.code}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
    return None

# Display Pokémon data
def display_pokemon():
    pokemon_name = entry.get().strip()
    if not pokemon_name:
        messagebox.showinfo("Input Required", "Please enter a Pokémon name.")
        return

    data = fetch_pokemon_data(pokemon_name)
    if data:
        name = data["name"].capitalize()
        height = data["height"] / 10  # Convert decimeters to meters
        weight = data["weight"] / 10  # Convert hectograms to kilograms
        types = ", ".join(t["type"]["name"].capitalize() for t in data["types"])
        abilities = ", ".join(a["ability"]["name"].capitalize() for a in data["abilities"])

        output_text.set(
            f"Name: {name}\n"
            f"Height: {height} m\n"
            f"Weight: {weight} kg\n"
            f"Types: {types}\n"
            f"Abilities: {abilities}"
        )

# Set up the Pokedex-style GUI
root = tk.Tk()
root.title("Pokédex")
root.geometry("400x600")  # Adjusted size to fit the resized image

# Load the Pokédex template image
image_path = "pokedex_template.png"  # Path to the converted PNG file
bg_image = Image.open(image_path).resize((400, 600), Image.Resampling.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

# Create a canvas for the background
canvas = tk.Canvas(root, width=400, height=600)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# Input Field
entry = tk.Entry(root, font=("Arial", 12), width=18)
entry_window = canvas.create_window(180, 500, window=entry)

# Search Button
search_btn = tk.Button(root, text="Search", font=("Arial", 12), bg="#fdd835", fg="black", command=display_pokemon)
search_btn_window = canvas.create_window(300, 500, window=search_btn)

# Output Label
output_text = tk.StringVar()
output_label = tk.Label(root, textvariable=output_text, font=("Courier", 10), bg="black", fg="white", justify="left", wraplength=300, anchor="nw")
output_label_window = canvas.create_window(200, 300, window=output_label, width=300, height=150)

# Run the Pokedex app
root.mainloop()

