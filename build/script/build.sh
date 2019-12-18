#! /bin/sh
cd ../../
UTRY_ROOT_PATH=$(pwd)
if [ "$1" == "D" ] || [ "$1" == "d" ]
then
  echo 'do debug '
else
  echo 'do release'
fi

# test output
if ! test -d "$UTRY_ROOT_PATH"/utry_output
then
  mkdir -p "$UTRY_ROOT_PATH"/utry_output
fi
# get release path
# shellcheck disable=SC2164
cd "$UTRY_ROOT_PATH"/utry_output
UTRY_RELEASE_PATH=$(pwd)

currentfile=linux_$(date +%Y%m%d%H%M%S)
#mkdir "$UTRY_RELEASE_PATH"/"$currentfile"

if ! test -d "$UTRY_ROOT_PATH"/release/bin/ui
then
  mkdir -p "$UTRY_ROOT_PATH"/release/bin/ui
fi
# shellcheck disable=SC2164
cd "$UTRY_ROOT_PATH"/release/bin/ui
PATH_BIN=$(pwd)

# shellcheck disable=SC2034
PATH_RELEASE="$UTRY_ROOT_PATH"/release

# shellcheck disable=SC2034
PATH_RELEASE_UTRY_SHELL="$PATH_RELEASE"/utry_shell


if ! test -d "$UTRY_ROOT_PATH"/release/res
then
  mkdir -p "$UTRY_ROOT_PATH"/release/res
fi
# shellcheck disable=SC2164
cd "$UTRY_ROOT_PATH"/release/res
PATH_RES_TO=$(pwd)

PATH_RES_FROM="$UTRY_ROOT_PATH"/res

UTRY_SRC_PATH="$UTRY_ROOT_PATH"/src/usher/

# shellcheck disable=SC2164
cd "$PATH_RES_FROM"

echo "start build ui"
sleep 1
echo "step 0:  make rc.py"
pyrcc5 image.qrc -o image_rc.py
# shellcheck disable=SC2164
cd "$UTRY_SRC_PATH"
echo "step 1:  build"
pyinstaller -F --noconsole main/ui_main.spec
if [ "$1" == "D" ] || [ "$1" == "d" ]
then
  pyinstaller -F --noconsole auto_test/start_test.py
fi
#pyinstaller -F --noconsole auto_test/start_test_unstop.py
echo "step 2: mv file"
rm "$PATH_BIN"/*
mv dist/ui_main "$PATH_BIN"
rm "$PATH_RELEASE_UTRY_SHELL"/start_test
if [ "$1" == "D" ] || [ "$1" == "d" ]
then
  mv dist/start_test "$PATH_RELEASE_UTRY_SHELL"
fi
#mv dist/start_test_unstop "$PATH_RELEASE_UTRY_SHELL"
cp "$PATH_RES_FROM"/image_rc.py "$PATH_RES_TO"/
echo "step 3: clear build/"
rm build/ -r
echo "step 4: clear dist/"
rm dist/ -r
echo "step 5: clear .spec/"
rm ./*.spec
echo "step 6: zip file"
# shellcheck disable=SC2164
cd "$UTRY_ROOT_PATH"
if [ "$1" == "D" ] || [ "$1" == "d" ]
then
  zip -r "$UTRY_RELEASE_PATH"/"${currentfile}"_utry_d.zip release/*
else
  zip -r "$UTRY_RELEASE_PATH"/"${currentfile}"_utry.zip release/*
fi
echo "----------------zip complete----------------"




