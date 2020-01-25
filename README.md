# capture-pages 

`capture-pages` allows you to capture a screenshot of any website and save the image to disk.

## Prerequisites

1. First, make sure you have installed **Chrome** browser.
2. Download a compatible driver from: *<https://sites.google.com/a/chromium.org/chromedriver/downloads>* and add it to your **path**.
3. Run `pip install -r requirements.txt`.


## Running
To run the script, run the following command:
```

```

### Saving to S3
To write to S3, create config file `capture-pages.ini` in your working directory.
```
[AWS]
AWSAccessKeyId = your access key id
AWSSecretAccessKey = your secret access key
Bucket = your bucket name
```

And run the script as following: 
```
python capture.py -u [url] -s3
```