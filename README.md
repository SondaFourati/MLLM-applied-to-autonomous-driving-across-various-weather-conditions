# MLLM applied to autonomous driving across various weather conditions


## Table of Contents
1. [Introduction](#introduction)
2. [Project Overview](#project-overview)
3. [Requirements](#requirements)
4. [Installation](#installation)
5. [Project Structure](#project-structure)
6. [Usage](#usage)
7. [Acknowledgments](#acknowledgments)
8. [Citation](#Citation)




## 1.Introduction
This project explores the use of Multimodal Large Language Models (MLLMs) in autonomous driving applications, specifically under challenging environmental conditions. By leveraging GPT-4 and the LimSim++ simulator integrated with CARLA, this project investigates how MLLMs can be applied to improve the performance of autonomous vehicles by adapting to various weather conditions using different sensor setups (e.g., front and back cameras, LiDAR).

## 2. Project Overview
- **Objective**: To enhance autonomous driving capabilities by applying MLLMs in harsh environmental conditions.
- **Simulator**: [LimSim++](https://github.com/PJLab-ADG/LimSim) integrated with CARLA for realistic simulation environments.
- **Weather Conditions**: Tested across a range of adverse conditions (Heavy rain,fog,Storm,wetness).
- **Sensors Used**: Camera (front, back) and LiDAR for a comprehensive sensory setup.

## 3.Requirements

To run this project, you need the following dependencies and tools:
- Python 3.9.0 +
- [LimSim++](https://github.com/PJLab-ADG/LimSim)
- [CARLA Simulator](https://github.com/carla-simulator/carla)
- [SUMO Simulator](https://www.eclipse.org/sumo/) (for additional simulation of traffic and urban mobility)
- Additional Python packages:
  - `pytorch`
  - `transformers`
  - `opencv-python`
  - `numpy`
  - `pandas`
  - `matplotlib`
    
 ## 4.Installation

  ### 4.1. LimSim++ Setup

  Download and Install LimSim++: Follow the official instructions from [LimSim++ GitHub page](https://github.com/PJLab-ADG/LimSim).


  ### Example command to install LimSim++

  ```bash
  git clone https://github.com/PJLab-ADG/LimSim.git

  ```
  ### 4.2.  CARLA Setup
  Download CARLA: Obtain the CARLA simulator from the [Carla Website](https://carla.org/) or directly from [Github](https://github.com/carla-simulator/carla)
  and download [AdditionalMaps_0.9.15.zip](https://github.com/carla-simulator/carla/releases)

  ### 4.3. SUMO Setup
  Download and Install SUMO: Follow the instructions on the [SUMO installation guide](https://sumo.dlr.de/docs/index.html#simulation).



  ### 4.4. Install Python Dependencies
   
  With the main dependencies installed, install the required Python packages for this project:

  ```bash
  cd LimSim
  pip install -r requirements.txt

  ```
## 5.Project Structure


The following files have been modified or newly added to achieve the specific results required for this project. These files may need to be integrated into the main LimSim++ repository for broader use.

```Plaintext
MLLM-Autonomous-Driving/

├── ExampleEvaluator1.py                # evaluation script for obtaining simulation results under specific performance metrics
├── ExampleVLMAgentCloseLoop6cam1.py     # New MLLM agent setup script using a 6-camera system
├── ExampleVLMAgentCloseLoop6camLidarPrompt1.py # New MLLM agent setup script with LiDAR and 6-camera integration
├── MPGUl6cam.py                         # New GUI script for visualizing simulation with a 6-camera setup
├── Model2.py                            # Modified model enables selection of specific weather conditions

```
## 6.Usage

This section provides instructions on how to use the modified files for running simulations, evaluating models, and visualizing results.

### 6.1. Evaluating MLLM Performance
Use `ExampleEvaluator1.py` to evaluate the performance of the Multimodal Large Language Model (MLLM) under different simulation conditions.

#### Run Evaluation Script
```bash
python ExampleEvaluator1.py
```
### 6.2. Running the MLLM Agent with a 6-Camera Setup
ExampleVLMAgentCloseLoop6cam1.py configures an MLLM agent to operate using a 6-camera system for environment sensing.

#### Run Agent with 6-Camera Setup
```bash
python ExampleVLMAgentCloseLoop6cam1.py
```

### 6.3. Running the MLLM Agent with Camera and LiDAR Setup
Use ExampleVLMAgentCloseLoop6camLidarPrompt1.py for a setup that integrates both camera and LiDAR inputs, offering a more comprehensive view of the environment.
This configuration is especially useful for evaluating the agent’s performance in low-visibility conditions.
#### Run Agent with Camera and LiDAR Setup
```bash
python ExampleVLMAgentCloseLoop6camLidarPrompt1.py
```
Under SimModel, integrate: Model3Update.py

### 6.4. Updated interface with 6 cameras
To monitor and visualize data from the 6-camera setup, use the MPGUl6cam.py GUI script. 
This graphical interface allows real-time observation of the simulation environment as perceived by the agent.

Launch 6-Camera Visualization GUI
```bash
python MPGUl6cam.py
```
This will open a GUI displaying the output from each of the six cameras, enabling you to visually track the agent’s perception in real-time.

### 6.5. Changing Weather Conditions in the Simulation
In this script, you can select specific weather conditions or customize weather settings, allowing for enhanced testing under various environmental scenarios

```bash
python Model2.py 
```
## 7.Acknowledgments

- Special thanks to **PJLab-ADG** for developing and maintaining [LimSim++](https://github.com/PJLab-ADG/LimSim), which has been instrumental in enabling advanced simulations for this project.
- Thanks to the **CARLA** team for their powerful [CARLA simulator](https://carla.org/), which provided a realistic simulation environment essential for testing autonomous driving models.
- Appreciation to the contributors of **SUMO** ([Simulation of Urban MObility](https://sumo.dlr.de/docs/)) for their valuable open-source tool that supports traffic simulation.
  
## 8.Citation
To cite our work,use the following BibTeX entry:

```bash
@article{author2024,
  title={A Novel MLLM-based Approach for Autonomous Driving in Different Weather Conditions},
  author={Sonda Fourati, Wael Jaafar, Noura Baccar},
  journal={IEEE Transactions on Intelligent Transportation Systems},
  year={2024},
  url={[https://link-to-article.com](https://arxiv.org/abs/2411.10603)}
}
```

