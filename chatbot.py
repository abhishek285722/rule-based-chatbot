"""
chatbot.py - Rule-Based Chatbot Engine
Task 5: Rule-Based Chatbot Implementation

This module contains:
1. Text preprocessing and normalization (case folding, punctuation stripping).
2. Intent definition dictionary with keyword patterns and response templates.
3. Multi-word phrase & regex word-boundary matching logic.
4. Dynamic handlers (real-time clock, calendar, arithmetic evaluation).
5. Fallback mechanisms for out-of-domain queries.
"""

import re
import random
import datetime


def preprocess_text(text: str) -> str:
    """
    Cleans and normalizes user input for pattern matching:
    1. Converts text to lowercase.
    2. Strips apostrophes (so "today's" -> "todays", "what's" -> "whats").
    3. Strips punctuation (keeping alphanumeric characters, basic math symbols, and spaces).
    4. Trims and normalizes multiple whitespace characters into single spaces.
    """
    if not text or not isinstance(text, str):
        return ""
    
    # Convert to lowercase
    cleaned = text.lower().strip()
    
    # Remove apostrophes/single quotes first to normalize contractions
    cleaned = re.sub(r"['`’]", "", cleaned)
    
    # Replace punctuation characters except math operators (+, -, *, /) with spaces
    cleaned = re.sub(r"[^\w\s\+\-\*\/]", " ", cleaned)
    
    # Normalize multiple whitespace characters
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


def _get_current_time() -> str:
    """Returns dynamic current time string."""
    now = datetime.datetime.now()
    return f"🕒 The current time is **{now.strftime('%I:%M:%S %p')}** (Local Time)."


def _get_current_date() -> str:
    """Returns dynamic current date string."""
    now = datetime.datetime.now()
    return f"📅 Today is **{now.strftime('%A, %B %d, %Y')}**."


def _try_simple_math(cleaned_text: str):
    """
    Attempts to evaluate simple arithmetic expressions like '5 + 7', '12 * 4', '100 / 2', '20 - 8'.
    Returns formatted result or None if not an arithmetic query.
    """
    math_pattern = r"(?:what is|calculate|solve)?\s*(\d+(?:\.\d+)?)\s*([\+\-\*\/])\s*(\d+(?:\.\d+)?)"
    match = re.search(math_pattern, cleaned_text)
    if match:
        num1 = float(match.group(1))
        op = match.group(2)
        num2 = float(match.group(3))
        
        try:
            if op == "+":
                res = num1 + num2
            elif op == "-":
                res = num1 - num2
            elif op == "*":
                res = num1 * num2
            elif op == "/":
                if num2 == 0:
                    return "⚠️ Division by zero is undefined! Even bots cannot divide by 0. 🤖"
                res = num1 / num2
            else:
                return None
            
            # Format nicely as int if whole number
            formatted_res = int(res) if res.is_integer() else round(res, 4)
            return f"🔢 **Calculation Result**: `{num1:g} {op} {num2:g} = {formatted_res}`"
        except Exception:
            return None
    return None


# Dictionary-based Intent Knowledge Base
RULES = {
    "math": {
        "patterns": [
            "calculate", "solve", "math", "what is", "plus", "minus", "divided by", "times"
        ],
        "responses": [],  # Handled dynamically
    },
    "time": {
        "patterns": [
            "what time", "current time", "time now", "tell me the time", 
            "whats the time", "what is the time", "clock"
        ],
        "responses": [],  # Handled dynamically
    },
    "date": {
        "patterns": [
            "what date", "today's date", "todays date", "current date", 
            "what day is today", "what is the date", "tell me the date", "what day is it"
        ],
        "responses": [],  # Handled dynamically
    },
    "name": {
        "patterns": [
            "your name", "who are you", "what are you", "what is your name", 
            "what do i call you", "what should i call you", "introduce yourself"
        ],
        "responses": [
            "🤖 I am **PyBot**, an intelligent rule-based chatbot designed with Python!",
            "👋 My name is **PyBot**! I'm a lightweight, rule-driven virtual assistant.",
            "You can call me **PyBot**! I use pattern matching and dictionary rules to converse with you."
        ],
    },
    "creator": {
        "patterns": [
            "who made you", "who built you", "who created you", "who programmed you", 
            "who is your developer", "who designed you", "who is your creator"
        ],
        "responses": [
            "👨‍💻 I was developed as part of **Task 5 (Rule-Based Chatbot)** using pure Python and Streamlit!",
            "🛠️ I was built by an AI & Python developer applying rule-based natural language processing techniques.",
            "💻 A developer created me to demonstrate deterministic keyword pattern matching and automated responses without heavy ML models!"
        ],
    },
    "joke": {
        "patterns": [
            "joke", "tell me a joke", "make me laugh", "say a joke", 
            "funny", "something funny", "another joke"
        ],
        "responses": [
            "😂 **Why do programmers prefer dark mode?**\nBecause light attracts bugs! 🐛",
            "🐍 **Why did the Python developer wear glasses?**\nBecause they couldn't C#! 👓",
            "💻 There are **10 types of people** in the world: those who understand binary, and those who don't.",
            "⚙️ **A SQL query walks into a bar**, walks up to two tables and asks: *'Can I join you?'* 🍻",
            "☕ **How do programmers take their coffee?**\n`try: coffee.drink() except: panic()` ☕",
            "🚀 **There's no place like `127.0.0.1`!** 🏠"
        ],
    },
    "quote": {
        "patterns": [
            "quote", "inspire me", "motivate me", "motivation", 
            "inspiration", "daily quote", "inspirational quote"
        ],
        "responses": [
            "✨ *'Simplicity is prerequisite for reliability.'* — **Edsger W. Dijkstra**",
            "💡 *'First, solve the problem. Then, write the code.'* — **John Johnson**",
            "🚀 *'Any fool can write code that a computer can understand. Good programmers write code that humans can understand.'* — **Martin Fowler**",
            "🌟 *'Code is like humor. When you have to explain it, it’s bad.'* — **Cory House**",
            "🎯 *'The best error message is the one that never shows up.'* — **Thomas Fuchs**"
        ],
    },
    "mood": {
        "patterns": [
            "how are you", "how do you feel", "how are things", "hows it going", 
            "how is it going", "what's good", "whats good", "are you okay", "how is your day"
        ],
        "responses": [
            "😊 I'm functioning with 100% CPU efficiency! How are you doing today?",
            "🌟 Doing fantastic! Ready to chat, share jokes, or help you with your questions. How can I assist you?",
            "⚡ All systems operational and running smoothly! How has your day been?"
        ],
    },
    "weather_faq": {
        "patterns": [
            "weather", "is it raining", "temperature outside", "forecast", "sunny today", "how is the weather"
        ],
        "responses": [
            "☀️ I don't have real-time satellite sensors, but looking outside your window or checking your local weather app is always the safest bet!",
            "🌧️ As a Python bot running on your local machine, the only climate I monitor is my CPU temperature! Check your local weather provider for current forecasts."
        ],
    },
    "help": {
        "patterns": [
            "help", "what can you do", "commands", "features", "capabilities", 
            "menu", "options", "what do you know", "instructions"
        ],
        "responses": [
            """💡 **Here is what I can do:**
- **Greetings & Goodbyes**: Say *"Hello"*, *"Good morning"*, or *"Bye"*.
- **Introduce Myself**: Ask *"Who are you?"* or *"Who created you?"*.
- **Check Status**: Ask *"How are you?"* or *"How are things?"*.
- **Real-Time Clock & Date**: Ask *"What time is it?"* or *"What is today's date?"*.
- **Humor & Motivation**: Type *"Tell me a joke"* or *"Inspire me"*.
- **Quick Math**: Try *"What is 25 * 4?"* or *"Calculate 100 / 5"*.
- **General FAQs**: Ask about *"weather"*, *"thanks"*, or *"help"*.

Feel free to try any of these commands! 🚀"""
        ],
    },
    "thanks": {
        "patterns": [
            "thanks", "thank you", "thx", "appreciate it", "grateful", 
            "much appreciated", "thank u", "ty"
        ],
        "responses": [
            "🙏 You're very welcome! Glad I could help.",
            "😊 Anytime! Let me know if you need anything else.",
            "✨ Happy to be of assistance! Have a wonderful day!"
        ],
    },
    "greeting": {
        "patterns": [
            "hi", "hello", "hey", "whats up", "what's up", "greetings", 
            "good morning", "good afternoon", "good evening", "howdy", "hola", "sup"
        ],
        "responses": [
            "👋 Hello there! How can I help you today?",
            "✨ Hey! Great to hear from you. What's on your mind?",
            "🤖 Hi! I'm PyBot, ready to assist you. Ask me anything or type 'help' for options!"
        ],
    },
    "farewell": {
        "patterns": [
            "bye", "goodbye", "see you", "see ya", "later", "catch you later", 
            "take care", "cya", "farewell", "quit", "exit"
        ],
        "responses": [
            "👋 Goodbye! Have a productive and wonderful day ahead!",
            "✨ Take care! Feel free to return anytime you need assistance.",
            "🚀 See you later! Happy coding!"
        ],
    },
    "unknown": {
        "patterns": [],
        "responses": [
            "🤔 I'm not quite sure I understand that. Type **'help'** to see the list of topics and questions I can answer!",
            "🤖 Hmm, that query is outside my current rule-set. Try asking for a **joke**, **the time**, or type **'help'**.",
            "❓ I didn't catch that. As a rule-based bot, I match specific keywords. Type **'what can you do'** to view supported commands!"
        ],
    },
}


def match_intent(cleaned_input: str) -> str:
    """
    Matches normalized user text against dictionary patterns.
    Uses regex word boundaries for single words to avoid false positive substring matches
    (e.g., 'this' shouldn't match 'hi', 'white' shouldn't match 'hi').
    Multi-word phrases are matched as exact contiguous phrase occurrences.
    """
    if not cleaned_input:
        return "unknown"
    
    # First check if user is asking for math calculation
    if any(op in cleaned_input for op in ["+", "-", "*", "/"]) or "calculate" in cleaned_input or "solve" in cleaned_input:
        math_result = _try_simple_math(cleaned_input)
        if math_result is not None:
            return "math"

    # Evaluate intents in order of specificity
    for intent, data in RULES.items():
        if intent in ["unknown", "math"]:
            continue
            
        patterns = data.get("patterns", [])
        for pattern in patterns:
            # Multi-word phrase: match exact phrase with word boundaries
            if " " in pattern:
                escaped = re.escape(pattern)
                if re.search(rf"\b{escaped}\b", cleaned_input):
                    return intent
            else:
                # Single word: match whole word using \b boundaries
                escaped = re.escape(pattern)
                if re.search(rf"\b{escaped}\b", cleaned_input):
                    return intent

    return "unknown"


def get_response_with_intent(user_input: str) -> tuple[str, str]:
    """
    Processes user input and returns a tuple: (response_text, intent_name).
    """
    cleaned = preprocess_text(user_input)
    if not cleaned:
        return ("Please enter a message so I can respond! 😊", "empty")
    
    intent = match_intent(cleaned)
    
    # Handle dynamic intents
    if intent == "math":
        math_res = _try_simple_math(cleaned)
        if math_res:
            return (math_res, "math")
        # If math format didn't match cleanly, give helpful guide
        return (
            "🔢 You can ask me to solve basic arithmetic! For example: *'what is 15 * 8'* or *'calculate 120 / 4'*.",
            "math"
        )
        
    elif intent == "time":
        return (_get_current_time(), "time")
        
    elif intent == "date":
        return (_get_current_date(), "date")
        
    # Standard static intents
    responses = RULES.get(intent, RULES["unknown"]).get("responses", RULES["unknown"]["responses"])
    return (random.choice(responses), intent)


def get_response(user_input: str) -> str:
    """
    Primary API function as planned: takes user text, returns response string.
    """
    response, _ = get_response_with_intent(user_input)
    return response


def get_supported_intents() -> dict:
    """
    Returns a dictionary of supported intents and their sample trigger phrases for UI display.
    """
    summary = {}
    for intent, data in RULES.items():
        if intent == "unknown":
            continue
        patterns = data.get("patterns", [])
        sample = patterns[:4] if patterns else ["Dynamic arithmetic"]
        summary[intent] = {
            "title": intent.replace("_", " ").title(),
            "samples": sample
        }
    return summary


if __name__ == "__main__":
    print("🤖 PyBot Rule-Based Chatbot CLI Test")
    print("Type 'exit' to quit.\n")
    while True:
        try:
            msg = input("You: ")
            if msg.lower().strip() in ["exit", "quit"]:
                print("PyBot: Goodbye!")
                break
            reply, matched_intent = get_response_with_intent(msg)
            print(f"PyBot [{matched_intent}]: {reply}\n")
        except (KeyboardInterrupt, EOFError):
            print("\nPyBot: Goodbye!")
            break
