# Deepfake Video Detection Tool

This is a video deepfake detection tool designed to help users easily upload and analyze videos to identify potential manipulations. The app utilizes an advanced ensemble of four deep-learning models that detect fake videos by analyzing spatial and temporal features.

## Features

- **Advanced Detection Models**: The tool employs four detection models:
  - **Two models focus on spatial features**: These models analyze patterns in individual video frames, detecting inconsistencies or artifacts that may signal manipulation.
  - **Two models focus on temporal features**: These models track motion between frames using optical flow to detect unnatural movements or frame transitions, helping to identify temporal inconsistencies that are common in deepfakes.

By combining these approaches, the system provides a more reliable method for identifying deepfake videos.

## Installation

### Install git lfs
-   The models' size is bigger than the allowed file size in git, to porperly be able to fetch them, please install git lfs as described here: [git lfs](https://git-lfs.com/)
-   Alternatively, you can download the models folder from [models](https://drive.google.com/drive/folders/14qk4c3YwAwwRrKgrwAhtwLxvVPIqZHjA?usp=drive_link) and replace the models folder in the backend with the downloaded folder

### Backend Setup

1. Clone the repository and open backend folder

```
   git clone https://github.com/noranMoh/video-deepfake-detection-app.git
```
```
   cd video-deepfake-detection-app/backend
```
2. Install requirements
```
pip install -r requirements.txt
```
3. Run the backend
```
python app.py
```

### Frontend Setup

1. Navigate to the frontend directory 

```
cd deepfake-detection-app/frontend
```
2. Install dependencies

```
npm install
```
3. Start the frontend

```
npm start
```
4. Open the app on your browser, default URL: http://localhost:3000

### Usage

1. Upload a video file by dragging and dropping it into the upload area or click to select a file. You can upload as many videos as you want.
2. Click the detect button next to the video you want to analyze
3. Wait for the system to process the video.
4. Once the analysis is complete, the result will display whether the video is real or fake.


