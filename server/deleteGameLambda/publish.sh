#!/bin/bash

rm deleteGame.zip
zip -r9 deleteGame.zip *.py
echo "File successfully zipped"

aws lambda update-function-code --function-name yeetcode2020-deleteGame --zip-file fileb://deleteGame.zip

echo "Published to lambda"

exit 0
