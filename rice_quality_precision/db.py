"""MySQL access: schema.sql, seed data (rice library, samples.csv)."""
import csv, os
import mysql.connector
from ds import GRADES

import config
HERE = os.path.dirname(__file__)
CFG = dict(host=config.DB_HOST, port=config.DB_PORT, user=config.DB_USER, password=config.DB_PASS)
DBN = config.DB_NAME

RICE = [  # name, country/region, grain, notes
("Basmati", "India / Pakistan", "long", "Aromatic, grains elongate 2x when cooked; biryani and pulao."),
("Jasmine (Hom Mali)", "Thailand", "long", "Fragrant, soft and slightly sticky; staple of Thai cooking."),
("Jasmine ST25", "Vietnam", "long", "Award-winning aromatic variety from the Mekong Delta."),
("Sona Masuri", "India (Andhra/Karnataka)", "medium", "Lightweight, low-starch; everyday South Indian rice."),
("Ponni", "India (Tamil Nadu)", "medium", "Soft, popular for idli, dosa and daily meals."),
("Matta (Rosematta)", "India (Kerala)", "medium", "Red parboiled rice, earthy flavour, high fibre."),
("Ambemohar", "India (Maharashtra)", "short", "Smells of mango blossom; soft and fragrant."),
("Kalanamak", "India (Uttar Pradesh)", "medium", "Black-husked aromatic heritage rice."),
("Gobindobhog", "India (West Bengal)", "short", "Small aromatic rice used for sweets and festive dishes."),
("Njavara", "India (Kerala)", "short", "Ayurvedic medicinal red rice used in therapies."),
("Miniket", "Bangladesh", "short", "Polished small-grain everyday rice."),
("Samba (Keeri Samba)", "Sri Lanka", "short", "Tiny aromatic grains for festive rice and kiribath."),
("Arborio", "Italy", "short", "High starch, creamy; classic risotto rice."),
("Carnaroli", "Italy", "medium", "Holds shape well; chef's choice for risotto."),
("Bomba", "Spain (Valencia)", "short", "Absorbs liquid well without turning mushy; paella."),
("Koshihikari", "Japan", "short", "Sticky, slightly sweet; sushi and table rice."),
("Calrose", "USA (California)", "medium", "Soft, sticky; common sushi/everyday rice."),
("Carolina Gold", "USA (South Carolina)", "long", "Historic heirloom variety revived by Southern chefs."),
("Texmati", "USA (Texas)", "long", "Basmati-type aromatic grown in the US."),
("Glutinous (Sticky) rice", "Thailand / Laos", "short", "Very sticky when steamed; mango sticky rice, Lao dishes."),
("Black Forbidden rice", "China", "medium", "Dark purple bran rich in anthocyanins; once reserved for emperors."),
("Thai Riceberry", "Thailand", "long", "Deep purple jasmine-type cross; nutty."),
("Red Cargo rice", "Philippines", "medium", "Unpolished red rice with chewy bite."),
("Bhutanese Red", "Bhutan", "short", "Mountain red rice, nutty, cooks quickly."),
("Camargue Red", "France", "medium", "Red rice from the Rhone delta; nutty."),
("Pandanwangi", "Indonesia (Cianjur)", "medium", "Pandan-scented, very soft; premium local rice."),
("IR64", "Philippines (IRRI)", "long", "High-yielding modern variety grown across Asia."),
("Ofada", "Nigeria", "medium", "Local unpolished aromatic rice for ofada stew."),
("Wild rice (not true rice)", "North America", "long", "Seed of an aquatic grass (Zizania), not Oryza."),
("Brown rice", "Worldwide", "any", "Whole grain with bran; more fibre, longer cooking."),
("Parboiled (Sella) rice", "India / worldwide", "any", "Steamed in husk before milling; firm, non-sticky."),
("Broken rice (Brokens)", "Vietnam / Thailand / India", "any", "Fragments shorter than 3/4 of a whole grain. Cheaper, "
 "cooks fast; used for porridge, flour, noodles and West African dishes. Lower grade, not unsafe by itself."),
]

RICE += [tuple(r.values()) for r in csv.DictReader(open(os.path.join(HERE, "data", "more_rice.csv")))]

def conn(use_db=True):
    return mysql.connector.connect(database=DBN if use_db else None, **CFG)

def init_db():
    c = conn(False); cur = c.cursor()
    cur.execute(f"CREATE DATABASE IF NOT EXISTS {DBN}"); c.commit(); c.close()
    c = conn(); cur = c.cursor()
    cur.execute("SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE TABLE_SCHEMA=%s AND TABLE_NAME='samples'", (DBN,))
    sample_columns = {r[0] for r in cur.fetchall()}
    required_columns = {"label", "score", "grade", "broken", "grain", "verdict"}
    if sample_columns and not required_columns.issubset(sample_columns):
        cur.execute("SELECT COUNT(*) FROM information_schema.TABLES WHERE TABLE_SCHEMA=%s AND TABLE_NAME='samples_legacy'", (DBN,))
        if cur.fetchone()[0]:
            raise RuntimeError("Incompatible samples table found and samples_legacy already exists; preserve or rename the existing tables before starting.")
        cur.execute("RENAME TABLE samples TO samples_legacy")
        print("Preserved the incompatible samples table as samples_legacy.")
    for stmt in open(os.path.join(HERE, "schema.sql")).read().split(";"):
        if stmt.strip(): cur.execute(stmt)
    for col in ("variety VARCHAR(80)", "country VARCHAR(80)", "user_id INT"):   # upgrade older tables
        try: cur.execute("ALTER TABLE samples ADD COLUMN " + col)
        except mysql.connector.Error: pass
    cur.execute("SELECT name FROM rice_types"); have = {r[0] for r in cur.fetchall()}
    cur.executemany("INSERT INTO rice_types(name,country,grain,info) VALUES(%s,%s,%s,%s)", [r for r in RICE if r[0] not in have])
    cur.execute("SELECT label FROM samples"); seen = {r[0] for r in cur.fetchall()}
    S = list(csv.DictReader(open(os.path.join(HERE, "data", "samples.csv"))))
    for r in S:
        if r["label"] in seen: continue
        s = float(r["score"])
        cur.execute("INSERT INTO samples(label,score,grade,broken,grain,verdict) VALUES(%s,%s,%s,%s,%s,%s)",
                    (r["label"], s, GRADES.floor(s), float(r["broken"]), r["grain"], r["verdict"]))
    cur.execute("SELECT COUNT(*) FROM alerts")
    if cur.fetchone()[0] == 0:
        for r in S:
            if r["verdict"] != "safe":
                bad = r["verdict"] == "unsafe"
                cur.execute("INSERT INTO alerts(severity,message) VALUES(%s,%s)", ("danger" if bad else "warning",
                            r["label"] + (": do not eat - mould or heavy discolouration" if bad else ": defects or broken grains - inspect before use")))
    c.commit(); c.close()

def rows(sql, args=()):
    c = conn(); cur = c.cursor(dictionary=True); cur.execute(sql, args)
    r = cur.fetchall(); c.close(); return r

def run(sql, args=()):
    c = conn(); cur = c.cursor(); cur.execute(sql, args); c.commit(); i = cur.lastrowid; c.close(); return i
