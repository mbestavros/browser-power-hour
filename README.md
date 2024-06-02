# browser-power-hour

A simple power consumption benchmark for Android web browsers utilizing [Battery Historian](https://developer.android.com/topic/performance/power/battery-historian).

## Motivation

I've always been curious whether my choice of web browser has a material impact on things beyond raw speed - particularly power consumption. Outside of desktop, this question is especially relevant on Android due to the platform's allowance for alternative browser runtimes; though Firefox and Chrome (for example) may render the same webpage, they behave fundamentally different under the hood.

What does that mean for end users? Is one browser meaningfully better than another for battery life? Does the answer to the previous question change for different devices and SoC models?

`browser-power-hour` aims to provide a tool to gather data in support of answers to those questions.

> _(Alternative, more biased motivation: "I like Firefox on Android. I know it probably won't be quite as good as Chrome, a browser made by Google for Google's operating system, especially when running on Google's own Tensor chips... but is it actually materially, measurably worse? Can I test that?")_

## How does it work?

The benchmark utilizes ADB to perform an automated suite of general browser actions for a set of browser apps:

- Perform a Speedometer 3.0 test, screenshot the result, and save it
- Navigate to a set of news websites and scroll around
- Run the [`testufo`](https://www.testufo.com/) benchmark for a minute

The suite repeats for a given number of iterations (default 3) before moving on to the next browser.

When all browsers have been tested, the benchmark will generate battery stats and a bugreport, which can be plugged into the [Android Battery Historian](https://developer.android.com/topic/performance/power/battery-historian) tool. From there, power consumption for each of the browsers can be compared and contrasted!

### Why not use random testing?

This tool is NOT meant to be a general purpose battery benchmark for devices. It is designed to specifically test the power efficiency of browser apps. To ensure a fair comparison, it's crucial that every test carries the same steps out in the same order; the only variable should be the individual browsers' behavior.

## Tested browsers

As of 2024-01-02, the tool supports three different Android browsers (more to come):

- Google Chrome
- Firefox for Android
- Firefox for Android (Beta)
- [Cromite](https://github.com/uazo/cromite)
- Brave
- Vivaldi
- Vanadium

The tool will automatically detect and use any supported browsers installed on the test device. If you're not interested in testing a particular browser, just make sure it's uninstalled (or disable it in the script by changing the appropriate `include` key to `False` in the `BROWSERS` dictionary).

The touch targets for these browsers were tested using a Google Pixel 4a 5G. The tool should scale them to work on any size phone screen; however, there's always a possibility that other variables (particularly UI scale and font size) may break things. Feel free to play around with the touch targets in the code if the defaults don't work for you.

## Guide

### Prerequisites

The benchmark is written in Python, and utilizes the [`pure-python-adb`](https://pypi.org/project/pure-python-adb/) package to interact with Android via ADB. If a recent version of Python is installed, run `pip install -r requirements.txt` to install all needed Python packages.

The benchmark also assumes that ADB is installed and usable anywhere on the system via `PATH`. On Linux, installing ADB through a package manager should suffice. Other OSes may need to do some additional setup. [Here's](https://www.androidpolice.com/install-and-use-adb-on-windows-mac-linux-android-chromebooks-browser/) a guide that may help.

### Device setup

There are a few things to set up on the Android device that will run the benchmark.

Firstly, the device must be set up with and accessible by wireless ADB. [Here's](https://www.androidpolice.com/how-to-use-wireless-adb-on-your-android-phone/) a good guide for that.

> _Why is wireless ADB necessary?_ The Battery Historian tool only tracks power consumption when the device is on battery, and wired ADB would charge the device.

Next, you'll need to prepare each web browser for the benchmark. Here's what's required for each.

#### Chrome

Google Chrome should come installed on most, if not all, GMS-equipped devices.

As of writing (2023-04-15), Google Chrome's homepage will sometimes put the address/search bar in unpredictable locations (i.e. further down the screen than normal). To ensure the benchmark will work, it's recommended to set the Chrome start page to a simple website, like [google.com](https://www.google.com/) or [xkcd.com](https://xkcd.com/), for the duration of the test.

#### Firefox (and Firefox Beta)

There are two tweaks to make in order to ensure the benchmark runs smoothly:

- The benchmark assumes that Firefox uses bottom navigation.
- Turn off "Autocomplete URLs" under Search settings. This setting sometimes causes Firefox to autofill sites different from what we want in the benchmark, which we want to avoid.

Everything else should work out of the box.

It may be interesting to play with different settings, such as having an adblocker enabled, to see what kind of impact they have on both speed and power consumption.

#### Cromite

The benchmark assumes that Bromite uses bottom navigation, which is accessible via a flag. If that setting is active, everything else should work out of the box.

#### Brave

Brave should work out of the box, but maybe do a test run to double check. I added support for this a while ago and forgot to push it...

#### Vivaldi

The benchmark assumes that Vivaldi uses bottom navigation, available in settings. If that setting is active, everything else should work out of the box.

#### Vanadium

Should work out of the box.

### Final preparation

With everything set up, the benchmark should be ready to run! Here's a last-minute checklist to make sure the benchmark goes smoothly:

- Make sure the device is not charging, since Battery Historian only reports power consumption when running on battery.
- Set screen timeout to at least five minutes (necessary to not interfere with Speedometer benchmarks)
- Close all background apps
- Close all open tabs in the browsers that will be tested
- Close out of said browsers and force stop them
- Enable Do Not Disturb (banner notifications can interfere with the testing)
- Set device brightness to its lowest level (for control purposes)

Additionally, make sure your ADB client device (your laptop/desktop) won't fall asleep during the test - this can cause interruptions and inconsistent data.

### Running the benchmark

It's time to run the benchmark! Provide your Android device's IP and ADB port as separate arguments to `browser-power-hour.py` (accessible in the Wireless Debugging settings):

```shell
python browser-power-hour.py <device ip> <device port>
```

While the script is intended to work seamlessly with any device, it's not guaranteed. It's recommended to monitor the device until it starts the Speedometer benchmark. If it doesn't start the benchmark (or doesn't even make it to the benchmark's site in the first place), you may need to change a few variables in the script to get it working correctly (namely: the relative coordinate values for `searchbar` and `speedometer_start`).

**DO NOT** touch the device while it's running the tests. When the script has finished running in your terminal (including generating output), wireless ADB should automatically disconnect, and the device should be safe to use again.

If you need to stop the test early, interrupt the Python script in your terminal with `Ctrl-C` or equivalent, and give the device a few seconds to deal with any lingering ADB inputs. Wireless ADB may still be connected at this point; disconnect it with `adb disconnect`.

### Analyzing the output

At the end of the test, `output/bugreport.zip` should be generated. This can be viewed and analyzed using the Android Battery Historian tool.

Follow [this guide](https://developer.android.com/topic/performance/power/setup-battery-historian#how-to) to install Battery Historian. Note that you only need to run through the `Install Battery Historian` section; `browser-power-hour` has already automated all the other steps!

Once you've navigated to the Battery Historian webpage, plug in the `bugreport.zip` we generated as part of the test.

Voila! Battery stats! Geek out!

If you do run the test locally, feel free to share the results for your device - I've set up a [Github discussion](https://github.com/mbestavros/browser-power-hour/discussions/1) for just that!

## Development

Contributions to the benchmark are welcome! This is by no means a perfect tool. Suggestions, improvements, and additions are all warmly appreciated. Submit a pull request and I'll give it a review.

Adding support for new browsers should be relatively easy; you'll just need to add a new entry to the `BROWSERS` dictionary using the same format as existing entries. If you do add support for a new browser, be sure to update this `README`'s [Tested browsers](#tested-browsers) section, and put any setup notes in [Device setup](#device-setup)!

Though the test must be run over wireless ADB to get meaningful power consumption results, it's also possible to use wired ADB just to see if new features work as expected.

## License

Licensed under Apache 2.0.
