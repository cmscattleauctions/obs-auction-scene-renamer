# OBS Auction Scene Renamer

This project takes:
- an exported OBS scene collection JSON file
- a monthly auction CSV

and creates a new OBS scene collection JSON with the lot scenes renamed to match the new month's lot order.

It was designed for an OBS workflow where scenes look like this:
- `401-A Transition`
- `401-A Video`
- `402 Transition`
- `402 Video`

and where fixed scenes such as `Option Lot Interlude ...`, logo scenes, waiting room scenes, breed divider scenes, and ending scenes should stay untouched.

---

## What this version does

- Reads the lot order directly from the CSV.
- Builds scene names from the `Lot Number` and `Option` columns.
- Fills the reusable lot slots in the OBS JSON in order.
- Renames extra unused lot slots to unique names like `UNUSED 001 Transition` and `UNUSED 001 Video`.
- Prevents duplicate target scene names.
- Leaves interludes and fixed scenes alone.

---

## What files you need each month

You need two files:

1. **OBS scene collection export**
   - In OBS, export your current scene collection as a JSON file.

2. **Monthly auction CSV**
   - This should include at least:
     - `Lot Number`
     - `Option`

---

## Very detailed setup guide for a non-technical user

### Step 1: Make a GitHub account
If you do not already have one:
1. Go to GitHub.
2. Click **Sign up**.
3. Create your account.
4. Verify your email.

### Step 2: Create a new GitHub repository
1. Log in to GitHub.
2. Click the **+** button in the top-right corner.
3. Click **New repository**.
4. Repository name: `obs-auction-scene-renamer`
5. Make it **Private** unless you want others to see it.
6. Click **Create repository**.

### Step 3: Put these project files into GitHub
You have two easy choices.

#### Option A: Use the GitHub website
1. Open the repository you just created.
2. Click **uploading an existing file**.
3. Upload every file and folder from this project.
4. Commit the upload.

#### Option B: Upload the zip, then extract locally
If you keep the project as a zip on your computer, unzip it first, then upload the files into GitHub.

### Step 4: Install Python on your Mac
1. Go to python.org.
2. Download Python 3.11 or newer.
3. Run the installer.
4. When it finishes, open **Terminal**.
5. Type this and press Enter:

```bash
python3 --version
```

If it shows a version number, you are ready.

### Step 5: Download your GitHub project to your Mac
You can either:
- click **Code** > **Download ZIP** in GitHub
- or use GitHub Desktop if you prefer a visual app

If you download the ZIP:
1. Unzip it.
2. Move the folder somewhere easy, like your Desktop.

### Step 6: Open Terminal and go into the project folder
Example:

```bash
cd ~/Desktop/obs-auction-scene-renamer
```

If the folder is somewhere else, drag the folder into Terminal after typing `cd `.

### Step 7: Run the script
Put your two working files somewhere easy to find.
For example:
- OBS export: `~/Desktop/April Scene Collection.json`
- CSV: `~/Desktop/May Lots.csv`

Then run:

```bash
python3 src/main.py \
  --obs ~/Desktop/April\ Scene\ Collection.json \
  --csv ~/Desktop/May\ Lots.csv \
  --out ~/Desktop/May\ Scene\ Collection.json
```

### Step 8: Import the new file back into OBS
1. Open OBS.
2. Import or load the updated scene collection JSON.
3. Check that your lot scene names now match the new month's lots.
4. Your fixed interlude scenes and divider scenes should still be there.

---

## Example workflow each month

1. Export your current OBS scene collection.
2. Save the new monthly CSV.
3. Run the command.
4. Import the new JSON into OBS.
5. Drop in your updated videos and banners.

---

## How the naming logic works

### If the CSV has
- `Lot Number = 401A`, `Option = A`

The script creates:
- `401-A Transition`
- `401-A Video`

### If the CSV has
- `Lot Number = 402`, `Option = blank`

The script creates:
- `402 Transition`
- `402 Video`

### If the OBS template has more lot slots than the month needs
The extra slots become:
- `UNUSED 001 Transition`
- `UNUSED 001 Video`
- `UNUSED 002 Transition`
- `UNUSED 002 Video`

This is done so OBS never has duplicate scene names.

---

## Important limitation

This first version only renames scenes.
It does **not** yet automatically relink the videos, banners, or Dropbox file paths.
That can be added later.

---

## Troubleshooting

### Error: Could not find a lot number column
Your CSV probably does not have a column named `Lot Number`.
Open the CSV and confirm the exact header text.

### Error: The CSV contains more lots than the OBS template has slots
That means your OBS template needs more backup scenes at the end.
Add more slot pairs in OBS, export again, and rerun the script.

### Error: command not found: python3
Python is not installed, or your Mac cannot find it yet.
Reinstall Python from python.org and try again.

---

## Future upgrades

Possible future versions:
- simple drag-and-drop desktop app
- automatic Dropbox file relinking
- report showing exactly which old scenes became which new scenes
- one-click Mac app build
