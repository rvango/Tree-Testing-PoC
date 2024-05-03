# Tree Testing interface demo

## Overview

This project provides a Python-based implementation of a Tree Testing Interface, designed to mimic the experience and
rules of navigating a Tree Test task on a platform like Kort. 
Users navigate a hierarchical tree structure, while the system records their paths and timestamps.
This interface can also be adapted for use as a LangChain tool.

## Usage

Create Conda environment:

```bash
conda env create -f environment.yml
```

Activate Conda environment:

```bash
conda activate tree-testing-poc
```

Run the proof of concept:

```bash
python poc
```

## Features

- **Interactive tree testing**: Turn by turn navigation through a hierarchical tree structure.
- **Navigation options**: At each node, users are presented with a list of available options to choose from, such as '
  _Electronics_', '_Clothing_', '_Books_', etc.
- **Submit or Give Up**: Users can submit their final choice or give up at any point.
- **Metrics recording**: The interface records metrics such as the navigation path and timestamps for each node visited.

## Example output

```plaintext
Current node: [/]
Available options: 'Electronics', 'Clothing', 'Books' or 'SUBMIT' or 'GIVE_UP'
 Enter your choice from the options above: Books
 
Current node: [Books]
Available options: 'Electronics', 'Clothing', 'Books', 'Books/Fiction', 'Books/Non-Fiction' or 'SUBMIT' or 'GIVE_UP'
 Enter your choice from the options above: Books/Fiction
 
Current node: [Books/Fiction]
Available options: 'Electronics', 'Clothing', 'Books', 'Books/Fiction', 'Books/Fiction/Novels', 'Books/Fiction/Short Stories', 'Books/Non-Fiction' or 'SUBMIT' or 'GIVE_UP'
 Enter your choice from the options above: Books/Fiction/Novels
 
Current node: [Books/Fiction/Novels]
Available options: 'Electronics', 'Clothing', 'Books', 'Books/Fiction', 'Books/Fiction/Novels', 'Books/Fiction/Novels/Sci-Fi', 'Books/Fiction/Novels/Fantasy', 'Books/Fiction/Short Stories', 'Books/Non-Fiction' or 'SUBMIT' or 'GIVE_UP'
 Enter your choice from the options above: Books/Fiction/Novels/Sci-Fi
 
Current node: [Books/Fiction/Novels/Sci-Fi]
Available options: 'Electronics', 'Clothing', 'Books', 'Books/Fiction', 'Books/Fiction/Novels', 'Books/Fiction/Novels/Sci-Fi', 'Books/Fiction/Novels/Fantasy', 'Books/Fiction/Short Stories', 'Books/Non-Fiction' or 'SUBMIT' or 'GIVE_UP'
 Enter your choice from the options above: SUBMIT
 
Recorded metrics: [2024-05-01 10:44:44 - Books], [2024-05-01 10:44:52 - Books/Fiction], [2024-05-01 10:45:00 - Books/Fiction/Novels], [2024-05-01 10:45:04 - Books/Fiction/Novels/Sci-Fi]
Submitted: Books/Fiction/Novels/Sci-Fi
```

## Edge cases covered

- **Duplicate paths**: The interface prevents recording duplicate navigation paths to avoid redundant metrics. Another
  way to handle this would be to filter out duplicate paths during data analysis.

## Adaptation for LangChain

By presenting the output _"Available options: ..."_ to an LLM agent and prompting it to make a selection, we can
replicate the decision-making process of a human using Kort.
However, it crucial to ensure that all edge cases of Kort are covered to ensure a fair comparison between human and LLM
users.

## Alternative Integration Method

Initially, I explored the possibility of directly integrating an LLM with Kort to participate in unmoderated tree
testing. This method would have required creating hooks into Kort to interface with an LLM, given that Kort lacks a
dedicated API.

The primary solutions considered were:

- Developing an API for Kort: This would involve extending Kort's functionality to support API calls, allowing direct
  communication with an LLM.
- Using a WebDriver: This approach would simulate user interactions with Kort through a browser automation tool, thereby
  enabling the LLM to navigate the tree testing experiment.

However, both options presented significant challenges. Developing an API would require extensive modifications to
Kort's existing architecture, and using a WebDriver seems complex and brittle.

As a result, I recommend for a simpler and possibly more robust solution: replicating Kort's rules and actions within a tailored
tool.
This tool provides a clear, step-by-step interaction model for LLMs, closely mimicking the human user experience on Kort
but in a constrained, easily manageable environment.

# BONUS: Conversion tool for Kort

This project includes a `convert_to_kort.py` script that facilitates populating Kort with tree tests using a friendly structure.

## Usage

```bash
python convert_to_kort.py tree.json
```

To output the data in a compact format, use the --compact flag instead:

```bash
python convert_to_kort.py tree.json --compact
```

The script will convert the tree structure into the Kort-compatible format and display the result in the terminal. The output can then be copied and pasted into the MongoDB table to populate the database with the tree structure.