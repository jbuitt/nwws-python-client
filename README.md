
# nwws-python-client

This is a simple product download client for the NWWS-OI ([NOAA Weather Wire Service](http://www.nws.noaa.gov/nwws/) Open Interface) written in Python. The NOAA Weather Wire Service is a satellite 
data collection and dissemination system operated by the [National Weather Service](http://weather.gov), which was established in October 2000. Its purpose is to provide state and federal government, 
commercial users, media and private citizens with timely delivery of meteorological, hydrological, climatological and geophysical information. 

This client was developed and tested on [Ubuntu 22.04](http://ubuntu.com) using Python v3.10 and makes use of the [slixmpp](https://slixmpp.readthedocs.io/en/latest/) Python library for connecting to 
the NWWS OI XMPP-based server.

## How do I run it?

It's now super simple to run this using [Docker](https://www.docker.com/) and [docker-compose](https://docs.docker.com/compose/)! However, you'll need to first create a config file, documented below. 

Once you have your config.json file created, create the directory that you'll save products to (e.g. `products`):

```
mkdir products
```

Now, start up the client by running:

```
docker compose up
```

It will take care of building the Docker image and running it. You can also run the client in the background by running:

```
docker compose up -d
```

If you can't or don't want to use Docker, you can run it on Debian-based systems (Ubuntu, Raspberry Pi, Linux Mint) by first installing the Slixmpp Python library by running:

```
sudo apt-get install python3-slixmpp -y
```

You can then proceed to the section below 'Running the client outside of Docker' to run the client.

## Config file 

The NWWS Client requires a JSON config file using the following format:

```
{
  "server": "nwws-oi.weather.gov",
  "port": 5222,
  "username": "[username]",
  "password": "[password]",
  "resource": "[resource]",
  "archivedir": "[archivedir]",
  "pan_run": "[pan_run]",
  "pan_run_log": "[pan_run_log]",
  "retry": true,
  "use_tls": true,
  "use_ssl": false
}
```

The variables `username` and `password` are required and refer to your NWWS-OI credentials obtained by signing up [on the NOAA Weather Wire Service website](http://www.nws.noaa.gov/nwws/#NWWS_OI_Request).

You may use whatever string you would like for `resource`. The variable is required. Also, the NWWS-OI server keeps track of resource names, so you should make the name unique if you are running this 
client in multiple locations.

The `archivedir` variable is optional and specifies the directory on your system where you would like to store the downloaded products. The variable is optional in case you'd like to avoid saving products 
to your local system and only process them using a `pan_run` command, defined below.

The `pan_run` variable is also optional and specifies the path to a script or program that you'd like to run on product arrival. The client automatically passes the full path to the product to the supplied 
script or program. If `archivedir` is not specified, the product is temporarily saved to your `/tmp/` directory and then removed after the program or script is run.

The `pan_run_log` variable is an optional variable to specify the log file where messages are run when the `pan_run` program script is run. Otherwise, the messages will be send to /dev/null.

The `retry` variable specifies whether you would like to retry the connection upon disconnection from the server. You'll likely want to set this to `true`.

The options `use_tls` and `use_ssl` are for specifying the security settings on the NWWS-OI connection. Typically, you'll want to set `use_tls` to `true` and `use_ssl` to `false`.

## Running the client outside of Docker

```
$ python nwws.py config.json
```

Provided that you're able to connect to the NWWS and your credentials are accepted, you will start to see products downloaded, and if the `archivedir` config variable was specified, you'll see the products 
saved to the directory in the following format:

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

The script will continue to run, downloading products to your system. If products are being archved, they will eventually fill up your filesystem and you'll likely want to clear out old products. For example, 
to automatically remove products older than a week, insert the following line into your crontab:

```
0 0 * * *   /usr/bin/find [archivedir] -type f -mtime +7 -delete >/dev/null
```

You will want to replace [archivedir] with the path to the product directory.

## Running the client in the background

If you would like to run the client in the background, you can use GNU screen, tmux, or nohup. Examples:

```
$ sudo apt-get install screen -y
$ screen -d -m python nwws.py config.json
# Run the following to re-attach to the screen session. Type Ctrl+a d to detach
$ screen -r
```

```
$ sudo apt-get install tmux -y
$ tmux new-session -d -s "nwws" python nwws.py config.json
# Run the following to re-attach to the tmux session. Type Ctrl+b d to detach
$ tmux a -t nwws
```

```
$ nohup python -u nwws.py config.json >>nwws.log 2>&1 &
# To tail the log file..
$ tail -f nwws.log
```

## Author

+	[jbuitt at gmail.com](mailto:jbuitt@gmail.com)

## License

See [LICENSE](https://github.com/jbuitt/nwws-python-client/blob/master/LICENSE) file.

