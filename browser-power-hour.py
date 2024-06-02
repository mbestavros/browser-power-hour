import os, sys, time
from ppadb.client import Client as AdbClient

# Tutorials:
# https://developer.android.com/topic/performance/power/setup-battery-historian
# https://itnext.io/how-you-can-control-your-android-device-with-python-45c3ab15e260

URLS = [
    "https://www.arstechnica.com",
    "https://www.theverge.com",
    "https://www.phoronix.com/",
    "https://www.techdirt.com/",
    "https://9to5google.com/",
    "https://www.droid-life.com/",
    "https://www.xda-developers.com/",
    "https://www.androidpolice.com/",
    "https://www.anandtech.com/",
    "https://www.wired.com/",
    "https://themarkup.org/"
]

BROWSERS = {
    "firefox_beta": {
        "include": False,
        "package": "org.mozilla.firefox_beta",
        "searchbar": {
            "horizontal": 0.5,
            "vertical": 0.9401, # 2200/2340
        },
        "speedometer_start": {
            "horizontal": 0.5,
            "vertical": 0.5,
        }
    },
    "firefox": {
        "include": True,
        "package": "org.mozilla.firefox",
        "searchbar": {
            "horizontal": 0.5,
            "vertical": 0.9401, # 2200/2340
        },
        "speedometer_start": {
            "horizontal": 0.5,
            "vertical": 0.5,
        }
    },
    "chrome": {
        "include": True,
        "package": "com.android.chrome",
        "searchbar": {
            "horizontal": 0.5,
            "vertical": 0.1, # 234/2340
        },
        "speedometer_start": {
            "horizontal": 0.5,
            "vertical": 0.55,
        }
    },
    "vanadium": {
        "include": False,
        "package": "app.vanadium.browser",
        "searchbar": {
            "horizontal": 0.5,
            "vertical": 0.1, # 234/2340
        },
        "speedometer_start": {
            "horizontal": 0.5,
            "vertical": 0.55,
        }
    },
    "brave": {
        "include": False,
        "package": "com.brave.browser",
        "searchbar": {
            "horizontal": 0.5,
            "vertical": 0.1, # 234/2340
        },
        "speedometer_start": {
            "horizontal": 0.5,
            "vertical": 0.55,
        }
    },
    "vivaldi": {
        "include": False,
        "package": "com.vivaldi.browser",
        "searchbar": {
            "horizontal": 0.4629, # 500/1080
            "vertical": 0.9401, # 2200/2340
        },
        "speedometer_start": {
            "horizontal": 0.5,
            "vertical": 0.5,
        }
    },
    "cromite": {
        "include": False,
        "package": "org.cromite.cromite",
        "searchbar": {
            "horizontal": 0.4629, # 500/1080
            "vertical": 0.9401, # 2200/2340
        },
        "speedometer_start": {
            "horizontal": 0.5,
            "vertical": 0.5,
        }
    },
}

TOUCH_TARGETS = {
    "swipe_top": {
        "horizontal": 0.1,
        "vertical": 0.3846,
    },
    "swipe_medium": {
        "horizontal": 0.1,
        "vertical": 0.5982,
    },
    "swipe_bottom": {
        "horizontal": 0.1,
        "vertical": 0.8547,
    }
}


def get_coordinate_string(device, coordinate):
    dimensions = device.shell('wm size').strip().replace("Physical size: ", "").split("x")
    width = int(dimensions[0])
    height = int(dimensions[1])
    horizontal_coordinate = width * coordinate["horizontal"]
    vertical_coordinate = height * coordinate["vertical"]

    return f"{horizontal_coordinate} {vertical_coordinate}"


def test_app(device, app_name, iterations=1):
    browser_data = BROWSERS[app_name]
    if not browser_data["include"]:
        print(f"Skipping browser {app_name}")
        return
    elif not device.shell(f'pm list package {browser_data["package"]}'):
        print(f"Browser {app_name} not installed; skipping")
        return
    else:
        print(f"Testing browser {app_name}...")
    app_location = browser_data["package"]
    search_bar = get_coordinate_string(device, browser_data["searchbar"])

    swipe_top = get_coordinate_string(device, TOUCH_TARGETS["swipe_top"])
    swipe_medium = get_coordinate_string(device, TOUCH_TARGETS["swipe_medium"])
    swipe_bottom = get_coordinate_string(device, TOUCH_TARGETS["swipe_bottom"])

    device.shell(f'monkey -p {app_location} 1')

    time.sleep(1) # wait for browser to load
    start = time.time()

    iteration = 1
    while iteration <= iterations:
        print(f"Beginning iteration {iteration} of {iterations}")

        speedometer_start = browser_data.get("speedometer_start", None)
        if speedometer_start:
            print("Running Speedometer...")
            time.sleep(1)
            device.shell(f'input tap {search_bar}')
            time.sleep(1)
            device.shell(f'input text "https://browserbench.org/Speedometer3.0/"')
            time.sleep(1)
            device.shell('input keyevent 66')
            time.sleep(5.0)

            device.shell(f'input tap {get_coordinate_string(device, speedometer_start)}')
            time.sleep(120)

            # write screenshot of results
            screenshot = device.screencap()

            screenshot_title = f"output/speedometer-{app_name}-{iteration}.png"
            with open(screenshot_title, "wb") as f:
                f.write(screenshot)
                print(f"Saved Speedometer result screenshot to {screenshot_title}")

        counter = 0
        for url in URLS:

            device.shell(f'input tap {search_bar}')
            time.sleep(1)
            device.shell(f'input text "{url}"') # make sure you have the quotation marks around your text
            time.sleep(1)
            device.shell('input keyevent 66')
            time.sleep(5.0)
            device.shell(f'input touchscreen swipe {swipe_bottom} {swipe_top} 200')
            time.sleep(0.5)
            device.shell(f'input touchscreen swipe {swipe_bottom} {swipe_top} 200')
            time.sleep(3.0)
            device.shell(f'input touchscreen swipe {swipe_top} {swipe_medium} 200')
            time.sleep(3.0)

            counter = counter + 1
            if counter % 2 == 0:
                device.shell('input keyevent 4')

        time.sleep(3)

        device.shell(f'input tap {search_bar}')
        time.sleep(1)
        device.shell(f'input text "https://www.testufo.com/"')
        time.sleep(1)
        device.shell('input keyevent 66')
        time.sleep(30.0)

        print(f"Completed iteration {iteration} of {iterations}; elapsed time: {time.time() - start}")
        iteration = iteration + 1

    # quit app by spamming back
    print(f"Completed testing for app {app_name}; quitting")
    for _ in range(0, 15*iterations):
        device.shell('input keyevent 4')


# main function
if __name__ == '__main__':
    # gather CLI inputs
    device_ip = None
    device_port = None
    if len(sys.argv) > 1:
        device_ip = sys.argv[1]
        device_port = sys.argv[2]
    client = AdbClient(host="127.0.0.1", port=5037) # Default is "127.0.0.1" and 5037

    # attempt to connect wirelessly if no devices are currently connected
    wireless = False
    devices = client.devices()
    if len(devices) == 0:
        if device_ip and device_port:
            print('No wired devices found; trying wireless')
            client.remote_connect(device_ip, int(device_port))
            device = client.device(f"{device_ip}:{device_port}")
            wireless =  True
        else:
            print("No wired devices found, and no wireless addresses provided! Exiting...")
            sys.exit(1)
    else:
        device = devices[0]

    print(f'Connected to {device.shell("getprop ro.product.name")}')

    # Clear old battery statistics
    os.system("adb shell dumpsys batterystats --reset")

    # Test each app in BROWSERS
    for app in BROWSERS.keys():
        test_app(device, app, 3)

    # When done benchmarking, dump batterystats and create a bug report
    batterystats_path = "output/batterystats.txt"
    bugreport_path = "output/bugreport.zip"
    os.system(f"adb shell dumpsys batterystats > {batterystats_path}")
    print(f"batterystats written to {batterystats_path}")
    os.system(f"adb bugreport {bugreport_path}")
    print(f"bugreport written to {bugreport_path}")

    # Disconnect if connected remotely
    if wireless:
        print("Disconnecting wireless ADB...")
        client.remote_disconnect()
    print("Test complete!")
