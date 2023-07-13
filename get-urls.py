from bs4 import BeautifulSoup
import requests
from ebooklib import epub

link_list = []
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
            href = link.get('href')
            link_list.append(href)

link_list2 = link_list[::2]
print('Number of chapters')
print(len(link_list2))

all_text =''
for link in link_list2:
    url = link
    response = requests.get(url)
    html_content = response.content

    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.find_all(class_='postdata-content')
    text = str(text)
    all_text += text
    print(len(text))

print(len(all_text))

# Create an ePub book
book = epub.EpubBook()

# Set the metadata
book.set_title('Магистр Дьявольского Культа')
book.set_language('en')

# Create an ePub item
content = "<html><body>" + all_text + "</body></html>"
chapter = epub.EpubHtml(title='Chapter 1', file_name='chapter1.xhtml', content=content)

# Add the chapter to the book
book.add_item(chapter)

# Create the table of contents
book.toc = (chapter,)  # Tuple of items for the table of contents

# Add navigation files
book.add_item(epub.EpubNcx())
book.add_item(epub.EpubNav())

# Define the CSS styles
style = '''
    body {
        font-family: Arial, sans-serif;
        font-size: 25px;
        line-height: 1.5;
    }
'''

# Add CSS to the book
book.add_item(epub.EpubItem(uid="style_default", file_name="style/default.css", content=style))

# Set the CSS for the chapter
chapter.add_link(href="style/default.css", rel="stylesheet", type="text/css")

# Define the order of items
book.spine = [chapter]

# Generate the ePub file
epub.write_epub('my_ebook.epub', book, {})

