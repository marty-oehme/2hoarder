# Shaarli 2 Hoarder converter

Convert your shaarli bookmarks to hoarder json format.

Simply run it like the following `uv run python convert.py <shaarli-export-file>`,
pointing th efile at your exported html file from shaarli.

It will print out the JSON representation of those bookmarks, 
readable by Hoarder.

Run it like the following `uv run python convert.py bookmarks.html > out.json`
to generate a valid json file which you can then import thorugh the hoarder interface.
