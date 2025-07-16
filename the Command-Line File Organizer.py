
import os
import shutil

# 1. Get the directory path from user input
path = input("Enter the path of the directory to organize: ")

# 2. Check if the path is valid
if not os.path.isdir(path):
    print("Error: The specified path is not a valid directory.")
    exit()

# 3. Get a list of all files in the directory
try:
    list_of_files = os.listdir(path)
except Exception as e:
    print(f"An error occurred: {e}")
    exit()

print(f"\nOrganizing files in: {path}\n")

# 4. Loop through each file to organize it
for file in list_of_files:
    # Use os.path.join to create a full path to the file for accurate checks
    full_path = os.path.join(path, file)

    # Skip directories
    if os.path.isdir(full_path):
        continue

    # Get the file name and extension
    name, ext = os.path.splitext(file)

    # Remove the dot from the extension
    ext = ext[1:]

    # If there's no extension, you can decide to skip or move to a 'misc' folder
    if ext == '':
        # Optionally, handle files with no extension
        continue

    # 5. Create a destination folder based on the extension
    destination_folder_path = os.path.join(path, ext.upper() + "_Files")

    # Check if the destination folder exists, if not, create it
    if not os.path.exists(destination_folder_path):
        os.makedirs(destination_folder_path)
        print(f"Created folder: {destination_folder_path}")

    # 6. Move the file to the new folder
    try:
        shutil.move(full_path, os.path.join(destination_folder_path, file))
        print(f"Moved '{file}' -> '{destination_folder_path}'")
    except Exception as e:
        print(f"Could not move {file}. Error: {e}")

print("\n✨ File organization complete! ✨")



import os
import shutil
import argparse

# Define categories for file extensions
CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".pptx", ".xls", ".odt"],
    "Audio": [".mp3", ".wav", ".aac", ".m4a"],
    "Video": [".mp4", ".mkv", ".mov", ".avi", ".flv"],
    "Archives": [".zip", ".rar", ".tar", ".gz"],
    "Scripts": [".py", ".js", ".sh", ".java"],
    "Other": [] # Default category for unknown types
}

def organize_files(path, is_dry_run=False):
    """Organizes files in the specified path into category-based subdirectories."""
    if not os.path.isdir(path):
        print(f"Error: Path '{path}' is not a valid directory.")
        return

    print(f"\nScanning directory: {path}\n")

    for item in os.listdir(path):
        source_path = os.path.join(path, item)

        # Skip if it's a directory
        if os.path.isdir(source_path):
            continue

        filename, file_ext = os.path.splitext(item)
        file_ext = file_ext.lower()

        # Find the correct category for the file
        target_category = "Other" # Default
        for category, extensions in CATEGORIES.items():
            if file_ext in extensions:
                target_category = category
                break

        destination_folder = os.path.join(path, target_category)
        
        # Create the category folder if it doesn't exist
        if not os.path.exists(destination_folder):
            if not is_dry_run:
                os.makedirs(destination_folder)
            print(f"[Action] Created folder: {destination_folder}")
        
        # Handle file name collisions before moving
        destination_path = os.path.join(destination_folder, item)
        counter = 1
        while os.path.exists(destination_path):
            new_filename = f"{filename}({counter}){file_ext}"
            destination_path = os.path.join(destination_folder, new_filename)
            counter += 1

        # Perform the move or simulate it
        if is_dry_run:
            print(f"[Dry Run] Would move '{item}' -> '{destination_path}'")
        else:
            try:
                shutil.move(source_path, destination_path)
                print(f"Moved '{item}' -> '{destination_path}'")
            except Exception as e:
                print(f"Error moving {item}: {e}")

    print("\n✨ Organization complete! ✨")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Organize files in a directory by category.")
    parser.add_argument("path", type=str, help="The target directory path to organize.")
    parser.add_argument("-d", "--dry-run", action="store_true", help="Simulate organization without moving files.")
    
    args = parser.parse_args()
    
    organize_files(args.path, args.dry_run)