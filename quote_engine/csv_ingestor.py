"""Strategy object for the CSV file type."""
# from .quote_model import QuoteModel
# from .ingestor_interface import IngestorInterface
from quote_engine import ( 
                         QuoteModel
                        ,IngestorInterface
)
import pandas as pd

class CSVIngestor(IngestorInterface):
    """This class is responsible for parsing CSV files"""
    
    #The file extension supported is '.csv'
    #allowed_extensions = ['csv']

    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """Check if the given path is a CSV file.
        
        Returns:
            True if the path is a CSV file
        """
        # return file_extension in cls.allowed_extensions
        return path.endswith('.csv')

    @classmethod
    def parse(cls, path: str) -> list[QuoteModel]:
        """Extract the quote body and author from the file given.
        
        Returns:
            quotes: list of QuoteModel objects
        """
        # list of QuoteModel objects extracted from the given csv file
        quotes = []

        try:
            with open(path, 'r') as file:
                csv_reader = pd.read_csv(path, header=0)
                # parse line by line
                for _, row in csv_reader.iterrows():
                    body = row['body']
                    author = row['author']
                    # create a corresponding QuoteModel object
                    quote = QuoteModel(body, author)
                    # store in the quotes list
                    quotes.append(quote)
        except FileNotFoundError:
            print(f"File not found: {path}")
        except Exception as e:
            print(f"There is error \"{str(e)}\" when parsing the file {path}")

        return quotes