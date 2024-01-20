# Shibuya-risk-detection-and-Alert
## Introduction

 In this project, the goal is to construct a pipeline for a Computer Vision Object Detection Application using YOLO and OpenCV. The state-of-the-art YOLO model developed by Ultralytics, known as YOLOv8, will be utilized. The purpose of this application is to detect individuals crossing the street outside of the crosswalk (i.e., people at risk). Initially, the application will perform detection for each frame of the video using YOLOv8. Subsequently, it will identify individuals at risk and send SMS alerts through Twilio.  

## Method
### SAHI (Slicing Aided Hyper Inference)
The concept of sliced inference is basically; performing inference over smaller slices of the original image and then merging the sliced predictions on the original image. It can be illustrated below:

![1_5VGHuTkeQlQVxELUAtwIfQ](https://github.com/TushirSahu/Shibuya-risk-detection-and-Alert/assets/96677478/e521be62-cc60-4788-9358-91becb02c452)


## Results
### SAHI-Output
https://github.com/TushirSahu/Shibuya-risk-detection-and-Alert/assets/96677478/e9f09a1a-0f2f-4c5d-af65-c75038a1be5f
### YOLOv8 Output

https://github.com/TushirSahu/Shibuya-risk-detection-and-Alert/assets/96677478/c382d794-4910-43f4-8c15-0ab3e26608c6

