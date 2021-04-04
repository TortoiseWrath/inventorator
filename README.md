# inventorator

A tool for keeping inventory of my belongings (and practicing with Flask and Vue).

## Installation

Tested on Debian.

Install dependencies:

```shell
# Install Python and pip
sudo apt install python3 python3-pip

# Install node.js
# See: https://github.com/nvm-sh/nvm#install--update-script
# Change zsh to another shell if you want
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.38.0/install.sh | zsh
source ~/.zshrc
nvm install node

# See: https://github.com/nodesource/distributions/blob/master/README.md#deb
curl -fsSL https://deb.nodesource.com/setup_current.x | sudo bash -
sudo apt install nodejs

# Install MariaDB
sudo apt install mariadb-server
sudo mysql_secure_installation

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
pip install venv
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
$EDITOR config.py
```

Run the Flask server at http://localhost:5000/ with `python app.py`.

Run the Node server at http://localhost:8080/ with `cd client && npm run serve`.

