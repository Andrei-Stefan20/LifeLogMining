# Event Log Analysis and Process Mining

## Overview
This project is designed to analyze and discover process models from event logs using various process mining techniques. The implementation leverages the **PM4Py** library to perform process discovery, evaluation, and conformance checking. The models are extracted using **Alpha Miner**, **Heuristics Miner**, and **Inductive Miner**, then visualized and assessed for performance.

## Features
- **Load and preprocess event logs** from XES files.
- **Extract process structures** including traces, events, and activities.
- **Apply process discovery algorithms** (Alpha, Heuristics, and Inductive Miner).
- **Visualize generated process models** using Petri nets.
- **Evaluate models** based on process conformance and fitness.
- **Check conformance** through token-based replay analysis.

## Prerequisites
Ensure you have Python installed (recommended version 3.8+). The required dependencies are listed below:

### Install Required Packages
```bash
pip install pm4py
```

## Usage
### 1. Prepare Your Event Log
Ensure you have an event log file in `.xes` format. Place it in the `Datasets/` directory.

### 2. Run the Analysis
Execute the script using:
```bash
python Scripts/process_mining.py
```

### 3. Outputs
- The script will print statistics about the event log, including traces and activities.
- Generated Petri net models will be saved in `PetriNets/`.
- Model evaluations will be printed in the console.
- Conformance checking results will be displayed.

## File Structure
```
ProcessMiningProject/
├── Datasets/
│   ├── ProcessLog_Original_20231027.xes
│   ├── ProcessLog_ClaudeAugmented_20231027.xes
│   └── ProcessLog_GeminiAugmented_20231027.xes
├── PetriNets/
│   ├── PetriNets_Original/
│   │   └── ... (immagini)
│   ├── PetriNets_ClaudeAugmented/
│   │   └── ... (immagini)
│   └── PetriNets_GeminiAugmented/
│       └── ... (immagini)
├── Scripts/
│   └── process_mining.py
└── README.md
```

## Functions Overview
### Load Event Log
```python
log, log_df = load_event_log(file_path)
```
- Converts XES logs into a structured format.

### Process Discovery
```python
models = apply_discovery_algorithms(log, filtered_log)
```
- Extracts process models using different mining techniques.

### Visualization
```python
visualize_models(models)
```
- Saves Petri nets in `PetriNets/` for each discovered model.

### Conformance Checking
```python
check_conformance(filtered_log, *models["inductive_filtered"])
```
- Evaluates how well the process model aligns with actual event logs.

## Contributing
Feel free to contribute by improving the code, adding more evaluation techniques, or refining the visualization methods.

## License
This project is open-source and available under the MIT License.

