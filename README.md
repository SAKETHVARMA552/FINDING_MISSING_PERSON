Missing Person Finder Using Face Recognition
Project Overview

The Missing Person Finder is an AI-based web application that helps locate missing individuals using face recognition technology. The system allows users to upload images of missing persons and compare them with available images to detect matches. When a match is found, the system can notify the concerned person through email.

This project is built using Python, Streamlit, OpenCV, and Face Recognition techniques to provide a simple and efficient platform for identifying missing people.

Features

Upload and register missing person details

Face detection using computer vision

Face matching using image comparison

Email notification system when a match is found

Store missing person records in a database

View missing person details

User-friendly web interface built with Streamlit

Multi-language support

Technologies Used
Programming Language

Python

Libraries & Frameworks

Streamlit

OpenCV

NumPy

Pandas

SQLite

smtplib

Matplotlib

AI / Computer Vision

Face Detection

Face Matching

Image Processing

Project Architecture
Missing Person Finder
│
├── miss.py                # Main Streamlit application
├── face_detection.py      # Detect faces from images
├── face_match.py          # Face comparison logic
├── database.py            # SQLite database operations
├── email_utils.py         # Email notification system
├── translations.py        # Multi-language support
├── style.css              # UI styling
├── missing_person.db      # SQLite database
├── bg.jpg                 # Background image
│
└── lfw-deepfunneled/      # Face image dataset
How the System Works

User uploads a missing person's photo and details.

The system stores the details in a database.

Face detection extracts facial features from the image.

The system compares the face with stored images.

If a match is found:

The system identifies the person.

Sends an email notification to the registered contact.

Installation Guide
1. Clone the Repository
git clone https://github.com/your-username/missing-person-finder.git
cd missing-person-finder
2. Install Required Libraries
pip install streamlit
pip install opencv-python
pip install numpy
pip install pandas
pip install matplotlib
3. Run the Application
streamlit run miss.py
Database

The project uses SQLite database to store missing person records.

Example stored data:

Name

Age

Gender

Last Seen Location

Contact Email

Photo

Dataset

This project uses the Labeled Faces in the Wild (LFW) dataset for face recognition testing.

Dataset folder:

lfw-deepfunneled/

Each folder contains images of a person used for training and testing the face recognition system.

Screenshots
Home Page

User-friendly interface to register or search missing persons.

Upload Missing Person

Upload image and enter missing person details.

Face Detection

System detects faces in uploaded images.

Match Found

Displays matching person details.

Future Improvements

Real-time CCTV integration

Mobile application version

GPS-based tracking

Police database integration

Deep learning face recognition models

Cloud deployment

Use Cases

Police departments

NGOs working for missing persons

Child safety organizations

Public missing person reporting systems

Author

Saketh Varma
B.Tech – Computer Science & Engineering
Mallareddy College of Engineering
