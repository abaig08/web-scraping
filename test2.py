import requests
import spacy
from bs4 import BeautifulSoup

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

# Function to extract main content from a website
def extract_main_content(url):
    # Send a GET request to the website
    response = requests.get(url)
    
    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the main content element(s) based on the website's structure
    main_content = soup.find('div', class_='main-content')  # Replace 'div' and 'class_' with appropriate selectors
    
    # Extract the text from the main content element(s)
    extracted_text = main_content.get_text() if main_content else 'Main content not found.'
    
    return extracted_text

# URL of the website you want to extract the main content from
website_url = 'https://www.google.com'  # Replace with the actual URL

# Extract the main content
content = extract_main_content(website_url)

# Process the content using spaCy
doc = nlp(content)

# Filter out non-content parts (e.g., ads, navigation)
filtered_content = [token.text for token in doc if not token.is_stop and not token.is_punct]

# Join the filtered content into a single string
filtered_text = ' '.join(filtered_content)

# Save the extracted content in a text file
output_file = 'main_content.txt'
with open(output_file, 'w', encoding='utf-8') as file:
    file.write(filtered_text)

print(f"Main content extracted and saved in '{output_file}' successfully.")