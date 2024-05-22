abs_path=$(dirname $(readlink -e "$0"))
pip install requests
echo "alias pycalc='python3  \"$abs_path/py/main.py\"'" >> ~/.bashrc