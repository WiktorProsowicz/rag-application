# Web

A web application with chat interface. It communicates with backend service in order to obtain either user-related data, context for RAG or LLM responses.


## Development

In order to run the application for development purposes, first activate the environment:

```bash
source .venv/bin/activate
```

Then run the mock interface as a background job / in another terminal:

```bash
python .devcontainer/res/mock_backend.py
```

Finally, in order to leverage the Gradio's reloading feature, run the app via:

```bash
gradio main_dev.py --watch-dirs . --demo-name web_app
```