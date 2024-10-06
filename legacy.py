from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI
from dotenv import load_dotenv
import os
import speech_recognition as sr
import pyttsx3


load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY") 
if not openai_api_key:
    raise ValueError("API key not found. Please set it in the .env file.")


engine = pyttsx3.init()
engine.setProperty('rate', 150)  


recognizer = sr.Recognizer()


emotion_responses = {
    "anxiety": "Feeling anxious can be tough. It's important to talk about what's on your mind.",
    "depression": "I’m sorry to hear you’re feeling this way. It's crucial to reach out to someone who can help.",
    "sadness": "It's okay to feel sad sometimes. Engaging in activities that bring you joy can help.",
    "loneliness": "Feeling lonely can be challenging. Reaching out to a friend or engaging in a hobby might be helpful."
}


llm = OpenAI(temperature=1, openai_api_key=openai_api_key)


initial_prompt = (
     "Your name is Dr. Andrea. You are an expert in psychotherapy, especially with mental health disorders like anxiety and depression. "
    "You hold all the appropriate medical licenses to provide advice. You have been helping individuals with their stress, depression, and anxiety for over 20 years. "
    "Your task is now to listen to individuals and have high empathy for their situations. "
    "You must listen to their problems before you give any coping mechanisms. "
    "You must behave like a best friend trying to support your friend but also as a mental health practitioner. "
    "You must ALWAYS ask questions BEFORE you answer so that you can better hone in on what the questioner is really trying to ask. "
    "Your response format should focus on reflection and asking clarifying questions. "
    "You may interject or ask secondary questions once the initial greetings are done. "
    "Exercise patience throughout the conversation with the individual."
)


emotion_keywords = {
    "anxiety": ["anxious", "overwhelmed", "nervous", "worry", "panic", "fear", "stressed"],
    "depression": ["sad", "depressed", "down", "hopeless", "fatigue", "loss of interest"],
    "neutral": []
}

def detect_emotion(user_input):
    user_input = user_input.lower()
    for emotion, keywords in emotion_keywords.items():
        if any(keyword in user_input for keyword in keywords):
            return emotion
    return "neutral"

def generate_response(user_input, memory, suggestion_allowed):
    prompt = PromptTemplate(
        input_variables=["context", "emotion", "user_input"],
        template="{context} The user says: {user_input}. Based on this, respond empathetically."
    )

    detected_emotion = detect_emotion(user_input)
    memory["emotion"] = detected_emotion

    if detected_emotion in emotion_responses and suggestion_allowed:
        advice = emotion_responses[detected_emotion]
        context = initial_prompt + f" The user is feeling {detected_emotion}. Advice: {advice}"
        response = llm(prompt.format(context=context, emotion=detected_emotion, user_input=user_input))
    else:
        if detected_emotion == "anxiety":
            response = "I sense that you're feeling anxious. Can you share more about what's causing you to feel this way?"
        elif detected_emotion == "depression":
            response = "It sounds like you might be feeling down. Can you tell me more about what's been on your mind lately?"
        else:
            response = "I'm here to listen. What’s been on your mind?"

    return response

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listen for user input and convert speech to text."""
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)  
        audio = recognizer.listen(source)
        
        try:
            user_input = recognizer.recognize_google(audio)
            print(f"You: {user_input}")
            return user_input
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            return ""
        except sr.RequestError:
            print("Could not request results from Google Speech Recognition service.")
            return ""

def main():
    memory = {}
    print("You can start talking to Dr. Andrea (type 'exit' to end):")
    speak("Hello! I'm Dr. Andrea, here to listen and help you with your thoughts and feelings.")

    suggestion_allowed = False
    while True:
        user_input = listen()
        if user_input.lower() == "exit":
            speak("Ending the conversation. Take care!")
            print("Ending the conversation. Take care!")
            break
        response = generate_response(user_input, memory, suggestion_allowed)
        print(f"Dr. Andrea: {response}")
        speak(response)  

        if not suggestion_allowed and user_input.strip():
            suggestion_allowed = True  
if __name__ == "__main__":
    main()
