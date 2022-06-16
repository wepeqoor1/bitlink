# Bitly url shorterer
Generate short link(Bitlink) from URL and gives total clicks from Bitlink.
***

## How to install
Python3 should be already installed. Then use pip (or pip3, if there is a conflict with Python2) to install dependencies:
```bash
$ pip install -r requirements.txt
```
***

## How to use
### Register on Bitly service https://bitly.com/
Sign up for Bitly via email instead of social media. This will make it easier to get the token.

### Get `API_KEY` https://app.bitly.com/settings/integrations/. 
Need token "GENERIC ACCESS TOKEN".

### Environment variables
Put API_TOKEN=<`API_KEY`> in `.env` file.

### Start script
```bash
$ python3 main.py
```
Next, you can enter a `URL` or `Bitlink`.
