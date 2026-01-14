# UIDAI AIGAP Ultimate – Governance Intelligence Platform

> **AI‑powered governance, risk intelligence & decision support for Aadhaar operations** 🇮🇳

![UIDAI](https://upload.wikimedia.org/wikipedia/en/c/cf/Aadhaar_Logo.svg)

---

## 🛠️ Installation & Setup

### 🔧 Prerequisites

* **Python 3.9 or higher**
* **pip** package manager
* Git (optional but recommended)

---

### 📥 Step 1: Clone the Repository

```bash
git clone https://github.com/KINGSTABLE/UIDAI.git
cd UIDAI
```

---

### ⚙️ Step 2: Run the Setup Script

The **`main.py`** file acts as a **self‑contained installer**. It automatically:

* Creates the full project directory structure
* Generates all required source files
* Prepares the environment for execution

```bash
python main.py
```

✅ This will create a new folder:

```
UIDAI_AIGAP_ULTIMATE/
```

containing all modules, dashboards, and configuration files.

---

### 📦 Step 3: Install Dependencies

Navigate into the generated project directory and install dependencies:

```bash
cd UIDAI_AIGAP_ULTIMATE
pip install -r requirements.txt
```

---

## 💻 Usage

### 1️⃣ Generate Synthetic Governance Data

Before launching the dashboard, generate the Aadhaar governance dataset:

```bash
python data_generator.py
```

📊 This creates:

* `aadhaar_ultimate_data.csv`
* `aadhaar_ultimate_data.parquet`

Each file contains **50,000+ synthetic records** enriched with:

* Risk & compliance scores
* Fraud indicators
* Processing metrics
* Citizen satisfaction data

---

### 2️⃣ Launch the Governance Dashboard

Start the Streamlit application:

```bash
streamlit run app.py
```

---

### 3️⃣ Access the Interface

* **URL:** [http://localhost:8501](http://localhost:8501)
* **Login:** `admin`
* **Password:** `admin`

🔓 You may also continue using **Guest Mode** with limited functionality.

---

## 📂 Project Structure

```
UIDAI_AIGAP_ULTIMATE/
├── app.py                     # Main Streamlit Dashboard Application
├── data_generator.py          # Synthetic Data Generator with Governance Metrics
├── requirements.txt           # Project Dependencies
├── aadhaar_ultimate_data.csv  # Generated Dataset (CSV)
├── aadhaar_ultimate_data.parquet # Generated Dataset (Parquet)
│
├── modules/                   # Core Intelligence Modules
│   ├── governance_engine.py     # Risk Scoring & AI Recommendations
│   ├── reporting_engine.py      # PDF Report Generation (FPDF)
│   └── visualization_engine.py  # Plotly Charts, Maps & Network Graphs
│
└── reports/                   # Output directory for generated PDF reports
```

---

## 🧠 What This Platform Delivers

* 📊 **Governance Risk Scoring (0–100)**
* 🚨 **Anomaly & Fraud Detection**
* 🌍 **Geospatial Intelligence & Heatmaps**
* 📑 **Executive‑grade PDF Reports**
* 🎯 **AI‑generated Actionable Recommendations**

---

## ⚠️ Disclaimer

This project uses **synthetic data only** and does **NOT** connect to real UIDAI or Aadhaar systems.

It is intended strictly for:

* Research & experimentation
* Governance analytics demos
* AI/ML portfolio & academic use

---

## 👤 Author

**KINGSTABLE**

🔗 GitHub: [https://github.com/KINGSTABLE](https://github.com/KINGSTABLE)

---

## 📜 License

MIT License — free to use for educational and research purposes.

---

🇮🇳 *Built for governance excellence & digital public infrastructure.*
