# 🚀 Content Engine Pro

**Content Engine Pro** is an enhanced multimodal AI-powered content generation application built with **Streamlit**. It transforms a simple product brief into a complete marketing campaign and improves the generated content using AI-powered quality checks, voiceover generation, and multi-channel adaptation.

## ✨ Features

* 📝 AI-generated Campaign Tagline
* 📖 200-word Blog Introduction
* 📱 Social Media Posts

  * Twitter/X
  * Instagram
  * LinkedIn
* 🎨 AI-generated Hero Image
* 🎬 AI-generated Promotional Video
* 🎙️ AI-generated Voiceover (MP3)
* ✅ AI Self-Critique with Automatic Regeneration
* 🔄 Multi-Channel Content Adaptation

  * B2B LinkedIn
  * Gen-Z TikTok
  * Parents Facebook
* ⚡ One-click generation from a single product brief

---

## 🏗️ Tech Stack

* **Frontend:** Streamlit
* **Language:** Python 3.11+
* **Framework:** Streamlit
* **LLM Provider:** OpenRouter API
* **Image Generation:** OpenAI GPT Image API
* **Video Generation:** Alibaba Wan 2.6 Model
* **Text-to-Speech:** OpenAI TTS
* **Environment Management:** python-dotenv

---

## 📂 Project Structure

```text
content_engine_pro/
│
├── app.py
├── text_gen.py
├── image_gen.py
├── video_gen.py
├── voiceover.py
├── critic.py
├── adapter.py
├── config.py
├── utils.py
├── requirements.txt
├── .env.example
└── README.md
```

---

## ⚙️ Prerequisites

* Python 3.11 or later
* OpenRouter API Key
* OpenAI API Key

---

## 🔑 Environment Variables

Create a `.env` file in the project root.

```env
OPENROUTER_API_KEY=your_openrouter_api_key
OPENAI_API_KEY=your_openai_api_key
```

---

## 📦 Installation

Clone the repository.

```bash
git clone <your-repository-url>
cd content_engine_pro
```

Create a virtual environment.

```bash
python -m venv .venv
```

Activate the virtual environment.

### Windows

```bash
.venv\Scripts\activate
```

### macOS/Linux

```bash
source .venv/bin/activate
```

Install the required dependencies.

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

---

## 🚀 How It Works

1. Enter the **Product Name**.
2. Enter the **Target Audience**.
3. Select the **Brand Tone**.
4. Click **Generate Campaign**.
5. The application:

   * Generates a Campaign Tagline
   * Generates a Blog Introduction
   * Generates Social Media Posts
   * Creates a Hero Image
   * Creates a Promotional Video
   * Reviews all text assets using an AI Self-Critique
   * Regenerates weak outputs automatically (up to 2 retries)
   * Generates a Voiceover from the blog content
   * Allows content adaptation for different channels

---

## 🤖 AI Models Used

| Task                 | Model / Service      |
| -------------------- | -------------------- |
| Text Generation      | OpenRouter LLM       |
| Image Generation     | OpenAI GPT Image API |
| Video Generation     | Alibaba Wan 2.6      |
| Voiceover Generation | OpenAI TTS           |

---

## 📸 Outputs

The application generates a complete AI-powered marketing campaign consisting of:

* Campaign Tagline
* Blog Introduction
* Social Media Posts
* Hero Image
* Promotional Video
* AI Self-Critique Report
* Voiceover Audio (MP3)
* Multi-Channel Adapted Content
