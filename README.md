# 🤖 Task 5 — Rule-Based Chatbot (PyBot)

An intelligent, lightweight, and deterministic conversational virtual assistant built using pure Python and Streamlit.

---

## 📌 Project Overview

This project satisfies the requirements for **Task 5 (Rule-Based Chatbot)**:
- **Core Technology**: Pure Python (`re`, `datetime`, `random`) — zero heavy machine learning dependencies.
- **Decision Engine**: Dictionary-based rule matching with regular expression word-boundary detection.
- **User Interface**: Streamlit web chat application featuring real-time message streaming, intent transparency badges, quick suggestion chips, and conversation analytics.
- **Execution Architecture**: Dedicated isolated application window launcher with automated clean session termination.

---

## 🎯 What It Does & How It Works

Unlike machine learning or LLM chatbots that require massive weights and probabilistic sampling, a **rule-based chatbot** maps inputs deterministically to predefined intents:

```
[User Input] 
      │
      ▼
[Text Preprocessor] ──> Lowercase, normalize contractions, strip punctuation, clean whitespace
      │
      ▼
[Intent Engine]     ──> Match multi-word phrases & regex word-boundary patterns in RULES dictionary
      │
      ├─── Match Found? ──────> Extract intent & select random response template
      │                          (or invoke dynamic handler for Time / Date / Math)
      │
      └─── No Match Found? ───> Return helpful fallback with guidance ('unknown' intent)
```

### 🧠 Pattern Matching Highlights
1. **Contraction Normalization**: Converts `"what's"` to `"whats"`, `"today's"` to `"todays"`, ensuring conversational contractions match rules reliably.
2. **Regex Word Boundaries (`\b...\b`)**: Prevents substring false positives (e.g., the word `"this"` or `"white"` will never falsely trigger `"hi"`).
3. **Dynamic Computation**:
   - `time`: Generates live system timestamps (`datetime.now()`).
   - `date`: Generates live calendar dates.
   - `math`: Evaluates arithmetic queries (`+`, `-`, `*`, `/`) with division-by-zero protection.

---

## 📖 Supported Intents & Capabilities

| Intent | Sample User Queries | Behavior / Type |
|---|---|---|
| `greeting` | *"Hello"*, *"Hi there"*, *"Good morning"* | Friendly conversational greeting (Static) |
| `farewell` | *"Goodbye"*, *"See you later"*, *"Bye"* | Polite departure response (Static) |
| `name` | *"Who are you?"*, *"What is your name?"* | Bot self-introduction (Static) |
| `creator` | *"Who created you?"*, *"Who is your developer?"* | Project & internship credits (Static) |
| `mood` | *"How are you?"*, *"How's it going?"* | Upbeat status replies (Static) |
| `joke` | *"Tell me a joke"*, *"Make me laugh"* | Clean programming & CS jokes (Static) |
| `quote` | *"Inspire me"*, *"Daily quote"* | Software engineering wisdom (Static) |
| `help` | *"Help"*, *"What can you do?"*, *"Commands"* | Full listing of capabilities (Static) |
| `weather_faq` | *"How's the weather?"*, *"Is it raining?"* | Witty offline FAQ advice (Static) |
| `thanks` | *"Thank you"*, *"Appreciate it"*, *"Thx"* | Polite gratitude response (Static) |
| `time` | *"What time is it?"*, *"Tell me the time"* | **Dynamic**: Real-time clock output |
| `date` | *"What is today's date?"*, *"What day is it?"* | **Dynamic**: Real-time calendar output |
| `math` | *"What is 45 * 12"*, *"Calculate 100 / 5"* | **Dynamic**: Safe arithmetic solver |
| `unknown` | *Any unmapped query* | Fallback advice with command suggestions |

---

## 📁 Project Structure

```
rule based chatbot/
│
├── chatbot.py            # Core rule-based matching engine & dynamic handlers
├── app.py                # Streamlit chat interface with suggestion chips & sidebar
├── launch.py             # Dedicated window launcher & process supervisor
├── test_chatbot.py       # Comprehensive unit test suite (9 test cases)
├── requirements.txt      # Python dependencies (Streamlit)
├── run.bat               # One-click Windows launcher
├── run.sh                # One-click Linux / macOS launcher
├── .gitignore            # Git exclusion rules
├── .streamlit/
│   └── config.toml       # Streamlit theme & headless server configuration
└── README.md             # Complete documentation
```

---

## 🚀 Quickstart & Installation

### Option 1: One-Click Launcher (Recommended)
- **Windows**: Double-click [`run.bat`](file:///c:/Users/mymai/OneDrive/Desktop/projects/rule%20based%20chatbot/run.bat)
- **macOS / Linux**: Run `bash run.sh` in your terminal

The script automatically verifies dependencies, starts the background Streamlit server, and launches the app in its own dedicated, distraction-free window.

### Option 2: Manual Terminal Execution
1. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
2. Launch via Python supervisor:
   ```bash
   python launch.py
   ```
   Or directly with Streamlit:
   ```bash
   streamlit run app.py
   ```

---

## 🧪 Automated Testing

To run the automated unit test suite verifying intent detection, word boundaries, math solving, and normalization:

```bash
python test_chatbot.py
```

All tests run in `< 0.02s` with zero external dependencies.

---

## 🛑 Clean Session Shutdown
Clicking the **🛑 Stop Session** button in the sidebar will:
1. Terminate the local Streamlit server cleanly.
2. Automatically close the dedicated application window without affecting your other browser tabs.
