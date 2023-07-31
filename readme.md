# ADO-PR-Agent

ADO-PR-Agent is a powerful tool designed to seamlessly connect to your Azure DevOps instance, retrieve commits from a specified pull request, and analyze the changes using the Azure OpenAI service. The result is a comprehensive summary of all the modifications made to each file in the pull request.

## Description

Developers often encounter situations where they need to review and understand the changes made in a pull request thoroughly. This process can be time-consuming and tedious, especially when dealing with large codebases or complex changes.

ADO-PR-Agent simplifies this process by automating the analysis of pull requests and presenting the changes in an easily digestible format. By utilizing the capabilities of Azure OpenAI, the tool intelligently identifies the modifications in the code and generates a summary that highlights the key changes for each file.

## Features

- **Seamless Integration**: Connects effortlessly with your Azure DevOps instance, streamlining the retrieval of pull request data.

- **Smart Analysis**: Utilizes the power of Azure OpenAI to accurately analyze the code changes, providing valuable insights at a glance.

- **Summarized Output**: Presents a concise summary of each file's modifications, making it easier to understand the scope of the changes.

- **Time-Saving**: Automates the review process, saving developers time and effort in manually inspecting pull requests.

## Requirements

- Python 3.x (Replace with the required Python version)
- Azure DevOps Account and Personal Access Token (PAT) for authentication
- Azure OpenAI service API key for code analysis

## Installation

1. Clone the repository: `git clone https://github.com/NiranAmos/ado-pr-agent.git`
2. Navigate to the project directory: `cd ado-pr-agent`
3. Install dependencies: `pip install -r requirements.txt`

## Usage

1. Configure your Azure DevOps account and obtain the Personal Access Token (PAT).
2. Set up the Azure OpenAI service and obtain the API key for code analysis.
3. Configure the tool with the necessary credentials and settings.
4. Run the agent to fetch and analyze pull requests.

## Contributing

We welcome contributions to improve and enhance ADO-PR-Agent. If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/your-feature-name`
3. Make your changes and commit them: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Create a pull request.

## License

Specify the license for your project here. For example: MIT License, Apache License 2.0, etc.

For detailed information on using the tool, refer to the documentation (if available) or reach out to the project maintainers.

Enjoy using ADO-PR-Agent and simplify your pull request reviews with ease!
