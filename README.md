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
9. [Acknowledgments](#acknowledgments)





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

  Download and Install LimSim++: Follow the official instructions from [LimSim++ GitHub page](https://github.com/PJLab-ADG/LimSim).


  ### Example command to install LimSim++

  ```bash
  git clone https://github.com/PJLab-ADG/LimSim.git

  ```
  ### 2.  CARLA Setup
  Download CARLA: Obtain the CARLA simulator from the [Carla Website](https://carla.org/) or directly from [Github](https://github.com/carla-simulator/carla)

  ### 3. SUMO Setup
  Download and Install SUMO: Follow the instructions on the [SUMO installation guide](https://sumo.dlr.de/docs/index.html#simulation).



  ### 4. Install Python Dependencies
   
  With the main dependencies installed, install the required Python packages for this project:

  ```bash
  cd LimSim
  pip install -r requirements.txt

  ```
## Project Structure
## Acknowledgments

- Special thanks to **PJLab-ADG** for developing and maintaining [LimSim++](https://github.com/PJLab-ADG/LimSim), which has been instrumental in enabling advanced simulations for this project.
- Thanks to the **CARLA** team for their powerful [CARLA simulator](https://carla.org/), which provided a realistic simulation environment essential for testing autonomous driving models.
- Appreciation to the contributors of **SUMO** ([Simulation of Urban MObility](https://sumo.dlr.de/docs/)) for their valuable open-source tool that supports traffic simulation.
