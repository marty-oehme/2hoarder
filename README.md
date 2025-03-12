# Hoarder migration scripts

Simple scripts which try to ease the migration to a self-hosted hoarder instance.

## Wallabag

Use one of the flavours of transferring your wallabag entries into hoarder.
Run it like: `./wallabag2hoarder/convert.py <input-file>`

Where input file is a wallabag json export of all your saved entries.
There are options to change the style of output (netscape HTML, native JSON) and the file to output to.
By default converts to hoard JSON and prints to stdout.
