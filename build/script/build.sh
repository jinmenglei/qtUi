#! /bin/sh
UTRY_SCRIPT_PATH=`pwd`

cd ../../
UTRY_ROOT_PATH=`pwd`

# test output
if ! test -d $UTRY_ROOT_PATH/utry_output
then
  mkdir -p $UTRY_ROOT_PATH/utry_output
fi
# get release path
cd $UTRY_ROOT_PATH/utry_output
UTRY_RELEASE_PATH=`pwd`

currentfile=linux_`date +%Y%m%d%H%M%S`
mkdir $UTRY_RELEASE_PATH/$currentfile

if ! test -d $UTRY_ROOT_PATH/release/bin/ui
then
  mkdir -p $UTRY_ROOT_PATH/release/bin/ui
fi
cd $UTRY_ROOT_PATH/release/bin/ui
PATH_BIN=`pwd`

PATH_RELEASE=$UTRY_ROOT_PATH/release


if ! test -d $UTRY_ROOT_PATH/release/res
then
  mkdir -p $UTRY_ROOT_PATH/release/res
fi
cd $UTRY_ROOT_PATH/release/res
PATH_RES_TO=`pwd`

PATH_RES_FROM=$UTRY_ROOT_PATH/res

UTRY_SRC_PATH=$UTRY_ROOT_PATH/src/ui

cd $UTRY_SRC_PATH

echo "start build ui"
sleep 1
echo "step 1:  build"
pyinstaller -F --noconsole ui_main.py
pyinstaller -F --noconsole launchStart.py
echo "step 2: mv file"
rm $PATH_BIN/*
mv dist/* $PATH_BIN
cp $PATH_RES_FROM/* $PATH_RES_TO/ -r
echo "step 3: clear build/"
rm build/ -r
echo "step 4: clear dist/"
rm dist/ -r
echo "step 5: clear .spec/"
rm *.spec
echo "step 6: zip file"
cd $UTRY_ROOT_PATH
zip -r $UTRY_RELEASE_PATH/$currentfile/"${currentfile}"_utry.zip release/*
echo "----------------zip complete----------------"




