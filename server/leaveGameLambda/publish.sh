#!/bin/bash

rm leaveGame.zip
zip -r9 leaveGame.zip *.py
echo "File successfully zipped"

aws lambda update-function-code --function-name yeetcode2020-leaveGame --zip-file fileb://leaveGame.zip

echo "Published to lambda"

exit 0