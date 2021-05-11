### Kcowin


Notifies when vaccines are available in your district using apisetu public api


*You can specify your own:*

- District code
- Age Limit
- Number of days to search

in the config file `cowin.conf`

Valid options : age_limit, num_days, district_code

![kdialog](/src/img/kdialog.png)


#### Requirements:

OS : Linux

Dependecies : kdialog, python/python3

#### Install dependencies:

Arch/Manjaro Linux:

`sudo pacman -S kdialog`

Fedora:

`sudo dnf install kdialog`

Ubuntu:

`sudo apt install kdialog`

#### Setup:

```
git clone https://github.com/brpy/kcowin.git
cd kcowin/src
chmod +x setup.sh
sh setup.sh
```


#### Todo: [PR appreciated]

- Hourly Cron job setup
- Windows support through Tkinter


#### State/District codes:

|state_id | state_name|
|---------|------------|
1|Andaman and Nicobar Islands
2|Andhra Pradesh
3|Arunachal Pradesh
4|Assam
5|Bihar
6|Chandigarh
7|Chhattisgarh
8|Dadra and Nagar Haveli
37|Daman and Diu
9|Delhi
10|Goa
11|Gujarat
12|Haryana
13|Himachal Pradesh
14|Jammu and Kashmir
15|Jharkhand
16|Karnataka
17|Kerala
18|Ladakh
19|Lakshadweep
20|Madhya Pradesh
21|Maharashtra
22|Manipur
23|Meghalaya
24|Mizoram
25|Nagaland
26|Odisha
27|Puducherry
28|Punjab
29|Rajasthan
30|Sikkim
31|Tamil Nadu
32|Telangana
33|Tripura
34|Uttar Pradesh
35|Uttarakhand
36|West Bengal

To find a district code, check [codes](/codes/) folder for your stateid-statename.csv file.
