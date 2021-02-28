#!/bin/bash
#This is a script that can be used to set up the virtual environment
# check how many parameters were passed to the script
if (($# != 2)); then
    echo "Illegal number of parameters passed"
    echo "The script was expecting two parameters following the format: install.sh 'conda environment name'"
else 
    env_name="$1"
    reqirements="$2"

    #check if conda exist
    if !command -v conda &> /dev/null; then
        echo "found anaconda installation"
        echo "setting up the conda virtual environment"

        #creating and activating the conda environment
        conda create -n "$env_name" python=3.8
        echo "Activating the new environment"
        source activate "$env_name"

        #making sure pip is up to date
        echo "fetching the newest version of pip"
        conda install pip
        

        pip install -r requirements.txt
    else
        echo "setting up the python virtual environment"

        #upgrading pip to newest version
        pip install --upgrade pip

        pip install virtualenv
        
        python3 -m venv $env_name
        
        # This works for mac need to upgrade it so it also works for windows
        source $env_name/bin/activate
        
        #install packages from requirements.txt
        pip install -r requirements.txt
    fi
fi
