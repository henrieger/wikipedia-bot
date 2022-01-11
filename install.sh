#!/bin/bash

# --- Help Message ---
MESSAGE="Usage:\n\t./install.sh <interface1> <interface2> ... [options]\n\n" 

MESSAGE=$MESSAGE"Install script for dependencies of the Wikipedia Bot project.\n\n" 

MESSAGE=$MESSAGE"Possible interfaces:\n" 
MESSAGE=$MESSAGE"\tall:\t\tInstall all interfaces.\n" 
MESSAGE=$MESSAGE"\tdiscord:\tInstall all dependencies for Discord version of bot.\n" 
MESSAGE=$MESSAGE"\ttelegram:\tInstall all dependencies for Telegram version of bot.\n"
MESSAGE=$MESSAGE"All options include the following packages:\n"
MESSAGE=$MESSAGE"\t- beautifulsoup4\n\t- python-dotenv\n\t- requests\n and all their dependencies.\n\n"

MESSAGE=$MESSAGE"Options:\n" 
MESSAGE=$MESSAGE"\t-h --help:\tDisplay this message help.\n" 
MESSAGE=$MESSAGE"\t-u --user:\tInstall dependencies for user only (pip --user).\n" 
MESSAGE=$MESSAGE"\t-q --quiet:\tDisplay nothing in standard output.\n" 
MESSAGE=$MESSAGE"\t-v --verbose:\tDisplay all output for pip in standard output.\n" 
MESSAGE=$MESSAGE"\t--log <path>:\tPath to a verbose appending log.\n\n" 

MESSAGE=$MESSAGE"Press 'q' to leave"
# ------

# Display help message if no valid arguments were given
if [[ $# -eq 0 ]]; then
    echo -e $MESSAGE | less
    exit
fi

# Get all interfaces requested by user
VALID_INTERFACES=("discord" "telegram")
REQ_INTERFACES=""
while [[ $1 != -* ]]; do
    case "$1" in
    "all")
        REQ_INTERFACES=${VALID_INTERFACES[@]}
        shift
        break
        ;;
    "discord")
        if [[ $REQ_INTERFACES != *discord* ]]; then
            REQ_INTERFACES="$REQ_INTERFACES discord"
        fi
        shift
        ;;
    "telegram")
        if [[ $REQ_INTERFACES != *telegram* ]]; then
            REQ_INTERFACES="$REQ_INTERFACES telegram"
        fi
        shift
        ;;
    *)
        if [[ ! -z $1 ]]; then
            >&2 echo "Error: interface '$1' is not valid. Type './install.sh --help' for a list of all valid interfaces."
            exit 1
        fi
        shift
        break
        ;;
    esac
done

# Compile valid optional arguments
VALID_ARGS=$(getopt -o huqvl: --long help,user,quiet,verbose,log: -- $@)
if [[ $? -ne 0 ]]; then
    exit 1;
fi

FILE="/dev/null"
USER_OPT=""
QUIET=0
VERBOSE=0

# Check for all optional arguments
eval set -- "$VALID_ARGS"
while [ : ]; do
  case "$1" in
    -h | --help)
        echo -e $MESSAGE | less
        exit 0
        ;;
    -u | --user)
        USER_OPT=" --user"
        shift
        ;;
    -q | --quiet)
        QUIET=1
        shift
        ;;
    -v | --verbose)
        VERBOSE=1
        shift
        ;;
    --log)
        FILE=$2
        shift 2
        ;;
    --) shift;
        break 
        ;;
  esac
done

if [[ -z $REQ_INTERFACES ]]; then
    >&2 echo "Error: no valid interface was given. Interfaces must be declared before the arguments. Aborting..."
    exit 2
fi

echo -e "Wikipedia Bot Log\nStart time: $(date)\n" > $FILE

# --- Install base packages ---

#bs4
if [[ QUIET -eq 0 ]]; then
    echo -n "install.sh:117: " >> $FILE
    echo "Installing beautifulsoup4..." | tee -a $FILE
else
    echo -n "install.sh:120: " >> $FILE
    echo "Installing beautifulsoup4..." >> $FILE
fi
echo "" >> $FILE

if [[ VERBOSE -eq 0 || QUIET -ne 0 ]]; then
    echo "install.sh:126:pip3 install$USER_OPT beautifulsoup4:" >> $FILE
    pip3 install$USER_OPT beautifulsoup4 >> $FILE 2>&1
    echo "" >> $FILE
else
    echo "install.sh:130:pip3 install$USER_OPT beautifulsoup4:" >> $FILE
    pip3 install$USER_OPT beautifulsoup4 2>&1 | tee -a $FILE 2>&1
    echo "" | tee -a $FILE
fi

#dotenv
if [[ QUIET -eq 0 ]]; then
    echo -n "install.sh:137: " >> $FILE
    echo "Installing python-dotenv..." | tee -a $FILE
else
    echo -n "install.sh:140: " >> $FILE
    echo "Installing python-dotenv..." >> $FILE
fi
echo "" >> $FILE

if [[ VERBOSE -eq 0 || QUIET -ne 0 ]]; then
    echo "install.sh:146:pip3 install$USER_OPT pyhton-dotenv:" >> $FILE
    pip3 install$USER_OPT python-dotenv >> $FILE 2>&1
    echo "" >> $FILE
else
    echo "install.sh:150:pip3 install$USER_OPT pyhton-dotenv:" >> $FILE
    pip3 install$USER_OPT python-dotenv 2>&1 | tee -a $FILE 2>&1
    echo "" | tee -a $FILE
fi

# requests
if [[ QUIET -eq 0 ]]; then
    echo -n "install.sh:157: " >> $FILE
    echo "Installing requests..." | tee -a $FILE
else
    echo -n "install.sh:160: " >> $FILE
    echo "Installing requests..." >> $FILE
fi
echo "" >> $FILE

if [[ VERBOSE -eq 0 || QUIET -ne 0 ]]; then
    echo "install.sh:166:pip3 install$USER_OPT requests:" >> $FILE
    pip3 install$USER_OPT requests >> $FILE 2>&1
    echo "" >> $FILE
else
    echo "install.sh:170:pip3 install$USER_OPT requests:" >> $FILE
    pip3 install$USER_OPT requests 2>&1 | tee -a $FILE 2>&1
    echo "" | tee -a $FILE
fi

# ------

# Install specific interface packages
for INTERFACE in $REQ_INTERFACES; do
    case $INTERFACE in
        
        # discord
        "discord")
            if [[ QUIET -eq 0 ]]; then
                echo -n "install.sh:184: " >> $FILE
                echo "Installing discord..." | tee -a $FILE
            else
                echo -n "install.sh:187: " >> $FILE
                echo "Installing discord..." >> $FILE
            fi
            echo "" >> $FILE

            if [[ VERBOSE -eq 0 || QUIET -ne 0 ]]; then
                echo "install.sh:193:pip3 install$USER_OPT discord:" >> $FILE
                pip3 install$USER_OPT discord >> $FILE 2>&1
                echo "" >> $FILE
            else
                echo "install.sh:197:pip3 install$USER_OPT discord:" >> $FILE
                pip3 install$USER_OPT discord 2>&1 | tee -a $FILE 2>&1
                echo "" | tee -a $FILE
            fi
            ;;
        
        # python-telegram-bot
        "telegram")
            if [[ QUIET -eq 0 ]]; then
                echo -n "install.sh:207: " >> $FILE
                echo "Installing python-telegram-bot..." | tee -a $FILE
            else
                echo -n "install.sh:210: " >> $FILE
                echo "Installing python-telegram-bot..." >> $FILE
            fi
            echo "" >> $FILE

            if [[ VERBOSE -eq 0 || QUIET -ne 0 ]]; then
                echo "install.sh:216:pip3 install$USER_OPT python-telegram-bot:" >> $FILE
                pip3 install$USER_OPT python-telegram-bot >> $FILE 2>&1
                echo "" >> $FILE
            else
                echo "install.sh:220:pip3 install$USER_OPT python-telegram-bot:" >> $FILE
                pip3 install$USER_OPT python-telegram-bot 2>&1 | tee -a $FILE 2>&1
                echo "" | tee -a $FILE
            fi
            ;;
    esac
done

echo -e "End time: $(date)\n" >> $FILE