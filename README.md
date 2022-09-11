A discord bot that uses the model davinci_002 from gpt-3 to answer whatever you say to it.
The bot also has a text to speech function.

Created by hacktail and Spannnn45

# Usage

After cloning this repository begin with running

```python
pip install -r requirements.txt 
``` 

in working directory.

In .env write

```
OPENAI_APIKEY=yourApiKey
DISCORD_TOKEN=yourDiscordToken
```

where yourApiKey is your openai api key and yourDiscordToken is the token for your discord bot.

now you should be able to run
```shell
python main.py 
```

# Commands

la! "used to change the language pronounciation. An example is en for english"

!gen "What you wanna say to the gpt-3 bot"

!join "for it to join the voice channel that the user who wrote the command is in"

!stop "for it to finish the thing it's saying on the voice channel"
