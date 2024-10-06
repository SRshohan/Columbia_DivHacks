import os
import speech_recognition as sr
import pyttsx3
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import play  
import random

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY") 
if not openai_api_key:
    raise ValueError("OpenAI API key not found. Please set it in the .env file.")

elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")
if not elevenlabs_api_key:
    raise ValueError("ElevenLabs API key not found. Please set it in the .env file.")

# Initialize ElevenLabs client
client = ElevenLabs(api_key=elevenlabs_api_key)

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)

# Initialize speech recognizer
recognizer = sr.Recognizer()


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
def detect_emotion(user_input):
    user_input = user_input.lower()
    emotion_keywords = {
    "suicidal": ["hopeless", "despair", "worthless", "isolated", "trapped", "helpless","suicidal","kill","end","end-life"],
    "anxiety": ["anxious", "overwhelmed", "nervous", "worry", "panic", "fear", "stressed"],
    "depression": ["sad", "depressed", "down", "hopeless", "fatigue", "loss of interest", "despair"],
    "sadness": ["sad", "tears", "cry", "unhappy", "sorrow", "melancholy"],
    "loneliness": ["lonely", "isolated", "alone", "forlorn", "desolate"],
    "neutral": ["calm", "stable", "indifferent", "unemotional", "balanced"],
    "anger": ["angry", "mad", "irritated", "frustrated", "enraged", "fuming"],
    "joy": ["happy", "joyful", "excited", "elated", "cheerful", "delighted"],
    "fear": ["scared", "frightened", "terrified", "apprehensive", "panicked"],
    "surprise": ["surprised", "shocked", "astonished", "amazed", "bewildered"],
    "disgust": ["disgusted", "revolted", "sickened", "appalled", "nauseated"],
    "love": ["loving", "affectionate", "adored", "cherished", "passionate"],
    "envy": ["jealous", "resentful", "covetous", "envious"],
    "shame": ["ashamed", "embarrassed", "guilty", "humiliated"],
    "pride": ["proud", "accomplished", "self-satisfied", "content"],
    "confusion": ["confused", "bewildered", "perplexed", "uncertain", "disoriented"],
    "boredom": ["bored", "disinterested", "uninspired", "weary"],
    "hope": ["hopeful", "optimistic", "aspiring", "encouraged"],
    "grief": ["grieving", "mourning", "heartbroken", "sorrowful"],
    "guilt": ["guilty", "remorseful", "repentant", "ashamed"],
    "frustration": ["frustrated", "irritated", "exasperated", "annoyed"],
    "contentment": ["content", "satisfied", "pleased", "fulfilled"],
    "embarrassment": ["embarrassed", "self-conscious", "awkward"],
    "trust": ["trusting", "secure", "confident", "faithful"],
    "relief": ["relieved", "unburdened", "lightened"],
    "anticipation": ["anticipating", "excited", "eager", "hopeful"],
    "nostalgia": ["nostalgic", "wistful", "reflective", "sentimental"],
    "excitement": ["excited", "thrilled", "energized", "enthusiastic"],
    "calm": ["calm", "peaceful", "relaxed", "serene"],
    "assertiveness": ["assertive", "confident", "self-assured"],
    "vulnerability": ["vulnerable", "exposed", "open"],
    "courage": ["courageous", "brave", "fearless", "valiant"],
    "doubt": ["doubtful", "uncertain", "skeptical", "insecure"],
    "indifference": ["indifferent", "apathetic", "unconcerned"],
    "resentment": ["resentful", "bitter", "hostile"],
    "vigor": ["energetic", "vital", "dynamic"],
    "exasperation": ["exasperated", "fed up", "frustrated"],
    "longing": ["longing", "yearning", "desiring"],
    "pessimism": ["pessimistic", "cynical", "defeatist"],
    "satisfaction": ["satisfied", "content", "pleased"],
    }
    for emotion, keywords in emotion_keywords.items():
        if any(keyword in user_input for keyword in keywords):
            return emotion
    return emotion
def generate_response(user_input, memory):
    coping_mechanisms = {
        "suicide": [
            "If you are feeling suicidal or in crisis, please reach out for help.", 
            "Call the National Suicide Prevention Lifeline at 1-800-273-TALK (8255) or text 'HOME' to 741741 for immediate support."],
            "anxiety": [
                "Try deep breathing exercises to calm your mind.",
                "Consider writing down your thoughts to process them.",
                "Engage in physical activity; it can help relieve tension.",
                "Practice mindfulness or meditation to stay grounded.",
                "Reach out to someone you trust and talk about your feelings."
            ],
            "depression": [
                "Establish a routine to create structure in your day.",
                "Engage in activities that you once enjoyed, even if you don't feel like it.",
                "Consider talking to a professional for support.",
                "Practice self-care; take time to pamper yourself.",
                "Stay connected with friends or family, even if it's just a text."
            ],
            "sadness": [
                "Allow yourself to feel the sadness; it’s okay to cry.",
                "Talk about your feelings with a friend or loved one.",
                "Engage in creative activities, like art or music.",
                "Spend time in nature; it can lift your spirits.",
                "Consider keeping a journal to express your emotions."
            ],
            "loneliness": [
                "Reach out to friends or family; a conversation can help.",
                "Consider joining a group or class to meet new people.",
                "Volunteer for a cause you care about; it can foster connections.",
                "Engage in activities that you enjoy and can do with others.",
                "Practice self-compassion; it’s okay to feel lonely sometimes."
            ],
            "neutral": [
                "Take a moment to appreciate the calmness.",
                "Engage in a hobby that you enjoy.",
                "Consider reading a book or watching a movie.",
                "Reflect on things you are grateful for.",
                "Spend time in a peaceful environment."
            ],
            "anger": [
                "Practice physical activity to release pent-up energy.",
                "Take deep breaths and count to ten before responding.",
                "Express your feelings in a journal to process them.",
                "Try to identify the root cause of your anger.",
                "Talk to someone you trust about how you feel."
            ],
            "joy": [
                "Share your happiness with others; it can amplify joy.",
                "Engage in activities that make you feel even more joyful.",
                "Reflect on the things that brought you joy.",
                "Consider keeping a gratitude journal.",
                "Celebrate your achievements, no matter how small."
            ],
            "fear": [
                "Identify what is making you fearful and confront it gradually.",
                "Talk to someone about your fears; sharing can help lessen them.",
                "Engage in grounding exercises to bring you back to the present.",
                "Practice visualization techniques to imagine a positive outcome.",
                "Limit exposure to triggering stimuli when possible."
            ],
            "surprise": [
                "Take a moment to process what surprised you.",
                "Reflect on the positive aspects of the surprise.",
                "Share your surprise with someone and discuss it.",
                "Consider how surprises can lead to new opportunities.",
                "Keep an open mind for future surprises."
            ],
            "disgust": [
                "Take a break from the situation that disgusts you.",
                "Express your feelings through art or writing.",
                "Consider why you feel disgusted and explore those feelings.",
                "Talk to someone about your feelings to gain perspective.",
                "Engage in activities that bring you joy to counteract the feeling."
            ],
            "love": [
                "Express your love through words or actions.",
                "Spend quality time with loved ones.",
                "Reflect on what love means to you.",
                "Practice self-love and care.",
                "Engage in activities that foster connections."
            ],
            "envy": [
                "Acknowledge your feelings of envy and explore their roots.",
                "Focus on your own achievements and strengths.",
                "Practice gratitude for what you have.",
                "Consider reaching out to the person you envy for support.",
                "Transform envy into inspiration to pursue your goals."
            ],
            "shame": [
                "Talk to someone you trust about your feelings of shame.",
                "Practice self-compassion and recognize that everyone makes mistakes.",
                "Reflect on what you've learned from the situation.",
                "Engage in activities that promote self-acceptance.",
                "Consider professional help to address deeper feelings of shame."
            ],
            "pride": [
                "Share your achievements with others; it can inspire them.",
                "Reflect on the effort that led to your pride.",
                "Consider ways to use your pride positively.",
                "Practice humility; recognize that everyone has their journey.",
                "Celebrate your successes without downplaying them."
            ],
            "confusion": [
                "Take a break and give yourself time to think.",
                "Write down your thoughts to organize them.",
                "Ask questions to clarify your confusion.",
                "Talk to someone who can provide a different perspective.",
                "Engage in a grounding activity to refocus your mind."
            ],
            "boredom": [
                "Try a new activity or hobby to stimulate your interest.",
                "Set small goals for yourself to add structure.",
                "Consider taking a break and doing nothing for a while.",
                "Reflect on your interests to find new ones.",
                "Engage in a creative activity to spark inspiration."
            ],
            "hope": [
                "Set achievable goals to turn hope into action.",
                "Reflect on past successes to fuel your hope.",
                "Share your hopes with someone supportive.",
                "Consider creating a vision board to visualize your future.",
                "Stay open to new possibilities and opportunities."
            ],
            "grief": [
                "Allow yourself to feel and express your grief.",
                "Talk to someone who understands your loss.",
                "Engage in rituals that honor your loved one.",
                "Consider joining a support group for shared experiences.",
                "Be patient with yourself; healing takes time."
            ],
            "guilt": [
                "Reflect on the situation and learn from it.",
                "Consider making amends if possible.",
                "Practice self-forgiveness; everyone makes mistakes.",
                "Talk about your feelings with someone you trust.",
                "Engage in activities that promote self-care."
            ],
            "frustration": [
                "Take a break from the situation causing frustration.",
                "Practice mindfulness or deep breathing to calm down.",
                "Express your feelings through art or writing.",
                "Identify what you can control and focus on that.",
                "Talk to someone about your frustrations."
            ],
            "contentment": [
                "Reflect on the things that bring you contentment.",
                "Practice gratitude by acknowledging your blessings.",
                "Engage in activities that enhance your sense of peace.",
                "Share your feelings of contentment with someone.",
                "Continue to set small goals for personal growth."
            ],
            "embarrassment": [
                "Acknowledge your feelings and practice self-compassion.",
                "Talk to someone about the incident to gain perspective.",
                "Engage in activities that boost your confidence.",
                "Reflect on the humor in the situation.",
                "Consider that everyone experiences embarrassment."
            ],
            "trust": [
                "Reflect on your relationships and what builds trust.",
                "Communicate openly with those you trust.",
                "Practice being trustworthy yourself.",
                "Engage in activities that foster connection and security.",
                "Consider professional help if trust issues arise."
            ],
            "relief": [
                "Take time to enjoy the feeling of relief.",
                "Reflect on what led to this relief and how to sustain it.",
                "Share your sense of relief with someone.",
                "Consider engaging in self-care to maintain this feeling.",
                "Practice gratitude for what has lifted your burden."
            ],
            "anticipation": [
                "Channel your excitement into preparation for what's coming.",
                "Practice mindfulness to stay present while anticipating.",
                "Share your excitement with others to enhance the experience.",
                "Consider visualizing positive outcomes.",
                "Stay open to unexpected surprises along the way."
            ],
            "nostalgia": [
                "Allow yourself to reminisce and reflect on the past.",
                "Engage in activities that bring back positive memories.",
                "Share nostalgic stories with friends or family.",
                "Consider creating a scrapbook or memory box.",
                "Balance nostalgia with appreciation for the present."
            ],
            "excitement": [
                "Channel your excitement into action; try something new.",
                "Share your excitement with others; it can enhance the feeling.",
                "Reflect on what makes you feel excited and pursue it.",
                "Consider setting goals to sustain this feeling.",
                "Engage in activities that further ignite your passion."
            ],
            "calm": [
                "Practice mindfulness or meditation to maintain your calm.",
                "Engage in activities that promote relaxation.",
                "Reflect on what brings you peace and prioritize those things.",
                "Share your feelings of calm with others.",
                "Consider practicing gratitude to enhance your sense of calm."
            ],
            "assertiveness": [
                "Practice clear and direct communication.",
                "Reflect on your needs and express them confidently.",
                "Engage in activities that boost your self-esteem.",
                "Seek feedback from trusted friends on your assertiveness.",
                "Consider assertiveness training if needed."
            ],
            "vulnerability": [
                "Acknowledge that vulnerability is a strength.",
                "Practice sharing your feelings with trusted individuals.",
                "Engage in activities that foster authentic connections.",
                "Reflect on past experiences of vulnerability and growth.",
                "Consider journaling about your feelings to process them."
            ],
            "courage": [
                "Acknowledge your fears and confront them step by step.",
                "Reflect on times you’ve shown courage in the past.",
                "Engage in activities that challenge you to grow.",
                "Share your courageous moments with others for support.",
                "Consider setting small goals to build your courage."
            ],
            "hopefulness": [
                "Set achievable goals to keep your hope alive.",
                "Reflect on what inspires you and seek those influences.",
                "Share your hopes with someone who supports you.",
                "Practice gratitude to focus on the positive aspects of life.",
                "Engage in activities that bring you joy and hope."
            ],
            "restlessness": [
                "Engage in physical activity to channel your energy.",
                "Consider taking breaks throughout your day.",
                "Practice mindfulness to ground yourself.",
                "Reflect on what might be causing your restlessness.",
                "Try new activities to stimulate your mind."
            ],
            "animosity": [
                "Reflect on the source of your animosity and why you feel this way.",
                "Consider talking to someone about your feelings.",
                "Practice empathy and try to understand the other person’s perspective.",
                "Engage in activities that promote compassion.",
                "Focus on self-care to alleviate feelings of animosity."
            ],
            "resentment": [
                "Acknowledge your feelings of resentment and explore them.",
                "Consider talking to the person you're resenting if appropriate.",
                "Practice forgiveness for yourself and others.",
                "Engage in activities that promote healing.",
                "Reflect on what you can learn from the situation."
            ],
            "overwhelm": [
                "Take a step back and breathe deeply.",
                "Break tasks into smaller, manageable steps.",
                "Engage in self-care activities that help you recharge.",
                "Consider talking to someone about how you're feeling.",
                "Practice mindfulness to stay grounded."
            ],
            "restoration": [
                "Engage in self-care to replenish your energy.",
                "Reflect on what brings you joy and pursue those activities.",
                "Share your restoration journey with others for support.",
                "Consider taking breaks to recharge throughout your day.",
                "Practice gratitude for the moments of restoration."
            ],
            "acceptance": [
                "Reflect on what acceptance means to you.",
                "Practice self-compassion and kindness.",
                "Engage in activities that promote peace of mind.",
                "Share your journey of acceptance with others.",
                "Consider journaling about your feelings of acceptance."
            ],
            "impatience": [
                "Practice mindfulness to stay present in the moment.",
                "Reflect on the reasons for your impatience.",
                "Engage in activities that require patience and focus.",
                "Consider setting small goals to cultivate patience.",
                "Talk to someone about your feelings of impatience."
            ],
            "closure": [
                "Reflect on what closure means for you.",
                "Consider journaling about your experiences.",
                "Engage in rituals that promote a sense of closure.",
                "Talk to someone who can provide perspective.",
                "Practice self-compassion as you seek closure."
            ],
            "clarity": [
                "Take time to reflect and meditate on your thoughts.",
                "Engage in activities that promote clear thinking.",
                "Share your insights with someone who can provide feedback.",
                "Consider journaling to clarify your thoughts.",
                "Practice mindfulness to maintain clarity."
            ],
            "disappointment": [
                "Acknowledge your feelings of disappointment.",
                "Reflect on what you can learn from the experience.",
                "Engage in self-care activities to lift your spirits.",
                "Consider talking to someone who can provide support.",
                "Focus on what you can do moving forward."
            ],
            "growth": [
                "Reflect on your progress and celebrate small victories.",
                "Engage in activities that foster personal development.",
                "Share your growth journey with others.",
                "Consider setting goals for continued growth.",
                "Practice gratitude for your experiences."
            ],
            "rejection": [
                "Acknowledge your feelings of rejection and process them.",
                "Engage in self-compassion and kindness towards yourself.",
                "Talk to someone who can provide support.",
                "Reflect on the situation and what you can learn from it.",
                "Focus on your strengths and what makes you unique."
            ],
            "vigilance": [
                "Practice mindfulness to stay present and grounded.",
                "Engage in activities that promote relaxation.",
                "Reflect on what makes you feel safe and secure.",
                "Share your feelings of vigilance with someone you trust.",
                "Consider taking breaks to recharge."
            ],
            "skepticism": [
                "Reflect on the reasons behind your skepticism.",
                "Engage in discussions to gain different perspectives.",
                "Consider the benefits of being open-minded.",
                "Practice curiosity by exploring new ideas.",
                "Talk to someone who can provide support."
            ],
            "vulnerability": [
                "Recognize that vulnerability can lead to deeper connections.",
                "Practice self-compassion and kindness.",
                "Share your feelings with someone you trust.",
                "Engage in activities that promote authentic expression.",
                "Consider journaling about your vulnerabilities."
            ],
            "enthusiasm": [
                "Share your enthusiasm with others to amplify it.",
                "Engage in activities that excite you.",
                "Reflect on what fuels your enthusiasm.",
                "Consider setting goals to pursue your passions.",
                "Practice gratitude for the things that inspire you."
            ]
    }
    
    detected_emotion = detect_emotion(user_input)
    memory["emotion"] = detected_emotion  

    if detected_emotion == "suicidal":
        coping = coping_mechanisms[detected_emotion]
        response = (
            "".join(coping)
        )
        return response
    elif detected_emotion in coping_mechanisms:
        coping = coping_mechanisms[detected_emotion]
        response = (
            f"I'm really sorry to hear that you're feeling {detected_emotion}. It's important to talk about it. "
            "Here are some coping mechanisms you might consider:\n" + "\n".join(coping)
        )
    else:
        responses = ["I'm here to listen. Can you explain more?","It’s okay to share more about what you’re going through. I’m here for you.", "Please feel free to share more details. I'm listening and here for you."]
        response = random.choice(responses)
    return response
def generate_audio(text):
    """Generate and play audio response using ElevenLabs."""
    print(text)
    audio = client.generate(
        text=text,
        voice="WljsxseqtJlL72K5Zh8j", 
        model="eleven_multilingual_v2" 
    )
    play(audio)
def speak(text):
    """Convert text to speech using pyttsx3 (optional fallback)."""
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
        

