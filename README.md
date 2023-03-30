# A reinforcement learning environment for tiramisu autoscheduler

This project offers a ready to use environment for the reinforcement learning project.

## Installation

To use this project, you'll need to do the following:

1. Clone the repository to your local machine.
2. Make sure you have Anaconda installed.
3. Update the paths in the `env_api/utils/config/config.yaml` file to match your preferences.

## Usage

To run the project, do the following:

1. Activate the conda environment:
`conda activate <tiramisu_env>`
2. You need to have some generated Tiramisu cpp functions to optimize.
3. Use `TiramisuEnvAPI()` to do the following : select a program, apply a transformation on the program, get the speedup of the schedule and the representation.
4. You can find the code of the reinforcement learning agent under `rl_agent/`

## Contributing

If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your changes.
3. Make your changes and test them thoroughly.
4. Submit a pull request.
