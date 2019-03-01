wget --no-check-certificate https://github.com/splunk/splunk-sdk-python/archive/$(curl --silent "https://api.github.com/repos/splunk/splunk-sdk-python/releases/latest" |grep '"tag_name":'  | sed -E 's/.*"([^"]+)".*/\1/' ).tar.gz -O splunk-sdk-python.tar.gz
mkdir ~/splunk-sdk
tar xvf splunk-sdk.tar -C ~/splunk-sdk
