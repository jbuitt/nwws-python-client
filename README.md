
# nwws-python-client

A simple product downloader for the NWWS-2 OI ([NOAA Weather Wire Service](http://www.nws.noaa.gov/nwws/) version 2 Open Interface) written in Python. The NOAA Weather Wire Service is a satellite data collection and dissemination system operated by the [National Weather Service](http://weather.gov), which was established in October 2000. Its purpose is to provide state and federal government, commercial users, media and private citizens with timely delivery of meteorological, hydrological, climatological and geophysical information. 

This client makes use of the following Python libraries:

* [sleekxmpp](https://github.com/fritzy/SleekXMPP)
* [minidom](https://docs.python.org/2/library/xml.dom.minidom.html)
* [json](https://docs.python.org/2/library/json.html)

## How do I run it?

This script was developed and tested on [Ubuntu 16.04](http://ubuntu.com) using ***Python v2.7***. After downloading the latest [release](https://github.com/jbuitt/nwws-python-client).

Now create a JSON config file with the following format:

```
{
  "username": "[username]",
  "password": "[password]",
  "resource": "[resource]",
  "archivedir": "/path/to/archive/dir",
  "pan_run": "/path/to/executable_or_script"
}
```

Where `[username]` and `[password]` are your NWWS-2 credentials obtained by signing up [on the NOAA Weather Wire Service website](http://www.nws.noaa.gov/nwws/#NWWS_OI_Request). You may use whatever you would like for `[resource]`. The `pan_run` variable is an optional Product Arrival Notification (PAN) script that you'd like to run on product arrival.

Now run the script:

```
$ python ./nwws2.py /path/to/config/file
```

Provided that you're able to connect to the NWWS and your credentials are accepted, you will start to see products appear in the supplied archive directory in the following format:

```
[archive_dir]/
   [wfo]/
      [wfo]_[wmo_TTAAii]-[awips_id].[product_dayhourmin]_[product_id].txt
```

You can either run it via [screen](https://www.gnu.org/software/screen/)/[tmux](https://github.com/tmux/tmux/wiki) or use the included `nwws2` script to run it using [nohup](https://en.wikipedia.org/wiki/Nohup). The client will automatically reconnect to NWWS if the connection is dropped.

## Author

+	[jbuitt at gmail.com](mailto:jbuitt@gmail.com)

## License

See [LICENSE](https://github.com/jbuitt/nwws-python-client/blob/master/LICENSE) file.

