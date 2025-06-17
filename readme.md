# Image Hosting

A simple web application for uploading, viewing, and downloading images, built with FastAPI, Jinja2 for templating, and styled with CSS in a warm pastel color scheme.

## Overview

The application allows users to:
- Upload images with optional descriptions via a form or drag-and-drop.
- View a gallery of images with thumbnails, descriptions, and upload dates.
- Open images in a modal window with their descriptions.
- Copy image URLs and download images.
- Interact with a user-friendly interface styled in warm pastel tones (peach, creamy white, coral).

## Technologies

- **Backend**: FastAPI (Python) for handling routes and file uploads.
- **Frontend**: Jinja2 for rendering HTML templates, pure CSS, and JavaScript for interactivity.
- **Image Processing**: Pillow for generating thumbnails.
- **Data Storage**: Temporary in-memory storage (using the `demo_images` list).

## Project Structure

```
project/
├── static/
│   ├── style.css               # Styles in a warm pastel color scheme
│   ├── images/                 # Folder for original images
│   ├── thumbnails/             # Folder for thumbnails
├── templates/
│   ├── base.html               # Base template with header and footer
│   ├── index.html              # Homepage
│   ├── upload.html             # Image upload page
│   ├── images.html             # Gallery page
└── app.py                      # Main FastAPI application file
```

## Features

- **Homepage (`/`)**: Welcome message with buttons to navigate to upload or gallery pages.
- **Upload Page (`/upload`)**:
  - Form for selecting an image and adding a description.
  - Drag-and-drop support.
  - Success message after upload.
- **Gallery Page (`/images`)**:
  - Displays a list of images as cards with thumbnails, descriptions, and upload dates.
  - Modal window for viewing full-size images with descriptions.
  - Options to copy image URLs or download images.

## Installation

1. **Clone the repository** (or set up the project structure):
   ```bash
   git clone <https://github.com/MrJonson75/Site-for-photos.git>
   cd image-hosting
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install fastapi uvicorn python-multipart Pillow
   ```

4. **Create directories for static files**:
   ```bash
   mkdir -p static/images static/thumbnails
   ```


## Running the Application

1. **Start the server**:
   ```bash
   uvicorn app:app --reload
   ```

2. **Access the application**:
   - Open `http://127.0.0.1:8000` in your browser.
   - Homepage: `http://127.0.0.1:8000/`
   - Upload: `http://127.0.0.1:8000/upload`
   - Gallery: `http://127.0.0.1:8000/images`

## Usage

1. **Uploading an Image**:
   - Navigate to `/upload`.
   - Drag and drop an image or select a file.
   - (Optional) Add a description.
   - Click "Upload" and wait for the success message.

2. **Viewing the Gallery**:
   - Go to `/images`.
   - Click a thumbnail to open the image in a modal window.
   - Copy the image URL or download the image using the respective buttons.

## Limitations

- Data is stored in memory (`demo_images`) and resets on server restart. A database is needed for persistent storage.


## License

© 2025 Image Hosting. All rights reserved.