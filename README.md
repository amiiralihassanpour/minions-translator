#  Minion Translator

*At the moment, the internet in Iran has been banned because of the war. We hope for better days.*

A fun **English ↔ Minionese translator** with a graphical Minion that speaks the translated text.

This project translates English sentences into Minion language (from *Despicable Me*) and displays the result in a speech bubble above a drawn Minion.

---

## Features

*  **Two-way translation**

  * English → Minionese
  * Minionese → English

*  **Phrase support**
  Supports full phrases like:

  ```
  I love you → Tulaliloo ti amo
  ```

*  **Graphical interface**

  * Minion character drawn with Tkinter
  * Speech bubble output

*  **Smart translation**

  * Preserves capitalization
  * Handles punctuation
  * Falls back to original word if unknown

---

##  Preview

Example:

```
English: I love you
```

Minion says:

```
Tulaliloo ti amo
```

---

##  Requirements

* Python **3.8+**
* Tkinter (included with most Python installations)

Check Python:

```bash
python --version
```

---

##  Run the program

Clone the repo:

```bash
git clone https://github.com/amiiralihassanpour/minions-translator.git
```

Enter the project folder:

```bash
cd minions-translator
```

Run the app:

```bash
python main.py
```

---

##  Project Structure

```
minion-translator
│
├── main.py      # GUI translator app
├── words.py     # English ↔ Minionese dictionary
└── README.md
```

---

##  Example Dictionary Entry

Inside `words.py`:

```python
words = {
    "hello": "bello",
    "goodbye": "poopaye",
    "fire": "beedo",
    "i love you": "tulaliloo ti amo"
}
```

---

**Bello! 🍌**
