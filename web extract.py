import tkinter as tk
from tkinter import filedialog
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import spacy

def extract_main_content(url):
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)

    driver.get(url)
    time.sleep(5)

    page_source = driver.page_source

    soup = BeautifulSoup(page_source, 'html.parser')

    main_content =  soup.find('div', id='mw-parser-output')
    if main_content:
        paragraphs = main_content.find_all('p')  # Find all <p> elements within the main content
        extracted_text = '\n\n'.join([p.get_text() for p in paragraphs])  # Extract text from each paragraph
        extracted_text = ' '.join(extracted_text.split())

        return extracted_text
    else:
        print("Failed to find main content on the website.")
        print("Extracting all possible content...")

    response = requests.get(url)
    if response.status_code == 200:
        content = response.text

        soup = BeautifulSoup(content, 'html.parser')

        paragraphs = soup.find_all('p')  # Find all <p> elements on the page
        extracted_text = '\n\n'.join([p.get_text() for p in paragraphs])  # Extract text from each paragraph
        extracted_text = ' '.join(extracted_text.split())

        return extracted_text
    print("All possible content extracted")

    driver.quit()

def extract_and_save_main_content():
    nlp = spacy.load("en_core_web_sm")

    window = tk.Tk()

    def open_file_dialog():
        output_file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if output_file_path:
            website_url = entry.get()
            text = extract_main_content(website_url)

            if text:
                doc = nlp(text)
                filtered_content = [token.text for token in doc if not token.is_stop and not token.is_punct]
                filtered_text = ' '.join(filtered_content)

                with open(output_file_path, 'w', encoding='utf-8') as file:
                    file.write(filtered_text)

                print("Content extracted and saved as", output_file_path)

                window.destroy()

    label = tk.Label(window, text="Enter Website URL")
    label.pack()

    entry = tk.Entry(window)
    entry.pack()

    button = tk.Button(window, text="Extract", command=open_file_dialog)
    button.pack()
    window.title('Website Content Extraction')
    window_width = 600
    window_height = 400
    window_position_x = 100
    window_position_y = 100
    window.geometry(f"{window_width}x{window_height}+{window_position_x}+{window_position_y}")
    window.mainloop()


extract_and_save_main_content()