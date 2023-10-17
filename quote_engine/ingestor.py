"""Ingestor module to select an appropriate module for parsing the corresponding file"""
from quote_engine import ( 
                         QuoteModel
                        ,IngestorInterface
                        ,DOCXIngestor
                        ,CSVIngestor
                        ,PDFIngestor
                        ,TXTIngestor
)

class Ingestor(IngestorInterface):
    """The class to select an appropriate module for parsing the corresponding"""
    
    # the list of all ingestor helper classes
    ingestors = [DOCXIngestor(), CSVIngestor(), PDFIngestor(), TXTIngestor()]
    
    # def __init__(self, path):
    #     """Initialize the list of ingestors"""
    #     self.ingestors = [DOCXIngestor(), CSVIngestor(), PDFIngestor(), TXTIngestor()]
    
    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """From all helper classes, find an appropriate class to parse the given path if any.
        """
        return any(ingestor.can_ingest(path) for ingestor in cls.ingestors)

    @classmethod
    def parse(cls, path: str) -> list[QuoteModel]:
        """Parse the file if supported and extract the quotes
        """
        # a list of parsed quotes from a file
        quotes = []

        for ingestor in cls.ingestors:
            if ingestor.can_ingest(path):
                quotes = ingestor.parse(path)
                break

        return quotes