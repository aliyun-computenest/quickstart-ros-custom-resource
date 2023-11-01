set -ex

BUILD_DIR=build
CODE_DIR=code
TARGET=$BUILD_DIR/$CODE_DIR

echo clean old build
rm -rf $BUILD_DIR

echo copy files
if [ -f "index.py" ]; then
    error "index.py is not allowed"
fi
mkdir -p $TARGET
cp -rf custom_resource $TARGET/
cp -f *.py $TARGET/
mv $TARGET/fc.py $TARGET/index.py

echo install python packages
pip install -t $TARGET -r requirements.txt
find $TARGET -iname "*.pyc" | xargs rm -f

cd $TARGET
set +e
zip -r -D ../code.zip *
ret_code=$?
set -e
if [ $ret_code -ne 0 ]; then
    cd -
    pip install -r requirements.pipeline.txt
    python -c "from fc2 import util; util.zip_dir('${TARGET}', '${BUILD_DIR}/code.zip')"
fi