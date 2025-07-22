#!/bin/bash

set -e

UNOS=`uname`
UNMACARCH=`uname -m`
INSTALL_ARCH=""
INSTALL_OS=""

CLI_VERSION="5.3"
BITO_FILE="bito"
LCA_BUNDLE="bito-lca"
LCA_BUNDLE_EXTENSION="tar.gz"
SUPPORTEDFILE="bito-slashCommands.json"
BITO_CLI_CONFIG_PATH=~/.bitoai/etc
USR_LOCAL_BIN_PATH=/usr/local/bin

BASE_CLI_URL="https://github.com/gitbito/CLI/raw/main/version-$CLI_VERSION"
BASE_LCA_URL="https://github.com/gitbito/CLI/releases/download/packages"
BASE_SUPPORTEDFILES_URL="https://github.com/gitbito/CLI/releases/download/packages/$SUPPORTEDFILE"

sudo mkdir -p $BITO_CLI_CONFIG_PATH
sudo chmod -R 0777 $BITO_CLI_CONFIG_PATH

if [ "$UNOS" == "Darwin" ]; then
    echo "Installing for Mac"
    INSTALL_OS="macos"
elif [ "$UNOS" == "Linux" ]; then
    echo "Installing for Linux"
    INSTALL_OS="linux"
else
    echo "Unsupported operating system: $UNOS"
    exit 1
fi

if [ "$UNMACARCH" == "x86_64" ]; then
    echo "Machine architecture is x86_64"
    INSTALL_ARCH="x86"
elif [ "$UNMACARCH" == "aarch64" ]; then
    echo "Machine architecture is ARM64"
    INSTALL_ARCH="arm"
elif [ "$UNMACARCH" == "arm64" ]; then
    echo "Machine architecture is ARM64"
    INSTALL_ARCH="arm"
else
    echo "Cannot install Bito CLI on Unsupported machine architecture: $UNMACARCH"
    exit 1
fi

# Use following in case we have separate directory for OS/platform within which we have bito binary to download
#DOWNLOAD_URL=$BASE_CLI_URL/$INSTALL_OS/$INSTALL_ARCH/bito

# Use following in case we have one download directory where the binary files are named as bito-<OS>-<ARCH>
# example: bito-linux-arm or bito-linux-x86
DOWNLOAD_URL=$BASE_CLI_URL/$BITO_FILE-$INSTALL_OS-$INSTALL_ARCH
# This is test using the file there DOWNLOAD_URL=$BASE_CLI_URL/$BITO_FILE-$INSTALL_OS
echo $DOWNLOAD_URL

DOWNLOAD_LCA_URL=$BASE_LCA_URL/$LCA_BUNDLE-$INSTALL_OS.$LCA_BUNDLE_EXTENSION 
echo $DOWNLOAD_LCA_URL

DOWNLOAD_SUPPORTED_FILES=$BASE_SUPPORTEDFILES_URL
echo $DOWNLOAD_SUPPORTED_FILES

# Define the download URL and the file name
BITO_URL=$DOWNLOAD_URL
LCA_BUNDLE_URL=$DOWNLOAD_LCA_URL
SLASH_COMMANDS_FILE_URL=$DOWNLOAD_SUPPORTED_FILES 

echo "[DEBUG] Descargando binario principal desde: $BITO_URL"
# Remove older residue files if exists at this location
sudo rm -rf /tmp/$BITO_FILE
# Download the bito binary from the URL
curl -fS -L $BITO_URL -o /tmp/$BITO_FILE
if [ $? -ne 0 ]; then
    echo "[ERROR] Downloading Bito CLI failed, please contact support@bito.ai"
    exit 1
else
    echo "[DEBUG] Descarga de binario principal exitosa: /tmp/$BITO_FILE"
fi


echo "[DEBUG] Descargando LCA bundle desde: $LCA_BUNDLE_URL"
# Remove older residue files if exists at this location
sudo rm -rf /tmp/$LCA_BUNDLE.$LCA_BUNDLE_EXTENSION
sudo rm -rf /tmp/$LCA_BUNDLE
# Download the lca bundle binary from the URL
curl -fS -L $LCA_BUNDLE_URL -o /tmp/$LCA_BUNDLE.$LCA_BUNDLE_EXTENSION
if [ $? -ne 0 ]; then
    echo "[ERROR] Downloading LCA bundle failed, please contact support@bito.ai"
    exit 1
else
    echo "[DEBUG] Descarga de LCA bundle exitosa: /tmp/$LCA_BUNDLE.$LCA_BUNDLE_EXTENSION"
fi
echo "[DEBUG] Extrayendo LCA bundle..."
tar -xzvf /tmp/$LCA_BUNDLE.$LCA_BUNDLE_EXTENSION
if [ $? -ne 0 ]; then
    echo "[ERROR] Extracción de LCA bundle fallida"
    exit 1
else
    echo "[DEBUG] Extracción de LCA bundle exitosa"
fi
mv $LCA_BUNDLE-$INSTALL_OS /tmp/$LCA_BUNDLE 
if [ $? -ne 0 ]; then
    echo "[ERROR] Movimiento de LCA bundle fallido"
    exit 1
else
    echo "[DEBUG] Movimiento de LCA bundle exitoso: /tmp/$LCA_BUNDLE"
fi


echo "[DEBUG] Descargando archivo de comandos soportados desde: $SLASH_COMMANDS_FILE_URL"
# Download the supported files from the URL
curl -fS -L $SLASH_COMMANDS_FILE_URL -o /tmp/$SUPPORTEDFILE
if [ $? -ne 0 ]; then
    echo "[ERROR] Downloading supporting files failed, please contact support@bito.ai"
    exit 1
else
    echo "[DEBUG] Descarga de supporting files exitosa: /tmp/$SUPPORTEDFILE"
fi
# Remove existing file named "bin" in /usr/local directory which was getting created because of earlier versions of Bito CLI.
if [ -f $USR_LOCAL_BIN_PATH ]; then
    sudo rm -f $USR_LOCAL_BIN_PATH
fi

#!/bin/bash
# Check if brew is installed
if command -v brew &> /dev/null; then
    if brew list --formula -1 | grep -qw "^bito-cli$";
    then
        echo "Updating dependencies..."
        brew update
        brew upgrade bito-cli
    fi
fi

# Check if the CLI is installed
if command -v "$BITO_FILE" &> /dev/null; then
    # Get the path of the installed CLI
    cli_path=$(command -v "$BITO_FILE")
    dir_path=$(dirname "$cli_path")
    # echo "directory path is: $dir_path. move it there."
    # Move the bito binary to dir_path
    sudo mv /tmp/$BITO_FILE /tmp/$LCA_BUNDLE /tmp/$SUPPORTEDFILE $dir_path
    sudo chmod +x $dir_path/$BITO_FILE $dir_path/$LCA_BUNDLE $dir_path/$SUPPORTEDFILE
else
    # echo "$BITO_FILE is not installed on the system. move it to usr/local/bin"
    # Check if /usr/local/bin directory exists, create it if not
    if [ ! -d $USR_LOCAL_BIN_PATH ]; then
        sudo mkdir -p $USR_LOCAL_BIN_PATH
    fi
    # Move the bito binary to /usr/local/bin
    sudo mv /tmp/$BITO_FILE /tmp/$LCA_BUNDLE /tmp/$SUPPORTEDFILE $USR_LOCAL_BIN_PATH
    sudo chmod +x $USR_LOCAL_BIN_PATH/$BITO_FILE $USR_LOCAL_BIN_PATH/$LCA_BUNDLE $USR_LOCAL_BIN_PATH/$SUPPORTEDFILE
    # Ensure that /usr/local/bin is in the PATH
    if ! echo $PATH | grep -q $USR_LOCAL_BIN_PATH ; then
        echo 'export PATH=$PATH:/usr/local/bin' >> ~/.bashrc
        export PATH=$PATH:$USR_LOCAL_BIN_PATH
    fi
fi

if [ -d "/var/log/bito" ] 
then
    sudo touch /var/log/bito/bitocli.log
else
    sudo mkdir /var/log/bito
    sudo touch /var/log/bito/bitocli.log
fi
sudo chmod -R 0777 /var/log/bito
echo "Bito CLI is now installed"
