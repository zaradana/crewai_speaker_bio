# Speaker Introduction System

This system generates professional speaker introductions for events, combining information about the speaker and their company.

## Overview

The Speaker Introduction System is available in two implementations:

1. **Traditional Crew implementation** - Uses CrewAI's crew-based approach
2. **Flow-based implementation** - Uses CrewAI's newer flow-based approach

Both implementations achieve the same goal but use different architectural patterns.

## Components

The system consists of three agents:

1. **Speaker Introduction Agent** - Researches and creates personalized introductions for speakers
2. **Company Showcase Agent** - Researches and creates showcases for companies
3. **Manager Agent** - Combines the outputs into a cohesive final introduction

## Usage

### Running the Flow-based Implementation (Default)

```bash
python -m src.speaker_introduction.main 
```


### Running the Traditional Crew Implementation

```bash
python -m src.speaker_introduction.main --mode crew --speaker "John Doe" --company "Acme Inc" --event "Tech Conference 2023"
```

### Running a Specific Step of the Flow

```bash
python -m src.speaker_introduction.main --mode step --step create_speaker_introduction --speaker "John Doe" --company "Acme Inc" --event "Tech Conference 2023"
```

Available steps:
- `create_speaker_introduction`
- `create_company_showcase`
- `create_final_introduction`

### Testing the Implementation

You can test either implementation with different model configurations:

```bash
# Test the flow implementation (default)
python -m src.speaker_introduction.main --mode test --iterations 3 --model "openai/gpt-4o-mini"

# Test the crew implementation
python -m src.speaker_introduction.main --mode test --iterations 3 --model "openai/gpt-4o-mini" --implementation crew
```

This will run the specified number of iterations with the given model and save the results to the `output/test_results` directory.

### Generating a Flow Visualization

```bash
python -m src.speaker_introduction.main --mode plot
```

This will generate an HTML visualization of the flow in the current directory.

## Output

The system saves the generated introduction to the `output` directory with a filename based on the speaker and event names. 
