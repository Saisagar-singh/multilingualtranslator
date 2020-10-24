import requests
from bs4 import BeautifulSoup
import sys

args = sys.argv

languages = ['arabic', 'german', 'english', 'spanish', 'french', 'hebrew', 'japanese', 'dutch', 'polish', 'portuguese',
             'romanian', 'russian', 'turkish', ]
print('''Hello, you're welcome to the translator. Translator supports: 
1. Arabic
2. German
3. English
4. Spanish
5. French
6. Hebrew
7. Japanese
8. Dutch
9. Polish
10. Portuguese
11. Romanian
12. Russian
13. Turkish'''
      )
lan1 = str(args[1])
lan2 = str(args[2])
word = str(args[3])
headers = {"User-Agent": "Mozilla/5.0"}
s = requests.Session()
if lan1 not in languages and lan1 != 'all':
    print(f"Sorry, the program doesn't support {lan1}")
    exit()
if lan2 not in languages and lan2 != 'all':
    print(f"Sorry, the program doesn't support {lan2}")
    exit()
if lan2 == 'all':
    with open(f'{word}.txt', 'w+', encoding="utf-8") as f:
        for i in languages:
            if i == lan1:
                continue
            url = f"https://context.reverso.net/translation/{lan1}-{i}/{word}"
            my_request = s.get(url, headers=headers)
            if my_request.status_code == 404:
                print(f"Sorry, unable to find {word}")
                exit()
            if my_request.status_code != 200:
                print("Something wrong with your internet connection")
                exit()
            soup = BeautifulSoup(my_request.text, "html.parser")
            sentence_examples = []
            for sentence in soup.find(id="examples-content").select(".ltr"):
                sentence_examples.append(sentence.text.strip())
            word_examples = []
            for word in soup.find(id='translations-content').select('a'):
                word_examples.append(word.text.strip())
            f.write(f"{i.capitalize()} translations:\n")
            f.write(word_examples[0] + "\n")
            f.write(f"{i.capitalize()} examples:\n")
            f.write("\n\n".join(("\n".join(j for j in sentence_examples[i:i + 2]) for i in range(0, 2, 2))) + "\n")
        f.seek(0)
        print(f.read())

else:
    url = f"https://context.reverso.net/translation/{lan1}-{lan2}/{word}"
    my_request = s.get(url, headers=headers)
    if my_request.status_code == 404:
        print(f"Sorry, unable to find {word}")
        exit()
    if my_request.status_code != 200:
        print("Something wrong with your internet connection")
        exit()
    soup = BeautifulSoup(my_request.text, "html.parser")
    sentence_examples = []
    for sentence in soup.find(id="examples-content").select(".ltr"):
        sentence_examples.append(sentence.text.strip())
    word_examples = []
    for word in soup.find(id='translations-content').select('a'):
        word_examples.append(word.text.strip())
    print(f"{lan2.capitalize()} Translations:")
    print(*word_examples[:5], sep='\n')
    print(f"{lan2.capitalize()} Examples:")
    print("\n\n".join(("\n".join(j for j in sentence_examples[i:i + 2]) for i in range(0, 10, 2))))
