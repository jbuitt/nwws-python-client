
# nwws-python-client

This is a simple product download client for the NWWS-OI ([NOAA Weather Wire Service](http://www.nws.noaa.gov/nwws/) Open Interface) written in Python. The NOAA Weather Wire Service is a satellite data collection and dissemination system operated by the [National Weather Service](http://weather.gov), which was established in October 2000. Its purpose is to provide state and federal government, commercial users, media and private citizens with timely delivery of meteorological, hydrological, climatological and geophysical information. 

This client was developed and tested on [Ubuntu 18.04](http://ubuntu.com) using Python v3.6 and makes use of the [sleekxmpp](https://github.com/fritzy/SleekXMPP) Python library for connecting to the NWWS-2 OI XMPP-based server.

## How do I run it?

On Ubuntu, first install the `sleekxmpp` library:

```
sudo apt-get install python3-sleekxmpp
```

If not on Ubuntu, you can use pip to install:

```
pip3 install -r requirements.txt
```

Now, after cloning the latest [release](https://github.com/jbuitt/nwws-python-client), create a JSON config file using the following format:

```
{
  "server": "[server]",
  "port": "[port]",
  "username": "[username]",
  "password": "[password]",
  "resource": "[resource]",
  "archivedir": "[archivedir]",
  "pan_run": "[pan_run]",
  "pan_run_log": "[pan_run_log]"
}
```

The variables `[server]` and `[port]` are required and refer to the NWWS-OI server hostname and port, usually `nwws-oi.weather.gov` and `5222` respectively. The variables `[username]` and `[password]` are required and refer to your NWWS-OI credentials obtained by signing up [on the NOAA Weather Wire Service website](http://www.nws.noaa.gov/nwws/#NWWS_OI_Request).

You may use whatever string you would like for `[resource]`. The variable is required.

The `[archivedir]` variable is optional and specifies the directory on your system where you would like to store the downloaded products. The variable is optional in case you'd like to avoid saving products to your local system and only process them using a `[pan_run]` command, defined below.

The `[pan_run]` variable is also optional and specifies the path to a script or program that you'd like to run on product arrival. The client automatically passes the full path to the product to the supplied script or program. If `[archivedir]` is not specified, the product is temporarily saved to your `/tmp/` directory and then removed after the program or script is run.

The `[pan_run_log]` variable is an optional variable to specify the log file where messages are run when the `[pan_run]` program script is run. Otherwise, the messages will be send to /dev/null.

The client has the following usage:

```
$ python3 nwws.py /path/to/config/file
```

Provided that you're able to connect to the NWWS and your credentials are accepted, you will start to see products downloaded, and if the `[archivedir]` config variable was specified, you'll see the products saved to the directory in the following format:

```
[archivedir]/
   [cccc]/
      [cccc]_[ttaaii]-[awipsid].[ddHHMM]_[id].txt
```

The above variables have the following meaning:

* `cccc` - International four-letter location indicator of the station or centre originating or compiling the product
* `ttaaii` - tt - Report type, aa - Region of the report, ii - Report number. ([more info](http://weather.unisys.com/noaaport/WMO_Header_Text.php))
* `awipsid` - Product's [AWIPS](https://www.unidata.ucar.edu/software/awips2/) ID
* `ddHHMM` - Day, hour, and minute of product issuance
* `id` - Unique product ID

You can either run it via [screen](https://www.gnu.org/software/screen/) / [tmux](https://github.com/tmux/tmux/wiki) or use the included `start.sh` script which starts it and sends it to the background using nohup. The client will automatically reconnect to NWWS if the connection is dropped.

The script will continue to run, downloading products to your system. If products are being archved, they will eventually fill up your filesystem and you'll likely want to clear out old products. For example, to automatically remove products older than a week, insert the following line into your crontab:

```
0 0 * * *   /usr/bin/find [archivedir] -type f -mtime +7 -delete >/dev/null
```

You will want to replace [archivedir] with the path to the product directory.

## Author

+	[jbuitt at gmail.com](mailto:jbuitt@gmail.com)

## License

See [LICENSE](https://github.com/jbuitt/nwws-python-client/blob/master/LICENSE) file.

