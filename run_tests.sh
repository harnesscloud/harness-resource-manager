#!/bin/bash

##### if we do not run this script inside a container, we create a temporary container to run this script ####
if [ ! -f /.dockerinit ]; then
echo -------------------------------------[launching container]----
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"

docker run --rm -v $DIR:/test -t ubuntu:14.04 /bin/bash -c "cd /test && /test/run_tests.sh"
exit 
fi
 

########## code to start testing  
apt-get update
apt-get -y install curl python
curl -s https://bootstrap.pypa.io/get-pip.py | python -
pip install -r requirements.txt
pip install coverage pytest
python setup.py test

