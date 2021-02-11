import discord
import Utils

from datetime import datetime, timedelta
from asyncio import sleep
import requests


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
available_stats = Utils.AttrDict({
        "USA": {
            "reaction":      "🇺🇸",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"USA",
            "sep":           b"</td>"
        },
        "India": {
            "reaction":      "🇮🇳",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"India",
            "sep":           b"</td>"
        },
        "Brazil": {
            "reaction":      "🇧🇷",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Brazil",
            "sep":           b"</td>"
        },
        "Russia": {
            "reaction":      "🇷🇺",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Russia",
            "sep":           b"</td>"
        },
        "UK": {
            "reaction":      "🇬🇧",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"UK",
            "sep":           b"</td>"
        },
        "France": {
            "reaction":      "🇫🇷",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"France",
            "sep":           b"</td>"
        },
        "Spain": {
            "reaction":      "🇪🇸",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Spain",
            "sep":           b"</td>"
        },
        "Italy": {
            "reaction":      "🇮🇹",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Italy",
            "sep":           b"</td>"
        },
        "Turkey": {
            "reaction":      "🇹🇷",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Turkey",
            "sep":           b"</td>"
        },
        "Germany": {
            "reaction":      "🇩🇪",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Germany",
            "sep":           b"</td>"
        },
        "Colombia": {
            "reaction":      "🇨🇴",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Colombia",
            "sep":           b"</td>"
        },
        "Argentina": {
            "reaction":      "🇦🇷",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Argentina",
            "sep":           b"</td>"
        },
        "Mexico": {
            "reaction":      "🇲🇽",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Mexico",
            "sep":           b"</td>"
        },
        "Poland": {
            "reaction":      "🇵🇱",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Poland",
            "sep":           b"</td>"
        },
        "Iran": {
            "reaction":      "🇮🇷",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Iran",
            "sep":           b"</td>"
        },
        "South Africa": {
            "reaction":      "🇿🇦",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"South Africa",
            "sep":           b"</td>"
        },
        "Ukraine": {
            "reaction":      "🇺🇦",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Ukraine",
            "sep":           b"</td>"
        },
        "Peru": {
            "reaction":      "🇵🇪",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Peru",
            "sep":           b"</td>"
        },
        "Indonesia": {
            "reaction":      "🇮🇩",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Indonesia",
            "sep":           b"</td>"
        },
        "Czech Republic": {
            "reaction":      "🇨🇿",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Czechia",
            "sep":           b"</td>"
        },
        "Netherlands": {
            "reaction":      "🇳🇱",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Netherlands",
            "sep":           b"</td>"
        },
        "Canada": {
            "reaction":      "🇨🇦",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Canada",
            "sep":           b"</td>"
        },
        "Portugal": {
            "reaction":      "🇵🇹",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Portugal",
            "sep":           b"</td>"
        },
        "Chile": {
            "reaction":      "🇨🇱",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Chile",
            "sep":           b"</td>"
        },
        "Romania": {
            "reaction":      "🇷🇴",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Romania",
            "sep":           b"</td>"
        },
        "Belgium": {
            "reaction":      "🇧🇪",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Belgium",
            "sep":           b"</td>"
        },
        "Israel": {
            "reaction":      "🇮🇱",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Israel",
            "sep":           b"</td>"
        },
        "Iraq": {
            "reaction":      "🇮🇶",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Iraq",
            "sep":           b"</td>"
        },
        "Sweden": {
            "reaction":      "🇸🇪",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Sweden",
            "sep":           b"</td>"
        },
        "Pakistan": {
            "reaction":      "🇵🇰",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Pakistan",
            "sep":           b"</td>"
        },
        "Philippines": {
            "reaction":      "🇵🇭",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Philippines",
            "sep":           b"</td>"
        },
        "Bangladesh": {
            "reaction":      "🇧🇩",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Bangladesh",
            "sep":           b"</td>"
        },
        "Switzerland": {
            "reaction":      "🇨🇭",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Switzerland",
            "sep":           b"</td>"
        },
        "Morocco": {
            "reaction":      "🇲🇦",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Morocco",
            "sep":           b"</td>"
        },
        "Austria": {
            "reaction":      "🇦🇹",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Austria",
            "sep":           b"</td>"
        },
        "Serbia": {
            "reaction":      "🇷🇸",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Serbia",
            "sep":           b"</td>"
        },
        "Japan": {
            "reaction":      "🇯🇵",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Japan",
            "sep":           b"</td>"
        },
        "Hungary": {
            "reaction":      "🇭🇺",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Hungary",
            "sep":           b"</td>"
        },
        "Saudi Arabia": {
            "reaction":      "🇸🇦",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Saudi Arabia",
            "sep":           b"</td>"
        },
        "Jordan": {
            "reaction":      "🇯🇴",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Jordan",
            "sep":           b"</td>"
        },
        "United Arabic Emirates": {
            "reaction":      "🇦🇪",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"UAE",
            "sep":           b"</td>"
        },
        "Panama": {
            "reaction":      "🇵🇦",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Panama",
            "sep":           b"</td>"
        },
        "Lebanon": {
            "reaction":      "🇱🇧",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Lebanon",
            "sep":           b"</td>"
        },
        "Nepal": {
            "reaction":      "🇳🇵",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Nepal",
            "sep":           b"</td>"
        },
        "Slovakia": {
            "reaction":      "🇸🇰",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Slovakia",
            "sep":           b"</td>"
        },
        "Georgia": {
            "reaction":      "🇬🇪",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Georgia",
            "sep":           b"</td>"
        },
        "Belarus": {
            "reaction":      "🇧🇾",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Belarus",
            "sep":           b"</td>"
        },
        "Ecuador": {
            "reaction":      "🇪🇨",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Ecuador",
            "sep":           b"</td>"
        },
        "Malaysia": {
            "reaction":      "🇲🇾",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Malaysia",
            "sep":           b"</td>"
        },
        "Croatia": {
            "reaction":      "🇭🇷",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Croatia",
            "sep":           b"</td>"
        },
        "Azerbaijan": {
            "reaction":      "🇦🇿",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Azerbaijan",
            "sep":           b"</td>"
        },
        "Bolivia": {
            "reaction":      "🇧🇴",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Bolivia",
            "sep":           b"</td>"
        },
        "Bulgaria": {
            "reaction":      "🇧🇬",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"",
            "sep":           b"</td>"
        },
        "Dominican Republic": {
            "reaction":      "🇩🇴",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Dominican Republic",
            "sep":           b"</td>"
        },
        "Tunisia": {
            "reaction":      "🇹🇳",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Tunisia",
            "sep":           b"</td>"
        },
        "Ireland": {
            "reaction":      "🇮🇪",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Ireland",
            "sep":           b"</td>"
        },
        "Denmark": {
            "reaction":      "🇩🇰",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Denmark",
            "sep":           b"</td>"
        },
        "Kazakhstan": {
            "reaction":      "🇰🇿",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Kazakhstan",
            "sep":           b"</td>"
        },
        "Costa Rica": {
            "reaction":      "🇨🇷",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Costa Rica",
            "sep":           b"</td>"
        },
        "Lithuania": {
            "reaction":      "🇱🇹",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Lithuania",
            "sep":           b"</td>"
        },
        "Slovenia": {
            "reaction":      "🇸🇮",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Slovenia",
            "sep":           b"</td>"
        },
        "Kuwait": {
            "reaction":      "🇰🇼",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Kuwait",
            "sep":           b"</td>"
        },
        "Egypt": {
            "reaction":      "🇪🇬",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Egypt",
            "sep":           b"</td>"
        },
        "Armenia": {
            "reaction":      "🇦🇲",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"",
            "sep":           b"</td>"
        },
        "Greece": {
            "reaction":      "🇬🇷",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Greece",
            "sep":           b"</td>"
        },
        "Moldova": {
            "reaction":      "🇲🇩",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Moldova",
            "sep":           b"</td>"
        },
        "Guatemala": {
            "reaction":      "🇬🇹",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Guatemala",
            "sep":           b"</td>"
        },
        "Palestine": {
            "reaction":      "🇵🇸",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Palestine",
            "sep":           b"</td>"
        },
        "Honduras": {
            "reaction":      "🇭🇳",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Honduras",
            "sep":           b"</td>"
        },
        "Qatar": {
            "reaction":      "🇶🇦",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Qatar",
            "sep":           b"</td>"
        },
        "Ethiopia": {
            "reaction":      "🇪🇹",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Ethiopia",
            "sep":           b"</td>"
        },
        "Myanmar": {
            "reaction":      "🇲🇲",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Myanmar",
            "sep":           b"</td>"
        },
        "Nigeria": {
            "reaction":      "🇳🇬",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Nigeria",
            "sep":           b"</td>"
        },
        "Paraguay": {
            "reaction":      "🇵🇾",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Paraguay",
            "sep":           b"</td>"
        },
        "Oman": {
            "reaction":      "🇴🇲",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Oman",
            "sep":           b"</td>"
        },
        "Venezuela": {
            "reaction":      "🇻🇪",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Venezuela",
            "sep":           b"</td>"
        },
        "Libya": {
            "reaction":      "🇱🇾",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Libya",
            "sep":           b"</td>"
        },
        "Bosnia and Herzegovina": {
            "reaction":      "🇧🇦",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Bosnia and Herzegovina",
            "sep":           b"</td>"
        },
        "Algeria": {
            "reaction":      "🇩🇿",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Algeria",
            "sep":           b"</td>"
        },
        "Bahrain": {
            "reaction":      "🇧🇭",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Bahrain",
            "sep":           b"</td>"
        },
        "Kenya": {
            "reaction":      "🇰🇪",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Kenya",
            "sep":           b"</td>"
        },
        "North Macedonia": {
            "reaction":      "🇲🇰",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"North Macedonia",
            "sep":           b"</td>"
        },
        "China": {
            "reaction":      "🇨🇳",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"China",
            "sep":           b"</td>"
        },
        "Albania": {
            "reaction":      "🇦🇱",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"",
            "sep":           b"</td>"
        },
        "Kyrgyzstan": {
            "reaction":      "🇰🇬",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Kyrgyzstan",
            "sep":           b"</td>"
        },
        "South Korea": {
            "reaction":      "🇰🇷",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"S. Korea",
            "sep":           b"</td>"
        },
        "Uzbekistan": {
            "reaction":      "🇺🇿",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Uzbekistan",
            "sep":           b"</td>"
        },
        "Latvia": {
            "reaction":      "🇱🇻",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Latvia",
            "sep":           b"</td>"
        },
        "Ghana": {
            "reaction":      "🇬🇭",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Ghana",
            "sep":           b"</td>"
        },
        "Sri Lanka": {
            "reaction":      "🇱🇰",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Sri Lanka",
            "sep":           b"</td>"
        },
        "Montenegro": {
            "reaction":      "🇲🇪",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Montenegro",
            "sep":           b"</td>"
        },
        "Norway": {
            "reaction":      "🇳🇴",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Norway",
            "sep":           b"</td>"
        },
        "Zambia": {
            "reaction":      "🇿🇲",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Zambia",
            "sep":           b"</td>"
        },
        "Singapore": {
            "reaction":      "🇸🇬",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Singapore",
            "sep":           b"</td>"
        },
        "El Salvador": {
            "reaction":      "🇸🇻",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"El Salvador",
            "sep":           b"</td>"
        },
        "Afghanistan": {
            "reaction":      "🇦🇫",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Afghanistan",
            "sep":           b"</td>"
        },
        "Luxembourg": {
            "reaction":      "🇱🇺",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Luxembourg",
            "sep":           b"</td>"
        },
        "Estonia": {
            "reaction":      "🇪🇪",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Estonia",
            "sep":           b"</td>"
        },
        "Finland": {
            "reaction":      "🇫🇮",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Finland",
            "sep":           b"</td>"
        },
        "Uruguay": {
            "reaction":      "🇺🇾",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Uruguay",
            "sep":           b"</td>"
        },
        "Mozambique": {
            "reaction":      "🇲🇿",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Mozambique",
            "sep":           b"</td>"
        },
        "Uganda": {
            "reaction":      "🇺🇬",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Uganda",
            "sep":           b"</td>"
        },
        "Namibia": {
            "reaction":      "🇳🇦",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Namibia",
            "sep":           b"</td>"
        },
        "Zimbabwe": {
            "reaction":      "🇿🇼",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Zimbabwe",
            "sep":           b"</td>"
        },
        "Cuba": {
            "reaction":      "🇨🇺",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Cuba",
            "sep":           b"</td>"
        },
        "Cyprus": {
            "reaction":      "🇨🇾",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Cyprus",
            "sep":           b"</td>"
        },
        "Cameroon": {
            "reaction":      "🇨🇲",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Cameroon",
            "sep":           b"</td>"
        },
        "Ivory Coast": {
            "reaction":      "🇨🇮",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Ivory Coast",
            "sep":           b"</td>"
        },
        "Senegal": {
            "reaction":      "🇸🇳",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Senegal",
            "sep":           b"</td>"
        },
        "Australia": {
            "reaction":      "🇦🇺",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Australia",
            "sep":           b"</td>"
        },
        "Malawi": {
            "reaction":      "🇲🇼",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Malawi",
            "sep":           b"</td>"
        },
        "Sudan": {
            "reaction":      "🇸🇩",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Sudan",
            "sep":           b"</td>"
        },
        "Botswana": {
            "reaction":      "🇧🇼",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Botswana",
            "sep":           b"</td>"
        },
        "Thailand": {
            "reaction":      "🇹🇭",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Thailand",
            "sep":           b"</td>"
        },
        "Democratic Republic of Congo": {
            "reaction":      "🇨🇬",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"DRC",
            "sep":           b"</td>"
        },
        "Angola": {
            "reaction":      "🇦🇴",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Angola",
            "sep":           b"</td>"
        },
        "Madagascar": {
            "reaction":      "🇲🇬",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Madagascar",
            "sep":           b"</td>"
        },
        "Malta": {
            "reaction":      "🇲🇹",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Malta",
            "sep":           b"</td>"
        },
        "French Polynesia": {
            "reaction":      "🇵🇫",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"French Polynesia",
            "sep":           b"</td>"
        },
        "Jamaica": {
            "reaction":      "🇯🇲",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Jamaica",
            "sep":           b"</td>"
        },
        "Maldives": {
            "reaction":      "🇲🇻",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Maldives",
            "sep":           b"</td>"
        },
        "Mauritania": {
            "reaction":      "🇲🇷",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Mauritania",
            "sep":           b"</td>"
        },
        "Rwanda": {
            "reaction":      "🇷🇼",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Rwanda",
            "sep":           b"</td>"
        },
        "French Guiana": {
            "reaction":      "🇬🇫",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"French Guiana",
            "sep":           b"</td>"
        },
        "Swaziland": {
            "reaction":      "🇸🇿",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Eswatini",
            "sep":           b"</td>"
        },
        "Guinea": {
            "reaction":      "🇬🇳",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Guinea",
            "sep":           b"</td>"
        },
        "Syria": {
            "reaction":      "🇸🇾",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Syria",
            "sep":           b"</td>"
        },
        "Cape Verde": {
            "reaction":      "🇨🇻",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Cabo Verde",
            "sep":           b"</td>"
        },
        "Tajikistan": {
            "reaction":      "🇹🇯",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Tajikistan",
            "sep":           b"</td>"
        },
        "Belize": {
            "reaction":      "🇧🇿",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Belize",
            "sep":           b"</td>"
        },
        "Haiti": {
            "reaction":      "🇭🇹",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Haiti",
            "sep":           b"</td>"
        },
        "Gabon": {
            "reaction":      "🇬🇦",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Gabon",
            "sep":           b"</td>"
        },
        "Mayotte": {
            "reaction":      "🇾🇹",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Mayotte",
            "sep":           b"</td>"
        },
        "Burkina Faso": {
            "reaction":      "🇧🇫",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Burkina Faso",
            "sep":           b"</td>"
        },
        "Hong Kong": {
            "reaction":      "🇭🇰",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Hong Kong",
            "sep":           b"</td>"
        },
        "Réunion": {
            "reaction":      "🇷🇪",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           "Réunion".encode(),
            "sep":           b"</td>"
        },
        "Andorra": {
            "reaction":      "🇦🇩",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Andorra",
            "sep":           b"</td>"
        },
        "Lesotho": {
            "reaction":      "🇱🇸",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Lesotho",
            "sep":           b"</td>"
        },
        "Guadeloupe": {
            "reaction":      "🇬🇵",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Guadeloupe",
            "sep":           b"</td>"
        },
        "Suriname": {
            "reaction":      "🇸🇷",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Suriname",
            "sep":           b"</td>"
        },
        "Bahamas": {
            "reaction":      "🇧🇸",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Bahamas",
            "sep":           b"</td>"
        },
        "Mali": {
            "reaction":      "🇲🇱",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Mali",
            "sep":           b"</td>"
        },
        "Congo": {
            "reaction":      "🇨🇩",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Congo",
            "sep":           b"</td>"
        },
        "Guyana": {
            "reaction":      "🇬🇾",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Guyana",
            "sep":           b"</td>"
        },
        "Trinidad & Tobago": {
            "reaction":      "🇹🇹",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Trinidad and Tobago",
            "sep":           b"</td>"
        },
        "Aruba": {
            "reaction":      "🇦🇼",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Aruba",
            "sep":           b"</td>"
        },
        "Martinique": {
            "reaction":      "🇲🇶",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Martinique",
            "sep":           b"</td>"
        },
        "Nicaragua": {
            "reaction":      "🇳🇮",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Nicaragua",
            "sep":           b"</td>"
        },
        "Iceland": {
            "reaction":      "🇮🇸",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Iceland",
            "sep":           b"</td>"
        },
        "Djibouti": {
            "reaction":      "🇩🇯",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Djibouti",
            "sep":           b"</td>"
        },
        "Equatorial Guinea": {
            "reaction":      "🇬🇶",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Equatorial Guinea",
            "sep":           b"</td>"
        },
        "Togo": {
            "reaction":      "🇹🇬",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Togo",
            "sep":           b"</td>"
        },
        "Central African Republic": {
            "reaction":      "🇨🇫",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"CAR",
            "sep":           b"</td>"
        },
        "Somalia": {
            "reaction":      "🇸🇴",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Somalia",
            "sep":           b"</td>"
        },
        "South Sudan": {
            "reaction":      "🇸🇸",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"South Sudan",
            "sep":           b"</td>"
        },
        "Niger": {
            "reaction":      "🇳🇪",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Niger",
            "sep":           b"</td>"
        },
        "Curaçao": {
            "reaction":      "🇨🇼",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           "Curaçao".encode(),
            "sep":           b"</td>"
        },
        "Gambia": {
            "reaction":      "🇬🇲",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Gambia",
            "sep":           b"</td>"
        },
        "Benin": {
            "reaction":      "🇧🇯",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Benin",
            "sep":           b"</td>"
        },
        "Gibraltar": {
            "reaction":      "🇬🇮",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Gibraltar",
            "sep":           b"</td>"
        },
        "Jersey": {
            "reaction":      "🇯🇪",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Channel Islands",
            "sep":           b"</td>"
        },
        "Sierra Leone": {
            "reaction":      "🇸🇱",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Sierra Leone",
            "sep":           b"</td>"
        },
        "Chad": {
            "reaction":      "🇹🇩",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Chad",
            "sep":           b"</td>"
        },
        "San Marino": {
            "reaction":      "🇸🇲",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"San Marino",
            "sep":           b"</td>"
        },
        "Comoros": {
            "reaction":      "🇰🇲",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Comoros",
            "sep":           b"</td>"
        },
        "Guinea-Bissau": {
            "reaction":      "🇬🇼",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Guinea-Bissau",
            "sep":           b"</td>"
        },
        "Liechtenstein": {
            "reaction":      "🇱🇮",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Liechtenstein",
            "sep":           b"</td>"
        },
        "Eritrea": {
            "reaction":      "🇪🇷",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Eritrea",
            "sep":           b"</td>"
        },
        "New Zealand": {
            "reaction":      "🇳🇿",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"New Zealand",
            "sep":           b"</td>"
        },
        "Mongolia": {
            "reaction":      "🇲🇳",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Mongolia",
            "sep":           b"</td>"
        },
        "Yemen": {
            "reaction":      "🇾🇪",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Yemen",
            "sep":           b"</td>"
        },
        "Vietnam": {
            "reaction":      "🇻🇳",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Vietnam",
            "sep":           b"</td>"
        },
        "Saint Lucia": {
            "reaction":      "🇱🇨",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Saint Lucia",
            "sep":           b"</td>"
        },
        "Liberia": {
            "reaction":      "🇱🇷",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Liberia",
            "sep":           b"</td>"
        },
        "Sint Maarten": {
            "reaction":      "🇸🇽",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Sint Maarten",
            "sep":           b"</td>"
        },
        "Barbados": {
            "reaction":      "🇧🇧",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Barbados",
            "sep":           b"</td>"
        },
        "Turks & Caicos Islands": {
            "reaction":      "🇹🇨",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Turks and Caicos",
            "sep":           b"</td>"
        },
        "Burundi": {
            "reaction":      "🇧🇮",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Burundi",
            "sep":           b"</td>"
        },
        "Monaco": {
            "reaction":      "🇲🇨",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Monaco",
            "sep":           b"</td>"
        },
        "Seychelles": {
            "reaction":      "🇸🇨",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Seychelles",
            "sep":           b"</td>"
        },
        "São Tomé & Príncipe": {
            "reaction":      "🇸🇹",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Sao Tome and Principe",
            "sep":           b"</td>"
        },
        "St. Vincent & Grenadines": {
            "reaction":      "🇻🇨",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"St. Vincent Grenadines",
            "sep":           b"</td>"
        },
        "Saint Martin": {
            "reaction":      "🇲🇫",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Saint Martin",
            "sep":           b"</td>"
        },
        "Taiwan": {
            "reaction":      "🇹🇼",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Taiwan",
            "sep":           b"</td>"
        },
        "Papua New Guinea": {
            "reaction":      "🇵🇬",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Papua New Guinea",
            "sep":           b"</td>"
        },
        "Bhutan": {
            "reaction":      "🇧🇹",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Bhutan",
            "sep":           b"</td>"
        },
        "Diamond Princess": {
            "reaction":      "🚢",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Diamond Princess",
            "sep":           b"</td>"
        },
        "Bermuda": {
            "reaction":      "🇧🇲",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Bermuda",
            "sep":           b"</td>"
        },
        "Faroe Islands": {
            "reaction":      "🇫🇴",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Faeroe Islands",
            "sep":           b"</td>"
        },
        "Mauritius": {
            "reaction":      "🇲🇺",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Mauritius",
            "sep":           b"</td>"
        },
        "Tanzania": {
            "reaction":      "🇹🇿",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Tanzania",
            "sep":           b"</td>"
        },
        "Cambodia": {
            "reaction":      "🇰🇭",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Cambodia",
            "sep":           b"</td>"
        },
        "Isle of Man": {
            "reaction":      "🇮🇲",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Isle of Man",
            "sep":           b"</td>"
        },
        "Cayman Islands": {
            "reaction":      "🇰🇾",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Cayman Islands",
            "sep":           b"</td>"
        },
        "Caribbean Netherlands": {
            "reaction":      "🇧🇶",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Caribbean Netherlands",
            "sep":           b"</td>"
        },
        "St. Barthélemy": {
            "reaction":      "🇧🇱",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"St. Barth",
            "sep":           b"</td>"
        },
        "Antigua and Barbuda": {
            "reaction":      "🇦🇬",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Antigua and Barbuda",
            "sep":           b"</td>"
        },
        "Brunei": {
            "reaction":      "🇧🇳",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Brunei",
            "sep":           b"</td>"
        },
        "Grenada": {
            "reaction":      "🇬🇩",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Grenada",
            "sep":           b"</td>"
        },
        "Dominica": {
            "reaction":      "🇩🇲",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Dominica",
            "sep":           b"</td>"
        },
        "British Virgin Islands": {
            "reaction":      "🇻🇬",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"British Virgin Islands",
            "sep":           b"</td>"
        },
        "Timor-Leste": {
            "reaction":      "🇹🇱",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Timor-Leste",
            "sep":           b"</td>"
        },
        "Fiji": {
            "reaction":      "🇫🇯",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Fiji",
            "sep":           b"</td>"
        },
        "Falkland Islands": {
            "reaction":      "🇫🇰",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Falkland Islands",
            "sep":           b"</td>"
        },
        "New Caledonia": {
            "reaction":      "🇳🇨",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"New Caledonia",
            "sep":           b"</td>"
        },
        "Macao Sar China": {
            "reaction":      "🇲🇴",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Macao",
            "sep":           b"</td>"
        },
        "Laos": {
            "reaction":      "🇱🇦",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Laos",
            "sep":           b"</td>"
        },
        "Saint Kitts and Nevis": {
            "reaction":      "🇰🇳",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Saint Kitts and Nevis",
            "sep":           b"</td>"
        },
        "Greenland": {
            "reaction":      "🇬🇱",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Greenland",
            "sep":           b"</td>"
        },
        "Vatican City": {
            "reaction":      "🇻🇦",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Vatican City",
            "sep":           b"</td>"
        },
        "Saint Pierre Miquelon": {
            "reaction":      "🇵🇲",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Saint Pierre Miquelon",
            "sep":           b"</td>"
        },
        "Montserrat": {
            "reaction":      "🇲🇸",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Montserrat",
            "sep":           b"</td>"
        },
        "Anguilla": {
            "reaction":      "🇦🇮",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Anguilla",
            "sep":           b"</td>"
        },
        "Solomon Islands": {
            "reaction":      "🇸🇧",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Solomon Islands",
            "sep":           b"</td>"
        },
        "Western Sahara": {
            "reaction":      "🇪🇭",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Western Sahara",
            "sep":           b"</td>"
        },
        "MS Zaandam": {
            "reaction":      "🛳️",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"MS Zaandam",
            "sep":           b"</td>"
        },
        "Wallis and Futuna": {
            "reaction":      "🇼🇫",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Wallis and Futuna",
            "sep":           b"</td>"
        },
        "Marshall Islands": {
            "reaction":      "🇲🇭",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Marshall Islands",
            "sep":           b"</td>"
        },
        "Samoa": {
            "reaction":      "🇼🇸",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Samoa",
            "sep":           b"</td>"
        },
        "Micronesia": {
            "reaction":      "🇫🇲",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Micronesia",
            "sep":           b"</td>"
        },
        "Vanuatu": {
            "reaction":      "🇻🇺",
            "url":           "https://www.worldometers.info/coronavirus/",
            "tag":           b"Vanuatu",
            "sep":           b"</td>"
        },
    })


async def __main__(client: discord.Client, _event: int, reaction: discord.RawReactionActionEvent = None):

    channel: discord.TextChannel = client.get_channel(id_channel)
    message: discord.Message = await channel.fetch_message(id_message)

    if _event == Utils.EVENT.on_raw_reaction_add:

        if reaction.member == client.user:
            return

        '''  # To reset the reactions
        msgs = [await channel.fetch_message(_id) for _id in msg_ids]
    
        for msg in msgs:
            await msg.clear_reactions()
    
        _ = 0
        for key in list(available_stats.keys()):
            await msgs[_//20].add_reaction(discord.PartialEmoji(name=available_stats[key].reaction))
            _ += 1
        '''

        key = url = ""

        if reaction.channel_id == id_channel:
            msg = await channel.fetch_message(reaction.message_id)
            for _id in msg_ids:
                if reaction.message_id == _id:
                    for key in list(available_stats.keys()):
                        if reaction.emoji == discord.PartialEmoji(name=available_stats[key].reaction):
                            url = available_stats[key].url
                            break
                    break
            await msg.remove_reaction(reaction.emoji, reaction.member)

        await update(key, url, message)

    elif _event == Utils.EVENT.on_ready:
        while True:
            key = message.content.splitlines()[0].split()[1].replace("*", "").replace("_", "")
            url = available_stats[key].url

            await update(key, url, message)

            await sleep((timedelta(minutes=1)-timedelta(seconds=datetime.utcnow().second, microseconds=datetime.utcnow().microsecond)).total_seconds())


async def update(key: str, url: str, message: discord.Message):
    if url:
        data: requests.Response = requests.get(url)

        pos = data.content.find(available_stats[key].tag)
        data: Utils.List[bytes] = data.content[pos:].split(available_stats[key].sep)

        cases = data[1].split(b">")[-1]
        deaths = data[3].split(b">")[-1]
        recovered = data[5].split(b">")[-1]
        active = data[7].split(b">")[-1]

        msg = f"""
__**{available_stats[key].reaction} {key}**__
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

> UTC {datetime.utcnow().date()} {datetime.utcnow().hour}:{"0"+str(datetime.utcnow().minute) if datetime.utcnow().minute < 10 else datetime.utcnow().minute}```
coded by <@{Utils.DATA.Author_id}> for @here :)
[updating the country can take some time]
"""

        await message.edit(content=msg)
