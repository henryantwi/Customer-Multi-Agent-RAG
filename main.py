from decouple import config
import json
import streamlit as st
import requests
from icecream import ic


BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "69509d96-a607-4d60-839a-5b2c52c1230b"

FLOW_ID = "109ca906-67fb-4549-b2d8-3b697ca7dab7"
APPLICATION_TOKEN = config("APP_TOKEN")

ENDPOINT = "customer"



def run_flow(message: str) -> dict:
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{ENDPOINT}"

    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
    }
    headers = {"Authorization": "Bearer " + APPLICATION_TOKEN, "Content-Type": "application/json"}
    response = requests.post(api_url, json=payload, headers=headers)
    ic(response.json())
    return response.json()


def main():
    st.title("LangFlow Chatbot")
    message = st.text_input("Message", placeholder="Ask something...")
    if st.button("Run Flow"):
        if not message.strip():
            st.warning("Please enter a message")
            return

        try:
            with st.spinner("Running the flow..."):
                response = run_flow(message)
            
            response = response['outputs'][0]['outputs'][0]['results']['message']['text']
            st.markdown(f"**Response:** {response}")
        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
