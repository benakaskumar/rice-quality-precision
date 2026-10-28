"""Creates synthetic rice photos in static/samples for demos."""
import os, random
from PIL import Image, ImageDraw

OUT = os.path.join(os.path.dirname(__file__), "static", "samples")
os.makedirs(OUT, exist_ok=True)
BAD = [(60, 170, 70), (215, 190, 60), (150, 100, 50)]


def make(name, length, broken, bad, seed):
    random.seed(seed)
    im = Image.new("RGB", (600, 450), (25, 25, 25))
    for cx in range(10):
        for cy in range(9):
            L = length * (random.uniform(0.3, 0.5) if random.random() < broken else random.uniform(0.9, 1.1))
            col = random.choice(BAD) if random.random() < bad else (245, 240, 225)
            g = Image.new("RGBA", (int(L) + 4, 20), (0, 0, 0, 0))
            ImageDraw.Draw(g).ellipse((1, 3, L + 2, 17), fill=col + (255,))
            g = g.rotate(random.uniform(0, 180), expand=True)
            im.paste(g, (cx * 60 + 30 - g.width // 2, cy * 50 + 25 - g.height // 2), g)
    im.save(os.path.join(OUT, name))


def make_brown_bowl(name="brown_bowl.png"):
    random.seed(42)
    im = Image.new("RGB", (600, 450), (248, 248, 248))
    d = ImageDraw.Draw(im)
    # White ceramic bowl
    d.ellipse((75, 25, 525, 425), fill=(245, 245, 242), outline=(225, 225, 220), width=6)
    d.ellipse((95, 45, 505, 405), fill=(240, 240, 236))
    for _ in range(850):
        gx = random.randint(115, 485)
        gy = random.randint(65, 385)
        if ((gx - 300) / 190) ** 2 + ((gy - 225) / 160) ** 2 < 0.92:
            r = random.randint(155, 195)
            g = random.randint(115, 148)
            b = random.randint(75, 108)
            d.ellipse((gx - 10, gy - 4, gx + 10, gy + 4), fill=(r, g, b), outline=(r - 20, g - 20, b - 20))
    im.save(os.path.join(OUT, name))


def make_red_heap(name="red_heap.png"):
    random.seed(99)
    im = Image.new("RGB", (600, 450), (125, 40, 32))
    d = ImageDraw.Draw(im)
    for _ in range(1200):
        gx = random.randint(10, 590)
        gy = random.randint(10, 440)
        r = random.randint(145, 185)
        g = random.randint(45, 75)
        b = random.randint(35, 60)
        d.ellipse((gx - 12, gy - 5, gx + 12, gy + 5), fill=(r, g, b), outline=(r - 25, g - 15, b - 15))
    im.save(os.path.join(OUT, name))


make("good_long.png", 40, 0.03, 0.0, 1)
make("broken_mix.png", 30, 0.6, 0.0, 2)
make("mouldy.png", 36, 0.1, 0.3, 3)
make_brown_bowl("brown_bowl.png")
make_red_heap("red_heap.png")
print("All sample images written to", OUT)
