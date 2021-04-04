curr_path=$PWD

echo "alias pycalc='
    cd $curr_path
    python3 py/main.py'" >> ~/.bashrc