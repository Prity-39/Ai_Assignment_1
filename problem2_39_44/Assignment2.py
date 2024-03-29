import dis
from operator import contains, is_
import re
import time
from turtle import distance
import webbrowser
from selenium import webdriver
from selenium.webdriver.common.by import By
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
import nltk
from sumy.summarizers.text_rank import TextRankSummarizer

nltk.download('punkt')


def remove_all_sentence_except_english(text):
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    return text


def textSummerize(text):
    text = text.replace("\n", " ")
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = TextRankSummarizer()
    summary = summarizer(parser.document, 2)
    text_summary = ""
    for sentence in summary:
        text_summary += str(sentence)
    return text_summary


def fileClear():
    open('textBFS.txt', 'w').close()
    open('linksBFS.txt', 'w').close()
    open('textDFS.txt', 'w').close()
    open('linksDFS.txt', 'w').close()


def fileAddDFS(data, file_path):
    with open(file_path, "a") as file:
        file.write(data + "\n")


def fileAddBFS(data, file_path):
    with open(file_path, "a") as file:
        file.write(data + "\n")


def is_subset(subset, string):
    subset = subset.lower()
    string = string.lower()
    return subset in string


def scrape_pTag_text(driver):
    pTag = driver.find_elements(By.TAG_NAME, "p")
    text = "#URL: " + driver.current_url + "\n"
    for tag in pTag:
        text += tag.text
        text += " "
    if pTag is not None:
        text += "\n\n"

    text = remove_all_sentence_except_english(text)
    text = textSummerize(text)

    return text


class Search:
    def __init__(self, max_depth=3, max_breadth=3):
        self.linkset = set()
        self.Graph = {}
        self.max_depth = max_depth
        self.max_breadth = max_breadth

    def get_all_links_with_selenium(self, url, targeted_text, method):
        goal = False
        try:
            driver = webdriver.Chrome()
            driver.set_page_load_timeout(30)
            driver.get(url)
            text = scrape_pTag_text(driver)
            if method == "DFS":
                fileAddDFS(text, 'textDFS.txt')
            else:
                fileAddBFS(text, 'textBFS.txt')
            goal = self.is_reach_goal(text=text, targeted_text=targeted_text)
            if goal:
                quit()
            elements = driver.find_elements(By.TAG_NAME, "a")

            navbar_links = driver.find_elements(By.XPATH, "//nav//a")

            non_navbar_links = [link for link in elements if link not in navbar_links]
            elements = non_navbar_links

            urls = []
            i = 0
            for element in elements:
                href = element.get_attribute("href")
                if i > 20:
                    break
                if href:
                    if not (is_subset("google", href) or is_subset("facebook", href) or is_subset("youtube", href) or is_subset("twitter", href) or is_subset("instagram", href) or is_subset("linkedin", href) or is_subset("pinterest", href) or is_subset("reddit", href) or is_subset("tumblr", href) or is_subset("amazon", href) or is_subset("ebay", href) or is_subset("yahoo", href) or is_subset("bing", href) or is_subset("netflix", href) or is_subset("craigslist", href) or is_subset("paypal", href) or is_subset("wordpress", href) or is_subset("apple", href) or is_subset("microsoft", href) or is_subset("adobe", href)):
                        if href not in urls:
                            urls.append(href)
                            if method == "DFS":
                                fileAddDFS(href, 'linksDFS.txt')
                            else:
                                fileAddBFS(href, 'linksBFS.txt')
                            i += 1
            time.sleep(2)
            driver.quit()
            return urls, goal
        except Exception as e:
            print(e)
            return [], goal

    def is_reach_goal(self, text, targeted_text):
        targets = targeted_text.split(" ")
        for word in targets:
            if not is_subset(word, text):
                return False
        return True

    def DFS(self, graph, node, targeted_text, visited=None, distance=0):
        if distance > self.max_depth:
            return
        distance += 1
        if visited is None:
            visited = set()
        if node not in visited:
            visited.add(node)
            urls, goal = self.get_all_links_with_selenium(node, targeted_text, "DFS")
            print(node, distance)
            if urls:
                print(urls[0])
            graph[node] = urls[:self.max_breadth]
            for neighbour in graph[node]:
                self.DFS(graph, neighbour, targeted_text, visited, distance)
        return visited

    def BFS(self, graph, start, targeted_text, visited=None):
        if visited is None:
            visited = set()
        queue = [start]
        visited.add(start)
        distance = 0
        while queue and distance <= self.max_depth:
            s = queue.pop(0)
            print(s, distance)
            urls, goal = self.get_all_links_with_selenium(s, targeted_text, "BFS")
            graph[s] = urls[:self.max_breadth]
            distance += 1
            for neighbour in graph[s]:
                if neighbour not in visited:
                    queue.append(neighbour)
                    visited.add(neighbour)
        return visited


# Example usage:
my_graph = Search()

start_node = input('What would you like to search on Google?\n')
start_node = 'https://www.google.com/search?q=' + start_node
targeted_text = input('What are you looking for?\n')
print("DFS starting from node", start_node)

fileClear()
my_graph.Graph = {start_node: []}

dfs_visited = my_graph.DFS(my_graph.Graph, start_node, targeted_text=targeted_text)
bfs_visited = my_graph.BFS(my_graph.Graph, start_node, targeted_text=targeted_text)

# Summarize DFS
with open('textDFS.txt', 'r') as f:
    dfs_text = f.read()
dfs_summary = textSummerize(dfs_text)
with open('dfs_summary.txt', 'w') as f:
    f.write(dfs_summary)

# Summarize BFS
with open('textBFS.txt', 'r') as f:
    bfs_text = f.read()
bfs_summary = textSummerize(bfs_text)
with open('bfs_summary.txt', 'w') as f:
    f.write(bfs_summary)
