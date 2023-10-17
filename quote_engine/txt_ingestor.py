"""Strategy object for the txt file type."""
# from .quote_model import QuoteModel
# from .ingestor_interface import IngestorInterface
from quote_engine import ( 
                         QuoteModel
                        ,IngestorInterface
)

class TXTIngestor(IngestorInterface):
    """This class is responsible for parsing txt files"""
    
    #The file extension supported is '.txt'
    #allowed_extensions = ['txt']
    
    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """Check if the given path is a txt file.
        
        Returns:
            True if the path is a txt file
        """
        # # splits the path by '.' and compares the last element with the allowed extensions.
        # file_extension = path.split('.')[-1]

        # return file_extension in cls.allowed_extensions
        return path.endswith('.txt')

    @classmethod
    def parse(cls, path: str) -> list[QuoteModel]:
        """Extract the quote body and author from the file given.
        
        Returns:
            quotes: list of QuoteModel objects
        """
        # list of QuoteModel objects extracted from the given txt file
        quotes = []

        try:
            with open(path, 'r') as file:
                # parse line by line
                for line in file:
                    """extract body and author
                    strip(): remove any leading or trailing whitespace characters
                    split(' - '): split the line into a list of values based on the comma (,) delimiter
                    """
                    body, author = line.strip().split(' - ')
                    # create a corresponding QuoteModel object
                    quote = QuoteModel(body, author)
                    # store in the quotes list
                    quotes.append(quote)
        except FileNotFoundError:
            print(f"File not found: {path}")
        except Exception as e:
            print(f"There is error \"{str(e)}\" when parsing the file {path}")

        return quotes