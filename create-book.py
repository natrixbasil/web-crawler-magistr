from bs4 import BeautifulSoup
import requests
from ebooklib import epub

chap_list = []
for i in range(1, 7):
    url = f'https://younettranslate.com/projects/magistr-dyavolskogo-kulta?page={i}'
    response = requests.get(url)
    html_content = response.content

    soup = BeautifulSoup(html_content, 'html.parser')

    div_element = soup.find('tbody')  # Replace 'your-div-id' with the actual ID of the div

    if div_element:
        # Find all <a> tags within the div
        link_elements = div_element.find_all('a')

        # Extract the link URLs and add them to the list
        for link in link_elements:
            chapter = link.get_text()
            chap_list.append(chapter)

chap_list2 = chap_list[::2]

# Create an ePub book
book = epub.EpubBook()

# Set the metadata
book.set_title('Мосян Тунсю - Магистр Дьявольского Культа')
book.set_language('en')

spine = []  # Create an empty list to store the chapters for the spine

for chapter_name in chap_list2:
    # Define the filename based on the chapter name
    filename = f"{chapter_name.replace(' ', '_').lower()}.html"  # Adjust the filename format as desired

    # Read the content from the file
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()

    # Create an ePub item for each chapter
    chapter = epub.EpubHtml(title=chapter_name, file_name=filename, content=content)

    # Add the chapter to the book
    book.add_item(chapter)

    # Add the chapter to the spine
    spine.append(chapter)

# Set the table of contents
book.toc = spine

# Set the order of items in the spine
book.spine = spine

# Add navigation files
book.add_item(epub.EpubNcx())
book.add_item(epub.EpubNav())

# Set the CSS styles
style = '''
    body {
        font-family: Arial, sans-serif;
        font-size: 16px;
        line-height: 1.5;
    }
'''

# Add CSS to the book
book.add_item(epub.EpubItem(uid="style_default", file_name="style/default.css", content=style))

# Set the CSS for the chapters
for chapter in book.get_items_of_type(epub.EpubHtml):
    chapter.add_link(href="style/default.css", rel="stylesheet", type="text/css")

# Generate the ePub file
epub.write_epub('Мосян_Тунсю_Магистр_Дьявольского_Культа.epub', book, {})
