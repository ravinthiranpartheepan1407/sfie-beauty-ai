import streamlit as st
import urllib.request
import json
import os
import ssl

st.set_page_config(
    page_title="SFIE Beauty Sandbox"
)

# Sidebar menu
st.sidebar.title("Menu")
app_mode = st.sidebar.selectbox("Choose the app mode", ["SFIE Beauty LLM", "Personalized Beauty Care"])


# Function to allow self-signed HTTPS certificates
def allowSelfSignedHttps(allowed):
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context


allowSelfSignedHttps(True)


# SFIE Beauty LLM app
def sfie_beauty_llm():
    st.title("SFIE Beauty LLM")
    api_key = st.text_input("Enter your API key:", type="password")
    prompt = st.text_area("Enter your prompt here:")

    if st.button("Process"):
        if not api_key:
            st.error("Please provide an API key.")
        elif not prompt:
            st.error("Enter your prompt.")
        elif not is_psychology_related(prompt):
            st.error("Irrelevant prompt.")
        else:
            with st.spinner('Processing...'):
                response = get_response(prompt, api_key)
                st.success("Done!")
                st.write("Response:")
                st.write(response)


# Function to check if the prompt is psychology-related
def is_psychology_related(prompt):
    psychology_keywords = [
        'skincare', 'skin health', 'skin type', 'skincare routine', 'skincare products', 'moisturizer',
        'cleanser', 'toner', 'serum', 'sunscreen', 'exfoliation', 'hydration', 'acne treatment',
        'anti-aging', 'hyperpigmentation', 'sensitive skin', 'dry skin', 'oily skin', 'combination skin',
        'skin barrier', 'collagen', 'retinol', 'vitamin C', 'hyaluronic acid', 'niacinamide',
        'peptides', 'AHAs', 'BHAs', 'natural skincare', 'dermatologist', 'facial', 'skin concerns',
        'dark spots', 'redness', 'blemishes', 'eczema', 'psoriasis', 'rosacea', 'dermatitis',
        'pore size', 'skin texture', 'skin tone', 'under-eye care', 'skin detox', 'allergic reactions'
    ]
    return any(keyword.lower() in prompt.lower() for keyword in psychology_keywords)


# Function to get response from Azure-based LLM
def get_response(prompt, api_key):
    data = {
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": 1024,
        "temperature": 0.7,
        "top_p": 1,
        "stream": False
    }

    body = str.encode(json.dumps(data))

    url = 'https://Phi-3-small-8k-instruct-tjzmz.eastus2.models.ai.azure.com/v1/chat/completions'
    headers = {'Content-Type': 'application/json', 'Authorization': ('Bearer ' + api_key)}

    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)
        result = response.read()
        result_json = json.loads(result)
        return result_json['choices'][0]['message']['content']
    except urllib.error.HTTPError as error:
        return f"The request failed with status code: {error.code}\n{error.read().decode('utf8', 'ignore')}"


# Personalized Beauty Care app
def personalized_beauty_care():
    st.title("Personalized Beauty Care")

    # Define the screens
    if "current_screen" not in st.session_state:
        st.session_state.current_screen = 1

    if st.session_state.current_screen == 1:
        screen1()
    elif st.session_state.current_screen == 2:
        screen2()


def screen1():
    st.header("Get the best SFIE Beauty routine via our AI powered Skin Analysis")
    st.text("Take the skin quiz")
    st.text("Tell us your skin goals and budget (takes 2 minutes)")
    st.text("\nUpload your photos\nAdd 3 photos for your skin analysis")
    st.text("\nView your new routine\nReceive a routine in 2 minutes based on your needs and preferences")

    if st.button("Get Started"):
        st.session_state.current_screen = 2


def screen2():
    st.header("What’s your number one skin goal?")
    st.text("Select the goal that matters to you most. You can select more later.")

    goals = [
        "Reduce blemishes", "Minimise blackheads", "Minimise pores visibility",
        "Target post blemish marks", "Lighten pigmentation", "Reduce redness",
        "Reduce wrinkles", "Smooth fine lines", "Improve elasticity",
        "Enhance radiance", "Hydrate dry skin", "Smooth texture",
        "Reduce eye wrinkles", "Brighten dark circles", "Reduce under eye bags"
    ]

    selected_goals = st.multiselect("Choose your skin goals", goals)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Back"):
            st.session_state.current_screen = 1

    with col2:
        if st.button("Next"):
            st.session_state.current_screen = 3


# Run the appropriate app mode
if app_mode == "SFIE Beauty LLM":
    sfie_beauty_llm()
elif app_mode == "Personalized Beauty Care":
    personalized_beauty_care()
