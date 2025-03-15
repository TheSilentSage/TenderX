import pdfplumber
from extractor import extractTender,llmJson
from app import TenderApp,TenderObject


tenderObject = TenderObject(pdfplumber,extractTender,llmJson)
TenderApp(tenderObject)





