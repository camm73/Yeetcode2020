#!/bin/bash

rm createGame.zip
zip -r9 createGame.zip *.py
echo "File successfully zipped"

aws lambda update-function-code --function-name yeetcode2020-createGame --zip-file fileb://createGame.zip

echo "Published to lambda"

exit 0
