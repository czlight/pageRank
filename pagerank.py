import os
import random
import re
import sys
from collections import Counter

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    # crawl function parses html files in directory and returns
    # a dictionary representing the corpus. Keys represent pages
    # and values area a set of all the pages linked to by the key
    # e.g., {"1.html": {"2.html" , "3.html"}} means page 1 links to pages 2 & 3
    corpus = crawl(sys.argv[1])

    # sample_pagerank function's purpose is to estimate PageRank of each page by sampling
    # returns a dictionary where keys are page name and values are page's PageRank(0 - 1)
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")

    # iterate_pagerank calculates PageRank but using the iterative formula
    # method instead of sampling. return format is same as dict sample_pagerank function
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # initialize empty dictionary
    probabilities = dict()

    if page in corpus:
        print("outer loop page is", page)
        print("outer loop corpus is ", corpus)
        if not corpus[page]:
            print("not corpus[page] (i.e., no outgoing links for page: ", page)
            # page has no outgoing links
            # return all pages in corpus with equal probability
            # tested and works as expected!!
            for file in corpus:
                probabilities[file] = 1 / len(corpus)
                probabilities[file] = round(probabilities[file], 6)
            return(probabilities)

    # for each outgoing link, make probability damping factor / (1 - len(corpus))
    # PLUS 1 - damping factor / len(corpus)
    for file in corpus:
        print("page is", page)
        print("corpus is ", corpus)
        print("corpus[file] is:", corpus[file])
        probabilities[file] = (1 - damping_factor) / len(corpus)
        probabilities[file] = round(probabilities[file], 6)

    for link in corpus[page]:
        print("page!!", page)
        print("has link to", link)
        print("this page has this many links! len(corpus[page])", len(corpus[page]))
        probabilities[link] += damping_factor/len(corpus[page])
        probabilities[link] = round(probabilities[link], 6)
        print("rounded probabilities", probabilities[link])


    return probabilities



def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # initialize set of samples with random page

    page = list(corpus.keys())
    page = random.choice(page)

    # empty list to store pages
    data = []
    data.append(page)


    # use transition model to determine page to jump to
    for i in range(n):

        model = transition_model(corpus, page, damping_factor)
        next_pages = list(model.keys())
        probabilities = list(model.values())
        next_page = random.choices(next_pages, probabilities)[0]
        data.append(next_page)

    print(Counter(data))
    data = Counter(data)
    data = dict(data)

    for page in data:
        print("page in data!:", page)
        print("data[page]", data[page])
        data[page] = (data[page] / (n + 1))
        data[page] = round(data[page], 6)
        print("data page is now)", data[page])
    print("data is" ,data)
    return data


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """






    raise NotImplementedError


if __name__ == "__main__":
    main()
