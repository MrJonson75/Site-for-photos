# Image Hosting

A simple web application for uploading, viewing, and downloading images, built with FastAPI, Jinja2 for templating, and styled with CSS in a warm pastel color scheme.

## Overview

The application enables users to:
- Upload images with optional descriptions via a form or drag-and-drop, with client- and server-side validation.
- View a gallery of images with thumbnails, descriptions, and upload dates.
- Open images in a modal window with descriptions, closable by clicking outside the content area.
- Copy image URLs and download images directly from the gallery.
- Experience a smooth interface with a loading spinner during redirects and a warm pastel aesthetic (peach, creamy white, coral).

## Technologies

- **Backend**: FastAPI (Python) for handling routes and file uploads.
- **Frontend**: Jinja2 for rendering HTML templates, pure CSS for styling, and JavaScript for interactivity.
- **Image Processing**: Pillow for generating thumbnails.
- **Data Storage**: Temporary in-memory storage using the `demo_images` list.

## Project Structure

```
project/
├── static/
│   ├── js/
│   │   ├── upload.js           # JavaScript for upload page functionality
│   │   ├── images.js           # JavaScript for gallery page functionality
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

- **Homepage (`/`)**: Displays a welcome message with buttons to navigate to the upload or gallery pages.
- **Upload Page (`/upload`)**:
  - Form for selecting an image and adding a description, with drag-and-drop support.
  - Client-side validation for file format (`.jpg`, `.png`, `.gif`) and size (up to 5 MB).
  - Server-side validation for file format, size, and type.
  - Success message with a loading spinner, followed by automatic redirection to `/images/` after 1 second.
  - Error messages for invalid files displayed directly on the page.
- **Gallery Page (`/images`)**:
  - Displays images as cards with thumbnails, descriptions, and upload dates.
  - Modal window for viewing full-size images, closable by clicking outside or via a close button.
  - Options to copy image URLs or download images.

## Installation

1. **Clone the repository** (or set up the project structure):
   ```bash
   git clone https://github.com/MrJonson75/Site-for-photos.git
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
   mkdir -p static/images static/thumbnails static/js
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
   - Drag and drop an image or select a file (`.jpg`, `.png`, or `.gif`, up to 5 MB).
   - Optionally add a description.
   - Click "Upload" and wait for the success message with a loading spinner, then be redirected to `/images/`.
   - Invalid files trigger an error message on the page.

2. **Viewing the Gallery**:
   - Go to `/images`.
   - Click a thumbnail to open the image in a modal window; close it by clicking outside or using the close button.
   - Copy the image URL or download the image using the respective buttons.

## Limitations

- Data is stored in memory (`demo_images`) and resets on server restart. A database is required for persistent storage.
- No user authentication or file management (e.g., deletion).
- Limited file format validation (only `.jpg`, `.png`, `.gif` are supported).

## Potential Improvements

- Integrate a database (e.g., SQLite or PostgreSQL) for persistent storage.
- Add user authentication to manage uploaded files.
- Implement file deletion functionality in the gallery.
- Enhance the loading animation with a progress bar or countdown.
- Support additional image formats or larger file sizes with compression.

## License

© 2025 Image Hosting. All rights reserved.