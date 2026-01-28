Step-by-Step Solution
Step 1: Realize You're in a Restricted Shell
echo $SHELL gives /bin/rbash 
Since you have no commands, use shell built-ins and globbing: echo * 
step 2 : check the PATH variable it points to jail
step 3 : check the jail with echo jail/*
step 4: since we have the tar command in jail/ we can exploit the advanced feature of tar command since it allows exucting commands in archiving operation so find the escape script and excute  
tar cf /dev/null testfile --checkpoint=1 --checkpoint-action=exec=/tmp/escape.sh
step 5 : after we escaped we have to inspect the /opt/.secrets and read the flag that s inside with flag_reader

