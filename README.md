# NatureGuide

NatureGuide is a simple educational application designed as a proof of concept (PoC) for interoperability between xAI and OpenAI APIs. It uses Gradio for a user-friendly interface to identify and educate about species through image analysis.

## Features

- **Species Identification**: Identify plants, animals, and more from images.
- **Educational Content**: Provides interesting facts about identified species.
- **Dual API Support**: Compatible with both xAI and OpenAI for species recognition.


## Installation
```bash
pip install -r requirements.txt
```

## Usage
1. Set your API key:
   - For xAI: `export XAI_API_KEY='your_api_key'`
   - For OpenAI: `export OPENAI_API_KEY='your_api_key'`
2. Run the app:
   
```bash
python app.py

```
By default, this will start the Flask server. If you prefer to run the Gradio interface directly, you might need to adjust the script or use specific run commands.

## Features
- Species identification from images.
- Educational content about identified species.

## Acknowledgments
- xAI for their innovative AI models.
- OpenAI for their contributions to AI accessibility.
- Gradio for providing an easy-to-use interface for AI applications.


- Supports both xAI and OpenAI APIs.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

## License
[MIT](LICENSE)
