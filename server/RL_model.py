import numpy as np
import gymnasium as gym
from gymnasium import spaces
from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
from setiment_analysis import detect_sentiment

# Custom environment for emotion exercise
class EmotionExerciseEnv(gym.Env):
    def __init__(self):
        super(EmotionExerciseEnv, self).__init__()
        self.observation_space = spaces.Box(low=0, high=1, shape=(3,), dtype=np.float32)  # Example observation space
        self.action_space = spaces.Discrete(3)  # Three actions: exercise, song, quote
        self.exercises = ["Jumping Jacks", "Push-ups", "Squats"]
        self.songs = ["Happy Song", "Chill Beats", "Motivational Anthem"]
        self.quotes = ["Keep going!", "You can do it!", "Believe in yourself!"]

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.state = np.random.uniform(low=0, high=1, size=(3,)).astype(np.float32)  # Random initial state
        return self.state, {}

    def step(self, action):
        if action == 0:
            suggestion = np.random.choice(self.exercises)
        elif action == 1:
            suggestion = np.random.choice(self.songs)
        else:
            suggestion = np.random.choice(self.quotes)

        user_feedback = self.get_user_feedback(suggestion)
        reward = self.calculate_reward(user_feedback)

        self.state = np.random.uniform(low=0, high=1, size=(3,)).astype(np.float32)
        done = False
        return self.state, reward, done, False, {}

    def calculate_reward(self, feedback):
        if feedback == "yes":
            return 1.0
        elif feedback == "no":
            return -1.0
        else:
            return 0.0


    def get_user_feedback(self, suggestion):
        feedback = ''
        if suggestion == 'POSITIVE':
            feedback = 'yes'
        elif suggestion == 'NEGATIVE':
            feedback = 'no'
        return feedback
    
    def render(self, mode='human'):
        # Dummy render method
        pass


# Function to interact with the user and update the model
def interact_and_train(model, env, total_timesteps=10000):
    obs, _ = env.reset()
    for _ in range(total_timesteps):
        action, _states = model.predict(obs)
        obs, reward, done, truncated, info = env.step(action)
        model.learn(total_timesteps=100)  # Update the model with the new experience
        if done:
            obs, _ = env.reset()

# Function to load and evaluate the model
def load_and_evaluate_model(model_path, env, num_steps=1000):
    # Load the model
    model = PPO.load(model_path)

    # Evaluate the model
    obs, _ = env.reset()
    for _ in range(num_steps):
        action, _states = model.predict(obs)
        obs, rewards, done, truncated, info = env.step(action)
        env.render()
        if done:
            obs, _ = env.reset()

# # Check the environment
# env = EmotionExerciseEnv()
# check_env(env)

# # Initialize the model
# model = PPO("MlpPolicy", env, verbose=1)
# # Train the model with user interaction
# interact_and_train(model, env, total_timesteps=10000)

# # Save the model
# model.save("ppo_emotion_exercise")
# # Load the model
# model = PPO.load("ppo_emotion_exercise")

# # Evaluate the model
# obs, _ = env.reset()
# for _ in range(1000):
#     action, _states = model.predict(obs)
#     obs, rewards, done, truncated, info = env.step(action)
#     env.render()
#     if done:
#         obs, _ = env.reset()
