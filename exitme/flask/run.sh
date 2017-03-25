docker kill bsidesroc-exitme
docker rm bsidesroc-exitme
docker run --name bsidesroc-exitme -p "5000:5000" exitme-test
