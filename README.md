# 🤖 Multi-Tool AI Assistant builit by Praveen Kumar

Welcome to the **Multi-Tool AI Assistant**! This is a user-friendly web application built with Python and Streamlit that gives you access to a powerful AI model for various tasks. Whether you want to have a conversation or summarize a long article, this tool is designed to be your helpful AI companion.

*(Feel free to use it anywhere)*

---

## ✨ Key Features

This application is more than just a simple chatbot. It comes packed with features to make it versatile and easy to use:

- **Dual-Tool Functionality**: Seamlessly switch between two useful modes:
  - **AI Chatbot**: Have a natural, free-flowing conversation. The AI remembers the context of your chat to provide relevant and coherent responses.
  - **Text Summarizer**: Paste any long text, like a news article or a report, and get a concise, 3-line summary in seconds.

- **Powered by DeepSeek**: Utilizes the `deepseek/deepseek-r1-0528-qwen3-8b` model via the OpenRouter API, providing high-quality and fast responses for free.

- **Sleek & Simple UI**: Built with Streamlit, the interface is clean, intuitive, and fully interactive, with a convenient sidebar for navigation.

- **Chat History Management**: In Chatbot mode, you can clear the conversation history with a single click to start fresh.

---

## 🛠️ Getting Started: Running the App Locally

Want to run the app on your own machine? Just follow these simple steps.

### Prerequisites

- Python 3.8 or newer installed on your system.
- An API key from [OpenRouter.ai](https://openrouter.ai) (they have a generous free tier to get you started).

### 1. Clone the Repository

```bash
git clone https://github.com/praveenkumar0607/qna-chat-bot.git
cd qna-chat-bot
```
### 2. Add you api key

```base
OPENROUTER_API_KEY="sk-or-YourSecretKeyGoesHere"
```
### 3. Run the Program

```
streamlit run ui.py
```


