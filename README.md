# Facebook page scraper
The python script let's you search for FB pages and scrape their posts (including comments and likes).

## How to
Before carrying out the steps below you need to be a registered FB developer and have a valid access_token from Facebook Graph API.
If you're registered, you can grab a fresh token from https://developers.facebook.com/tools/explorer/

1. Open a new terminal window
2. `git clone git@github.com:chribsen/facebook-pages-scraper.git`
4. `cd facebook-pages-scraper`
3. `python3 facebooky.py`
4. Follow the instructions given in the in the shell

The script uses a 1 second delay between each call in order not to hit the Graph API rate limit. Thus, it might take some time.
When the script is finished, it will output a json file in the parent folder called `<page_id>.json`. For each pagination it will create
a temporary file.

The JSON output has been indented using `json.dumps(output, indent=2)` which increases readability, but significantly increases file size. 
Remove `indent=2` to make the JSON compact.

