import re
import tkinter as tk
from tkinter import ttk
from words import words

# Normalize dictionaries
english_to_minionese = {k.lower(): v for k, v in words.items()}
minionese_to_english = {v.lower(): k for k, v in words.items()}

TOKEN_RE = re.compile(r"\w+|[^\w\s]", re.UNICODE)


def apply_case(original, translated):
    if not original:
        return translated
    if original.isupper():
        return translated.upper()
    if original[:1].isupper():
        return translated.capitalize()
    return translated


def rebuild_text(tokens):
    result = ""
    for i, token in enumerate(tokens):
        if i == 0:
            result += token
        elif re.fullmatch(r"[^\w\s]", token):
            result += token
        elif tokens[i - 1] in "([{\"'":
            result += token
        else:
            result += " " + token
    return result


def translate(sentence, minionese=False):
    dictionary = minionese_to_english if minionese else english_to_minionese

    stripped = sentence.strip()
    lower_sentence = stripped.lower()

    # Full phrase match first
    if lower_sentence in dictionary:
        return apply_case(stripped, dictionary[lower_sentence])

    tokens = TOKEN_RE.findall(sentence)
    lowered = [t.lower() if re.fullmatch(r"\w+", t) else t for t in tokens]

    result = []
    i = 0
    phrase_keys = sorted(dictionary.keys(), key=lambda x: len(x.split()), reverse=True)

    while i < len(tokens):
        matched = False

        if re.fullmatch(r"\w+", tokens[i]):
            for phrase in phrase_keys:
                parts = phrase.split()
                n = len(parts)

                if i + n <= len(tokens):
                    token_chunk = tokens[i:i + n]
                    lower_chunk = lowered[i:i + n]

                    if all(re.fullmatch(r"\w+", t) for t in token_chunk) and lower_chunk == parts:
                        original_chunk = " ".join(token_chunk)
                        translated = apply_case(original_chunk, dictionary[phrase])
                        result.append(translated)
                        i += n
                        matched = True
                        break

        if not matched:
            token = tokens[i]
            if re.fullmatch(r"\w+", token):
                translated = dictionary.get(token.lower(), token)
                translated = apply_case(token, translated)
                result.append(translated)
            else:
                result.append(token)
            i += 1

    return rebuild_text(result)


class MinionTranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("English ↔ Minionese Translator")
        self.root.geometry("760x700")
        self.root.configure(bg="#f7f7f7")

        self.mode = tk.StringVar(value="english_to_minionese")

        self.build_ui()
        self.draw_minion("Bello!")

    def build_ui(self):
        title = tk.Label(
            self.root,
            text="English ↔ Minionese Translator",
            font=("Helvetica", 22, "bold"),
            bg="#f7f7f7",
            fg="#222222"
        )
        title.pack(pady=(18, 10))

        controls = tk.Frame(self.root, bg="#f7f7f7")
        controls.pack(pady=6)

        ttk.Radiobutton(
            controls,
            text="English → Minionese",
            variable=self.mode,
            value="english_to_minionese"
        ).pack(side="left", padx=10)

        ttk.Radiobutton(
            controls,
            text="Minionese → English",
            variable=self.mode,
            value="minionese_to_english"
        ).pack(side="left", padx=10)

        input_frame = tk.Frame(self.root, bg="#f7f7f7")
        input_frame.pack(fill="x", padx=20, pady=(10, 6))

        tk.Label(
            input_frame,
            text="Enter text:",
            font=("Helvetica", 12, "bold"),
            bg="#f7f7f7"
        ).pack(anchor="w")

        self.input_text = tk.Text(
            input_frame,
            height=5,
            font=("Helvetica", 13),
            wrap="word",
            relief="solid",
            bd=1
        )
        self.input_text.pack(fill="x", pady=(6, 0))
        self.input_text.bind("<Return>", self.handle_enter)

        buttons = tk.Frame(self.root, bg="#f7f7f7")
        buttons.pack(pady=12)

        tk.Button(
            buttons,
            text="Translate",
            command=self.on_translate,
            font=("Helvetica", 12, "bold"),
            bg="#ffd54f",
            activebackground="#ffca28",
            relief="flat",
            padx=18,
            pady=8
        ).pack(side="left", padx=8)

        tk.Button(
            buttons,
            text="Clear",
            command=self.on_clear,
            font=("Helvetica", 12),
            bg="#e0e0e0",
            activebackground="#d5d5d5",
            relief="flat",
            padx=18,
            pady=8
        ).pack(side="left", padx=8)

        output_frame = tk.Frame(self.root, bg="#f7f7f7")
        output_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        tk.Label(
            output_frame,
            text="Result:",
            font=("Helvetica", 12, "bold"),
            bg="#f7f7f7"
        ).pack(anchor="w", pady=(0, 6))

        self.canvas = tk.Canvas(
            output_frame,
            width=700,
            height=430,
            bg="white",
            highlightthickness=1,
            highlightbackground="#dddddd"
        )
        self.canvas.pack(fill="both", expand=True)

    def handle_enter(self, event):
        if event.state & 0x1:  # Shift+Enter -> newline
            return
        self.on_translate()
        return "break"

    def on_translate(self):
        text = self.input_text.get("1.0", "end").strip()
        if not text:
            self.draw_minion("Banana?")
            return

        minionese = self.mode.get() == "minionese_to_english"
        result = translate(text, minionese=minionese)
        self.draw_minion(result)

    def on_clear(self):
        self.input_text.delete("1.0", "end")
        self.draw_minion("Poopaye!")

    def draw_rounded_rect(self, x1, y1, x2, y2, radius=20, **kwargs):
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1
        ]
        return self.canvas.create_polygon(points, smooth=True, **kwargs)

    def draw_minion(self, message):
        self.canvas.delete("all")

        # Speech bubble
        bubble_x1, bubble_y1 = 40, 30
        bubble_x2, bubble_y2 = 660, 135
        self.draw_rounded_rect(
            bubble_x1, bubble_y1, bubble_x2, bubble_y2,
            radius=25,
            fill="#ffffff",
            outline="#cccccc",
            width=2
        )

        self.canvas.create_polygon(
            300, 135,
            340, 135,
            325, 165,
            fill="#ffffff",
            outline="#cccccc",
            width=2
        )

        self.canvas.create_text(
            350, 82,
            text=message,
            width=580,
            font=("Helvetica", 16, "bold"),
            fill="#222222"
        )

        # Minion body
        body_x1, body_y1 = 250, 175
        body_x2, body_y2 = 450, 385

        self.canvas.create_oval(
            body_x1, body_y1, body_x2, body_y2,
            fill="#f4d03f",
            outline="#c9a500",
            width=2
        )
        self.canvas.create_rectangle(
            body_x1, (body_y1 + body_y2) / 2,
            body_x2, body_y2,
            fill="#f4d03f",
            outline="#c9a500",
            width=2
        )

        # Goggles strap
        self.canvas.create_rectangle(
            245, 235, 455, 255,
            fill="#444444",
            outline="#444444"
        )

        # Goggles
        self.canvas.create_oval(
            285, 210, 355, 280,
            fill="#b0bec5",
            outline="#666666",
            width=3
        )
        self.canvas.create_oval(
            345, 210, 415, 280,
            fill="#b0bec5",
            outline="#666666",
            width=3
        )

        # Eyes
        self.canvas.create_oval(
            303, 228, 337, 262,
            fill="white",
            outline="#999999"
        )
        self.canvas.create_oval(
            363, 228, 397, 262,
            fill="white",
            outline="#999999"
        )
        self.canvas.create_oval(
            317, 242, 329, 254,
            fill="#5d4037",
            outline="#5d4037"
        )
        self.canvas.create_oval(
            377, 242, 389, 254,
            fill="#5d4037",
            outline="#5d4037"
        )

        # Smile
        self.canvas.create_arc(
            315, 270, 385, 320,
            start=200, extent=140,
            style="arc",
            width=3,
            outline="#5d4037"
        )

        # Hair
        self.canvas.create_line(320, 175, 312, 150, width=3, fill="#222222")
        self.canvas.create_line(350, 172, 350, 145, width=3, fill="#222222")
        self.canvas.create_line(380, 175, 388, 150, width=3, fill="#222222")

        # Overalls
        self.canvas.create_rectangle(
            270, 310, 430, 385,
            fill="#3f51b5",
            outline="#2c3e9f",
            width=2
        )
        self.canvas.create_polygon(
            300, 310, 400, 310, 385, 280, 315, 280,
            fill="#3f51b5",
            outline="#2c3e9f",
            width=2
        )
        self.canvas.create_line(315, 280, 292, 325, width=6, fill="#3f51b5")
        self.canvas.create_line(385, 280, 408, 325, width=6, fill="#3f51b5")

        # Pocket
        self.canvas.create_rectangle(
            330, 325, 370, 355,
            fill="#5c6bc0",
            outline="#2c3e9f",
            width=2
        )

        # Arms
        self.canvas.create_line(250, 315, 200, 290, width=8, fill="#f4d03f")
        self.canvas.create_line(450, 315, 500, 290, width=8, fill="#f4d03f")

        # Gloves
        self.canvas.create_oval(185, 280, 210, 305, fill="#222222", outline="#222222")
        self.canvas.create_oval(490, 280, 515, 305, fill="#222222", outline="#222222")

        # Legs
        self.canvas.create_line(315, 385, 305, 435, width=8, fill="#3f51b5")
        self.canvas.create_line(385, 385, 395, 435, width=8, fill="#3f51b5")

        # Shoes
        self.canvas.create_oval(280, 430, 325, 450, fill="#222222", outline="#222222")
        self.canvas.create_oval(375, 430, 420, 450, fill="#222222", outline="#222222")


def main():
    root = tk.Tk()
    app = MinionTranslatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()