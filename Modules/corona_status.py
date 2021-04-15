import discord
import Utils

from datetime import datetime, timedelta
from asyncio import sleep
from aiohttp import ClientSession, ClientResponse

EVENTS = [Utils.EVENT.on_raw_reaction_add, Utils.EVENT.on_ready]

id_channel: int = 808742319066579014
id_message: int = 809048491186716734
msg_ids = [809048529246617630,
           809048553640165376,
           809048671080939550,
           809048677951602688,
           809048681420029982,
           809048685329252372,
           809048691264454676,
           809048696078991400,
           809048707353935952,
           809048712051163197,
           809048718082048061,
           809049260527452161,
           809049436340224081,
           809049491273023519]
supported = Utils.AttrDict({
    "USA": {"reaction": "🇺🇸", "tag": b"USA"},
    "India": {"reaction": "🇮🇳", "tag": b"India"},
    "Brazil": {"reaction": "🇧🇷", "tag": b"Brazil"},
    "Russia": {"reaction": "🇷🇺", "tag": b"Russia"},
    "UK": {"reaction": "🇬🇧", "tag": b"UK"},
    "France": {"reaction": "🇫🇷", "tag": b"France"},
    "Spain": {"reaction": "🇪🇸", "tag": b"Spain"},
    "Italy": {"reaction": "🇮🇹", "tag": b"Italy"},
    "Turkey": {"reaction": "🇹🇷", "tag": b"Turkey"},
    "Germany": {"reaction": "🇩🇪", "tag": b"Germany"},
    "Colombia": {"reaction": "🇨🇴", "tag": b"Colombia"},
    "Argentina": {"reaction": "🇦🇷", "tag": b"Argentina"},
    "Mexico": {"reaction": "🇲🇽", "tag": b"Mexico"},
    "Poland": {"reaction": "🇵🇱", "tag": b"Poland"},
    "Iran": {"reaction": "🇮🇷", "tag": b"Iran"},
    "South Africa": {"reaction": "🇿🇦", "tag": b"South Africa"},
    "Ukraine": {"reaction": "🇺🇦", "tag": b"Ukraine"},
    "Peru": {"reaction": "🇵🇪", "tag": b"Peru"},
    "Indonesia": {"reaction": "🇮🇩", "tag": b"Indonesia"},
    "Czech Republic": {"reaction": "🇨🇿", "tag": b"Czechia"},
    "Netherlands": {"reaction": "🇳🇱", "tag": b"Netherlands"},
    "Canada": {"reaction": "🇨🇦", "tag": b"Canada"},
    "Portugal": {"reaction": "🇵🇹", "tag": b"Portugal"},
    "Chile": {"reaction": "🇨🇱", "tag": b"Chile"},
    "Romania": {"reaction": "🇷🇴", "tag": b"Romania"},
    "Belgium": {"reaction": "🇧🇪", "tag": b"Belgium"},
    "Israel": {"reaction": "🇮🇱", "tag": b"Israel"},
    "Iraq": {"reaction": "🇮🇶", "tag": b"Iraq"},
    "Sweden": {"reaction": "🇸🇪", "tag": b"Sweden"},
    "Pakistan": {"reaction": "🇵🇰", "tag": b"Pakistan"},
    "Philippines": {"reaction": "🇵🇭", "tag": b"Philippines"},
    "Bangladesh": {"reaction": "🇧🇩", "tag": b"Bangladesh"},
    "Switzerland": {"reaction": "🇨🇭", "tag": b"Switzerland"},
    "Morocco": {"reaction": "🇲🇦", "tag": b"Morocco"},
    "Austria": {"reaction": "🇦🇹", "tag": b"Austria"},
    "Serbia": {"reaction": "🇷🇸", "tag": b"Serbia"},
    "Japan": {"reaction": "🇯🇵", "tag": b"Japan"},
    "Hungary": {"reaction": "🇭🇺", "tag": b"Hungary"},
    "Saudi Arabia": {"reaction": "🇸🇦", "tag": b"Saudi Arabia"},
    "Jordan": {"reaction": "🇯🇴", "tag": b"Jordan"},
    "United Arabic Emirates": {"reaction": "🇦🇪", "tag": b"UAE"},
    "Panama": {"reaction": "🇵🇦", "tag": b"Panama"},
    "Lebanon": {"reaction": "🇱🇧", "tag": b"Lebanon"},
    "Nepal": {"reaction": "🇳🇵", "tag": b"Nepal"},
    "Slovakia": {"reaction": "🇸🇰", "tag": b"Slovakia"},
    "Georgia": {"reaction": "🇬🇪", "tag": b"Georgia"},
    "Belarus": {"reaction": "🇧🇾", "tag": b"Belarus"},
    "Ecuador": {"reaction": "🇪🇨", "tag": b"Ecuador"},
    "Malaysia": {"reaction": "🇲🇾", "tag": b"Malaysia"},
    "Croatia": {"reaction": "🇭🇷", "tag": b"Croatia"},
    "Azerbaijan": {"reaction": "🇦🇿", "tag": b"Azerbaijan"},
    "Bolivia": {"reaction": "🇧🇴", "tag": b"Bolivia"},
    "Bulgaria": {"reaction": "🇧🇬", "tag": b"Bulgaria"},
    "Dominican Republic": {"reaction": "🇩🇴", "tag": b"Dominican Republic"},
    "Tunisia": {"reaction": "🇹🇳", "tag": b"Tunisia"},
    "Ireland": {"reaction": "🇮🇪", "tag": b"Ireland"},
    "Denmark": {"reaction": "🇩🇰", "tag": b"Denmark"},
    "Kazakhstan": {"reaction": "🇰🇿", "tag": b"Kazakhstan"},
    "Costa Rica": {"reaction": "🇨🇷", "tag": b"Costa Rica"},
    "Lithuania": {"reaction": "🇱🇹", "tag": b"Lithuania"},
    "Slovenia": {"reaction": "🇸🇮", "tag": b"Slovenia"},
    "Kuwait": {"reaction": "🇰🇼", "tag": b"Kuwait"},
    "Egypt": {"reaction": "🇪🇬", "tag": b"Egypt"},
    "Armenia": {"reaction": "🇦🇲", "tag": b"Armenia"},
    "Greece": {"reaction": "🇬🇷", "tag": b"Greece"},
    "Moldova": {"reaction": "🇲🇩", "tag": b"Moldova"},
    "Guatemala": {"reaction": "🇬🇹", "tag": b"Guatemala"},
    "Palestine": {"reaction": "🇵🇸", "tag": b"Palestine"},
    "Honduras": {"reaction": "🇭🇳", "tag": b"Honduras"},
    "Qatar": {"reaction": "🇶🇦", "tag": b"Qatar"},
    "Ethiopia": {"reaction": "🇪🇹", "tag": b"Ethiopia"},
    "Myanmar": {"reaction": "🇲🇲", "tag": b"Myanmar"},
    "Nigeria": {"reaction": "🇳🇬", "tag": b"Nigeria"},
    "Paraguay": {"reaction": "🇵🇾", "tag": b"Paraguay"},
    "Oman": {"reaction": "🇴🇲", "tag": b"Oman"},
    "Venezuela": {"reaction": "🇻🇪", "tag": b"Venezuela"},
    "Libya": {"reaction": "🇱🇾", "tag": b"Libya"},
    "Bosnia and Herzegovina": {"reaction": "🇧🇦", "tag": b"Bosnia and Herzegovina"},
    "Algeria": {"reaction": "🇩🇿", "tag": b"Algeria"},
    "Bahrain": {"reaction": "🇧🇭", "tag": b"Bahrain"},
    "Kenya": {"reaction": "🇰🇪", "tag": b"Kenya"},
    "North Macedonia": {"reaction": "🇲🇰", "tag": b"North Macedonia"},
    "China": {"reaction": "🇨🇳", "tag": b"China"},
    "Albania": {"reaction": "🇦🇱", "tag": b"Albania"},
    "Kyrgyzstan": {"reaction": "🇰🇬", "tag": b"Kyrgyzstan"},
    "South Korea": {"reaction": "🇰🇷", "tag": b"S. Korea"},
    "Uzbekistan": {"reaction": "🇺🇿", "tag": b"Uzbekistan"},
    "Latvia": {"reaction": "🇱🇻", "tag": b"Latvia"},
    "Ghana": {"reaction": "🇬🇭", "tag": b"Ghana"},
    "Sri Lanka": {"reaction": "🇱🇰", "tag": b"Sri Lanka"},
    "Montenegro": {"reaction": "🇲🇪", "tag": b"Montenegro"},
    "Norway": {"reaction": "🇳🇴", "tag": b"Norway"},
    "Zambia": {"reaction": "🇿🇲", "tag": b"Zambia"},
    "Singapore": {"reaction": "🇸🇬", "tag": b"Singapore"},
    "El Salvador": {"reaction": "🇸🇻", "tag": b"El Salvador"},
    "Afghanistan": {"reaction": "🇦🇫", "tag": b"Afghanistan"},
    "Luxembourg": {"reaction": "🇱🇺", "tag": b"Luxembourg"},
    "Estonia": {"reaction": "🇪🇪", "tag": b"Estonia"},
    "Finland": {"reaction": "🇫🇮", "tag": b"Finland"},
    "Uruguay": {"reaction": "🇺🇾", "tag": b"Uruguay"},
    "Mozambique": {"reaction": "🇲🇿", "tag": b"Mozambique"},
    "Uganda": {"reaction": "🇺🇬", "tag": b"Uganda"},
    "Namibia": {"reaction": "🇳🇦", "tag": b"Namibia"},
    "Zimbabwe": {"reaction": "🇿🇼", "tag": b"Zimbabwe"},
    "Cuba": {"reaction": "🇨🇺", "tag": b"Cuba"},
    "Cyprus": {"reaction": "🇨🇾", "tag": b"Cyprus"},
    "Cameroon": {"reaction": "🇨🇲", "tag": b"Cameroon"},
    "Ivory Coast": {"reaction": "🇨🇮", "tag": b"Ivory Coast"},
    "Senegal": {"reaction": "🇸🇳", "tag": b"Senegal"},
    "Australia": {"reaction": "🇦🇺", "tag": b"Australia"},
    "Malawi": {"reaction": "🇲🇼", "tag": b"Malawi"},
    "Sudan": {"reaction": "🇸🇩", "tag": b"Sudan"},
    "Botswana": {"reaction": "🇧🇼", "tag": b"Botswana"},
    "Thailand": {"reaction": "🇹🇭", "tag": b"Thailand"},
    "Democratic Republic of Congo": {"reaction": "🇨🇬", "tag": b"DRC"},
    "Angola": {"reaction": "🇦🇴", "tag": b"Angola"},
    "Madagascar": {"reaction": "🇲🇬", "tag": b"Madagascar"},
    "Malta": {"reaction": "🇲🇹", "tag": b"Malta"},
    "French Polynesia": {"reaction": "🇵🇫", "tag": b"French Polynesia"},
    "Jamaica": {"reaction": "🇯🇲", "tag": b"Jamaica"},
    "Maldives": {"reaction": "🇲🇻", "tag": b"Maldives"},
    "Mauritania": {"reaction": "🇲🇷", "tag": b"Mauritania"},
    "Rwanda": {"reaction": "🇷🇼", "tag": b"Rwanda"},
    "French Guiana": {"reaction": "🇬🇫", "tag": b"French Guiana"},
    "Swaziland": {"reaction": "🇸🇿", "tag": b"Eswatini"},
    "Guinea": {"reaction": "🇬🇳", "tag": b"Guinea"},
    "Syria": {"reaction": "🇸🇾", "tag": b"Syria"},
    "Cape Verde": {"reaction": "🇨🇻", "tag": b"Cabo Verde"},
    "Tajikistan": {"reaction": "🇹🇯", "tag": b"Tajikistan"},
    "Belize": {"reaction": "🇧🇿", "tag": b"Belize"},
    "Haiti": {"reaction": "🇭🇹", "tag": b"Haiti"},
    "Gabon": {"reaction": "🇬🇦", "tag": b"Gabon"},
    "Mayotte": {"reaction": "🇾🇹", "tag": b"Mayotte"},
    "Burkina Faso": {"reaction": "🇧🇫", "tag": b"Burkina Faso"},
    "Hong Kong": {"reaction": "🇭🇰", "tag": b"Hong Kong"},
    "Réunion": {"reaction": "🇷🇪", "tag": b"R&eacute;union"},
    "Andorra": {"reaction": "🇦🇩", "tag": b"Andorra"},
    "Lesotho": {"reaction": "🇱🇸", "tag": b"Lesotho"},
    "Guadeloupe": {"reaction": "🇬🇵", "tag": b"Guadeloupe"},
    "Suriname": {"reaction": "🇸🇷", "tag": b"Suriname"},
    "Bahamas": {"reaction": "🇧🇸", "tag": b"Bahamas"},
    "Mali": {"reaction": "🇲🇱", "tag": b"Mali"},
    "Congo": {"reaction": "🇨🇩", "tag": b"Congo"},
    "Guyana": {"reaction": "🇬🇾", "tag": b"Guyana"},
    "Trinidad & Tobago": {"reaction": "🇹🇹", "tag": b"Trinidad and Tobago"},
    "Aruba": {"reaction": "🇦🇼", "tag": b"Aruba"},
    "Martinique": {"reaction": "🇲🇶", "tag": b"Martinique"},
    "Nicaragua": {"reaction": "🇳🇮", "tag": b"Nicaragua"},
    "Iceland": {"reaction": "🇮🇸", "tag": b"Iceland"},
    "Djibouti": {"reaction": "🇩🇯", "tag": b"Djibouti"},
    "Equatorial Guinea": {"reaction": "🇬🇶", "tag": b"Equatorial Guinea"},
    "Togo": {"reaction": "🇹🇬", "tag": b"Togo"},
    "Central African Republic": {"reaction": "🇨🇫", "tag": b"CAR"},
    "Somalia": {"reaction": "🇸🇴", "tag": b"Somalia"},
    "South Sudan": {"reaction": "🇸🇸", "tag": b"South Sudan"},
    "Niger": {"reaction": "🇳🇪", "tag": b"Niger"},
    "Curaçao": {"reaction": "🇨🇼", "tag": b"Cura&ccedil;ao"},
    "Gambia": {"reaction": "🇬🇲", "tag": b"Gambia"},
    "Benin": {"reaction": "🇧🇯", "tag": b"Benin"},
    "Gibraltar": {"reaction": "🇬🇮", "tag": b"Gibraltar"},
    "Jersey": {"reaction": "🇯🇪", "tag": b"Channel Islands"},
    "Sierra Leone": {"reaction": "🇸🇱", "tag": b"Sierra Leone"},
    "Chad": {"reaction": "🇹🇩", "tag": b"Chad"},
    "San Marino": {"reaction": "🇸🇲", "tag": b"San Marino"},
    "Comoros": {"reaction": "🇰🇲", "tag": b"Comoros"},
    "Guinea-Bissau": {"reaction": "🇬🇼", "tag": b"Guinea-Bissau"},
    "Liechtenstein": {"reaction": "🇱🇮", "tag": b"Liechtenstein"},
    "Eritrea": {"reaction": "🇪🇷", "tag": b"Eritrea"},
    "New Zealand": {"reaction": "🇳🇿", "tag": b"New Zealand"},
    "Mongolia": {"reaction": "🇲🇳", "tag": b"Mongolia"},
    "Yemen": {"reaction": "🇾🇪", "tag": b"Yemen"},
    "Vietnam": {"reaction": "🇻🇳", "tag": b"Vietnam"},
    "Saint Lucia": {"reaction": "🇱🇨", "tag": b"Saint Lucia"},
    "Liberia": {"reaction": "🇱🇷", "tag": b"Liberia"},
    "Sint Maarten": {"reaction": "🇸🇽", "tag": b"Sint Maarten"},
    "Barbados": {"reaction": "🇧🇧", "tag": b"Barbados"},
    "Turks & Caicos Islands": {"reaction": "🇹🇨", "tag": b"Turks and Caicos"},
    "Burundi": {"reaction": "🇧🇮", "tag": b"Burundi"},
    "Monaco": {"reaction": "🇲🇨", "tag": b"Monaco"},
    "Seychelles": {"reaction": "🇸🇨", "tag": b"Seychelles"},
    "São Tomé & Príncipe": {"reaction": "🇸🇹", "tag": b"Sao Tome and Principe"},
    "St. Vincent & Grenadines": {"reaction": "🇻🇨", "tag": b"St. Vincent Grenadines"},
    "Saint Martin": {"reaction": "🇲🇫", "tag": b"Saint Martin"},
    "Taiwan": {"reaction": "🇹🇼", "tag": b"Taiwan"},
    "Papua New Guinea": {"reaction": "🇵🇬", "tag": b"Papua New Guinea"},
    "Bhutan": {"reaction": "🇧🇹", "tag": b"Bhutan"},
    "Diamond Princess": {"reaction": "🚢", "tag": b"Diamond Princess"},
    "Bermuda": {"reaction": "🇧🇲", "tag": b"Bermuda"},
    "Faroe Islands": {"reaction": "🇫🇴", "tag": b"Faeroe Islands"},
    "Mauritius": {"reaction": "🇲🇺", "tag": b"Mauritius"},
    "Tanzania": {"reaction": "🇹🇿", "tag": b"Tanzania"},
    "Cambodia": {"reaction": "🇰🇭", "tag": b"Cambodia"},
    "Isle of Man": {"reaction": "🇮🇲", "tag": b"Isle of Man"},
    "Cayman Islands": {"reaction": "🇰🇾", "tag": b"Cayman Islands"},
    "Caribbean Netherlands": {"reaction": "🇧🇶", "tag": b"Caribbean Netherlands"},
    "St. Barthélemy": {"reaction": "🇧🇱", "tag": b"St. Barth"},
    "Antigua and Barbuda": {"reaction": "🇦🇬", "tag": b"Antigua and Barbuda"},
    "Brunei": {"reaction": "🇧🇳", "tag": b"Brunei "},
    "Grenada": {"reaction": "🇬🇩", "tag": b"Grenada"},
    "Dominica": {"reaction": "🇩🇲", "tag": b"Dominica"},
    "British Virgin Islands": {"reaction": "🇻🇬", "tag": b"British Virgin Islands"},
    "Timor-Leste": {"reaction": "🇹🇱", "tag": b"Timor-Leste"},
    "Fiji": {"reaction": "🇫🇯", "tag": b"Fiji"},
    "Falkland Islands": {"reaction": "🇫🇰", "tag": b"Falkland Islands"},
    "New Caledonia": {"reaction": "🇳🇨", "tag": b"New Caledonia"},
    "Macao Sar China": {"reaction": "🇲🇴", "tag": b"Macao"},
    "Laos": {"reaction": "🇱🇦", "tag": b"Laos"},
    "Saint Kitts and Nevis": {"reaction": "🇰🇳", "tag": b"Saint Kitts and Nevis"},
    "Greenland": {"reaction": "🇬🇱", "tag": b"Greenland"},
    "Vatican City": {"reaction": "🇻🇦", "tag": b"Vatican City"},
    "Saint Pierre Miquelon": {"reaction": "🇵🇲", "tag": b"Saint Pierre Miquelon"},
    "Montserrat": {"reaction": "🇲🇸", "tag": b"Montserrat"},
    "Anguilla": {"reaction": "🇦🇮", "tag": b"Anguilla"},
    "Solomon Islands": {"reaction": "🇸🇧", "tag": b"Solomon Islands"},
    "Western Sahara": {"reaction": "🇪🇭", "tag": b"Western Sahara"},
    "MS Zaandam": {"reaction": "🛳️", "tag": b"MS Zaandam"},
    "Wallis and Futuna": {"reaction": "🇼🇫", "tag": b"Wallis and Futuna"},
    "Marshall Islands": {"reaction": "🇲🇭", "tag": b"Marshall Islands"},
    "Samoa": {"reaction": "🇼🇸", "tag": b"Samoa"},
    "Micronesia": {"reaction": "🇫🇲", "tag": b"Micronesia"},
    "Vanuatu": {"reaction": "🇻🇺", "tag": b"Vanuatu"}
})
sep = b"</td>"
url = r"https://www.worldometers.info/coronavirus/"


async def __main__(client: discord.Client, _event: int, reaction: discord.RawReactionActionEvent = None):
    try:
        channel: discord.TextChannel = client.get_channel(id_channel)

        if _event == Utils.EVENT.on_raw_reaction_add:

            message: discord.Message = await channel.fetch_message(id_message)

            if reaction.member == client.user:
                return

            '''  # To reset the reactions
            msgs = [await channel.fetch_message(_id) for _id in msg_ids]
        
            for msg in msgs:
                await msg.clear_reactions()
        
            _ = 0
            for key in list(supported.keys()):
                await msgs[_//20].add_reaction(discord.PartialEmoji(name=supported[key].reaction))
                _ += 1
            '''

            key = ""

            if reaction.channel_id == id_channel:
                msg = await channel.fetch_message(reaction.message_id)
                for _id in msg_ids:
                    if reaction.message_id == _id:
                        for key in list(supported.keys()):
                            if reaction.emoji == discord.PartialEmoji(name=supported[key].reaction):
                                break
                        break
                await msg.remove_reaction(reaction.emoji, reaction.member)

            await update(key, message)

        elif _event == Utils.EVENT.on_ready:
            while True:

                message: discord.Message = await channel.fetch_message(id_message)

                key = message.content.splitlines()[0].split()[1].replace("*", "")[:-2]

                await update(key, message)

                await sleep((timedelta(minutes=1) - timedelta(seconds=datetime.utcnow().second,
                                                              microseconds=datetime.utcnow().microsecond)).total_seconds())

    except KeyError:
        pass

    except Exception as e:
        await Utils.send_exception(client=client, exception=e, source_name=__name__)


async def update(key: str, message: discord.Message):

    msg = f"""
__**<a:loading:832383867700772866> {key}**__
```md
COVID-19 Cases
------------------------
loading...

Deaths
------------------------
loading...

Recovered
------------------------
loading...

Active
------------------------
loading...

> loading...```
@here is the source: <{url}> :)
"""
    await message.edit(content=msg)

    async with ClientSession() as session:
        resp = session.get(url)

        data: ClientResponse = await resp
        content = await data.read()

    pos = content.find(supported[key].tag)
    data: Utils.List[bytes] = content[pos:].split(sep)

    cases:     bytes = data[1].split(b">")[-1]
    deaths:    bytes = data[3].split(b">")[-1]
    recovered: bytes = data[5].split(b">")[-1]
    active:    bytes = data[7].split(b">")[-1]

    msg = f"""
__**{supported[key].reaction} {key}**__
```md
COVID-19 Cases
------------------------
{cases.decode():11}

Deaths
------------------------
{deaths.decode():11}

Recovered
------------------------
{recovered.decode():11}

Active
------------------------
{active.decode():11}

> UTC {datetime.utcnow().date()} {datetime.utcnow().hour}:{"0" + str(datetime.utcnow().minute) if datetime.utcnow().minute < 10 else datetime.utcnow().minute}```
@here is the source: <{url}> :)
"""

    await message.edit(content=msg)
