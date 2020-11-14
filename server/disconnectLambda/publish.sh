#!/bin/bash

rm disconnect.zip
zip -r9 disconnect.zip *.py
echo "File successfully zipped"

aws lambda update-function-code --function-name yeetcode2020-disconnect --zip-file fileb://disconnect.zip

echo "Published to lambda"

exit 0