class TenderNotFoundError(Exception):
    def __init__(self):
        super().__init__("No Tender Found")