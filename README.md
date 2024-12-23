# 1Password to Apple Password Converter

This script attempts to mangle 1password .1pif file formated exports into an Apple Password CSV import file.

If you have exported the 1password fault as 1pif file you should be able to do something like this:
```
python3 mangle.py data.1pif > out.csv
```

The resulting CSV should import correctly in Apple Passwords. Including secure notes and OTP URIs.

## Caveats

The 1pif format includes a few different possible fields for the same value (i.e. multiple locations where you might find the password). This script attempts to find the right one and fall back to other possible locations in the json format.

## Bugs

If you run into bugs please create a PR with a fix.