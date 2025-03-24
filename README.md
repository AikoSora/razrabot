# RAZRABOT

Parsing keywords from WB product

Using private dependencies [quirkink](https://github.com/Quirkink)


## Install

Create a virtual environment

```bash
python3.11 -m venv env
```

Activate venv

```bash
source env/bin/activate
```

Install poetry

```bash
python -m pip install poetry
```

Install dependencies

```bash
poetry install
```

## Configure project

```bash
cp .env.dist .env
```

```bash
nano .env
```

## Run bot

```bash
python parser/main.py
```
