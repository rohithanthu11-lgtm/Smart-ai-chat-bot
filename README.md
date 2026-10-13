# Beginner-Friendly Local AI Chatbot

A small chatbot built with Python and Streamlit. It connects to Ollama on your
computer and uses the `qwen2.5:3b` model. A rule-based demo mode is also
available from the sidebar and does not call an AI model.

## Project files

- `app.py` contains the Streamlit interface, chat history, simple demo replies,
  and the local Ollama connection.
- `requirements.txt` lists the Python libraries the app needs.
- `README.md` explains setup, running the app, testing it, and troubleshooting.

## Requirements

- Windows 10 or 11
- Python 3.10 or newer
- Visual Studio Code and its Microsoft Python extension
- [Ollama for Windows](https://ollama.com/download)
- The `qwen2.5:3b` model downloaded in Ollama

## Set up in Windows

Open PowerShell (or the VS Code terminal) and run:

```powershell
# 1. Create and open the project folder
mkdir "$HOME\chatbot-project"
cd "$HOME\chatbot-project"
code .

# 2. Create a virtual environment
py -m venv .venv

# 3. Activate it in PowerShell
.\.venv\Scripts\Activate.ps1

# If PowerShell blocks activation, use this for the current terminal only:
# Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
# Then run the Activate.ps1 command again.

# 4. Install the project dependencies (after saving app.py and requirements.txt)
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# 5. Start the app
python -m streamlit run app.py
```

If you use Command Prompt instead of PowerShell, activate the environment with:

```bat
.venv\Scripts\activate.bat
```

Install [Python](https://www.python.org/downloads/) if `py --version` does not
work. During setup, select **Add Python to PATH**. Install
[Visual Studio Code](https://code.visualstudio.com/) and the **Python**
extension published by Microsoft. Save these project files in the folder you
opened in VS Code.

Streamlit prints a local address when it starts, usually
<http://localhost:8501>. Open that address in your browser.

## Connect to your local Qwen model

The sidebar is configured to use `qwen2.5:3b` at Ollama's standard local
address, `http://localhost:11434`. Confirm that the model is installed:

```powershell
ollama list
```

Your listed model name should include `qwen2.5:3b`. If it is missing, download
it once:

```powershell
ollama pull qwen2.5:3b
```

Keep Ollama running while the app is in use. In the sidebar, choose **Local
Ollama** for AI-generated answers. Choose **Rule-based demo** to try the UI
without using the model. Chat history is held in Streamlit session state for
the current browser session and is sent to the local model as conversational
context.

## How it works

1. Streamlit displays the welcome message and all messages stored in session
   state.
2. Type a message into the chat box at the bottom and press Enter to send it.
3. In **Local Ollama** mode, the app sends the conversation and a short
   assistant instruction to Ollama on your computer. The model's reply is
   displayed and saved in the same session.
4. In **Rule-based demo** mode, a small Python function handles greetings,
   thanks, and a few common questions.
5. **Clear chat** resets the conversation to the welcome message.

## Manual test cases

| Test | Steps | Expected result |
|---|---|---|
| Greeting | Send `Hello` in Rule-based demo mode | A friendly greeting appears |
| General question | Ask a question in Local Ollama mode | Qwen produces a response |
| Empty input | Submit whitespace or leave the chat box empty | Empty text is not added to the conversation |
| Repeated messages | Send `Hello` more than once | Each message and response appears in order |
| Clear history | Send a few messages, then select **Clear chat** | Only the welcome message remains |
| Ollama unavailable | Stop Ollama and send a message in Local Ollama mode | A visible connection error tells you to start Ollama |
| Wrong model name | Enter a model not shown by `ollama list` and send | A visible model error suggests checking the model name |
| Unexpected error | Set an invalid Ollama address and send a message | The failure is logged and a visible error is shown |

Streamlit's chat input does not submit empty messages with Enter, so empty
input is also guarded in the app before a message can be added.

## Common problems

- **`py` or `python` is not recognized:** Install Python and select **Add Python
  to PATH**. Restart the terminal afterward.
- **Activation is disabled in PowerShell:** Run
  `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in that terminal,
  then activate `.venv` again. This only changes the current PowerShell process.
- **`No module named streamlit` or `No module named ollama`:** Activate `.venv`
  and run `python -m pip install -r requirements.txt` again.
- **Cannot connect to Ollama:** Start the Ollama app and retry. The usual local
  API address is `http://localhost:11434`; adjust **Ollama address** in the
  sidebar only if your setup uses a different address.
- **Model not found:** Run `ollama list`, then use the exact displayed model
  name in the sidebar. If necessary, run `ollama pull qwen2.5:3b`.
- **Port 8501 is busy:** Start Streamlit on another port:
  `python -m streamlit run app.py --server.port 8502`.

## Future improvements

- Add other locally installed Ollama models using the model-name setting.
- Add streamed responses for a word-by-word display.
- Store conversations in SQLite if they should persist after a browser session.
- Add conversation titles, export, or search.
- If you later choose a hosted LLM, add its client and keep API keys in
  environment variables or Streamlit secrets; never commit keys to source
  control.
