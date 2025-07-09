# PhotoTales Blog

PhotoTales is a simple photo blogging platform built with Flask. It allows users to register, upload photos with camera details, compile them into stories, and interact with other users through comments and likes.

## Features

- **User Registration and Login** – Local authentication powered by Flask-Login. Social authentication can be integrated via extensions like `flask-dance`.
- **Photo Upload and Management** – Upload photos along with descriptions and shooting parameters.
- **Story Compilation** – Group multiple photos into a story with configurable visibility (public, friends, private).
- **Comments and Likes** – Users can comment on and like stories to encourage interaction.
- **Tags and Categories** – Basic models included for organizing content.
- **Notifications** – Minimal notification model for future use.

## Running the App

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the server:
   ```bash
   python app.py
   ```
3. Visit `http://localhost:5000` in your browser.

Uploaded files are saved in `phototales/static/uploads`. In production you should serve uploaded files properly and configure security settings.
