#!/bin/bash

rm voteSong.zip
zip -r9 voteSong.zip *.py
echo "File successfully zipped"

aws lambda update-function-code --function-name yeetcode2020-voteSong --zip-file fileb://voteSong.zip

echo "Published to lambda"

exit 0
