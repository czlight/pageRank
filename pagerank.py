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
        if not corpus[page]:
            # page has no outgoing links
            # return all pages in corpus with equal probability
            # tested and works as expected!!
            for file in corpus:
                probabilities[file] = 1 / len(corpus)
                probabilities[file] = round(probabilities[file], 4)
            return(probabilities)

    # for each outgoing link, make probability damping factor / (1 - len(corpus))
    # PLUS 1 - damping factor / len(corpus)
    for file in corpus:
        print("page is", page)
        print("corpus is ", corpus)
        print("corpus[file] is:", corpus[file])
        probabilities[file] = (1 - damping_factor) / len(corpus)
        probabilities[file] = round(probabilities[file], 4)

    for link in corpus[page]:
        print("page!!", page)
        print("has link to", link)
        print("this page has this many links! len(corpus[page])", len(corpus[page]))
        probabilities[link] += damping_factor/len(corpus[page])
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
        page = next_page
        data.append(next_page)

    print(Counter(data))
    data = Counter(data)
    data = dict(data)

    for page in data:
        print("page in data!:", page)
        print("data[page]", data[page])
        data[page] = (data[page] / n)
        # data[page] = round(data[page], 4)
        print("data page is now)", data[page])
    print("data is" ,data)

    total = sum(data.values())
    for item in data:
        data[item] /= total
        data[item] = round(data[item], 4)
    return data



def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # initialize each page an equal probability
    data = dict()
    for file in corpus:
        data[file] = 1 / len(corpus)
    print("data - probabilities are equal", data)

    # pageRank recursive mathematical expression
    # PR(p) = (1 - d)/n + d * summation PR(i)/ NumLinks(i)
    # i = each possible page that links to page p
    # NumLinks(i) = # of links on page i (we travel to any of a page's links with equal probability)
    # PR(i) = pageRank of page i, representing the probability we are on page i at any given time
    # n = possible pages in corpus

    # iterate over every page in corpus
    i = 0
    condition1 = (1 - damping_factor) / len(corpus)
    #
    # while(True):
    for a in range(2000):
        for page in corpus:
            i+= 1
            print("outer loop. let's start! loop::", i, "page::" , page)
            print("data list should be updated, data is: ", data)

            # 1. find possible pages i that link to page p. for each page get:
            # 2. it's page rank (i.e., probability)
            # 3. number of links on that page
            j = 0
            summ = 0
            for key in corpus:
                j+=1
                print("nested loop#:", j , "looking at key::", key, "in corpus::", corpus)
                # look for values (i.e., links to page)
                for value in corpus[key]:
                    print("value is:", value)
                    print("key is :", key)
                    print("page we're looking at is:", page)

                    # check for page i that links to page p

                    k = 0
                    if value == page:
                        k += 1
                        # found a page i that links to page p
                        print("found page in loop", k, "this key", key, " has link to page",  page)
                        probability_i = data[key]
                        print("probability of i:", probability_i)
                        num_links = len(corpus[key])
                        print("number of links for i is", num_links)
                        summ += (probability_i / num_links)
                        print("sum is now", summ)
            condition2 = damping_factor * summ
            print("condition2", condition2)
            print("data[page] before damping", data[page])
            data[page] = condition1 + condition2
            print("data[page] AFTER damping", data[page])
        total = sum(data.values())
        for item in data:
            data[item] /= total
            data[item] = round(data[item], 4)
        print("data is", data)
    return data

        # break while(True) loop when pageRank values, for each page, from current iteration
        # differ by less than 0.001. Afterwards, return data (at same level (and thus outside) of while loop)






if __name__ == "__main__":
    main()
