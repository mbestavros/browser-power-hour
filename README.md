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

As of 2024-06-11, the tool supports several different Android browsers:

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

#### OEM "optimizations"

In the past OEMs have been caught artifically limiting the performance of certain detected Apps which often included various different browsers. Notably Oneplus ([source](https://arstechnica.com/gadgets/2021/07/oneplus-admits-to-throttling-phones-after-launch-to-improve-battery-life/#:~:text=We%20have%20detected%20that%20OnePlus%20is%20blacklisting%20popular,top%20popular%20non-benchmark%20apps%20get%20notably%20reduced%20performance.)) and Samsung ([source](https://www.androidauthority.com/samsung-gos-throttling-apps-3125885/)) in the last couple of years.
Since the purpose of the benchmark is not to test some OEM cheating software you should perform a quick sanity check if the performance of your browser roughly falls roughly in line with other devices with the same chipset or primary CPU core. 
The benchmark [Octane JS by Google](https://chromium.github.io/octane) is a pure Javascript benchmark and runs in less than a minute and yields very constistant results. If the results for your device are more than 30% off its likley that some manipulation is going on. You can also try to prevent this by enabling any performance mode and disabling any battery saving related features on the device if available, however in the case of Samsung and Oneplus this still did not remove the artifical limits.

Also due to the singlethreaded nature of Javascript when using an App to monitor your phones CPU Clocks Speeds like [CPU Float](https://play.google.com/store/apps/details?id=com.waterdaaan.cpufloat&utm_source=global_co&utm_medium=prtnr&utm_content=Mar2515&utm_campaign=PartBadge&pcampaignid=MKT-Other-global-all-co-prtnr-py-PartBadge-Mar2515-1) upon starting the benchmarks the phone should almost immediatly reach the advertised max. CPU Clock or something close to it on at least one core.

<details>
  <summary>Score / SoC Table</summary>


| Soc            | Primary CPU                    | OctaneJS Chromium | OctaneJS Firefox |
|:--------------:|:------------------------------:|:-----------------:|:----------------:|
| Snapdragon 810 | Cortex-A57 @ 2 GHz             | ~ 9500            | ~ 5400           |
| Snapdragon 820 | Kryo @ 2.15 GHz                | ~ 11000           | ~ 6800           |
| Snapdragon 835 | Modified Cortex-A73 @ 2.45 GHz | ~ 14500           | ~ 8700           |
| Snapdragon 845 | Modified Cortex-A75 @ 2.8 GHz  | ~ 23000           | ~ 13000          |
| Snapdragon 855 | Modified Cortex-A76 @ 2.84 Ghz | ~ 32000           | ~ 19000          |
| Snapdragon 865 | Cortex-A77 @ 2.84 GHz          | ~ 41000           | ~ 22000          |
| Exynos 7420    | Cortex-A57 @ 2.1 GHz           | ~ 10800           | ~ 5300           |
| Exynos 8890    | Samsung M1 @ 2.6 Ghz           | ~ 13000           | ~ 8500           |
| Exynos 8895    | Samsung M2 @ 2.3 Ghz           | ~ 17000           | ~ 9300           |
| Exynos 9810    | Samsung M3 @ 2.9 Ghz           | ~ 24000           | ~ 12000          |
| Exynos 9820    | Samsung M4 @ 2.7 Ghz           | ~ 33000           | ~ 18000          |
| Kirin 955      | Cortex A-72 @ 2.55 Ghz         | ~ 14500           | ~ 8000           |
| Kirin 960      | Cortex A-73 @ 2.3GHz           | ~ 13500           | ~ 8000           |
| Kirin 970      | Cortex A-73 @ 2.3GHz           | ~ 14000           | ~ 8500           |
| Kirin 980      | Cortex A-76 @ 2.6 Ghz          | ~ 31000           | ~ 17000          |
| MTK Helio X20  | Cortex A-72 @ 2.3 Ghz          | ~ 11000           | ~ 6500           |

If you want to add more scores, please add ones if you have more than two or more samples from different phones with the same SoC that are within the margin of error ( ~ 15 %)
</details>



### Final preparation

With everything set up, the benchmark should be ready to run! Here's a last-minute checklist to make sure the benchmark goes smoothly:

- Make sure the device is not charging, since Battery Historian only reports power consumption when running on battery.
- Set screen timeout to at least five minutes (necessary to not interfere with Speedometer benchmarks)
- Close all background apps
- Close all open tabs in the browsers that will be tested
- Close out of said browsers and force stop them
- Run a sanity check to verify the browser your results are sane
- Charge to at above 30% (some OEMs are known to cap the performance when the phone is running out of charge)
- Enable Do Not Disturb (banner notifications can interfere with the testing)
- Set device brightness to its lowest level (for control purposes)

Additionally, make sure your ADB client device (your laptop/desktop) won't fall asleep during the test - this can cause interruptions and inconsistent data.

### Running the benchmark

It's time to run the benchmark! If you've manually connected your device with wireless debugging, just run `browser-power-hour.py`:

```shell
python browser-power-hour.py
```

Alternatively, provide your Android device's IP and ADB port (accessible in the Wireless Debugging settings) to the `-ip` flag, and the script will connect for you:

```shell
python browser-power-hour.py -ip <device ip>:<device port>
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

## Additional script flags

The script exposes some basic flags to make the script work better in some scenarios.

- `-n` or `--iterations`: the number of times to run the main test loop.
- `--speedometer_timeout`: how long to wait before Speedometer completes, in seconds. Defaults to 180 seconds; modern flagships may need much less than this (my Pixel 8 Pro can do it in under 120).

## Development

Contributions to the benchmark are welcome! This is by no means a perfect tool. Suggestions, improvements, and additions are all warmly appreciated. Submit a pull request and I'll give it a review.

Adding support for new browsers should be relatively easy; you'll just need to add a new entry to the `BROWSERS` dictionary using the same format as existing entries. If you do add support for a new browser, be sure to update this `README`'s [Tested browsers](#tested-browsers) section, and put any setup notes in [Device setup](#device-setup)!

Though the test must be run over wireless ADB to get meaningful power consumption results, it's also possible to use wired ADB just to see if new features work as expected.

## License

Licensed under Apache 2.0.
