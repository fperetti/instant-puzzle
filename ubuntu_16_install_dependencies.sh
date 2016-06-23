#Add extra repositories
sudo add-apt-repository ppa:kivy-team/kivy

sudo apt-get update

#Install dependencies
sudo apt-get install -y git python-kivy python-pip cython zlib1g-dev openjdk-8-jdk build-essential python-sh python-appdirs python-six python-colorama python-jinja2

#Now add 32bits
sudo dpkg --add-architecture i386
sudo apt-get update
sudo apt-get install -y libncurses5:i386 libstdc++6:i386 libgtk2.0-0:i386 libpangox-1.0-0:i386 libpangoxft-1.0-0:i386 libidn11:i386 zlib1g:i386

pip install --upgrade pip
sudo pip install buildozer

#Deploy on phone vía USB
#buildozer android_new debug deploy run
