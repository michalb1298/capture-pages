# capture-pages 
`capture-pages` allows you to capture a screenshot of any website and save the image to disk and S3. This script is supported only in **Python 3**.

## Prerequisites
1. First, make sure you have installed **Chrome** browser.
2. Download a compatible driver from: *<https://sites.google.com/a/chromium.org/chromedriver/downloads>* and add it to your **path**.
3. Run `pip install -r requirements.txt`.


## Running
To run the script, run the following command:
```
python capture.py [-f] [-l path_to_location] [-s3] <url>
```

### Taking a Full Screenshot
If your website page is longer than your screen height, 
you can take a full screenshot using the flag `-f` or `--full-screenshot`:
```
python capture.py -f <url>
```

### Changing Saving Location
By default, your screenshots will be saved in **`screenshots`** directory in your current working path.
If you would like to change saving destination use the flag `-l` or `--location` with your desired path.
For example:
```
python capture.py -l ~/my_cool_screenshots <url>
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
python capture.py -s3 <url>
```
