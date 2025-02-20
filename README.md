# [PremCaster](https://premcaster.onrender.com/)

> **PremCaster** is a comprehensive web application that empowers users to predict Premier League outcomes using live data from current standings and fixtures. It offers an interactive experience where you can simulate match predictions, view dynamic updates to the league table, and compare your forecasts with real results, Establishing it as a valuable tool for sports analysts and fans.

---

## ✨ Key Features:
- **Real-time Standings:** Automatically fetches current Premier League table data via API.
- **Upcoming Fixtures:** Predict match outcomes with an intuitive interface.
- **Dynamic Updates:** Watch the league standings adjust as you submit your predictions.
- **User-Friendly Interface:** Clean design for easy navigation and interaction.

---

## 🛠 Technical Overview:
- **Backend Framework:** Flask (Python) handles API requests and server logic.
- **Frontend:** Built using HTML, CSS, and JavaScript for a responsive experience.
- **API:** Utilizes an external API ([http://api.football-data.org/v4](http://api.football-data.org/v4)) for live data.
- **Data Processing:** Inputs predictions and recalculates standings in real time.
- **Hosting:** Deployed on Render for continuous availability.
- **Database:** Uses simple, file-based or in-memory storage for tracking predictions.

---

## 🚀 Getting Started

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/LethaXl/PremCaster.git
   ```
2. Navigate into the repository directory:
   ```bash
   cd PremCaster
   ```
3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Replace the default API key with your own:
   - Edit your configuration file (e.g., `.env` or `config.py`) and update the API key with the one you obtained from [http://api.football-data.org/v4](http://api.football-data.org/v4).

### 2. Run the App Locally

```bash
python app.py
```

---

## ⚽ Usage

- Click on **"Forecast"** to begin predicting match outcomes.
- Each match starts as a **0-0 draw** by default.
- Select **"Home"** or **"Away"** to register a **3-0 win** for the respective team.
- Choose **"Custom Score"** to manually enter a specific scoreline.
- Once selections are made, click **"Submit Predictions"** to update the table.
- The simulation recalculates standings **week by week**. You can also view the last week's changes by clicking **"View Standings"**.
- Continue through matchday 38 to view how your forecasts shape the final table.

---

## 🌐 Deployment

PremCaster is deployed on Render. Access the live web app [here](https://premcaster.onrender.com/).

