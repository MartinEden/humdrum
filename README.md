# humdrum
Shows you which of your repos are active

## Usage
1. Set up a settings.json file in the root of the repo that looks something like this:
```json
{
    "repos": [
        "ssh://hg@bitbucket.org/MartinEden/goodreads-suggestor", 
        "git@github.com:MartinEden/humdrum.git", 
    ], 
    "data_path": "path/to/where/to/store/data"
}
```
2. Run `python repositories.py`. This will take a long time the first time you run, as it has to clone all of the repos into data_path. In the future it will be quicker, as it will only be syncing changes (unless you add new repos to settings.json).
3. Run `python main.py`, or otherwise get the flask web app running, and point your browser at it.
