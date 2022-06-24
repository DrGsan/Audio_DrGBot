# Guide: How to Set Up and Use IKEv2 VPN

> Не забывайте, что постоянно под VPN лучше не сидеть, т.к. Он нужен для открытия заблокированных сервисов из другого
> региона, соответственно, некоторые программы которые работали без VPN, могут не работать под ним. В месяц на всех идёт
> 10 ТБ трафика (этого я думаю должно хватить).

# OS X (macOS)

- - - - -
First, securely transfer the generated `.mobileconfig` file to your Mac, then double-click and follow the prompts to
import as a macOS profile. If your Mac runs macOS Big Sur or newer, open System Preferences and go to the Profiles
section to finish importing. When finished, check to make sure "IKEv2 VPN" is listed under System Preferences ->
Profiles. To connect to the VPN:

1. Open System Preferences and go to the Network section.
2. Select the VPN connection with `Your VPN Server` IP (or DNS name).
3. Check the **Show VPN status in menu bar** checkbox.
4. Click **Connect**.

(Optional feature) You can choose to
enable [VPN On Demand](https://developer.apple.com/documentation/networkextension/personal_vpn/vpn_on_demand_rules).
This is an "always-on" feature that can automatically connect to the VPN while on Wi-Fi. To enable, check the **Connect
on demand** checkbox for the VPN connection, and click **Apply**.

Once successfully connected, you can verify that your traffic is being routed properly
by [looking up your IP address](https://www.google.com/search?q=my+ip) on Google. It should say "Your public IP address
is `Your VPN Server IP`".

# iOS

- - - - -
First, securely transfer the generated `.mobileconfig` file to your iOS device, then import it as an iOS profile. To
transfer the file, you may use:

1. AirDrop, or
2. Upload to your device (any App folder) using [File Sharing](https://support.apple.com/en-us/HT210598), then open
   the "Files" App on your iOS device, move the uploaded file to the "On My iPhone" folder. After that, tap the file and
   go to the "Settings" App to import, or
3. Host the file on a secure website of yours, then download and import it in Mobile Safari.

When finished, check to make sure "IKEv2 VPN" is listed under Settings -> General -> VPN & Device Management or Profile(
s).

To connect to the VPN:

1. Go to Settings -> VPN. Select the VPN connection with `Your VPN Server IP` (or DNS name).
2. Slide the **VPN** switch ON.

(Optional feature) You can choose to
enable [VPN On Demand](https://developer.apple.com/documentation/networkextension/personal_vpn/vpn_on_demand_rules).
This is an "always-on" feature that can automatically connect to the VPN while on Wi-Fi. To enable, tap the "i" icon on
the right of the VPN connection, and enable Connect On Demand.

Once successfully connected, you can verify that your traffic is being routed properly
by [looking up your IP address on Google](Once successfully connected, you can verify that your traffic is being routed
properly by [looking up your IP address on Google](). It should say "Your public IP address is Your VPN Server IP".
). It should say "Your public IP address is Your VPN Server IP".

# Android

- - - - -
1. Securely transfer the generated `.sswan` file to your Android device.
2. Install strongSwan VPN Client
   from [Google Play](https://play.google.com/store/apps/details?id=org.strongswan.android)
   , [F-Droid](https://f-droid.org/en/packages/org.strongswan.android/)
   or [strongSwan download server](https://download.strongswan.org/Android/).
3. Launch the strongSwan VPN client.
4. Tap the "more options" menu on top right, then tap **Import VPN profile**.
5. Choose the `.sswan` file you transferred from the VPN server. **Note**: To find the `.sswan` file, tap the three-line
   menu button, then browse to the location you saved the file.
6. On the "Import VPN profile" screen, tap **IMPORT CERTIFICATE FROM VPN PROFILE**, and follow the prompts.
7. On the "Choose certificate" screen, select the new client certificate, then tap Select.
8. Tap **IMPORT**.
9. Tap the new VPN profile to connect.

# Windows

- - - - -
Сертификат с расширением p12. Поместить в одну папку p12 и ikev2_config_import. Запустить ikev2_config_import от
администратора. Enter Enter Enter...