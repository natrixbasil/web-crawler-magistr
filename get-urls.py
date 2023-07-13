from bs4 import BeautifulSoup
import requests

link_list = []
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
            href = link.get('href')
            chapter = link.get_text()
            link_list.append(href)
            chap_list.append(chapter)

chap_list2 = chap_list[::2]
link_list2 = link_list[::2]

print(chap_list2[0:10])
print(link_list2[0:10])
print(len(link_list2))
print(len(chap_list2))

all_text = []
for link in link_list2:
    url = link
    response = requests.get(url)
    html_content = response.content

    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.find_all(class_='postdata-content')
    text = str(text)
    all_text.append(text)
    print(len(text))

print(len(all_text))

for chapter_name, chapter_content in zip(chap_list2, all_text):
    # Define the filename based on the chapter name
    filename = f"{chapter_name.replace(' ', '_').lower()}.html"

    # Write the text content to the file
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(chapter_content)

