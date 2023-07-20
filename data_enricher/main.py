import argparse
from enricher import Enricher

def main():
    """
    Main function to start the application.
    """

    # Create the argument parser
    parser = argparse.ArgumentParser(description="DataEnricherLLM application")

    # Add the arguments
    parser.add_argument("question", nargs='?', type=str, help="The prompt to enrich", default="Test question")
    parser.add_argument("-s", "--nsearches", type=int, help="How many searches to performs", default=3)
    parser.add_argument("-n", "--nresults", type=int, help="How many results from each search should be scraped", default=5)
    parser.add_argument("-v", "--verbose", type=bool, help="Traces everything that is does", default=True)
    parser.add_argument("-c", "--clipboard", type=bool, help="Puts on clipboard the resulting prompt", default=False)
    
    # Parse the arguments
    args = parser.parse_args()

    enricher = Enricher(args.nsearches, args.nresults, args.verbose, args.clipboard)
    completion = enricher.process(args.question)
    print(f"End result:\n{completion}")

if __name__ == "__main__":
    main()
