# Autonomous_toy_car

## Group Information
Luke Camilleri, Ewan Vaughan, Tham Yik Foong

## Overview
The aim of this assignment was to develop a cars with autonomous driving capabilities where it is capable of lane navigation and collision avoidance. ​The cars should be able to predict speed and steering angle based on the current view captured by its camera.

In this project, our group have developed a convolutional neural network (CNN) based on Nvidia's CNN Architecture. We also performed various types of data augmentation, image preprocessing and feature engineering to further enhance the performance of our model.

Other than that, we also developed a simulation using Unity to combat the issue of lack of data. Due to the Covid-19 situation, collecting real world data using PiCar is no longer possible. Therefore, this simulation allowed us to collect, in theory unlimited training data remotely.

## PiCar Simulation Overview

PiCar Simulation are developed using Unity, and scripts are written in C#. Models appear in this simulation are created using Blender while refering to real-wrold models provided by MLiS 2 course. This simulation allowed us to collect simulation data, with a similiar setting following the actual PiCar provided by faculty. A demo of this simulation can be found in [this video](https://www.youtube.com/watch?v=5SC681vJocY).

### Capabilities of PiCar Simulation

- Recording data
- Enable self-driving mode
- Configure camera angle
- Configure image capture interval
- Switch between tracks
- Switch between scenes
- Ability to configure environment
- Spawning object

## Neural Network Model Overview
Starting out our model based on the CNN architecture proposed by [Bojarski et al](https://arxiv.org/pdf/1604.07316.pdf), we have modify the network to better suit our task on classifying steering angle and speed. 

## Neural Net Hyper-parameters

| Hyper-parameter | Default Values |
|---|---|
| Epoch | 20 |
| Batch Size | 100 |
| Learning Rate | 0.001 |
| Input Layer Size | W:200 H:66 |
| Steps per Epoch | 300 |

## Result

Result of our trained model are shown in below video. Note that the video is speed up. [video](https://www.youtube.com/watch?v=U9EwczZAw5o)
