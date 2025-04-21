import os

def checkFile(domain, filepath):
    if os.path.exists(domain + filepath):
        return True
    return False

def getFile(domain, filepath):
    response = None

    if os.path.isfile(domain + filepath):
        with open(domain + filepath, 'r') as file:
            response = file.read()

    return response

def saveFile(domain, filepath, text):
    if filepath == "/":
        filepath == "/main.html"

    # Create folder
    try:
        os.mkdir(domain)
        print(f"Directory '{domain}' created successfully.")

    except FileExistsError:
        print(f"Directory '{domain}' already exists.")
    except PermissionError:
        print(f"Permission denied: Unable to create '{domain}'.")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    with open(domain + filepath, "w", encoding="utf-8") as file:
        file.write(text)

   
