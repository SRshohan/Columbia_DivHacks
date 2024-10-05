from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI
from dotenv import load_dotenv
import os


load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY") 
if not openai_api_key:
    raise ValueError("API key not found. Please set it in the .env file.")


emotion_responses = {
    "anxiety": "Feeling anxious can be tough.",
    "depression": "I’m sorry to hear you’re feeling this way. It's important to reach out to someone who can help, like a mental health professional.",
    "sadness": "It's okay to feel sad sometimes. Try to engage in activities that bring you joy or comfort.",
    "loneliness": "Feeling lonely can be challenging. Consider reaching out to a friend or engaging in a hobby you enjoy."
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


anxiety_keywords = ["anxious", "overwhelmed", "nervous", "worry", "panic", "fear", "stressed", "restless", "uneasy", "apprehensive"]
depression_keywords = ["sad", "depressed", "down", "hopeless", "fatigue", "tired", "loss of interest", "worthless", "empty", "no energy"]

def detect_emotion(user_input):
   
    user_input = user_input.lower()
    
  
    if any(keyword in user_input for keyword in anxiety_keywords):
        return "anxiety"
    

    elif any(keyword in user_input for keyword in depression_keywords):
        return "depression"
    
    return "neutral" 

def generate_response(user_input, memory, suggestion_allowed):
    
    prompt = PromptTemplate(
        input_variables=["context", "emotion", "user_input"],
        template="{context} The user says: {user_input}. Based on this, respond empathetically and provide advice based on their emotional state."
    )
    
    detected_emotion = detect_emotion(user_input)
    
 
    memory["emotion"] = detected_emotion
    

    if detected_emotion in emotion_responses and suggestion_allowed:
        advice = emotion_responses[detected_emotion]
        context = initial_prompt + f" The user is feeling {detected_emotion}. Advice: {advice}"
        response = llm(prompt.format(context=context, emotion=detected_emotion, user_input=user_input))
    else:
        if detected_emotion == "anxiety":
            response = "I sense that you're feeling anxious. Can you share more about what's causing you to feel this way? What are you worried about?"
        elif detected_emotion == "depression":
            response = "It sounds like you might be feeling down. Can you tell me more about what's been on your mind lately? What specific thoughts are you experiencing?"
        else:
            response = "I'm here to listen. Can you tell me more about how you're feeling? What’s been on your mind lately?"

    return response


def main():
    memory = {}  

    print("You can start talking to Dr. Andrea (type 'exit' to end):")
    
    
    first_interaction = True
    print("Dr. Andrea: Hello! I'm Dr. Andrea, here to listen and help you with your thoughts and feelings.")
    
    suggestion_allowed = False  

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Ending the conversation. Take care!")
            break
        if first_interaction:
            first_interaction = False  
        
        response = generate_response(user_input, memory, suggestion_allowed)
        print(f"Dr. Andrea: {response}")
        
       
        if not suggestion_allowed and user_input.strip():
            suggestion_allowed = True 

if __name__ == "__main__":
    main()
