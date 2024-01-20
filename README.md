# Shibuya-risk-detection-and-Alert
## Introduction

This project aims to build a pipeline of a Computer Vision Object Detection Aplication with Yolo and OpenCV. In this project will be used the state-of-the-art yolo model develop by Ultralytics **the Yolov8**.
This application aims detect people crossing the street outside the crosswalk (People in risk). First it's make detection for each frame of video with Yolo. After that it verify which one is in risk and send SMS alerts through twilio.

## Method
### SAHI (Slicing Aided Hyper Inference)
The concept of sliced inference is basically; performing inference over smaller slices of the original image and then merging the sliced predictions on the original image. It can be illustrated below:

![1_5VGHuTkeQlQVxELUAtwIfQ](https://github.com/TushirSahu/Shibuya-risk-detection-and-Alert/assets/96677478/e521be62-cc60-4788-9358-91becb02c452)


## Results
### SAHI-Output
https://github.com/TushirSahu/Shibuya-risk-detection-and-Alert/assets/96677478/e9f09a1a-0f2f-4c5d-af65-c75038a1be5f
### YOLOv8 Output

https://github.com/TushirSahu/Shibuya-risk-detection-and-Alert/assets/96677478/c382d794-4910-43f4-8c15-0ab3e26608c6

