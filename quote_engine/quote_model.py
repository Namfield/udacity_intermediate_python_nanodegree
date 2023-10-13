"""Quote model class"""

class QuoteModel:
    """A class encapsulating a quote with a body and an author."""

    def __init__(self, quote_body, author):
        """Takes in the body and author as parameters and 
        initializes the corresponding instance variables.
        """
        self.quote_body = quote_body
        self.author = author
    def __str__(self):
        """Returns a formatted string that combines the quote body and author 
        in the format: "quote body" - author.
        """
        return f'"{self.quote_body}" - {self.author}'
        