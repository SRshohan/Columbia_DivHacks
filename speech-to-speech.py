import os
import speech_recognition as sr
import pyttsx3
from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import play  

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

# Emotion responses
emotion_responses = {
    "anxiety": [
        "I feel overwhelmed and can't seem to relax.",
        "My mind is racing, and I can't focus.",
        "I'm constantly worrying about what might happen.",
        "I feel on edge and can't shake this nervousness.",
        "Panic sets in whenever I think about the future."
    ],
    "depression": [
        "I feel so low and hopeless right now.",
        "It's hard to find joy in anything anymore.",
        "I'm just so tired all the time.",
        "I’ve lost interest in things I used to love.",
        "Everything feels heavy and exhausting."
    ],
    "sadness": [
        "I can't stop crying; it just feels so sad.",
        "There's this deep sorrow in my heart.",
        "I feel utterly unhappy with everything.",
        "Tears keep coming, and I don't know why.",
        "It's a struggle to get through the day."
    ],
    "loneliness": [
        "I feel so lonely even when I'm surrounded by people.",
        "There's an emptiness I can't shake off.",
        "I just want someone to talk to.",
        "It feels like I'm all alone in this world.",
        "I long for connection but feel isolated."
    ],
    "neutral": [
        "I feel balanced and calm today.",
        "Things are okay; I'm just going with the flow.",
        "There's a sense of stability in my life right now.",
        "I'm feeling indifferent about everything.",
        "It's a neutral day; nothing too exciting."
    ],
    "anger": [
        "I’m so angry right now; I could explode.",
        "Everything is irritating me today.",
        "I feel frustrated and fed up with it all.",
        "This situation makes me really mad.",
        "I just can't believe what happened; it makes me furious."
    ],
    "joy": [
        "I feel so happy and full of life!",
        "Everything feels bright and joyful right now.",
        "I can't stop smiling; I'm just so excited!",
        "It's a wonderful day, and I'm feeling elated.",
        "I feel grateful and joyful for all I have."
    ],
    "fear": [
        "I'm scared of what might happen next.",
        "Fear is gripping me, and I can't seem to escape it.",
        "I feel terrified; my heart is racing.",
        "This situation is really frightening.",
        "I can’t shake this feeling of dread."
    ],
    "surprise": [
        "I’m completely taken aback by this!",
        "Wow, that was unexpected!",
        "I'm astonished; I didn't see that coming.",
        "This is such a surprise; I'm speechless.",
        "I feel amazed at how things turned out."
    ],
    "disgust": [
        "I'm feeling really disgusted by this situation.",
        "This makes me feel sick to my stomach.",
        "I can't believe what I just saw; it's appalling.",
        "I'm revolted by what happened.",
        "This is absolutely nauseating to me."
    ],
    "love": [
        "I feel so much love in my heart right now.",
        "There's a warmth and affection surrounding me.",
        "I cherish the people in my life deeply.",
        "I'm so passionate about this; it fills me with love.",
        "Love is what makes everything worthwhile."
    ],
    "envy": [
        "I can't help but feel envious of their success.",
        "I wish I had what they have.",
        "That makes me feel a bit resentful.",
        "I’m feeling jealous; it's hard to admit.",
        "I find myself coveting what others possess."
    ],
    "shame": [
        "I feel so ashamed of what I did.",
        "There's this deep embarrassment I can't shake.",
        "I wish I could hide; I'm feeling humiliated.",
        "I can't believe I let myself act that way.",
        "I feel guilty and regretful about my actions."
    ],
    "pride": [
        "I'm proud of my achievements and what I've done.",
        "I feel a sense of accomplishment and fulfillment.",
        "There's a warm glow of pride in my heart.",
        "I'm confident in who I am and what I've achieved.",
        "I feel satisfied with my progress and efforts."
    ],
    "confusion": [
        "I'm feeling so confused; nothing makes sense.",
        "I'm bewildered and can't find clarity.",
        "There's so much uncertainty; it's disorienting.",
        "I don't know what to think or feel right now.",
        "This situation is perplexing and complicated."
    ],
    "boredom": [
        "I'm so bored; nothing interests me.",
        "I feel restless and uninspired.",
        "This is just dull; I need something exciting.",
        "I can't seem to find anything to keep my attention.",
        "I feel like I'm just going through the motions."
    ],
    "hope": [
        "I feel hopeful about the future.",
        "There's a light at the end of the tunnel.",
        "I'm optimistic that things will get better.",
        "I have faith that things will improve.",
        "Hope is what keeps me going."
    ],
    "grief": [
        "I'm heartbroken and in mourning.",
        "This grief feels overwhelming at times.",
        "I miss them so much; it's hard to cope.",
        "I’m feeling sorrowful; it’s a painful process.",
        "Grief is a heavy burden to bear."
    ],
    "guilt": [
        "I feel so guilty about what I did.",
        "There’s this constant reminder of my mistakes.",
        "I can’t shake off this feeling of remorse.",
        "I wish I could take back my actions.",
        "Guilt is weighing heavily on my conscience."
    ],
    "frustration": [
        "I'm so frustrated; nothing seems to go right.",
        "This situation is really getting on my nerves.",
        "I feel irritated and exasperated.",
        "I can't deal with this anymore; it's maddening.",
        "My patience is wearing thin; I'm fed up."
    ],
    "contentment": [
        "I feel content and at peace with my life.",
        "There's a sense of satisfaction that fills me.",
        "I’m happy with where I am right now.",
        "I feel fulfilled and grateful for what I have.",
        "Life is good, and I feel settled."
    ],
    "embarrassment": [
        "I feel so embarrassed about that incident.",
        "I can't believe I said that; it was so awkward.",
        "I'm feeling self-conscious and exposed.",
        "That was a really awkward moment for me.",
        "I wish I could disappear; I'm so embarrassed."
    ],
    "trust": [
        "I feel secure in my relationships.",
        "There's a strong sense of trust between us.",
        "I have faith in those I love.",
        "I feel confident that things will work out.",
        "Trusting others comes easily to me."
    ],
    "relief": [
        "I feel relieved that it's finally over.",
        "There's a weight lifted off my shoulders.",
        "I can finally breathe again; I'm so relieved.",
        "I’m grateful for this sense of calm.",
        "Relief washes over me like a wave."
    ],
    "anticipation": [
        "I feel excited about what's coming next.",
        "I'm eagerly looking forward to the future.",
        "There's a sense of thrill in the air.",
        "I can’t wait to see what happens.",
        "Anticipation fills me with energy."
    ],
    "nostalgia": [
        "I'm feeling nostalgic about the good old days.",
        "There's a bittersweet longing for the past.",
        "I cherish those memories; they warm my heart.",
        "Nostalgia brings both joy and sadness.",
        "I often reflect on those times with fondness."
    ],
    "excitement": [
        "I feel so excited; my heart is racing!",
        "Everything is thrilling and full of potential.",
        "I can't contain my enthusiasm!",
        "This is such an exhilarating moment.",
        "I'm ready for the adventure ahead!"
    ],
    "calm": [
        "I feel calm and centered.",
        "There's a peacefulness within me.",
        "I’m at ease with everything around me.",
        "Calmness envelops me like a gentle wave.",
        "I feel relaxed and balanced."
    ],
    "assertiveness": [
        "I feel confident in expressing my needs.",
        "There's a sense of strength in my voice.",
        "I'm assertive and stand my ground.",
        "I know my worth and won't settle for less.",
        "Being assertive feels empowering."
    ],
    "vulnerability": [
        "I feel exposed and vulnerable right now.",
        "There's a strength in being open and honest.",
        "Being vulnerable is scary but also liberating.",
        "I’m allowing myself to feel deeply.",
        "Vulnerability can lead to true connection."
    ],
    "courage": [
        "I feel brave enough to face my fears.",
        "There's a strength in my heart that pushes me forward.",
        "I am courageous in pursuing my dreams.",
        "I face challenges with determination.",
        "Courage fuels my journey ahead."
    ],
    "doubt": [
        "I'm feeling doubtful about my decisions.",
        "There's uncertainty nagging at me.",
        "I question my choices and abilities.",
        "Doubt clouds my mind and makes me anxious.",
        "I'm struggling with insecurity right now."
    ],
    "indifference": []
}
# Coping mechanisms based on detected emotions
coping_mechanisms = {
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


def detect_emotion(user_input):
    user_input = user_input.lower()
    for emotion, keywords in emotion_keywords.items():
        if any(keyword in user_input for keyword in keywords):
            return emotion
    return "neutral"

def generate_response(user_input):
    prompt = PromptTemplate(
        input_variables=["context", "user_input"],
        template="{context} The user says: {user_input}. Based on this, respond empathetically."
    )

    detected_emotion = detect_emotion(user_input)
    context = initial_prompt + f" The user is feeling {detected_emotion}."

    response = llm(prompt.format(context=context, user_input=user_input))

    # Check if the user is asking for help with coping mechanisms
    if "help" in user_input.lower() or "coping" in user_input.lower() or "plan" in user_input.lower():
        coping = coping_mechanisms.get(detected_emotion, ["I don't have specific coping strategies for that emotion."])
        response += f"\n\nHere are some coping mechanisms you might consider:\n" + "\n".join(coping)

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

def main():
    print("You can start talking to Dr. Andrea (type 'exit' to end):")
    greeting = "Hello! I'm Dr. Andrea. I'm here to listen and support you. How are you feeling today?"
    generate_audio(greeting)

    while True:
        user_input = listen()
        if user_input.lower() == "exit":
            farewell_message = "Ending the conversation. Take care!"
            generate_audio(farewell_message)
            print(farewell_message)
            break

        response = generate_response(user_input)
        generate_audio(response)

if __name__ == "__main__":
    main()





""" 


import os
import assemblyai as aai
from elevenlabs.client import ElevenLabs
from elevenlabs import play  
from openai import OpenAI
from dotenv import load_dotenv
import speech_recognition as sr
import pyttsx3


load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY") 
if not openai_api_key:
    raise ValueError("OpenAI API key not found. Please set it in the .env file.")

elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")
if not elevenlabs_api_key:
    raise ValueError("ElevenLabs API key not found. Please set it in the .env file.")


client = ElevenLabs(api_key=elevenlabs_api_key)

engine = pyttsx3.init()
engine.setProperty('rate', 150)


recognizer = sr.Recognizer()


emotion_responses = {
    "anxiety": "It's completely understandable to feel anxious. Talking about your feelings can help. What’s been on your mind?",
    "depression": "I'm truly sorry to hear that you're feeling this way. It's really important to connect with someone who can help.",
    "sadness": "Feeling sad is a part of life. What activities usually help lift your spirits?",
    "loneliness": "It's okay to feel lonely sometimes. What are some things that help you feel connected to others?",
    "neutral": "Thank you for sharing. How can I assist you further?"
}

emotion_keywords = {
    "anxiety": ["anxious", "overwhelmed", "nervous", "worry", "panic", "fear", "stressed"],
    "depression": ["sad", "depressed", "down", "hopeless", "fatigue", "loss of interest"],
    "sadness": ["sad", "tears", "cry", "unhappy"],
    "loneliness": ["lonely", "isolated", "alone"],
    "neutral": []
}
transcriber = None
full_transcript = [
    {"role": "system", "content": "You are a mental health wellness assistant. Be empathetic and supportive."},
]

initial_prompt = (
    "Your name is Dr. Andrea. You are a mental health professional specializing in wellness and emotional support. "
    "You have extensive experience helping individuals navigate their feelings and challenges. "
    "Your task is to listen with empathy and provide a safe space for individuals to express themselves. "
    "You should ask clarifying questions before offering advice to ensure you understand their situation fully. "
    "Maintain a supportive and caring tone throughout the conversation."
)

def start_transcription():
    global transcriber
    transcriber = aai.RealtimeTranscriber(
        sample_rate=16000,
        on_data=on_data,
        on_error=on_error,
        on_open=on_open,
        on_close=on_close,
        end_utterance_silence_threshold=1000
    )
    transcriber.connect()
    microphone_stream = aai.extras.MicrophoneStream(sample_rate=16000)
    transcriber.stream(microphone_stream)

def stop_transcription():
    global transcriber
    if transcriber:
        transcriber.close()
        transcriber = None

def on_open(session_opened: aai.RealtimeSessionOpened):
    print("Session ID:", session_opened.session_id)

def on_data(transcript: aai.RealtimeTranscript):
    if not transcript.text:
        return

    if isinstance(transcript, aai.RealtimeFinalTranscript):
        generate_ai_response(transcript)
    else:
        print(transcript.text, end="\r")

def on_error(error: aai.RealtimeError):
    print("An error occurred:", error)

def on_close():
    return

def generate_ai_response(transcript):
    stop_transcription()

    global full_transcript
    full_transcript.append({"role": "user", "content": transcript.text})
    print(f"\nUser: {transcript.text}", end="\r\n")

    detected_emotion = detect_emotion(transcript.text)
    response = generate_response(detected_emotion)

    ai_response = response

    generate_audio(ai_response)

    start_transcription()
    print(f"\nReal-time transcription: ", end="\r\n")

def detect_emotion(user_input):
    user_input = user_input.lower()
    for emotion, keywords in emotion_keywords.items():
        if any(keyword in user_input for keyword in keywords):
            return emotion
    return "neutral"

def generate_response(detected_emotion):
    return emotion_responses.get(detected_emotion, emotion_responses["neutral"])

def generate_audio(text):
    global full_transcript
    full_transcript.append({"role": "assistant", "content": text})
    print(f"\nDr. Andrea: {text}")
    audio = client.generate(
        text=text,
        voice="WljsxseqtJlL72K5Zh8j",  
        model="eleven_multilingual_v2" 
    )

    play(audio)
greeting = "Hello! I'm Dr. Andrea. I'm here to listen and support you. How are you feeling today?"
generate_audio(greeting)
start_transcription()



 """