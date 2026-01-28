FROM ubuntu:22.04
# Install ONLY what's absolutely necessary
RUN apt-get update && apt-get install -y \
    bash \
    coreutils \
    tar \
    && rm -rf /var/lib/apt/lists/*

# Create challenge user with rbash
RUN useradd -m -s /bin/rbash ctfuser

# ============================================================================
# STEP 1: CREATE ALL DIRECTORIES AND FILES FIRST
# ============================================================================
# ONLY CHANGE: flag moved to /opt/.secrets/flag.txt
RUN mkdir -p /opt/.secrets && \
    echo "MOJO-JOJO{CURS3S!!_Y0u_unr4v3l3d_my_t4r_tr34ch3ry_4nd_st0l3_my_gl0ry!!}" > /opt/.secrets/flag.txt && \
    chown -R ctfuser:ctfuser /opt/.secrets && \
    chmod -R 755 /opt/.secrets && \
    chmod 644 /opt/.secrets/flag.txt

# Decoys (unchanged)
RUN echo "MOJO-JOJO{fake_flag_nice_try}" > /home/ctfuser/flag.txt && \
    echo "MOJO-JOJO{tmp_trick?_ur_brain_is_smaller_than_my_pinkie}" > /tmp/flag.txt && \
    echo "MOJO-JOJO{Mojo_Jojo_never_hides_his_masterpiece_in_plain_sight_fool!}" > /home/ctfuser/.flag

# Verify flag is readable by ctfuser
RUN su - ctfuser -c "test -r /opt/.secrets/flag.txt" || (echo "ERROR: Flag not readable by ctfuser!" && exit 1)

# Backup essential binaries BEFORE cleanup
RUN mkdir -p /opt/system_bins /opt/hidden_bins && \
    cp /bin/bash /opt/system_bins/bash && \
    cp /bin/rbash /opt/system_bins/rbash && \
    cp /bin/tar /opt/system_bins/tar && \
    cp /bin/cat /opt/hidden_bins/flag_reader && \
    chmod 755 /opt/hidden_bins/flag_reader && \
    cp /bin/sh /opt/system_bins/sh && \
    cp /bin/dash /opt/system_bins/dash 2>/dev/null || true



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

# ============================================================================
# STEP 2: CONFIGURE RBASH
# ============================================================================
RUN echo '# Restricted Shell Configuration' > /home/ctfuser/.bashrc && \
    echo 'PATH=/home/ctfuser/jail' >> /home/ctfuser/.bashrc && \
    echo 'SHELL=/bin/rbash' >> /home/ctfuser/.bashrc && \
    echo 'set +o history' >> /home/ctfuser/.bashrc && \
    echo 'unset HISTFILE' >> /home/ctfuser/.bashrc && \
    echo 'alias cd="echo cd: restricted"' >> /home/ctfuser/.bashrc

# Remove .profile and .bash_profile to prevent interference
RUN rm -f /home/ctfuser/.profile /home/ctfuser/.bash_profile

# ============================================================================
# STEP 3: SET PERMISSIONS
# ============================================================================
RUN chown -R ctfuser:ctfuser /home/ctfuser && \
    chmod 755 /home/ctfuser && \
    chmod 755 /home/ctfuser/jail && \
    chmod 700 /opt/.secrets && \
    chmod 755 /opt/hidden_bins

# ============================================================================
# STEP 4: REMOVE DANGEROUS BINARIES (carefully!)
# ============================================================================
RUN rm -f /etc/sudoers /etc/sudoers.d/* 2>/dev/null || true && \
    find / -perm -4000 -type f -delete 2>/dev/null || true && \
    find / -perm -2000 -type f -delete 2>/dev/null || true && \
    rm -rf /usr/share/doc /usr/share/man /usr/share/info /var/lib/apt /var/cache/apt /etc/apt 2>/dev/null || true && \
    cd /bin && ls -1 | grep -v -E '^(bash|rbash|tar|sh|dash)$' | xargs -r rm -f 2>/dev/null || true && \
    cd /usr/bin && ls -1 | xargs -r rm -f 2>/dev/null || true && \
    cd /sbin && ls -1 | xargs -r rm -f 2>/dev/null || true && \
    cd /usr/sbin && ls -1 | xargs -r rm -f 2>/dev/null || true && \
    cd /usr/local/bin && ls -1 | grep -v '^welcome.sh$' | xargs -r rm -f 2>/dev/null || true

# ============================================================================
# VERIFY: Make sure bash, rbash, and tar still exist
# ============================================================================
RUN test -f /bin/bash || (echo "ERROR: bash missing!" && exit 1)
RUN test -f /bin/rbash || (echo "ERROR: rbash missing!" && exit 1)
RUN test -f /bin/tar || (echo "ERROR: tar missing!" && exit 1)

# ============================================================================
# LAUNCH
# ============================================================================
USER ctfuser
WORKDIR /home/ctfuser
CMD ["/bin/bash", "-c", "/usr/local/bin/welcome.sh && exec /bin/rbash"]
