echo "Installing required packages to virtualenv..."
python3 -m venv venv

source venv/bin/activate
pip3 install -r requirements.txt
echo -e "Created virtualenv and installed required packages!\n"
echo "Setting up Flask environment variables..."
export FLASK_APP="app"
source venv/bin/activate
