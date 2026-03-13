import asyncio
import random
import math
from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client["adaptive_testing"]
questions = db["questions"]


def shuffle_options(opts):
    random.shuffle(opts)
    return opts


# ── Arithmetic ─────────────────────────────────────────────────────────────────
def gen_arithmetic():
    seen = set()
    results = []
    ops = [
        ("×", lambda a, b: a * b),
        ("+", lambda a, b: a + b),
        ("-", lambda a, b: a - b),
    ]
    attempts = 0
    while len(results) < 30 and attempts < 500:
        attempts += 1
        op_sym, op_fn = random.choice(ops)
        a = random.randint(12, 99)
        b = random.randint(2, 20)
        key = (op_sym, a, b)
        if key in seen:
            continue
        seen.add(key)
        correct = op_fn(a, b)
        offset = random.randint(3, 15)
        results.append({
            "question": f"What is {a} {op_sym} {b}?",
            "options": shuffle_options([
                str(correct),
                str(correct + offset),
                str(correct - offset),
                str(correct + offset * 2),
            ]),
            "correct_answer": str(correct),
            "difficulty": round(random.uniform(0.1, 0.35), 2),
            "topic": "arithmetic",
        })
    return results


# ── Algebra ────────────────────────────────────────────────────────────────────
def gen_algebra():
    seen = set()
    results = []
    attempts = 0
    while len(results) < 25 and attempts < 500:
        attempts += 1
        style = random.choice(["linear", "twovar", "quadratic_simple"])

        if style == "linear":
            a = random.randint(2, 15)
            b = random.randint(2, 30)
            key = ("linear", a, b)
            if key in seen:
                continue
            seen.add(key)
            correct = round(b / a, 4)
            offset = round(random.uniform(0.5, 2.0), 2)
            results.append({
                "question": f"Solve for x: {a}x = {b}",
                "options": shuffle_options([
                    str(correct),
                    str(round(correct + offset, 4)),
                    str(round(correct - offset, 4)),
                    str(round(correct + offset * 2, 4)),
                ]),
                "correct_answer": str(correct),
                "difficulty": round(random.uniform(0.35, 0.55), 2),
                "topic": "algebra",
            })

        elif style == "twovar":
            a = random.randint(2, 10)
            b = random.randint(1, 15)
            c = random.randint(10, 40)
            key = ("twovar", a, b, c)
            if key in seen:
                continue
            seen.add(key)
            correct = round((c - b) / a, 4)
            offset = round(random.uniform(0.5, 2.0), 2)
            results.append({
                "question": f"Solve for x: {a}x + {b} = {c}",
                "options": shuffle_options([
                    str(correct),
                    str(round(correct + offset, 4)),
                    str(round(correct - offset, 4)),
                    str(round(correct + offset * 2, 4)),
                ]),
                "correct_answer": str(correct),
                "difficulty": round(random.uniform(0.5, 0.65), 2),
                "topic": "algebra",
            })

        elif style == "quadratic_simple":
            c = random.choice([4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144])
            key = ("quad", c)
            if key in seen:
                continue
            seen.add(key)
            correct = int(math.sqrt(c))
            results.append({
                "question": f"Solve for x (x > 0): x² = {c}",
                "options": shuffle_options([
                    str(correct),
                    str(correct + 1),
                    str(correct + 2),
                    str(correct - 1 if correct > 1 else correct + 3),
                ]),
                "correct_answer": str(correct),
                "difficulty": round(random.uniform(0.55, 0.7), 2),
                "topic": "algebra",
            })

    return results


# ── Geometry ───────────────────────────────────────────────────────────────────
def gen_geometry():
    seen = set()
    results = []
    attempts = 0
    while len(results) < 25 and attempts < 500:
        attempts += 1
        style = random.choice(["circle_area", "circle_circ", "rect_area", "triangle_area", "rect_perimeter"])

        if style == "circle_area":
            r = random.randint(1, 20)
            key = ("ca", r)
            if key in seen: continue
            seen.add(key)
            correct = round(3.14159 * r * r, 2)
            results.append({
                "question": f"What is the area of a circle with radius {r}? (use π = 3.14159)",
                "options": shuffle_options([str(correct), str(round(correct+10,2)), str(round(correct-10,2)), str(round(correct+20,2))]),
                "correct_answer": str(correct),
                "difficulty": round(random.uniform(0.45, 0.65), 2),
                "topic": "geometry",
            })

        elif style == "circle_circ":
            r = random.randint(1, 20)
            key = ("cc", r)
            if key in seen: continue
            seen.add(key)
            correct = round(2 * 3.14159 * r, 2)
            results.append({
                "question": f"What is the circumference of a circle with radius {r}? (use π = 3.14159)",
                "options": shuffle_options([str(correct), str(round(correct+5,2)), str(round(correct-5,2)), str(round(correct+10,2))]),
                "correct_answer": str(correct),
                "difficulty": round(random.uniform(0.4, 0.6), 2),
                "topic": "geometry",
            })

        elif style == "rect_area":
            w = random.randint(2, 25)
            h = random.randint(2, 25)
            key = ("ra", w, h)
            if key in seen: continue
            seen.add(key)
            correct = w * h
            results.append({
                "question": f"What is the area of a rectangle with width {w} and height {h}?",
                "options": shuffle_options([str(correct), str(correct+w), str(correct-h), str(correct+w+h)]),
                "correct_answer": str(correct),
                "difficulty": round(random.uniform(0.3, 0.5), 2),
                "topic": "geometry",
            })

        elif style == "triangle_area":
            b = random.randint(4, 20)
            h = random.randint(4, 20)
            key = ("ta", b, h)
            if key in seen: continue
            seen.add(key)
            correct = round(0.5 * b * h, 2)
            results.append({
                "question": f"What is the area of a triangle with base {b} and height {h}?",
                "options": shuffle_options([str(correct), str(correct+b), str(correct+h), str(b*h)]),
                "correct_answer": str(correct),
                "difficulty": round(random.uniform(0.45, 0.65), 2),
                "topic": "geometry",
            })

        elif style == "rect_perimeter":
            w = random.randint(2, 30)
            h = random.randint(2, 30)
            key = ("rp", w, h)
            if key in seen: continue
            seen.add(key)
            correct = 2 * (w + h)
            results.append({
                "question": f"What is the perimeter of a rectangle with width {w} and height {h}?",
                "options": shuffle_options([str(correct), str(correct+4), str(correct-4), str(w+h)]),
                "correct_answer": str(correct),
                "difficulty": round(random.uniform(0.3, 0.5), 2),
                "topic": "geometry",
            })

    return results


# ── Calculus ───────────────────────────────────────────────────────────────────
def gen_calculus():
    results = []

    # Power rule: d/dx x^n = nx^(n-1)
    for n in range(2, 13):
        results.append({
            "question": f"What is the derivative of x^{n}?",
            "options": shuffle_options([
                f"{n}x^{n-1}",
                f"{n-1}x^{n}",
                f"x^{n}",
                f"{n+1}x^{n-1}",
            ]),
            "correct_answer": f"{n}x^{n-1}",
            "difficulty": round(random.uniform(0.6, 0.85), 2),
            "topic": "calculus",
        })

    # Standard derivatives — explicit question text, no template ambiguity
    standard = [
        ("What is the derivative of sin(x)?",   "cos(x)",     ["−sin(x)", "tan(x)", "sec(x)"],        0.70),
        ("What is the derivative of cos(x)?",   "−sin(x)",    ["sin(x)", "tan(x)", "−cos(x)"],        0.70),
        ("What is the derivative of tan(x)?",   "sec²(x)",    ["sin(x)", "cos(x)", "csc²(x)"],        0.75),
        ("What is the derivative of ln(x)?",    "1/x",        ["ln(x)", "x", "e^x"],                  0.75),
        ("What is the derivative of e^x?",      "e^x",        ["xe^x", "e^(x-1)", "xe^(x-1)"],        0.72),
        ("What is the derivative of x·e^x?",    "e^x(1 + x)", ["e^x", "xe^x", "e^x + x"],            0.85),
        ("What is the derivative of e^(2x)?",   "2e^(2x)",    ["e^(2x)", "2xe^x", "e^(2x-1)"],       0.82),
        ("What is the derivative of e^(3x)?",   "3e^(3x)",    ["e^(3x)", "3xe^x", "e^(3x-1)"],       0.83),
        ("What is the derivative of ln(2x)?",   "1/x",        ["2/x", "ln(2)", "2ln(x)"],             0.80),
        ("What is the derivative of ln(x²)?",   "2/x",        ["1/x", "2x", "ln(2x)"],               0.82),
    ]
    for q, ans, wrongs, diff in standard:
        results.append({
            "question": q,
            "options": shuffle_options([ans] + wrongs),
            "correct_answer": ans,
            "difficulty": round(diff + random.uniform(-0.03, 0.03), 2),
            "topic": "calculus",
        })

    # Chain rule: d/dx (ax)^n = n·a·(ax)^(n-1)
    for n in range(2, 6):
        for a in range(2, 6):
            ans = f"{n}·{a}·({a}x)^{n-1}"
            results.append({
                "question": f"What is the derivative of ({a}x)^{n}?",
                "options": shuffle_options([
                    ans,
                    f"{n}({a}x)^{n-1}",
                    f"{a}({a}x)^{n}",
                    f"{n}·({a}x)^{n}",
                ]),
                "correct_answer": ans,
                "difficulty": round(random.uniform(0.75, 0.95), 2),
                "topic": "calculus",
            })

    # Product rule: d/dx [ax · x^b] = a(b+1)x^b
    for a in range(2, 6):
        for b in range(2, 5):
            ans = f"{a*(b+1)}x^{b}"
            results.append({
                "question": f"Find d/dx [{a}x · x^{b}]",
                "options": shuffle_options([
                    ans,
                    f"{a}x^{b}",
                    f"{b}x^{b-1}",
                    f"{a+b}x^{b}",
                ]),
                "correct_answer": ans,
                "difficulty": round(random.uniform(0.8, 1.0), 2),
                "topic": "calculus",
            })

    return results


# ── Seed ───────────────────────────────────────────────────────────────────────
async def seed():
    all_questions = []
    all_questions.extend(gen_arithmetic())
    all_questions.extend(gen_algebra())
    all_questions.extend(gen_geometry())
    all_questions.extend(gen_calculus())

    for i, q in enumerate(all_questions, start=1):
        q["id"] = f"q{i}"

    print(f"Total questions generated: {len(all_questions)}")

    texts = [q["question"] for q in all_questions]
    dupes = set(t for t in texts if texts.count(t) > 1)
    if dupes:
        print(f"WARNING: {len(dupes)} duplicate question texts found:")
        for d in dupes:
            print(f"  - {d}")
    else:
        print("✓ All question texts are unique")

    await questions.delete_many({})
    await questions.insert_many(all_questions)
    print("✓ Seeded successfully.")


asyncio.run(seed())