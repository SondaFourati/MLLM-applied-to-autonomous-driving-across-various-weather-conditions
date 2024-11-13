# MLLM applied to autonomous driving across various weather conditions

Table of Contents:
Introduction
Project Overview
Requirements
Installation
Project Structure
Usage
Results and Performance
Contributing
License
Acknowledgments
Introduction
This project explores the use of Multimodal Large Language Models (MLLMs) in autonomous driving applications, specifically under challenging environmental conditions. By leveraging GPT-4 and the LimSim++ simulator integrated with CARLA, this project investigates how MLLMs can be applied to improve the performance of autonomous vehicles by adapting to various weather conditions using different sensor setups (e.g., front and back cameras, LiDAR).

Project Overview
Objective: To enhance autonomous driving capabilities by applying MLLMs in harsh environmental conditions.
Simulator: LimSim++ integrated with CARLA for realistic simulation environments.
Weather Conditions: Tested across a range of adverse conditions (rain, fog, snow, etc.).
Sensors Used: Camera (front, back) and LiDAR for a comprehensive sensory setup.
Requirements
To run this project, you need the following dependencies and tools:

Python 3.8+
LimSim++
CARLA Simulator
Additional Python packages:
torch
transformers
opencv-python
numpy
pandas
matplotlib
scipy
Use requirements.txt if provided, or install packages manually:

bash
Copier le code
pip install torch transformers opencv-python numpy pandas matplotlib scipy
Installation
Clone the Repository:

bash
Copier le code
git clone https://github.com/your-username/MLLM-Autonomous-Driving.git
cd MLLM-Autonomous-Driving
Set up LimSim++ and CARLA:

Follow the instructions provided on the LimSim++ GitHub page to install LimSim++.
Set up CARLA by following CARLA installation instructions.
Install Python Dependencies:

bash
Copier le code
pip install -r requirements.txt
Configuration:

Ensure all environment variables and paths are correctly configured for LimSim++ and CARLA.
Create a .env file (optional) to store configuration variables, like API keys or model paths, if needed.
Project Structure
Here's an overview of the project structure and the purpose of each file:

plaintext
Copier le code
MLLM-Autonomous-Driving/
│
├── ExampleEvaluator1.py                # Evaluates MLLM performance in simulation
├── ExampleVLMAgentCloseLoop6cam1.py     # MLLM agent setup with camera-based sensing
├── ExampleVLMAgentCloseLoop6camLidarPrompt.py # MLLM agent setup with LiDAR and camera data
├── MPGUl6cam.py                         # Multi-purpose graphical interface for 6-camera setup
├── Model2.py                            # Model definition and loading for autonomous driving
├── README.md                            # Project documentation
└── results/                             # Folder for storing output and result data (logs, images, etc.)
File Descriptions
ExampleEvaluator1.py: Script to evaluate the performance of MLLMs under various weather conditions and sensor setups.
ExampleVLMAgentCloseLoop6cam1.py: Implements the MLLM agent for close-loop control using only camera inputs.
ExampleVLMAgentCloseLoop6camLidarPrompt.py: Extends the MLLM agent to include both LiDAR and camera inputs for more accurate sensing.
MPGU16cam.py: GUI to visualize sensor data from the 6-camera setup.
Model2.py: Model architecture, training, and loading functions for deploying MLLMs in autonomous driving.
Usage
Run MLLM Evaluation: This script evaluates the MLLM performance under various conditions.

bash
Copier le code
python ExampleEvaluator1.py --weather 'rain' --sensors 'camera'
Run Agent with Camera and LiDAR Setup: This command initiates the MLLM agent with camera and LiDAR input.

bash
Copier le code
python ExampleVLMAgentCloseLoop6camLidarPrompt.py --weather 'fog' --sensors 'camera, lidar'
Visualize with GUI: Open the GUI to monitor real-time sensor input and model predictions.

bash
Copier le code
python MPGUl6cam.py
Model Training (Optional): If you wish to retrain or fine-tune the MLLM, use Model2.py.

bash
Copier le code
python Model2.py --train --data-path 'data/training_data'
Experimentation: Modify parameters in each script to test different weather conditions, sensor configurations, and model settings.

Results and Performance
Weather Conditions Tested: The model was evaluated under various weather conditions (e.g., clear, rain, fog, snow) using CARLA.
Performance Metrics: Results are stored in the results/ directory, containing performance logs and visual outputs.
Sample Results:
Accuracy of navigation and obstacle avoidance across different conditions.
Model predictions visualized using 6-camera GUI (MPGU16cam).
Example Graph: Add sample images or graphs here showing the MLLM's performance under different conditions.
Contributing
We welcome contributions! To contribute:

Fork the repository.
Create a new branch for your feature (git checkout -b feature-name).
Commit your changes (git commit -am 'Add new feature').
Push to your branch (git push origin feature-name).
Create a Pull Request.
Please follow the contribution guidelines for more details.

License
This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgments
Special thanks to PJLab-ADG for LimSim++ and the CARLA team for their invaluable simulation environment.
Thanks to contributors and the open-source community for libraries like PyTorch and Transformers.

