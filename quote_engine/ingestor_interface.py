"""Define the IngestorInterface abstract base class, which will be inherited by the ingestor classes."""
from abc import ABC, abstractmethod
from quote_engine import QuoteModel

class IngestorInterface(ABC):
    """Define a common interface for all the classes that will be responsible for 
    parsing different types of files containing quotes.
    """
    
    @classmethod
    @abstractmethod
    def can_ingest(cls, path: str) -> bool:
        """Determine if a particular strategy (file type (e.g., CSV, DOCX, PDF, TXT)) 
        can ingest (parse) a given file.

        It takes a file path as input and returns a boolean value 
        indicating whether the strategy can handle that file type.
        """
        pass
    
    @classmethod
    @abstractmethod
    def parse(cls, path: str) -> list[QuoteModel]:
        """Parse the file and extract the quotes
        It takes a file path as input and returns a list of QuoteModel objects, 
        which represent the extracted quotes.
        """
        pass