# inventorator

A tool for keeping inventory of my belongings (and practicing with Flask and Vue).

## Installation

Tested on Debian sid.

Install dependencies:

```shell
# Install dependencies
sudo apt install curl git python3 python3-pip python3-venv python-is-python3 mariadb-server

# Secure the MariaDB installation
sudo mysql_secure_installation

# Install node.js
# See: https://github.com/nvm-sh/nvm#install--update-script
# Change zsh to another shell if you want
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.38.0/install.sh | zsh
source ~/.zshrc
nvm install node

# Install Vue CLI
npm i -g @vue/cli

# You may need to increase fs.inotify.max_user_watches.
# See: https://stackoverflow.com/q/53930305
echo fs.inotify.max_user_watches=524288 | sudo tee /etc/sysctl.d/10-user-watches.conf
sudo sysctl --system
```

Create a database and user at the MySQL prompt (`sudo mysql`):

```mariadb
CREATE DATABASE inventorator;
GRANT ALL ON inventorator.* TO 'inventorator_flask'@'localhost' IDENTIFIED BY 'passw0rd' WITH GRANT OPTION;
FLUSH PRIVILEGES;
exit
```

Clone the inventorator repository, install pip and npm dependencies, and set up the database:

```shell
# Clone and enter the repository
git clone https://github.com/TortoiseWrath/inventorator
cd inventorator

# Create and enter a virtual environment (if desired)
python -m venv venv
source venv/bin/activate

# Install python dependencies
pip install -r requirements.txt

# Install npm dependencies
cd client
npm install
cd ..

# Load the database schema
mysql -u inventorator_flask -p inventorator < schema.sql

# Update the database configuration
git update-index --assume-unchanged config.py
$EDITOR config.py
```

Run the Flask server at http://localhost:5000/ with `python app.py`.

Run the Node server at http://localhost:8080/ with `cd client && npm run serve`.

## Usage

Some keyboard shortcuts:

F13 = Scan barcode (doesn't work yet)  
F14 = Edit parent  
F15 = Add child  
F16 = Add sibling  
F17 = Take photo 
F18 = Next sibling (when editing an existing item)
