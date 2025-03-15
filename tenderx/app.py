import streamlit as st


class TenderObject():
   def __init__(self,pdfReader,tenderExtractor,tenderLLM):
      self.pdfReader = pdfReader
      self.tenderExtractor = tenderExtractor
      self.tenderLLM = tenderLLM

      

def TenderApp(tenderObject:TenderObject):
  global number_of_pages


  st.set_page_config(page_title="TenderX", layout="wide")
  st.markdown(
  """
  <style>

  .stApp {
      background-color: white !important;
  }

  .stFileUploader {
      max-width: 60% !important;
      color: black !important;
      margin: auto;
  }

  .stJson {
      max-width: 60% !important;
      margin: auto;
  }


  .navbar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 10px 20px;
      background-color: white;
      border-bottom: 2px solid #e5e7eb;
      position: fixed;
      top: 1;
      left: 0;
      width: 100%;
      z-index: 1000;
  }

  .navbar .brand {
      display: flex;
      align-items: center;
      font-size: 1.5rem;
      font-weight: bold;
      color: black;
      text-decoration: none;
  }

  .navbar .brand img {
      height: 40px;
      margin-right: 10px;
  }

  .navbar .nav-links {
      position: absolute;
      left: 50%;
      transform: translateX(-50%);
      display: flex;
      gap: 30px;
  }

  .navbar .nav-links a {
      font-size: 1rem;
      color: black;
      text-decoration: none;
      font-weight: 500;
  }

  .navbar .nav-links a:hover {
      color: #a855f7;
  }

  .main-title{
      color: black;
      font-weight: 700;
      margin-left:30% !important;
      margin-top:10% !important;
      margin-bottom: 1rem;
      line-height: 1.1;
      font-size:72px !important;

  }
  .subtitle {
      font-size: 20px !important;
      margin-top: 1rem;
      line-height: 1.6;
      margin-left:30% !important;
      margin-top:2rem !important;
      color: black;
  }

  .infoTitle {
      font-size: 26px !important;
      line-height: 1.6;
      font-weight: 400 ;
      margin-top:20% !important;
      margin-left:20% !important;
      color: black;
  }

  .error-box {
      color:black;
      margin-left: 20% !important;
      max-width: 60% !important;
      background-color:#f2f2f2;
      border:1px solid #ccc;
      padding:5px;
      border-radius:5px;
  }
  </style>
  """,
  unsafe_allow_html=True
  )

  st.markdown("""
  <div class="navbar">
      <a href="#" class="brand">
          <img src="https://framerusercontent.com/images/SmKwsGk3XnUP0CKRGMy7PCYGGKw.png" alt="Logo"> TenderX
      </a>
      <div class="nav-links">
          <a href="#benefits">Benefits</a>
          <a href="#product">Product</a>
          <a href="#faqs">FAQs</a>
      </div>
  </div>
  <div class="spacer"></div>
  """, unsafe_allow_html=True)


  col1, col2 = st.columns([1.2, 1])

  with col1:
      st.markdown("""
      <p class="main-title">
          Streamline Your<br> Tender Process<br>
          with Cutting- <br> Edge AI
      </p>
      """, unsafe_allow_html=True)

      st.markdown("""
      <p class="subtitle">
          At TenderX, we redefine how you discover, apply, and manage tenders.
          Powered by advanced Language Learning Models and AI-driven Natural
          Language Processing, we tailor opportunities directly to your business
          needs, ensuring you never miss a beat in the competitive tendering landscape.
      </p>
      """, unsafe_allow_html=True)
      st.markdown('</div>', unsafe_allow_html=True)

  with col2:
      st.markdown("""
      <p class="infoTitle"">Process Tender Document.</p>
      """, unsafe_allow_html=True)
      uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

      if uploaded_file is not None:
          with st.spinner("Processing..."):
              try:
                with tenderObject.pdfReader.open(uploaded_file) as reader:
                  result = tenderObject.tenderExtractor(reader)
                  llmOutput = tenderObject.tenderLLM(result)

                  outputJson = {
                     uploaded_file.name : llmOutput
                  }

                  st.write("Processed Output: ")
                  st.json(outputJson)
              except Exception as e:
                  st.markdown(f'<p class="error-box">🚨 {e} </p>', unsafe_allow_html=True)

