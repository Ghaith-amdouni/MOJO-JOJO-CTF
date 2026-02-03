# ============================================================================
# STAGE 1: BUILD SECURE FLAG READER
# ============================================================================
FROM ubuntu:22.04 AS builder
RUN apt-get update && apt-get install -y gcc libc6-dev
RUN echo '#include <stdio.h>\n\
    #include <stdlib.h>\n\
    int main() {\n\
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

# Create empty jail directory and add tar symlink
RUN mkdir -p /home/ctfuser/jail && \
    ln -s /bin/tar /home/ctfuser/jail/tar

# Create test files for tar
RUN echo "Production backup data" > /home/ctfuser/testfile && \
    echo "Server logs backup" > /home/ctfuser/logs.txt && \
    echo "Configuration backup" > /home/ctfuser/config.txt

# Add realistic but unhelpful files
RUN echo "backup-server-01" > /home/ctfuser/hostname && \
    echo "System operational" > /home/ctfuser/status.log && \
    echo "2024-12-08 03:00:00 - Backup started" > /home/ctfuser/backup.log && \
    echo "2024-12-08 03:45:23 - Backup completed" >> /home/ctfuser/backup.log

# Create welcome script
RUN echo '#!/bin/bash' > /usr/local/bin/welcome.sh && \
    echo 'echo "=================================================="' >> /usr/local/bin/welcome.sh && \
    echo 'echo " RESTRICTED BACKUP SERVER"' >> /usr/local/bin/welcome.sh && \
    echo 'echo "=================================================="' >> /usr/local/bin/welcome.sh && \
    echo 'echo ""' >> /usr/local/bin/welcome.sh && \
    echo 'echo "User: ctfuser"' >> /usr/local/bin/welcome.sh && \
    echo 'echo "Access Level: RESTRICTED"' >> /usr/local/bin/welcome.sh && \
    echo 'echo ""' >> /usr/local/bin/welcome.sh && \
    echo 'echo "This system is for authorized use only."' >> /usr/local/bin/welcome.sh && \
    echo 'echo "Unauthorized access is prohibited."' >> /usr/local/bin/welcome.sh && \
    echo 'echo ""' >> /usr/local/bin/welcome.sh && \
    echo 'echo "=================================================="' >> /usr/local/bin/welcome.sh && \
    echo 'echo ""' >> /usr/local/bin/welcome.sh && \
    chmod +x /usr/local/bin/welcome.sh

# STEP 2: CONFIGURE RBASH
RUN echo '# Restricted Shell Configuration' > /home/ctfuser/.bashrc && \
    echo 'PATH=/home/ctfuser/jail' >> /home/ctfuser/.bashrc && \
    echo 'SHELL=/bin/rbash' >> /home/ctfuser/.bashrc && \
    echo 'set +o history' >> /home/ctfuser/.bashrc && \
    echo 'unset HISTFILE' >> /home/ctfuser/.bashrc && \
    echo 'alias cd="echo cd: restricted"' >> /home/ctfuser/.bashrc && \
    echo '# Restriction: Prohibit defining functions' >> /home/ctfuser/.bashrc && \
    echo 'shopt -s expand_aliases' >> /home/ctfuser/.bashrc && \
    echo 'alias function="echo Functions are disabled!"' >> /home/ctfuser/.bashrc && \
    echo 'set +o braceexpand' >> /home/ctfuser/.bashrc && \
    echo 'readonly -f' >> /home/ctfuser/.bashrc

# Remove .profile and .bash_profile to prevent interference
RUN rm -f /home/ctfuser/.profile /home/ctfuser/.bash_profile

# STEP 3: SET PERMISSIONS
RUN chown -R ctfuser:ctfuser /home/ctfuser && \
    chmod 755 /home/ctfuser && \
    chmod 755 /home/ctfuser/jail && \
    chmod 755 /opt/hidden_bins

# STEP 4: CLEANUP AND VERIFY
RUN find /usr/bin -type f -not -name bash -not -name rbash -not -name tar -not -name chown -not -name chmod -not -name rm -delete && \
    find /usr/bin -type l -not -name bash -not -name rbash -not -name tar -not -name chown -not -name chmod -not -name rm -delete && \
    rm -rf /usr/local/bin/* /usr/sbin/* /usr/share/doc /usr/share/man /usr/share/info /var/lib/apt /var/cache/apt /etc/apt 2>/dev/null || true && \
    # Set SUID for the restricted reader AFTER cleanup find
    chown root:root /opt/hidden_bins/flag_reader && \
    chmod 4755 /opt/hidden_bins/flag_reader && \
    rm /usr/bin/chown /usr/bin/chmod /usr/bin/rm && \
    # Verify essential parts (No rm/ls/etc anymore)
    [ -f /bin/bash ] && [ -f /bin/rbash ] && [ -f /bin/tar ] && [ -f /opt/hidden_bins/flag_reader ]

# LAUNCH
USER ctfuser
WORKDIR /home/ctfuser
CMD ["/bin/bash", "-c", "/usr/local/bin/welcome.sh && exec /bin/rbash"]
