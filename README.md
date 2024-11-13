# MLLM applied to autonomous driving across various weather conditions


## Table of Contents
1. [Introduction](#introduction)
2. [Project Overview](#project-overview)
3. [Requirements](#requirements)
4. [Installation](#installation)
5. [Project Structure](#project-structure)
6. [Usage](#usage)
7. [Results and Performance](#results-and-performance)
8. [Contributing](#contributing)
9. [License](#license)
10. [Acknowledgments](#acknowledgments)





## Introduction
This project explores the use of Multimodal Large Language Models (MLLMs) in autonomous driving applications, specifically under challenging environmental conditions. By leveraging GPT-4 and the LimSim++ simulator integrated with CARLA, this project investigates how MLLMs can be applied to improve the performance of autonomous vehicles by adapting to various weather conditions using different sensor setups (e.g., front and back cameras, LiDAR).

## Project Overview
- **Objective**: To enhance autonomous driving capabilities by applying MLLMs in harsh environmental conditions.
- **Simulator**: [LimSim++](https://github.com/PJLab-ADG/LimSim) integrated with CARLA for realistic simulation environments.
- **Weather Conditions**: Tested across a range of adverse conditions (Heavy rain,fog,Storm,wetness).
- **Sensors Used**: Camera (front, back) and LiDAR for a comprehensive sensory setup.

## Requirements

To run this project, you need the following dependencies and tools:
- Python 3.9.0 +
- [LimSim++](https://github.com/PJLab-ADG/LimSim)
- [CARLA Simulator](https://github.com/carla-simulator/carla)
- [SUMO Simulator](https://www.eclipse.org/sumo/) (for additional simulation of traffic and urban mobility)
- Additional Python packages:
  - `torch`
  - `transformers`
  - `opencv-python`
  - `numpy`
  - `pandas`
  - `matplotlib`
    
 ## Installation

### 1. LimSim++ Setup

Download and Install LimSim++: Follow the official instructions from the LimSim++ GitHub page.


### Example command to install LimSim++ 
git clone https://github.com/PJLab-ADG/LimSim.git
cd LimSim

### Follow any additional build or setup instructions in LimSim's README
Configure Environment Variables for LimSim++: Make sure to set up any required environment variables as outlined in the LimSim++ documentation.

### 2.  CARLA Setup
Download CARLA: Obtain the CARLA simulator from the CARLA website or directly from GitHub.

### 3. SUMO Setup
Download and Install SUMO: Follow the instructions on the SUMO installation guide.



### 4. Install Python Dependencies
   
With the main dependencies installed, install the required Python packages for this project:

pip install -r requirements.txt

