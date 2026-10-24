!pip install --upgrade buildozer
!sudo apt-get update
!sudo apt-get install -y build-essential ccache git libncurses5:i386 libstdc++6:i386 libgtk2.0-0 libpangox-1.0-0 libpangoxft-1.0-0 libidn11 python3-dev zlib1g-dev zlib1g:i386 libffi-dev libltdl-dev
!buildozer -v android debug
