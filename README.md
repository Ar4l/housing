## Housing Utilities 
Contains scraping & plotting tools. 

#### Install
In a suitable directory, clone the repository with 

```bash 
git clone git@github.com:Ar4l/housing
```

I use `uv` for python package management, it's necessary to run the code in this repo.

```bash
brew install uv   # for MacOS
```

> [Other install options](https://docs.astral.sh/uv/getting-started/installation/)

Lastly, web-scraping with Safari requires enabling remote automation. Go to `Settings > Advanced > Show features for Web Developers`, then `Developer > Allow remote automation`.

#### Usage 

```bash
# Scrape the url defined in housing/scrape/__main__.py
uv run python -m housing.scrape 
```

