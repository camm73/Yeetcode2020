#!/bin/bash

rm updateQueue.zip
zip -r9 updateQueue.zip *.py
echo "File successfully zipped"

aws lambda update-function-code --function-name yeetcode2020-updateQueue --zip-file fileb://updateQueue.zip

echo "Published to lambda"

exit 0
