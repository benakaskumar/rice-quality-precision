# Rice Quality Precision
Flask + MySQL web app: rice photo grading, safety verdict, alerts, world rice library, blend optimiser.

## Run (MySQL)
1. Install MySQL Server and make sure it is running.
2. Open `config.py` and set `DB_USER` and `DB_PASS` to your MySQL login (default: root, empty password).
3. Windows: double-click `run.bat`   Linux/Mac: `sh run.sh`
4. Open http://127.0.0.1:5000, click "Create an account", then log in.
The `rice_quality` database and tables are created and filled automatically on first start.
Demo photos are in `static/samples/`. Unit tests: `pytest tests`.

## Files
- `config.py` settings; `db.py` + `schema.sql` MySQL access and seeding (`data/*.csv`)
- `ds.py` linked list, stack, queue, BST (grade classifier), graph + BFS (supply-chain trace)
- `algos.py` quick sort, binary search, greedy / DP / backtracking blends (Tools tab); `vision.py` image analysis
- `app.py` Flask routes with login; `templates/` + `static/` front end

Every analysed photo becomes a batch (RQP-00001...). Origin is a shortlist from grain shape and colour; click "This is my rice" to confirm.
Photo results are an image-based estimate, not a lab test.
The analysis labels rice quality as high (score 85+), medium (70-84.9), or low (below 70), alongside the grade and food-safety verdict.
