#!/bin/bash

rm joinGame.zip
zip -r9 joinGame.zip *.py
echo "File successfully zipped"

aws lambda update-function-code --function-name yeetcode2020-joinGame --zip-file fileb://joinGame.zip

echo "Published to lambda"

exit 0
