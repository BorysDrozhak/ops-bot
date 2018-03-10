# You own Bot for OPS guys

### The ideas
* I'd like to work with my laptop via my phone
* I don't want to take care of how to teach a bot about all things I want, so let it be just anything my PC can do, like I'm using just my terminal
* I do not like the idea to rewrite code each time I want to see new actions my bot can do, so I want to use just a config file which will generate actions/handlers for the bot.

### Concept 
toml file will be the core here. It will generate needed buttons, inlines and handlers for the bot.

### A simple example of how it should be
I want to see my files by `/ls` command , but each of the file should be `inline`. Once I press the inline - it should cat the file to the chat.
note: (telegram inlines it is a buttons in the chat, instead of text. These ones you can click as well as just buttons but they don't print out the command to the chat). </br>

Have a look to the next syntax below:

```
[ command ]
name = ls
type = sh
action = 'cat <ARGS>'
[[ inlines ]]
type = sh
action = 'ls -ha'
```

So, what it should do.
1. Once you type `/ls` in the chat with bot - it should show you all files in the directory as inlines. It should execute `ls -ha` and convert the output to inlines buttons.
2. Each of the inlines callback with command `/ls name_of_the_file`.
3. For any callbacks with pattern `/ls <ARGS>` The bot should `cat` the file

### Sum up
1. command block declares a command I want
2. name is actually want I should write to the chat with command prefix `/` to execute a command
3. type declares a way of how to execute a command. Sh - means use python subprocess module for executing shell commands.
4. Inlines block declares which inlines to show once you press `/command`
4.a. output of the action will be processed and each line will be converted to an inline.
4.b Each inline should callback with pattern: `/command.name $inlines.action.output`

## Security
By declaring additional decorators which have control over a message the bot recipes, currently, We are able to restrict:
* people who can interact with bot(see toml file examples)
* public/secure functions
* restrict received time of messages to proceed.

## development
more docs are coming soon, here is a plenty of work.