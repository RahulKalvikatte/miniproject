
import google.generativeai as genai
genai.configure(api_key="AIzaSyCnPgTtaIKjWmSaGCcOWW6-luKfGRuuppk") 
model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")