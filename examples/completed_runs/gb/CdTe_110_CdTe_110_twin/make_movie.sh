# https://askubuntu.com/questions/610903/how-can-i-create-a-video-file-from-a-set-of-jpg-images
# 5 fps
ffmpeg -r 5 -f image2 -i frames/ingrained-%05d.png  -f mp4 -c 18 -q:v 0 -vcodec mpeg4 -r 20 ingrained_demo.mp4