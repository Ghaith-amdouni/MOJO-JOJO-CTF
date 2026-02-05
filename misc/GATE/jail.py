import gdb

# The list of commands to block
# We aim to block all high-level execution methods to force the memory call solution.
BLOCKLIST = [
    # Shell escapes
    "shell", "system", "!", "pipe", "|",
    
    # Scripting languages (if compiled in)
    "python", "pi", "py", 
    "guile", "gu",
    
    # Process control/loading that might reset the jail
    "exec-file", "file", "exec", 
    "target", 
    "attach", 
    "core-file",
    
    # Aliasing and Definitions (could be used to unblock or obfuscate)
    "define", "document",
    "usage", "alias", 
    "macro",
    
    # Alternate execution
    "interpreter-exec", 
    
    # Sourcing (force manual interaction or logging workaround if really needed, 
    # but strictly we want direct memory calls so blocking source is good)
    "source", "so" 
]

class JailCommand(gdb.Command):
    """A restricted placeholder for dangerous commands."""
    def __init__(self, name):
        super(JailCommand, self).__init__(name, gdb.COMMAND_USER)
        self.name = name

    def invoke(self, arg, from_tty):
        gdb.write(f"NO! Command '{self.name}' is blocked! GO DOWN BITCH!\n", gdb.STDERR)

# Register a hook for every dangerous command
for cmd in BLOCKLIST:
    try:
        JailCommand(cmd)
    except Exception as e:
        # Ignore if command doesn't exist or collision
        pass

# Disable auto-loading
gdb.execute("set auto-load off")
gdb.execute("set pagination off")
gdb.execute("set confirm off") # Don't ask for confirmation when quitting or running

print("The GATE is closed. You are in the jail.")
print("Do you know what gdb stands for?")
print("GO DOWN BITCH!!!!!!")
