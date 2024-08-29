from pagerank import *

DAMPING = 0.85
SAMPLES = 100



def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    # crawl function parses html files in directory and returns
    # a dictionary representing the corpus. Keys represent pages
    # and values area a set of all the pages linked to by the key
    # e.g., {"1.html": {"2.html" , "3.html"}} means page 1 links to pages 2 & 3
    corpus = crawl(sys.argv[1])

    # page4 has no outgoing links
    # probabilities = transition_model(corpus, "3.html", DAMPING)
    #print("testFile.py probabilities is: ",probabilities)

    sample_pagerank(corpus, DAMPING, SAMPLES)




if __name__ == "__main__":
    main()
