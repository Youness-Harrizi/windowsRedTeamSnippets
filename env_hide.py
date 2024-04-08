# code from John hammond video https://www.youtube.com/watch?v=8CiNx4nNqQ0&t=401s
import string
from pprint import pprint
import os
import random

# List of environment variables to be used for obfuscation.
env_vars = [
    "ALLUSERSPROFILE",
    "CommonProgramFiles",
    "CommonProgramW6432",
    "ComSpec",
    "PATHEXT",
    "ProgramData",
    "ProgramFiles",
    "ProgramW6432",
    "PSModulePath",
    "PUBLIC",
    "SystemDrive",
    "SystemRoot",
    "windir",
]

# Create a mapping of printable characters to their positions in environment variable values.
env_mapping = {}
for character in string.printable:
    env_mapping[character] = {}
    for var in env_vars:
        value = os.getenv(var)
        if character in value:
            env_mapping[character][var] = []
            for i, c in enumerate(value):
                if character == c:
                    env_mapping[character][var].append(i)

# Function to obfuscate a given string using the environment variable mapping.
def envhide_obfuscate(string):
    obf_code = []
    for c in string:
        # Get the list of environment variables that contain the character.
        possible_vars = list(env_mapping[c].keys())
        # If the character is not found in any variable, use the ASCII code for obfuscation.
        if not possible_vars:
            obf_code.append(f'[char]{ord(c)}')
            continue

        # Randomly choose one of the variables that contain the character.
        chosen_var = random.choice(possible_vars)
        # Get the list of positions where the character appears in the variable's value.
        possible_indices = env_mapping[c][chosen_var]
        # Randomly choose one of the positions for obfuscation.
        chosen_index = random.choice(possible_indices)

        # Create the PowerShell syntax for accessing the character through the environment variable.
        pwsh_syntax = f'$env:{chosen_var}[{chosen_index}]'
        obf_code.append(pwsh_syntax)
    return obf_code

# Function to further obfuscate the string for PowerShell.
def pwsh_obfuscate(string):
    # Get the obfuscated pieces from envhide_obfuscate function.
    pieces = envhide_obfuscate(string)
    # Join the pieces and include a random integer to form the PowerShell command.
    return f'& ({" , ".join(pieces)} -Join ${random.randint(1, 9999)})'

# Example PowerShell command to obfuscate.
powershell_command = 'dir'
# Obfuscate the command and print the result.
print(pwsh_obfuscate(powershell_command))
