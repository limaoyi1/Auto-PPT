# Auto_PPT: Generate Your PPT Automatically

## 中文指南
> 中文用户请移步 [中文指南](./Readme.md).

## Project Introduction

> Generate PPTX files with specified themes using gpt-3.5-turbo and pptx.

## Project Advantages

> 1. Users can generate a new PPTX by simply entering a title.
> 2. Utilizes the gpt-3.5-turbo-16k interface to ensure stable generation of PPT outlines.
> 3. Creatively uses the CSV format to generate PPT text, making it easier to create and generate stable PPTX files.
> 4. Utilizes Unsplash to obtain illustrations.
> 5. Can be deployed locally by adding your OpenAI API key and Unsplash API key information.

## Deployment Guide

> 1. Create a virtual environment

```bash
python -m venv venv
```

> 2. Activate the virtual environment

```bash
. venv/bin/activate
```

> 3. Install the required Python dependencies

```bash
pip install -r requirements.txt
```

> 4. Add your API key to the config.ini file

> 5. Run the project

```bash
python application.py
```

> 6. Visit [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Next Version

> 1. Deploy online services
> 2. Optimize generated content and provide more accurate generation services.
> 3. Improve generation formats to support multiple styles and templates.
> 4. Add a more user-friendly web UI.
> 5. Optimize the generation speed. The speed of the gptApi is currently too slow.

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=limaoyi1/Auto_PPT&type=Timeline)](https://star-history.com/#limaoyi1/Auto_PPT&Timeline)