# ============================================================================
# STAGE 1: BUILD SECURE FLAG READER
# ============================================================================
FROM ubuntu:22.04 AS builder
RUN apt-get update && apt-get install -y gcc libc6-dev
RUN echo '#include <stdio.h>\n\
    #include <stdlib.h>\n\
    int main() {\n\
    if (getenv("ESCAPED_PLATFORM") == NULL) {\n\
    printf("ERROR: Security breach detected! You must be in a verified session to access this tool.\\n");\n\
    return 1;\n\
    }\n\
    FILE *f = fopen("/opt/.secrets/flag.txt", "r");\n\
    if (f == NULL) {\n\
    perror("Error opening flag file");\n\
    return 1;\n\
    }\n\
    char c;\n\
    while ((c = fgetc(f)) != EOF) putchar(c);\n\
    fclose(f);\n\
    return 0;\n\
    }' > flag_reader.c
RUN gcc -O2 -static -o flag_reader flag_reader.c

# ============================================================================
# STAGE 2: FINAL CHALLENGE IMAGE
# ============================================================================
FROM ubuntu:22.04
# Install ONLY what's absolutely necessary
RUN apt-get update && apt-get install -y \
    bash \
    coreutils \
    tar \
    socat \
    && rm -rf /var/lib/apt/lists/*

# Create challenge user with rbash
RUN useradd -m -s /bin/rbash ctfuser

# STEP 1: CREATE ALL DIRECTORIES AND FILES FIRST
RUN mkdir -p /opt/.secrets && \
    echo "MOJO-JOJO{W0W_YOU_F0UND_IT_DO_YOU_WANT_A_B4NAN4_FOR_Y0UR_MEDIOCRE_EFFORT?!!}" > /opt/.secrets/flag.txt && \
    # Flag is root-only! Forces the use of the SUID reader.
    chown root:root /opt/.secrets/flag.txt && \
    chmod 400 /opt/.secrets/flag.txt && \
    chown root:root /opt/.secrets && \
    chmod 700 /opt/.secrets

# Sarcastic Decoys
RUN echo "MOJO-JOJO{oh_look_at_me_im_hacking_a_fake_flag_so_pro}" > /home/ctfuser/flag.txt && \
    echo "MOJO-JOJO{yup_this_is_totally_the_flag_keep_looking_here_forever}" > /tmp/flag.txt && \
    echo "MOJO-JOJO{is_your_iq_equivalent_to_a_bowl_of_cereal?_look_deeper!}" > /home/ctfuser/.flag

# Setup hidden bins directory
RUN mkdir -p /opt/hidden_bins

# Copy the secure flag_reader from builder
COPY --from=builder /flag_reader /opt/hidden_bins/flag_reader

# Create empty jail directory and add tar symlink + stubs for clean startup
RUN mkdir -p /home/ctfuser/jail && \
    ln -s /bin/tar /home/ctfuser/jail/tar && \
    echo '#!/bin/sh' > /home/ctfuser/jail/groups && \
    echo '#!/bin/sh' > /home/ctfuser/jail/locale-check && \
    chmod +x /home/ctfuser/jail/groups /home/ctfuser/jail/locale-check

# Create test files for tar
RUN echo "Production backup data" > /home/ctfuser/testfile && \
    echo "Server logs backup" > /home/ctfuser/logs.txt && \
    echo "Configuration backup" > /home/ctfuser/config.txt

# Add realistic but unhelpful files
RUN echo "backup-server-01" > /home/ctfuser/hostname && \
    echo "System operational" > /home/ctfuser/status.log && \
    echo "2024-12-08 03:00:00 - Backup started" > /home/ctfuser/backup.log && \
    echo "2024-12-08 03:45:23 - Backup completed" >> /home/ctfuser/backup.log && \
    mkdir -p /home/ctfuser/work

# Create welcome script
RUN echo '#!/bin/bash' > /usr/bin/welcome.sh && \
    echo 'echo "=================================================="' >> /usr/bin/welcome.sh && \
    echo 'echo " RESTRICTED BACKUP SERVER"' >> /usr/bin/welcome.sh && \
    echo 'echo "=================================================="' >> /usr/bin/welcome.sh && \
    echo 'echo ""' >> /usr/bin/welcome.sh && \
    echo 'echo "User: ctfuser"' >> /usr/bin/welcome.sh && \
    echo 'echo "Access Level: RESTRICTED"' >> /usr/bin/welcome.sh && \
    echo 'echo ""' >> /usr/bin/welcome.sh && \
    echo 'echo "This system is for authorized use only."' >> /usr/bin/welcome.sh && \
    echo 'echo "Unauthorized access is prohibited."' >> /usr/bin/welcome.sh && \
    echo 'echo ""' >> /usr/bin/welcome.sh && \
    echo 'echo "=================================================="' >> /usr/bin/welcome.sh && \
    echo 'echo ""' >> /usr/bin/welcome.sh && \
    chmod +x /usr/bin/welcome.sh

# STEP 2: CONFIGURE RBASH
RUN echo 'if [ -f ~/.bashrc ]; then . ~/.bashrc; fi' > /home/ctfuser/.bash_profile && \
    echo 'if [[ "$0" == *rbash* ]]; then' > /home/ctfuser/.bashrc && \
    echo '  /usr/bin/welcome.sh' >> /home/ctfuser/.bashrc && \
    echo '  export PATH=/home/ctfuser/jail' >> /home/ctfuser/.bashrc && \
    echo '  export PS1="rbash-jail:~\$ "' >> /home/ctfuser/.bashrc && \
    echo '  export SHELL=/bin/rbash' >> /home/ctfuser/.bashrc && \
    echo 'else' >> /home/ctfuser/.bashrc && \
    echo '  export PATH=/home/ctfuser/jail:/usr/bin:/bin' >> /home/ctfuser/.bashrc && \
    echo '  export PS1="ctfuser\$ "' >> /home/ctfuser/.bashrc && \
    echo '  export SHELL=/bin/bash' >> /home/ctfuser/.bashrc && \
    echo '  export ESCAPED_PLATFORM=1' >> /home/ctfuser/.bashrc && \
    echo 'fi' >> /home/ctfuser/.bashrc && \
    echo 'set +o history' >> /home/ctfuser/.bashrc && \
    echo 'unset HISTFILE' >> /home/ctfuser/.bashrc && \
    echo 'alias cd="echo cd: restricted"' >> /home/ctfuser/.bashrc && \
    echo 'shopt -s expand_aliases' >> /home/ctfuser/.bashrc && \
    echo 'alias function="echo Functions are disabled!"' >> /home/ctfuser/.bashrc && \
    echo 'set +o braceexpand' >> /home/ctfuser/.bashrc && \
    echo 'readonly -f' >> /home/ctfuser/.bashrc

# Remove old profile files and ensure ownership
RUN rm -f /home/ctfuser/.profile && \
    chown ctfuser:ctfuser /home/ctfuser/.bash_profile /home/ctfuser/.bashrc

# STEP 3: SET PERMISSIONS
RUN chown -R root:root /home/ctfuser && \
    chown ctfuser:ctfuser /home/ctfuser/work && \
    chmod 555 /home/ctfuser && \
    chmod 755 /home/ctfuser/work && \
    chmod 755 /home/ctfuser/jail && \
    # /opt must be readable for find/ls to work after escape
    chmod 755 /opt && \
    chmod 755 /opt/hidden_bins && \
    chmod 4755 /opt/hidden_bins/flag_reader

# STEP 4: CLEANUP AND VERIFY
RUN ln -sf /bin/bash /bin/sh && \
    # Create dummies for missing shell commands
    echo '#!/bin/sh' > /usr/bin/groups && \
    echo '#!/bin/sh' > /usr/bin/locale-check && \
    chmod +x /usr/bin/groups /usr/bin/locale-check && \
    find /usr/bin -type f ! -name bash ! -name rbash ! -name tar ! -name sh ! -name dash ! -name find ! -name ls ! -name chown ! -name chmod ! -name rm ! -name socat ! -name welcome.sh ! -name env ! -name groups ! -name locale-check -delete && \
    find /usr/bin -type l ! -name bash ! -name rbash ! -name tar ! -name sh ! -name dash ! -name find ! -name ls ! -name chown ! -name chmod ! -name rm ! -name socat ! -name welcome.sh ! -name env ! -name groups ! -name locale-check -delete && \
    rm -rf /usr/local/bin/* /usr/sbin/* /usr/share/doc /usr/share/man /usr/share/info /var/lib/apt /var/cache/apt /etc/apt 2>/dev/null || true && \
    # Set SUID for the restricted reader
    chown root:root /opt/hidden_bins/flag_reader && \
    chmod 4755 /opt/hidden_bins/flag_reader && \
    # Remove temporary build tools
    rm /usr/bin/chown /usr/bin/chmod /usr/bin/rm && \
    # Final check
    [ -f /bin/bash ] && [ -f /bin/rbash ] && [ -f /bin/tar ] && [ -f /usr/bin/find ] && [ -f /usr/bin/ls ] && [ -f /usr/bin/socat ] && [ -f /usr/bin/welcome.sh ] && [ -f /usr/bin/env ] && [ -f /opt/hidden_bins/flag_reader ]

# LAUNCH
USER ctfuser
WORKDIR /home/ctfuser
EXPOSE 1337
CMD ["socat", "-T120", "TCP-LISTEN:1337,reuseaddr,fork", "EXEC:\"/usr/bin/env -i PATH=/home/ctfuser/jail SHELL=/bin/rbash TERM=xterm /bin/rbash --login\",pty,stderr,sigint,setsid,sane"]
