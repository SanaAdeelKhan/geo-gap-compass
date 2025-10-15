# 🌍 GEO Gap Compass — AI Visibility & Opportunity Tracker

🚀 **“Discover where your brand is missing in AI-generated answers — and how to fix it.”**

---

## 🧠 Overview

**GEO Gap Compass** is an AI-powered visibility analytics dashboard that helps brands understand how often (and where) they are cited by AI assistants such as ChatGPT.

The tool identifies **citation gaps** — topics or prompt categories where your brand should appear but doesn’t — and offers actionable insights.

> In short, it’s *Google Analytics for Generative AI* — showing not just who mentions you, but who doesn’t and why.

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/54e48cf0-7a00-4ebf-a6bf-1af022263b05" />

---

## 🏁 Hackathon Track

-**Track:** Track#01 Intelligent GEO (Generative Engine Optimization) Insights

-**Category:** AI Search Visibility & SEO Intelligence

-**Goal:** Build an intelligent GEO insights tool using Reimagine.web and AI APIs.

---

## ✨ Key Features

### 🔍 1. Prompt Testing Lab

Input a brand or topic — the system auto-generates multiple prompt variations (e.g., “how-to,” “comparison,” “definition”) and tests them via ChatGPT.

Extracted citations are automatically logged and analyzed.
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/478a2aa7-e4ca-40d4-a818-547d0263748a" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/9da65cc0-cdbb-4c7c-9042-d2722794ba02" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/ec3fc414-df3f-48e5-ba95-75d90e072162" />


### 🔥 2. Citation Gap Heatmap

Visual heatmap showing which prompt types mention your brand and which don’t.

**Color-coded visibility:**

- 🟢 High — Frequently cited
- 🟡 Moderate — Occasionally cited
- 🔴 Low / Missing — Citation gap detected

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/b2c45f11-e1c5-40f9-b062-6fe0a0b34e60" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/a3b45e44-48f6-455c-b353-a0792201b100" />

### 🧩 3. Competitor Benchmarking

Add up to 3 competitors to compare citation frequencies and prompt performance side-by-side.

Identify which prompts trigger your competitors but skip your brand.
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/453b323d-46c2-4ed4-9701-67dcbbe209c9" />
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/ceab8cf9-884e-46bd-afeb-f4b725ada79e" />



### 💡 4. Actionable Insights

AI-generated, plain-language insights:

> “You’re missing citations in comparison and tutorial prompts.”

> “Your competitors appear 40% more often in how-to queries.”
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/2244b819-eed2-4366-b0b0-8a17e6cd398f" />

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/ead0c25f-9d07-401f-abf3-c3a81e17fa58" />

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/9a0679e1-f7ad-4bf8-b5d4-7e2ac8e964a2" />

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/59b87c37-317f-460e-a23b-ee7a37b98b36" />


### ⏱️ 5. (Optional) Time-Series Tracking

Track visibility trends over time (synthetic or real data).

See how citation frequency evolves after content or GEO optimizations.

### 6.Geo-Gap-Compass Analysis By ReimagineWeb:.

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/780b2f52-193a-4d5d-a935-7c9327d787ce" />

---

## 🧰 Tech Stack

| Layer | Technology |

|-------|-------------|

| **Frontend** | Next.js + Tailwind CSS |

| **Backend** | FastAPI (Python) / Express.js (Node.js) |

| **AI APIs** | OpenAI API (GPT-4 / GPT-4o-mini) |

| **SEO/GEO Data** | DuckDuckGo |

| **Database** | SQLite / JSON storage |

| **Visualization** | Recharts (Heatmap, Trend Graphs) |

| **Deployment** | Vercel (frontend) / Render (backend) |

---

## 🧭 System Architecture

```mermaid

flowchart TD

    A[User Input: Brand/Topic] --> B[Prompt Generator]

    B --> C[ChatGPT API Calls]

    C --> D[Extract Cited URLs]

    D --> E[Store Data in DB/JSON]

    E --> F[Gap Analysis Engine]

    F --> G[DuckDuckGo/GPT-4o mini]

    G --> H[Insights Generator]

    H --> I[Dashboard Visualization]

    I --> J[Heatmap + Competitor View]

```

---

## ⚙️ Quick Setup

### 1️⃣ Clone the Repository

```bash

gitclone https://github.com/SanaAdeelKhan/geo-gap-compass.git

cd geo-gap-compass

```

### 2️⃣ Backend Setup

**Python (FastAPI)**

```bash

cd backend

pip install-requirements.txt

backend\.venv\Scripts\python.exe -m uvicorn backend.app:app --reload --port 8000

```

**or Node.js (Express)**

```bash

cdbackend

npminstall

npmstart

```

### 3️⃣ Frontend Setup

```bash

cdfrontend

npminstall

npmrundev

```

### 4️⃣ Environment Variables

Create a `.env` file in the backend directory:

```

OPENAI_API_KEY=your_openai_api_key


```

### 5️⃣ Run the App

- Backend → http://localhost:8000
- Frontend → http://localhost:3000

---

## 📊 Example Output

### 🔸 Citation Gap Heatmap

| Prompt Type | Your Brand | Competitor A | Competitor B |

|--------------|-------------|---------------|---------------|

| How-To | 🟢 | 🟢 | 🟡 |

| Comparison | 🔴 | 🟢 | 🟢 |

| Informational | 🟡 | 🟢 | 🔴 |

| Problem Solving | 🔴 | 🟡 | 🟢 |

### 🔸 Insight Sample

🚨 *Your brand is underrepresented in “comparison” and “problem-solving” queries. Optimize content around these categories to improve AI visibility.*

---

## 🧩 Challenges Solved

- 🌐 Lack of visibility tracking across AI-generated answers
- 🧭 No existing metric for brand presence in Generative AI responses
- 📊 Difficulty comparing content GEO performance against competitors
- 💡 Turning unstructured AI outputs into actionable brand intelligence

---

## 🧠 Future Enhancements

- Multi-AI support (Claude, Perplexity, Gemini)
- Real-time citation monitoring with historical trends
- Automated content gap recommendations
- Team dashboard with exportable PDF reports

---

## 🎥 Demo Script (3-Minute)

1. Input brand name: “OpenAI”
2. Run auto-prompt tests → see citation results
3. Show heatmap: red zones = missing visibility
4. Add competitor → show comparison view
5. Show actionable insights panel
6. End with vision:

   > “GEO Gap Compass — helping brands win visibility in the age of AI search.”
   >

---

## 🏆 Why It Stands Out

✅ Tackles a brand-new problem — visibility in AI answers

✅ Combines prompt intelligence + GEO analytics

✅ Perfectly aligned with Reimagine.web integration goals

✅ Balanced blend of innovation, technical skill, and real-world value

---

## 👥 Team

| Team Members   | GitHub                            | LinkedIN                                              |
| -------------- | --------------------------------- | ----------------------------------------------------- |
| Sana Adeel     | https://github.com/SanaAdeelKhan  | https://www.linkedin.com/in/engr-sana-adeel-a1860ab1/ |
| Ali Jafar      | https://github.com/alijafarkamal  | https://www.linkedin.com/in/-ali-jafar/               |
| Maria Nadeem   | https://github.com/marianadeem755 | https://www.linkedin.com/in/maria-nadeem-4994122aa/   |
| Mehak Iftikhar | https://github.com/mehakiftikhar  | https://www.linkedin.com/in/mehak-iftikhar/           |

---

## 🧾 License

MIT License © 2025  Team Green





