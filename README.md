# SysPmt README

## Overview
SysPmt is a Python-based tool designed to convert pseudo-code written in a Python-like syntax into precise and actionable system prompts for Large Language Models (LLMs). This tool is intended to help developers and prompt engineers who are adept at programming but may need assistance in crafting effective system prompts for LLMs.

## How It Works
SysPmt processes a pseudo-code file (`.pmt`) and a configuration file (`.yaml`) to translate the pseudo-code into a system prompt using the mappings defined in the YAML configuration. The generated text is then provided to an LLM (in our case, ChatGPT 4) to create the final system prompt.

## Installation and Setup
1. Clone the repository:
   ```bash
   git clone [repository-url]
   ```
2. Ensure Python 3.x is installed on your machine.
3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Replace the placeholder API key in the script with your actual OpenAI API key.

## Usage
Run SysPmt by specifying the paths to your configuration and pseudo-code files:
```bash
python3 syspmt.py --config path/to/config.yaml --prompt path/to/prompt.pmt
```

## Configuration File (`config.yaml`)
The configuration file defines translations and message formats for converting pseudo-code into prompts. Here is an example configuration:
```yaml
messages:
  assign: "The AI assistant's '{var}' is set to {value}."
  if_condition: "If the condition '{condition}' is met, perform the following actions:"
  else_condition: "Otherwise, perform the following actions:"

translations:
  check_language: "check if the language is"
  mission: "set the mission to"
  context: "set the context to"
  reject: "reject with the message:"
  proceed: "Proceed with the request"
```

## Pseudo-Code File (`prompt.pmt`)
This file contains your custom pseudo-code. Example:
```python
mission = "travel agency support"
context = "travel discussion"
language = "English"
age = 28
gender = "Male"

if check_language(language):
    mission(mission)
    context(context)
elif check_language("French"):
    mission("French travel consultant specializing in Paris")
    context("discussion about travel offers in Paris")
else:
    reject("We are sorry, we cannot assist you at the moment.")

if context("travel discussion"):
    if check_language("English"):
        mission("English travel specials")
        context("exploring travel packages tailored for English speakers")
    elif check_language("Spanish"):
        mission("Spanish travel specials")
        context("exploring travel packages tailored for Spanish speakers")
    else:
        proceed()
elif context("adventure tourism"):
    mission("adventure tourism specialist")
    context("providing information on adventure tourism packages")
    if check_language("German"):
        mission("German-speaking adventure tourism specialist")
    else:
        proceed()
else:
    reject("Unfortunately, we cannot provide assistance for this request. Please check your input and try again.")
```

## Output
SysPmt outputs system prompts ready for LLM processing. Example output based on the above pseudo-code:
```
As a 28-year-old male AI assistant set in the travel agency support mission, and operating in a travel discussion context, your task is to communicate in English. However, you need to attend to the user query dynamically according to the preferred language. If you detect that the user's language is English, you should continue providing assistance about travel discussions as an English travel specials consultant. But if the user shifts the language to French, your role must be changed to a French travel consultant specializing in Paris, discussing travel offers in that region. 

Nonetheless, if any other language than English or French is detected, you are supposed to inform the user with a message, stating, 'We are sorry, we cannot assist you at the moment.'. Also, it is important that you adjust the discussion context according to the user's command. If the context switches to 'travel discussion,' you should cater to the user in the language they are speaking, English or Spanish, exploring travel packages tailored for English or Spanish speakers, respectively. Still, if the user's language is different from these two, you should proceed with the initial settings. 

Conversely, if the context becomes 'adventure tourism,' modify your mission to an adventure tourism specialist, and if the user is speaking German, serve as a German-speaking adventure tourism specialist. But, should the language setting not be identified or if the context does not match any predefined settings, you should provide a message that states, 'Unfortunately, we cannot provide assistance for this request. Please check your input and try again.'.
```

## Contributions
Contributions are welcome! Please fork the repository, make your modifications, and submit a pull request for review.