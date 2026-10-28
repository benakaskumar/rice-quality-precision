# Rice Quality Precision 🌾

A comprehensive Flask + MySQL web application for automated rice grain photo grading, safety evaluation, origin identification, supply chain tracing, and blend optimization.

---

## 📌 Overview

**Rice Quality Precision** leverages computer vision and core data structures/algorithms to analyze rice grain imagery and manage agricultural batch data. It provides:
- **Grain Photo Analysis**: Image segmentation & contour extraction to calculate grain count, average dimensions, aspect ratio, broken percentage, chalkiness, and discoloration.
- **Quality Grading & Safety Verdict**: Binary Search Tree (BST) grade classifier and defect thresholds delivering instant quality scores (High 85+, Medium 70–84.9, Low <70) and safety verdicts.
- **Origin Shortlisting**: Predicts potential rice variety and region based on physical grain dimensions and color profile.
- **Supply Chain Traceability**: Graph + Breadth-First Search (BFS) representation tracing grain origins, processing mills, and distribution batches.
- **Blend Optimizer**: Algorithmic tools (Greedy, Dynamic Programming, and Backtracking) to calculate optimal rice grain mixing proportions based on cost and target quality.
- **World Rice Library**: Seeded database cataloging global rice varieties, baseline parameters, and market values.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- MySQL Server (running locally or remotely)

### Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/benakaskumar/rice-quality-precision.git
   cd rice-quality-precision
   ```

2. **Configure Database Credentials:**
   Edit `rice_quality_precision/config.py` (or set environment variables):
   ```python
   DB_HOST = "localhost"
   DB_PORT = 3306
   DB_USER = "root"
   DB_PASS = "your_mysql_password"
   DB_NAME = "rice_quality"
   ```

3. **Run the Application:**
   - **Windows:** Double-click or run `run.bat`
   - **Linux / macOS:** Run `cd rice_quality_precision && sh run.sh`

   The database schema and initial rice datasets (`data/*.csv`) are automatically initialized on the first launch.

4. **Access the App:**
   Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser, register an account, and start analyzing.

---

## 🧪 Testing

To run the unit test suite:
```bash
pytest rice_quality_precision/tests
```

---

## 📁 Repository Structure

```plaintext
rice-quality-precision/
├── run.bat                                  # Root launcher for Windows
├── rice_quality_precision/
│   ├── app.py                              # Flask application & API routes
│   ├── config.py                           # App & database configuration
│   ├── db.py                               # MySQL connection & migration helpers
│   ├── schema.sql                          # Database schema
│   ├── ds.py                               # Custom Data Structures (Linked list, BST, Graph)
│   ├── algos.py                            # Algorithms (QuickSort, Binary Search, DP blend optimizer)
│   ├── vision.py                           # Computer vision & image processing engine
│   ├── rice_data.py                        # Dataset parsers & seed routines
│   ├── requirements.txt                    # Python dependencies
│   ├── data/                               # CSV datasets (samples, varieties, supply-chain edges)
│   ├── static/                             # Frontend assets (CSS, JS, sample images)
│   ├── templates/                          # HTML templates (Jinja2)
│   └── tests/                              # Unit & integration tests
└── README.md
```

---

## ⚠️ Disclaimer
Photo analysis results are computational estimates based on 2D image analysis and computer vision algorithms, and are not a replacement for certified laboratory biochemical tests.
