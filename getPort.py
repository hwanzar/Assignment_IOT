import re

# Read the content of output.txt
with open("ports.txt", "r") as file:
    output = file.read()

# Use regular expressions to find the PTY devices
matches = re.findall(r'PTY is (\S+)', output)

# Extract the PTY devices and save them in variables
if len(matches) == 2:
    pty1, pty2 = matches
    print("PTY 1:", pty1)
    print("PTY 2:", pty2)
else:
    print("Unable to find PTY devices in the output.")