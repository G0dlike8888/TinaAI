# How to run this — step by step

*Български: `START-HERE-BG.md`*

This document is written for someone who has **never run a program from a terminal**. Nothing is
assumed. Every step tells you exactly what to type, what you should see, and what to do if you see
something else.

> ## The fastest route: don't read this document
>
> On Windows, just **double-click `START-ASSISTANT.bat`** in the main folder. It opens with a short
> introduction of the assistant — **press Enter there to continue** — then does everything in this
> document for you: finds or installs Python, prepares the environment, asks for your API key
> (on every start and hidden as you type) and opens the app in your browser. When Anthropic is
> reachable, the launcher verifies the key with a free authenticated check; if Anthropic cannot be
> reached, a plausible-looking key can be accepted **unverified**, with a visible warning. The key
> is used for that session only. After a normal stop, the launcher removes its local file on a
> best-effort basis; an abruptly closed window can leave it behind, so always run
> `PREPARE-TO-SHARE.bat` before sharing the folder.
>
> You need this document only if: you are not on Windows, the launcher reported an error, or you
> want to understand exactly what is happening.

If you already work with Python and terminals, go straight to `03 Demo/HOW_TO_RUN.md` — same
ground, much shorter.

---

## What this is and what will happen

This folder contains a demo application that opens **in your browser** and runs **only on your own
computer**. It takes an "investigation note" and comments on how well documented it is.

Two things to know up front:

1. **The application sends your text to Anthropic (Claude) over the internet, and that costs
   money** — a small amount, but real, from your own account. That is why you need a personal API
   key (step 4).
2. **The tests (step 7) are free** — they never touch the internet. If you only want to check that
   everything is assembled correctly without paying anything, do steps 1–3 and then step 7.

First-time setup takes about 10–15 minutes. After that, starting it takes 30 seconds.

---

## Step 1 — Install Python (first time only)

Python is the program that runs this application. Check whether you already have it — if not,
install it.

1. Open **https://www.python.org/downloads/** in your browser.
2. Click the big **"Download Python"** button.
3. Run the downloaded file.
4. **THE MOST IMPORTANT PART:** on the installer's first screen, at the bottom, there is a checkbox
   **"Add python.exe to PATH"**. **Tick it.** If you skip it, the terminal will not find Python
   afterwards and nothing below will work.
5. Click "Install Now" and wait for it to finish.

> If you missed the checkbox: run the installer again, choose "Modify", and go through the steps
> with the checkbox ticked. You do not need to uninstall anything.

---

## Step 2 — Open a terminal in the right folder

A "terminal" is a black (or blue) window where you type commands. On Windows it is called
**PowerShell**.

The easiest way to open it **directly in this folder**:

1. Open the project folder in Windows Explorer — the one containing this file (`START-HERE-EN.md`).
   Inside you should see folders named `01 Contract`, `02 Skill`, `03 Demo`,
   `04 Evidence and Records`.
2. Click once in the **address bar** at the top (where the folder path is shown). The text will
   highlight in blue.
3. Type `powershell` over it and press **Enter**.

A terminal opens, already "standing" in the right folder. The last line should read something like:

```
PS D:\AI Investigation Assistant MVP>
```

Your path will differ — what matters is that it ends with the name of the folder holding the
project.

That text (`PS ...>`) is called the **prompt**. You type after it and press Enter. This document
shows commands in grey boxes — type only what is inside the box, never the `PS ...>` part.

> **Useful:** in the terminal, copy is `Ctrl+C` and paste is right-click or `Ctrl+V`. You can
> safely copy the commands from here and paste them instead of typing them by hand.

**Check that Python is visible.** Type:

```
python --version
```

You should get something like `Python 3.14.7` (the numbers may differ, but the version must be
**3.10 or newer** — the packages in step 3 do not install on older versions).

- If it says **"Python was not found"** or **"is not recognized as the name of a cmdlet"** — Python
  is either not installed, or installed without the PATH checkbox. Go back to step 1.
- If the Microsoft Store opens — Windows is redirecting you to install Python from there. Close it
  and install from python.org as in step 1.

---

## Step 3 — Install the required packages (first time only)

The application and its offline tests need several third-party packages. We will put them in a
separate `.venv` folder **inside the project**, so they do not mix with anything else on your
computer.

Type this command and press Enter:

```
python -m venv .venv
```

Nothing is printed — that is normal. It takes 10–20 seconds. If the `.venv` folder already exists,
the command simply does nothing, which is also fine.

Then type:

```
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Many lines of text will scroll past (`Collecting ...`, `Downloading ...`, `Installing ...`). That is
normal and takes 1–3 minutes. At the end you should see a line starting with
**`Successfully installed`**.

> **Why do we type `.venv\Scripts\python.exe` instead of just `python`?** Because that uses the
> Python inside the project folder, where we just installed the packages. The other approach you
> will find online — "activating" the environment — fails on many Windows machines with a security
> error (`running scripts is disabled on this system`). This way avoids it entirely, which is why
> it is used everywhere in this document.

---

## Step 4 — Get an API key (first time only)

The API key is the password the application uses to reach Claude. **Everyone uses their own key.**

1. Open **https://console.anthropic.com** and create an account (or sign in, if you have one).
2. You will need to load a small amount of credit — the application will not work on an empty
   account.
3. Find the **API Keys** section and click **Create Key**.
4. The key is shown **only once**. Copy it immediately. It looks like a long string starting with
   `sk-ant-`.

> ⚠️ **Treat the key like a bank card PIN.** Never send it to anyone, never publish it, never paste
> it into a chat (including a conversation with an AI), and never upload it to GitHub. If you have
> exposed it by accident — go to the console, revoke it, and create a new one.

---

## Step 5 — Save the key into a file (first time only)

The application reads the key from a file called `secrets.toml`. We will create it from the example
file that ships with the project.

In the terminal, type:

```
copy "03 Demo\.streamlit\secrets.toml.example" "03 Demo\.streamlit\secrets.toml"
```

**If nothing is printed, it worked.** That is normal: PowerShell stays silent when a copy succeeds.
A message appears only on failure (for example if you mistyped the folder name).

Now open the new file to put your key in:

```
notepad "03 Demo\.streamlit\secrets.toml"
```

Notepad opens. Find the line:

```
ANTHROPIC_API_KEY = "PASTE-YOUR-OWN-KEY-HERE"
```

Replace **only** `PASTE-YOUR-OWN-KEY-HERE` with your key, **keeping the quotation marks**. The
result should look like this (this is not a real key):

```
ANTHROPIC_API_KEY = "sk-ant-<your own long key goes here>"
```

Save with `Ctrl+S` and close Notepad.

> **Why copy the file from the terminal instead of creating it with a right-click?** Because Windows
> hides file extensions by default, so the file easily ends up named `secrets.toml.txt`, which the
> application will not find. The `copy` command gets the name right the first time.

---

## Step 6 — Start the application

This is the only part you repeat every time. Two commands.

First enter the demo folder:

```
cd "03 Demo"
```

The quotation marks are required, because the folder name contains a space. The prompt should now
end with `\03 Demo>`.

Then start it:

```
..\.venv\Scripts\python.exe -m streamlit run app.py
```

You will see several lines, among them:

```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
```

The browser usually opens by itself. If it does not — copy the address `http://localhost:8501` and
paste it into your browser manually.

**Leave the terminal open.** It is what keeps the application alive. If you close it, the
application stops.

### How to stop the application

Click on the terminal window and press **`Ctrl+C`**. The application stops and the prompt returns.

### Next time

Next time you start from here — step 2 (open a terminal), then step 6. Steps 1, 3, 4 and 5 are
one-time only.

---

## Using the application itself

When it opens in the browser:

1. At the top there is a **Български / English** switch. **The interface starts in Bulgarian** —
   click **English** to switch it. Everything below assumes you have.
2. There are two tabs: **🕹️ Test Site** (the actual work) and **📖 About the Assistant
   (Methodology)** (what has and has not been measured).
3. **Custom** is selected by default. Enter your fictional rule or alert context in **"Your rule /
   alert context"**, then enter the fictional note in **"Your investigation note"**. To use a
   bundled example instead, select one of the named scenarios; the **"🎲 Load the selected
   scenario"** button then appears, and clicking it fills both fields.
4. Click **"Analyze the note"**. The response appears in the right column after a few seconds.
   **This is where money is spent** — every click is one paid request.
5. The checkbox **"Apply experimental Gating Filter"** is off by default. Turning it on makes a
   **second** paid request. It is an experiment, not a better or more validated result — the
   original response always stays available separately.
6. The **"🧹 Clear input and result"** button clears the fields. It sends nothing and costs nothing.

> ⚠️ **Do not paste real data.** No real customer names, account numbers, genuine case notes, or
> internal rule/system names. Every bundled example is entirely fictional — use those, or your own
> invented text.

---

## Step 7 — Run the tests (optional, free)

The tests check that everything is wired up correctly. They **never touch the internet and cost
nothing** — you do not even need an API key for them.

If you are in the `03 Demo` folder, go back up first:

```
cd ..
```

Then:

```
.venv\Scripts\python.exe -m pytest
```

A successful result looks like this (the last line):

```
90 passed in 8.28s
```

If you see dots and `90 passed` — everything is fine.

---

## If something does not work

| What you see | What it means | What to do |
|---|---|---|
| `python : The term 'python' is not recognized` | Python is not installed, or installed without PATH | Step 1, with the "Add python.exe to PATH" checkbox ticked |
| `The system cannot find the path specified` after the step 6 command | You are not in the right folder | Look at the prompt. It must end with `\03 Demo>`. If not — go back with `cd ..` and run `cd "03 Demo"` again |
| `running scripts is disabled on this system` | You tried to "activate" the environment | Do not activate anything — use the `.venv\Scripts\python.exe` commands exactly as written here |
| `No module named streamlit` | The packages are not installed, or you are using the wrong Python | Repeat step 3, and make sure you type `.venv\Scripts\python.exe`, not just `python` |
| 🔑 **"No Anthropic API key found"** in the app, and the analyze button is greyed out | `secrets.toml` is missing, empty, or still holds the placeholder text | Steps 4 and 5. Check that you replaced `PASTE-YOUR-OWN-KEY-HERE` and kept the quotation marks |
| An authentication error after clicking "Analyze the note" | The key is wrong, expired, or the account has no credit | Create a new key at console.anthropic.com and save it again as in step 5 |
| A red box, **"Contract integrity check failed"** | The contract files have been moved or modified | Do not touch or "fix" the expected hash. Restore the original `01 Contract` and `02 Skill` folders next to `03 Demo` |
| A message that the text is too long | You exceeded the limit (4,000 characters for the rule, 16,000 for the note) | Shorten the text yourself. The app never truncates or summarizes it for you |
| Tests pass but end with `PermissionError ... pytest-current` | A stuck temporary file on Windows — the tests already passed | Run `.venv\Scripts\python.exe -m pytest --basetemp=.pytest-tmp` |
| `Port 8501 is already in use` | The application is already running in another terminal | Close the other terminal, or add `--server.port 8502` to the end of the command |
| Everything worked, but after you moved or renamed the project folder the `streamlit` command stops working | The `.venv` folder remembers the old path in some of its files | The commands in this document (using `.venv\Scripts\python.exe`) keep working. For a clean slate: delete the `.venv` folder and repeat step 3 |

---

## What not to do

- **Do not paste real data** into the application (see above).
- **Do not share the `secrets.toml` file** and do not upload it anywhere — it holds your personal,
  billable key.
- **If you are giving this folder to someone else — double-click `PREPARE-TO-SHARE.bat` first.**
  It deletes your key and the local environment, so the recipient starts clean and is asked for
  their own key. Copying a folder does not go through git, so `.gitignore` does not protect you
  here.
- **Do not modify the files** in `01 Contract`, `02 Skill` and `04 Evidence and Records`. They are
  pinned documents with verified checksums; the application deliberately refuses to run if they
  have been changed.
- **Do not rely on the application for decisions.** It comments on the documentation of a single
  note. It does not score, approve or decide anything — and it has not been validated. The details
  are in the "About the Assistant (Methodology)" tab and in the `04 Evidence and Records` folder.

---

*If anything in this document does not match what you see on screen, the more detailed technical
version is in `03 Demo/HOW_TO_RUN.md`.*
