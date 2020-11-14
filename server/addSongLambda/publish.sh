#!/bin/bash

rm addSong.zip
zip -r9 addSong.zip *.py
echo "File successfully zipped"

aws lambda update-function-code --function-name yeetcode2020-addSong --zip-file fileb://addSong.zip

echo "Published to lambda"

exit 0
