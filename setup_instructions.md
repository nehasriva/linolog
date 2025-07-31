# LinoLog Setup Instructions

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Set Up Google Service Account

### 2.1 Create Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" → "New Project"
3. Enter project name (e.g., "LinoLog") and click "Create"

### 2.2 Enable Google Sheets API
1. In your project, go to "APIs & Services" → "Library"
2. Search for "Google Sheets API"
3. Click on it and press "Enable"

### 2.3 Create Service Account
1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "Service Account"
3. Fill in:
   - Service account name: `linolog-service`
   - Service account ID: `linolog-service`
   - Description: `Service account for LinoLog application`
4. Click "Create and Continue"
5. Skip role assignment (click "Continue")
6. Click "Done"

### 2.4 Download JSON Key
1. Click on the service account you just created
2. Go to "Keys" tab
3. Click "Add Key" → "Create new key"
4. Select "JSON" and click "Create"
5. The JSON file will download automatically
6. Rename it to `creds.json` and place it in your LinoLog project directory

### 2.5 Create Google Sheet
1. Go to [Google Sheets](https://sheets.google.com/)
2. Create a new spreadsheet
3. Name it "LinoLog - Print Archive"
4. Copy the Sheet ID from the URL (it's the long string between /d/ and /edit)
5. Share the sheet with your service account email (found in the JSON file under `client_email`)

## Step 3: Configure Environment

1. Copy the environment template:
```bash
cp env.example .env
```

2. Edit `.env` with your values:
```env
# Google Sheets Configuration
GOOGLE_SHEET_ID=your_sheet_id_here
GOOGLE_SHEET_NAME=Sheet1

# Folder Watching
WATCH_DIRECTORY=/LinocutArchive

# Agent Configuration
ENABLE_METADATA_FILLER=true
ENABLE_COLOR_AGENT=true
ENABLE_TAG_AGENT=true

# Logging
LOG_LEVEL=INFO
LOG_FILE=linolog.log

# Processing
PROCESSED_LOG_FILE=processed_folders.txt
```

## Step 4: Create Watch Directory

```bash
mkdir -p ~/LinocutArchive
```

## Step 5: Test the System

1. Create a test folder:
```bash
mkdir -p "~/LinocutArchive/test_print_edition_1"
```

2. Add a test image (any .jpg file) to the folder

3. Run the system:
```bash
python main.py
```

## Troubleshooting

### Common Issues:

1. **"Missing required configuration: GOOGLE_SHEET_ID"**
   - Make sure you've set the GOOGLE_SHEET_ID in your .env file

2. **"Failed to set up Google Sheets client"**
   - Ensure `creds.json` is in the project directory
   - Check that the service account email has access to the Google Sheet

3. **"Watch directory does not exist"**
   - Create the `~/LinocutArchive` directory or change WATCH_DIRECTORY in .env

4. **Permission errors**
   - Make sure the service account email has edit access to your Google Sheet

### Getting Help:

- Check the log file (`linolog.log`) for detailed error messages
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Verify your Google Service Account setup is correct 