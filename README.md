# generate-thumbnails
*v1.0.0*

This is a command line tool to generate either one, or many thumbnails from a video timestamp. 

### Commands 
Generate a single thumbnail
```
$ python make_thumbs.py FILE DIR
```
*example*
```
$ python make_thumbs.py image.png output_thumbnails/`
```

Generate thumbnails from a directory of files
```
$ python make_thumbs.py -r DIR0 DIR1
```
*example*
```
$ python make_thumbs.py -r input_videos/ output_thumbnails/`
```

Optional time (in seconds) to grab thumbnail from
```
$ python make_thumbs.py FILE DIR [n]
$ python make_thumbs.py -r DIR0 DIR1 [n]
```
*example*
```
$ python make_thumbs.py -r input_videos/ output_thumbnails 14
```

### Other Features
1. This tool will skip over any files with non-video file extensions.
2. By default, the tool will choose 1s as the time to grab the thumbnail
3. Images are outputted as png's
