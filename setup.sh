abs_path=$(dirname $(readlink -e "$0"))
echo "alias pycalc='python3  \"$abs_path/py/main.py\"'" >> ~/.bashrc