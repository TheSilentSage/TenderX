import google.generativeai as genai
import os
import re
import json
from dotenv import load_dotenv
from tender_errors import TenderNotFoundError


load_dotenv()

filePath = "/content/drive/MyDrive/TenderX/valid7.pdf"
keywords = ["products","makes","manufacturers","recommended"]
pdfPageNum = 0
number_of_pages = 0


if not os.getenv("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY") == "YOUR_API_KEY":
     raise ValueError("GOOGLE_API_KEY not found in .env file. Please set it.")


def llmJson(text):
  if os.getenv("GOOGLE_API_KEY"):
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
  
  generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
  }

  model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="You are an expert in tenders and converting unstructured data to structured. Given a text which was scraped from pdf table convert it into the following json format:\n  [\n    {\n      \"product\": \"string\",\n      \"brands\": [\"string\"]\n    }\n  ]\n}. If no useful text return Not Found",
  )

  print(text)
  print("\n\n")
  response = model.generate_content(text)
  print(response)
  response = response.text.strip('```json\n').strip('\n```')
  if response.lower() == "not found":
    raise TenderNotFoundError()

  response = json.loads(response)
  if response == []:
    raise TenderNotFoundError()


  return response



def extractSectionText(pdfObj,currentSection):
    global pdfPageNum,number_of_pages
    text = ""
    extract = ""
    while pdfPageNum < number_of_pages:
          extract = pdfObj.pages[pdfPageNum].extract_text()
          patternSection = r'(\d+\.\d+(?:\.\d+)*)\s+'
          reSearchSection = re.compile(patternSection,re.IGNORECASE)
          pdfPageNum += 1

          matchSection = reSearchSection.findall(extract)
          if matchSection == [] or matchSection[0] == currentSection:
            text += extract
            continue
          else:
            text += extract
            break


    return text


def extractTender(pdfObj):
    global pdfPageNum,number_of_pages
    text = ""
    addText = False
    number_of_pages = len(pdfObj.pages)

    if number_of_pages < 10:
      print("No tender data found")



    while pdfPageNum < number_of_pages:
      extract = pdfObj.pages[pdfPageNum].extract_text()
      patternText = r'(\d+(?:\.\d+)*)\s+(SOURCE[S]* OF PROCUREMENT)'
      reSearchText = re.compile(patternText,re.IGNORECASE)
      matchText = reSearchText.findall(extract)
      if  matchText:
        current_section = matchText[0][0]
        text += extractSectionText(pdfObj,current_section)
        continue
      else:
        pdfPageNum+=1

      if any("list of " + word in extract.lower() for word in keywords):
          addText = True
          text += extract
          continue
      elif not addText:
        continue

      elif "signature of contractor" in extract.lower():
          addText = False
          text += extract

      if addText:
        text += extract
      else:
        break

    if text == "":
      raise TenderNotFoundError()

    return text


if __name__ == "__main__":
    main()