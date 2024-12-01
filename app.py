import streamlit as st
import requests
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import uvicorn
from threading import Thread

# --- FastAPI Backend --- #
app = FastAPI()

class ChatRequest(BaseModel):
    q: str        # Pertanyaan dari pengguna (string)
    long: float   # Longitude (float)
    lat: float    # Latitude (float)
    user: str     # Nama pengguna (string)

# Endpoint FastAPI untuk menerima input chatbot dan mengembalikan response JSON
@app.post("/chatbot")
async def chatbot_response(request: ChatRequest):
    response = {
        "question": request.q,
        "longitude": request.long,
        "latitude": request.lat,
        "user": request.user,
        "message": f"Hello {request.user}, you asked: '{request.q}'",
        "location": {
            "latitude": request.lat,
            "longitude": request.long
        }
    }
    return response

# Fungsi untuk menjalankan FastAPI di background thread
def run_fastapi():
    uvicorn.run(app, host="127.0.0.1", port=8000)

# --- Streamlit UI --- #

# Menampilkan title dan instruksi di Streamlit
# Menampilkan title dan dokumentasi API di Streamlit
st.title("Chatbot with FastAPI and Streamlit")
st.write("""
    This is a simple chatbot interface that interacts with a FastAPI backend. 
    You can enter your question, latitude, longitude, and your username, 
    and the server will respond with a message and your data.
""")

# --- Dokumentasi API --- #
st.subheader("API Documentation")

st.markdown("""
### API Endpoint
- **POST** `http://127.0.0.1:8000/chatbot`

### Request Body (JSON)
You need to send the following JSON data:

```json
{
  "q": "Your question here",
  "long": 106.8456,      # Longitude (float)
  "lat": -6.2088,       # Latitude (float)
  "user": "Your Name"    # Your username (string)
}
```
            """)

# Form input untuk pengguna
user_question = st.text_input("Ask a question:", "")
longitude = st.number_input("Enter longitude:", value=106.8456)
latitude = st.number_input("Enter latitude:", value=-6.2088)
username = st.text_input("Your name:", "")

# Tombol untuk mengirim data
if st.button("Send"):
    if user_question and username:
        # Kirim data ke FastAPI backend
        payload = {
            "q": user_question,
            "long": longitude,
            "lat": latitude,
            "user": username
        }
        response = requests.post("http://127.0.0.1:8000/chatbot", json=payload)
        
        if response.status_code == 200:
            data = response.json()
            st.subheader("Response from Chatbot")
            st.json(data)
        else:
            st.error("Error: Unable to get response from the server.")
    else:
        st.warning("Please fill in all fields.")

# Menjalankan FastAPI server di background
if __name__ == "__main__":
    thread = Thread(target=run_fastapi)
    thread.start()
    
    # Menjalankan Streamlit
    st.write("Streamlit is running...")
