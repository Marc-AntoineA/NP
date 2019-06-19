# TODO paramètre du fichier
for filename in ../frontend/public/data/images_full/*.JPG; do
    mv ${filename} ${filename:0:${#filename}-3}jpg
done

echo 'done'
