sudo apt-get update
sudo apt-get install  -y python-pip \
    python3-pip \
    python2 \
    python3 \
    jq
pip3 install --upgrade pip && pip3 install -r requirements.txt

wget --no-check-certificate https://github.com/splunk/splunk-sdk-python/archive/$(curl --silent "https://api.github.com/repos/splunk/splunk-sdk-python/releases/latest" |grep '"tag_name":'  | sed -E 's/.*"([^"]+)".*/\1/' ).tar.gz -O splunk-sdk-python.tar.gz

